from google import genai

from django.conf import settings


client = genai.Client(api_key=settings.GEMINI_API_KEY)


def ask_gemini(prompt):

    try:

        response = client.models.generate_content(

            model="gemini-2.5-flash-lite",

            contents=prompt,

            config={

                "max_output_tokens": 250,

                "temperature": 0.3,

            }

        )

        return response.text

    except Exception as e:

        print(

            "[GEMINI ERROR]",

            e

        )

        return (

            "I am currently unable to answer your question. "

            "Please try again in a few moments."

        )