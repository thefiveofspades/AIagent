import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_ITERS


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

    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose, model_name)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


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

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)
    
    if not response.function_calls:
        return response.text
    
    function_responses = []
    for part in response.function_calls:
        function_call_result = call_function(part, verbose)
        if not function_call_result.parts[0].function_response or not function_call_result.parts:
            raise Exception("Empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
    if not function_responses:
        raise Exception("No function responses generated, exiting.")
    
    messages.append(types.Content(role="tool", parts=function_responses))

if __name__ == "__main__":
    main()