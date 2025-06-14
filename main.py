import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()

    verbose = '--verbose' in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('Usage: python main.py "Your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    user_prompt = ' '.join(args)
    model_name = 'gemini-2.0-flash-001'

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose, model_name)


def generate_content(client, messages, verbose, model_name):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    if not response.function_calls:
        return response.text
    
    for part in response.function_calls:
        try:
            function_call_result = call_function(part, verbose)
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Fatal error")
            if verbose and function_call_result.parts[0].function_response.response:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        except Exception as e:
            print(e)

    

if __name__ == "__main__":
    main()