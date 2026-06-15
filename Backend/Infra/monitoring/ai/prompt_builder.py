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

        Rules:

        1. Use only provided information.
        2. Do not hallucinate.
        3. Confidence must be between 0 and 100.
        4. Recommendations must be actionable.

        Observability Data:

        {context}
    """