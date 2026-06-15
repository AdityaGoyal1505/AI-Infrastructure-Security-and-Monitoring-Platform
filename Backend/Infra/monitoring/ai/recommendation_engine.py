import json

from .openai_client import ask_openai
from monitoring.models import Recommendation

def generate_recommendations(root_cause,summary):

    prompt = f"""
        You are a Senior Site Reliability Engineer.

        Given the root cause analysis:

        Root Cause:
        {root_cause}

        Summary:
        {summary}

        Return ONLY JSON.

        Format:

        {{
        "recommendations": [
            {{
            "title": "...",
            "description": "...",
            "priority": "LOW|MEDIUM|HIGH|CRITICAL"
            }}
        ]
        }}
    """

    response = ask_openai(prompt)

    return json.loads(response)

def store_recommendations(workspace,node_id,rca):

    result = generate_recommendations(rca.root_cause,rca.summary)

    for item in result["recommendations"]:

        Recommendation.objects.create(

            workspace=workspace,

            node_id=node_id,

            root_cause_analysis=rca,

            title=item["title"],

            description=item["description"],

            priority=item["priority"]
        )