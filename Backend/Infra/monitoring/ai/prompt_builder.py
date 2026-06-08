def build_root_cause_prompt(context):

    return f"""
        You are an expert Site Reliability Engineer.

        Analyze the observability data.

        Return ONLY valid JSON.

        Format:

        {{
            "root_cause": "...",
            "summary": "...",
            "confidence": 0,
            "recommendations": [
                "...",
                "..."
            ]
        }}

        Observability Data:

        {context}
    """