import os
import sys
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from call_function import config, call_function

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=config)
        if response.candidates is not None:
            for cand in response.candidates:
                if cand.content is not None:
                    messages.append(cand.content)
        
        if not response.usage_metadata == None and args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls is not None:
            # list(map(lambda function_call: print(f"Calling function: {function_call.name}({function_call.args})"), response.function_calls))
            function_responses = []
            for func_call in response.function_calls:
                result = call_function(func_call, args.verbose)
                if result.parts is None or len(result.parts) == 0:
                    raise Exception("wrong response")
                if result.parts[0].function_response is None:
                    raise Exception("wrong response again")
                if result.parts[0].function_response.response is None:
                    raise Exception("wrong response again again")
                if args.verbose:
                    print(f"-> {result.parts[0].function_response.response}")
                
                function_responses.extend(result.parts)
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print(response.text)
            return
        
    print("Agent did not finish in time")
    sys.exit(1)

if __name__ == "__main__":
    main()
