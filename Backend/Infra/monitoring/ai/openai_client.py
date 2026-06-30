import json
from openai import OpenAI #type: ignore
from django.conf import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


# def ask_openai(prompt):

#     response = client.responses.create(
#         model="gpt-4o-mini",
#         # input=prompt
#         input=prompt,
#         text={
#             "format": {
#                 "type": "json_object"
#             }
#         }
#     )
    
#     return response.output_text


def ask_openai(prompt, json_mode=False):

    kwargs = {
        "model": "gpt-4o-mini",
        "input": prompt,
    }

    if json_mode:
        kwargs["text"] = {
            "format": {
                "type": "json_object"
            }
        }

    response = client.responses.create(**kwargs)

    return response.output_text