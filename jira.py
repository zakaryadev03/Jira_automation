from flask import Flask, request
import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_TOKEN = os.getenv("JIRA_API_TOKEN")
EMAIL = os.getenv("JIRA_EMAIL")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
ISSUE_TYPE_ID = os.getenv("JIRA_ISSUE_TYPE_ID")

# Set up Flask app
app = Flask(__name__)


@app.route('/createJira', methods=['POST'])
def createJira():
    payload = request.json
    issue = payload.get("issue", {})


    labels = [label["name"] for label in issue.get("labels", [])]
    if "confirmed" not in labels:
        return "Issue not confirmed — no Jira ticket created.", 200

    summary = issue.get("title")
    description_text = issue.get("body", "")

    url = "https://veeramallaabhishek.atlassian.net/rest/api/3/issue"
    auth = HTTPBasicAuth(EMAIL, API_TOKEN)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    jira_payload = json.dumps({
        "fields": {
            "project": { "key": PROJECT_KEY },
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{
                        "type": "text",
                        "text": description_text
                    }]
                }]
            },
            "issuetype": { "id": ISSUE_TYPE_ID }
        }
    })

    response = requests.post(url, headers=headers, auth=auth, data=jira_payload)

    return response.text, response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
