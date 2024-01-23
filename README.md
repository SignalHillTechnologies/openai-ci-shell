
# openai-ci-shell
**A Wildly Inefficient and Expensive Cloud Shell needlessly wrapped in AI**\
Did you ever want a random remote shell to a system? Using the OpenAI Assistants SDK and the "Code Interpreter" plugin built-in, now anyone can have their own linux shell within an Ubuntu container that runs on OpenAI's "Untrusted" Kubernetes cluster. 

![Screenshot in action](/screenshot.gif)

# About
OpenAI made a bold decision to allow the use of ephemeral containers to plugin directly to AI generated output. This allows you to suggest python code that will run inline with your chat session, and for the most part it works pretty great. This shell just bypasses the use of the chat interface to perform that interaction.

On the backend, the Code Interpreter listens as a service on port 8080. When a request is received, the code launches using Jupyter Notebook and they're sandboxed within a specially designed container configured to enforce network isolation. This restricts the ability to perform traditional DNS requests as well as to reach out to webpages on the internet. Furthermore, this also appears to restrict the ability to interface with other restricted containers on the network, but more research may be needed there.

# Is This A Vulnerability?
Although this might look like a vulnerability, and operates identically to a remote shell, there is no vulnerability being taken advantage of-- this is just authorized use of the current code sandbox. The shell interface still uses the approved OpenAI SDK and a little prompt wizardry to provide a shell-like interface. 

**To be clear though**: You are running linux commands on a remote linux system. Although being parsed through the AI chat interface, it is not hallucinated generative text output, but instead code being run on a remote container. 

Other vulnerability researchers (including those participating in the bug bounty program) have availed themselves to attempt to break out of the sandbox using similar methods. This just eliminates the chat based abstraction.
 
That being said, it's possible that abuse of this utility might violate your terms of use. Don't do that. Be mindful and explore with a sense of community. If you do discover something, report it to OpenAI immediately (but also drop us a line!)

# How to Run

 1. Obtain an OpenAI API account and key 
 2. Clone or download this repo
 3. Run: pip install -r requirements.txt
 4. python3 shell.py

# Disclaimer
This software is provided "as is" and "as available," without any warranty of any kind, either expressed or implied. The user assumes all responsibility and risk for the use of this software. The authors or contributors are not liable for any damages arising from its use. By using this software, you agree to these terms.
