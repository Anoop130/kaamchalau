import argparse
from groq import Groq
import os, subprocess
from dotenv import load_dotenv
import json

def generate_response(user_prompt):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": user_prompt}],
        max_tokens=4000,
        temperature=0.7
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
    print(response.choices[0].message.content)
    print(response.usage.prompt_tokens)
    print(response.usage.completion_tokens)
    total_tokens = response.usage.total_tokens
    print(total_tokens)

    # convert response to dict 
    response_dict = {
        'id': response.id,
        'model': response.model,
        'choices': [
            {
                'index': choice.index,
                'message': {
                    'role': choice.message.role,
                    'content': choice.message.content
                },
                'finish_reason': choice.finish_reason
            } for choice in response.choices
        ],
        'usage': {
            'prompt_tokens': response.usage.prompt_tokens,
            'completion_tokens': response.usage.completion_tokens,
            'total_tokens': response.usage.total_tokens
        }
    }
    with open("response.txt", "w") as f:
        json.dump(response_dict, f, indent=2)    
    with open("resume.tex", "w") as f:
        f.write(response.choices[0].message.content)

if __name__ == "__main__":
    main()