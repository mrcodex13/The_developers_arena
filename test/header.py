import requests
import os
import json
from dotenv import load_dotenv

load_dotenv() 

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "mrcodex13"
REPO_NAME = "repo_demo"
# print("key is " ,GITHUB_TOKEN)

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_pull_requests():
    # Endpoint to list pull requests
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
    response = requests.get(url, headers=headers)
    return response.json()

def get_pr_files(pr_number):
    # Endpoint to get the specific files changed in a PR
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/files"
    response = requests.get(url, headers=headers)
    return response.json()

def analyze_code(code_patch):

    # Define the system prompt and instructions
    prompt = f"""
You are an expert software engineer performing a code review.

Analyze the following code changes and suggest improvements,
possible bugs, performance issues, and style improvements.

Code Changes:
{code_patch}

Provide clear suggestions.
"""

    # Send the prompt to our local Ollama instance running Mistral
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    return result["response"]

def post_comment(pr_number, comment):

    # GitHub API treats PR comments as issue comments
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{pr_number}/comments"

    data = {
        "body": f"AI Code Review Suggestions:\n\n{comment}"
    }

    requests.post(url, headers=headers, json=data)