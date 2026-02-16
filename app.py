from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
import subprocess
import tempfile
import base64
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

def compile_latex_to_pdf(latex_content):
    """Compile LaTeX to PDF and return base64 encoded PDF"""
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_file = os.path.join(tmpdir, 'resume.tex')
            pdf_file = os.path.join(tmpdir, 'resume.pdf')
            
            # Write LaTeX to file
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            # Compile with pdflatex
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', tmpdir, tex_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Check if PDF was created
            if not os.path.exists(pdf_file):
                return {
                    "success": False,
                    "error": f"PDF compilation failed. LaTeX errors: {result.stdout[-500:]}"
                }
            
            # Read PDF and encode as base64
            with open(pdf_file, 'rb') as f:
                pdf_data = f.read()
            
            return {
                "success": True,
                "pdf_base64": base64.b64encode(pdf_data).decode('utf-8')
            }
    
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "PDF compilation timed out"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "pdflatex not found. Please install TeX Live: sudo apt-get install texlive-latex-base texlive-latex-extra"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"PDF compilation error: {str(e)}"
        }


def generate_resume_with_groq(resume_content, job_description_content, template_content=None):
    """Generate optimized resume using Groq API"""
    try:
        # Read template if not provided
        if not template_content:
            template_path = "txt_files/template.txt"
            if os.path.exists(template_path):
                with open(template_path, "r") as f:
                    template_content = f.read()
            else:
                template_content = ""  # Use empty if template doesn't exist

        # Construct prompt
        user_prompt = f"""You are a professional resume writer. Generate a LaTeX resume optimized for the job description below.
    You are allowed to bluff but do not MAKE UP ANY stats. For the same experience, use the keywords from the job description to generate the resume.

    LATEX TEMPLATE TO FILL:
    {template_content}

    INSTRUCTIONS:
    1. Replace placeholders like {{{{NAME}}}}, {{{{EMAIL}}}}, {{{{EXPERIENCE}}}} with actual content
    2. For {{{{EXPERIENCE}}}}: Select 2-4 most relevant jobs from resume and format as:
    \\subsection*{{Job Title -- Company \\hfill Dates}}
    \\begin{{itemize}}[leftmargin=*,noitemsep]
        \\item Achievement (quantified if numbers available)
        \\item Achievement
    \\end{{itemize}}

    3. For {{{{SUMMARY}}}}: Write 2-3 sentences highlighting experience relevant to this job
    4. For {{{{SKILLS}}}}: Include only skills relevant to job description
    5. Use ONLY information from the resume below - DO NOT fabricate

    CRITICAL:
    - Return ONLY the complete LaTeX code
    - Start with \\documentclass
    - Escape special characters: % → \\%, & → \\&, # → \\#
    - Do not include markdown code blocks

    USER'S RESUME:
    {resume_content}

    JOB DESCRIPTION:
    {job_description_content}

    Generate the complete LaTeX document now:"""

        # Call Groq API
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=4000,
            temperature=0.7
        )

        return {
            "success": True,
            "resume": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.route('/api/generate-resume', methods=['POST'])
def generate_resume():
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'jobDescription' not in data or 'resume' not in data:
            return jsonify({
                "error": "Missing required fields: jobDescription and resume"
            }), 400

        job_description = data['jobDescription'].strip()
        resume = data['resume'].strip()
        template = data.get('template', '').strip() if data.get('template') else None

        if not job_description or not resume:
            return jsonify({
                "error": "Job description and resume cannot be empty"
            }), 400

        # Check for API key
        if not os.getenv("GROQ_API_KEY"):
            return jsonify({
                "error": "GROQ_API_KEY not found in environment variables. Please set it in your .env file"
            }), 500

        # Generate resume
        result = generate_resume_with_groq(resume, job_description, template)

        if result["success"]:
            latex_code = result["resume"]
            
            # Compile LaTeX to PDF
            pdf_result = compile_latex_to_pdf(latex_code)
            
            response_data = {
                "resume": latex_code,
                "usage": result["usage"]
            }
            
            # Add PDF if compilation succeeded
            if pdf_result["success"]:
                response_data["pdf"] = pdf_result["pdf_base64"]
            else:
                # Include PDF error but don't fail the request
                response_data["pdf_error"] = pdf_result["error"]
            
            return jsonify(response_data), 200
        else:
            return jsonify({
                "error": f"Failed to generate resume: {result['error']}"
            }), 500

    except Exception as e:
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "groq_api_configured": bool(os.getenv("GROQ_API_KEY"))
    }), 200


if __name__ == '__main__':
    print("Starting Flask server...")
    print(f"GROQ_API_KEY configured: {bool(os.getenv('GROQ_API_KEY'))}")
    app.run(debug=True, port=5000)
