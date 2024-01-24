
# openai-ci-shell
**A Wildly Inefficient and Expensive Cloud Shell Needlessly Wrapped in AI**\
\
\
![Screenshot in action](/screenshot.gif)\
Did you ever want a random remote shell to a system? Using the OpenAI Assistants SDK and the use of the "Code Interpreter", now anyone can have their own linux shell within an Ubuntu container that runs on OpenAI's "Untrusted" Kubernetes cluster. 
# About
OpenAI made a bold decision to allow the use of ephemeral containers to plugin directly to AI generated output. This allows you to suggest python code that will run inline with your chat session, and for the most part it works pretty great. This shell just bypasses the use of the chat interface to perform that interaction.

On the backend, the Code Interpreter listens as a service on port 8080. When a request is received, the code launches using Jupyter Notebook and they're sandboxed within a specially designed container configured to enforce network isolation. This restricts the ability to perform DNS requests as well as to reach out to webpages on the internet. Furthermore, this also appears to restrict the ability to interface with other restricted containers on the network, but more research may be needed there.

# Is this a vulnerability?
Although this might look like a vulnerability, and operates similarly to a remote shell, there is no vulnerability being taken advantage of-- this is just authorized use of the current code sandbox. The shell interface still uses the approved OpenAI SDK and a little prompt wizardry to provide a shell-like interface. The code interpreter sandbox is afforded access to the local filesystem and through the use of subprocess calls in python, you can run linux commands.

**To be clear**: You are running commands on a remote linux system. Although being parsed through the AI chat interface, responses are not hallucinated generative text output, but instead code being run on a remote container hosted by OpenAI. Their container includes an entire linux filesystem as well as all of the necessary components to handle inputs into Jupyter Notebook. The only exception to this is where it pertains to error handling or where there is a prompt-based restriction to prohibit certain activities. The sandbox container has restrictions, and between the AI and the container configuration, both are working to prevent you from abusing their services. Navigating around this is an exercise for the user. 

That being said, it's possible that abuse of this utility might violate your terms of use. Don't do that. Be mindful and explore with a sense of community. If you do discover something, report it to OpenAI immediately (but also drop us a line!)

# How to run

 1. Obtain an OpenAI API account and key 
 2. Clone or download this repo
 3. Run: pip install -r requirements.txt
 4. Set your environment variable OPENAI_API_KEY to your OpenAI API key
 4. python3 openai-shell.py

# Known Limitations
- Many commands you may be used to in linux aren't installed on the container. In many cases you can actually use the Code Interpreter to approximate that functionality for you using python libraries
- No support for uploading and downloading files but it's definitely possible within chat, so could be possible at a later date
- Despite output coming from the code interpreter, it's still parsed and tokenized by the AI in the format currently being read. This means that commands that return a large amount of text may take a moment to actually return data. It also may be truncated, or warped arbitrarily. It's technically possible to get the output directly from the Code Interpreter, but I haven't investigated too closely
- Code interpreter has a timeout on commands that run a long period of time, so bear that in mind for anything with a large amount of output as well
- Pipes and redirects do not work correctly
- 
# Funny quirks
- Since the shell interpreter is being parsed by the AI, you can also issue commands like "Use the psutils python library to output the equivalent of netstat -tan" for commands that don't exist. 
- If you don't get a response back, try again. 
- Error handling is a bit ramshackle, and prone to "interpretation"
- Sometimes typos will get autocorrected for you -- again, this is not a strict shell interpreter but AI is converting your inputs to python code on the backend.
- Using "cd" commands are a dreadful hack, it kinda works, but sometimes doesn't. If something isn't working right, you're better off just issuing it to the directory you have in mind "ls /etc" for example.

# How do I know this isn't just fake AI generated output mimicking a shell?
- You can gauge the amount of determinism yourself from interactions on the filesystem but a few notes:
  - Getting the current time: LLMs do not have a concept of "now", but using the "Code Interpreter" you can obtain the current date and time. Give it a whirl within the shell by running the date command if you'd like. 
  - Obtaining response headers from local service ports such as 8080 also include the correct time.
  - Output of files are consistently deterministic and localized to the container, including the structure of hostnames and kubernetes configurations.
- With all of the above being considered, error responses and commands that may override with its prompted security controls (such as those enforcing no network access) will return AI generated responses. It is possible to work around them, but that is an exercise for the user.
- Remember that your commands being issued are being converted to python using the code interpreter. In most cases this will be a straight subprocess call to the command in linux, but in some cases it may not. 

# Disclaimer
This software is provided "as is" and "as available," without any warranty of any kind, either expressed or implied. The user assumes all responsibility and risk for the use of this software. The authors or contributors are not liable for any damages arising from its use. By using this software, you agree to these terms.
