import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import argparse



def generate_response(model_name: str, user_prompt:str):

    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16, device_map="auto")

    # Format prompt using chat template
    messages = [{"role": "user", "content": user_prompt}]
    formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    # Tokenize input
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(model.device)

    # Generation config (same as llm_wrapper.py)
    generation_config = GenerationConfig(
        max_new_tokens=1024,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )

    ## Generation config with sampling
    # generation_config = GenerationConfig(
    #     max_new_tokens=1024,
    #     do_sample=True,
    #     temperature=0.3,
    #     top_p=0.9,
    #     pad_token_id=tokenizer.eos_token_id
    #     )


    # Generate response
    with torch.no_grad():
        output_tokens = model.generate(**inputs, generation_config=generation_config)

    # Decode only newly generated tokens
    input_length = inputs['input_ids'].shape[1]
    newly_generated_tokens = output_tokens[0, input_length:]
    response = tokenizer.decode(newly_generated_tokens, skip_special_tokens=True).strip()
    print(user_prompt)
    print(response)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-r", "--resume", required=True)
    arg_parser.add_argument("-j", "--job_description", required=True)
    arg_parser.add_argument("-t", "--template", required=True, default="txt_files/template.txt")

    args = arg_parser.parse_args()
    model_name = "deepseek-ai/deepseek-coder-6.7b-instruct"
    user_prompt = "Take the resume of the user and generate a latex code for the resume based on the job description. You are allowed to bluff but do not MAKE UP ANY stats. Resume: {args.resume} Job Description: {args.job_description} Template: {args.template}"
    generate_response(model_name, user_prompt)


if __name__ == "__main__":
    main()