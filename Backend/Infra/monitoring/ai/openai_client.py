import json
from openai import OpenAI #type: ignore
from django.conf import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def ask_openai(prompt):

    response = client.responses.create(

        model="gpt-5",

        input=prompt
    )

    return response.output_text