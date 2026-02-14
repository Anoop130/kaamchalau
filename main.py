import argparse
from anthropic import Anthropic
import os, subprocess
from dotenv import load_dotenv
import json

def generate_response(user_prompt):
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return response

def get_prompt(args: argparse.Namespace) -> str:


    with open(args.resume, "r") as f:
        resume_content = f.read()
    with open(args.job_description, "r") as f:
        job_description_content = f.read()
    with open(args.template, "r") as f:
        template_content = f.read()

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
    return user_prompt

def main():
    load_dotenv()
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-r", "--resume", required=True)
    arg_parser.add_argument("-j", "--job_description", required=True)
    arg_parser.add_argument("-t", "--template", default="txt_files/template.txt")
    args = arg_parser.parse_args()


    user_prompt = get_prompt(args)
    response =generate_response(user_prompt)
    print(response.content[0].text)
    print(response.usage.input_tokens)
    print(response.usage.output_tokens)
    total_tokens = response.usage.input_tokens + response.usage.output_tokens
    print(total_tokens)

    # convert response to dict 
    response_dict = {
        'id': response.id,
        'type': response.type,
        'role': response.role,
        'model': response.model,
        'content': [
            {
                'type': block.type,
                'text': block.text
            } for block in response.content
        ],
        'stop_reason': response.stop_reason,
        'stop_sequence': response.stop_sequence,
        'usage': {
            'input_tokens': response.usage.input_tokens,
            'output_tokens': response.usage.output_tokens
        }
    }
    with open("response.txt", "w") as f:
        json.dump(response_dict, f, indent=2)    
    with open("resume.tex", "w") as f:
        f.write(response.content[0].text)

if __name__ == "__main__":
    main()