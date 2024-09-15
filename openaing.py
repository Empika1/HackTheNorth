apikey = "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"

import base64
import json
from litellm import completion


MODEL = "gpt-4o-2024-08-06"

data = []

with open("pic.png", "rb") as file:
        file_content = file.read()
        base64_encoded = base64.b64encode(file_content).decode("utf-8")
response = completion(
    api_key=apikey,
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """
                    perform emotional analysis on this photo. return a response in JSON with nothing else:
{
    "happiness": <number, 0-100>,
    "sadness": <number, 0-100>,
    "anger": <number, 0-100>,
    "fear": <number, 0-100>,
    "calmness": <number, 0-100>,
}
                    """,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_encoded}"
                    },
                },
            ],
        }
    ],
    response_format={"type": "json_object"},
)
parsed_response = json.loads(response.choices[0].message.content)
print(parsed_response)