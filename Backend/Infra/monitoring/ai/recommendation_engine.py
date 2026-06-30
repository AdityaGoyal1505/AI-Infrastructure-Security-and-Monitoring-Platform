import json

from .openai_client import ask_openai
from monitoring.models import Recommendation

def generate_recommendations(root_cause, summary):
    prompt = f"""
        You are a Senior Site Reliability Engineer.

        Analyze the following Root Cause Analysis.

        Root Cause:
        {root_cause}

        Summary:
        {summary}

        IMPORTANT:
        Return your response as a valid JSON object only.
        Do not include markdown.
        Do not include explanation.
        Do not wrap it inside ```.

        The JSON schema is:

        {{
        "recommendations": [
            {{
            "title": "string",
            "description": "string",
            "priority": "LOW|MEDIUM|HIGH|CRITICAL"
            }}
        ]
        }}
        """

    response = ask_openai(prompt,json_mode=True)

    return json.loads(response)

def store_recommendations(workspace,node_id,rca):
    existing = Recommendation.objects.filter(

        workspace=workspace,

        node_id=node_id,

        root_cause_analysis=rca

    )

    if existing.exists():

        print(

            f"[RECOMMENDATION] "

            f"Skipping "

            f"{node_id}"

        )

        return
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