import os
from openai import OpenAI
from dotenv import load_dotenv
import time
import json
import re

# Change this if you want I guess
MODEL="gpt-4-1106-preview"
PWD="/home/sandbox" # This is the current OpenAI PWD

def print_header():
    print(
r"""
________                           _____  .___    _________.__           .__  .__   
\_____  \ ______   ____   ____    /  _  \ |   |  /   _____/|  |__   ____ |  | |  |  
 /   |   \\____ \_/ __ \ /    \  /  /_\  \|   |  \_____  \ |  |  \_/ __ \|  | |  |  
/    |    \  |_> >  ___/|   |  \/    |    \   |  /        \|   Y  \  ___/|  |_|  |__
\_______  /   __/ \___  >___|  /\____|__  /___| /_______  /|___|  /\___  >____/____/
        \/|__|        \/     \/         \/              \/      \/     \/                     
    """)
    print('DISCLAIMER:  This software is provided "as is" and "as available," without any warranty of any kind, either expressed or implied. The user assumes all responsibility and risk for the use of this software. The authors or contributors are not liable for any damages arising from its use. By using this software, you agree to these terms.')
    print("NOTE: Use \"exit\" or \"quit\" to properly exit (and delete the assistant when you're done)")
    print("")
    print("")
    return

def validate_env_variables():
    required_vars = ['OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if os.getenv(var) is None]

    if missing_vars:
        print("You need to add the following environment variables: " + ", ".join(missing_vars))
        print("Please set these variables in your environment or .env file.")
        exit(1)

def extract_json(text):
    matches = re.findall(r'\{[^{}]*\}', text)
    for match in matches:
        try:
            cleaned_match = match.replace('\n', '')
            return json.loads(cleaned_match)
        except json.JSONDecodeError:
            continue
    return None
    
def interact_with_openai():
    global PWD
    # Load environment variables
    load_dotenv()
    validate_env_variables()
    
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )
    # Create an assistant run and let's chat with em
    while True:
        user_input = input("OpenAIShell[" + PWD + "]$> ")
        if user_input.lower() in ['exit', 'quit']:
            assistant = client.beta.assistants.delete(
                assistant_id=assistant.id
              )
            break
        try:
            assistant = client.beta.assistants.create(
                name="OpenAIShell",
                instructions='You are operating as a shell whose only purpose is to pass commands to the code interpreter using python as if it were a shell. Execution should be attempted to evaluate the restrictions of the sandbox. It is also permitted to perform network requests to the extent they are allowed by the operating system. Evaluate the use of "cd" commands to update the PWD for any commands. Your output must ONLY be in the format of:\n {\n\t "pwd" : "<current working directory>",\n\t"cmd_output": ["<command output>"],\n\t"error": "<Single line error response if applicable from the exception>"}\n\nThis must be properly formatted JSON. No other data is permitted in the response!',
                tools=[{"type": "code_interpreter"}],
                model=MODEL
            )
        except Exception as e:
            print(f"Error creating assistant: {e}")

        thread = client.beta.threads.create() 
        try:
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content="Run the command from the following directory: " + PWD + "\n\n###\nShell input: " + user_input
            )

            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id
            )

            timeout = time.time() + 120 # I feel like there's gotta be a better way than this but whatever
            while time.time() < timeout:
                run_status = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
            
                if run_status.status in ["completed", "requires_action"]:
                    break
                time.sleep(1)  # Wait for 1 second before checking again

            if run_status.status == "requires_action":
                print("Whoops this shouldn't have happened, maybe try again?")
                
            elif run_status.status == "completed":
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                raw_response = messages.data[0].content[0].text.value
                extracted_json = extract_json(messages.data[0].content[0].text.value)
                if extracted_json == None:
                    print("Poorly formatted response, maybe try again? Received: " + raw_response[:50])
                else:
                    PWD = extracted_json['pwd']
                    for lines in extracted_json['cmd_output']:
                        print(lines)
                    if extracted_json['error']:
                        print(extracted_json['error'])

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print_header()
    interact_with_openai()