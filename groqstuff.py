
from groq import Groq
import base64
import json

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def load_image(image_path):
    image_path = image_path
    base64_image = encode_image(image_path)
    return base64_image

client = Groq(
    # This is the default and can be omitted
    api_key="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",
)

IMGprompt = ("Give me detailed and lengthly text describing the scenery in the image, the people in it, and the general scenario of what is happening. Be sure to mention their facial expressions and body language, and also if they are smiling or not. Also, start every description by saying START:")
TXTprompt = ("Using the following description of a scenario, please provide a ranked listing of the emotions present in the image, by using the following format: \n" +
             "Happiness: x%\n" +
             "Sadness: x%\n" +
             "Anger: x%\n" +
             "Fear: x%\n" +
             "Calmness: x%\n"
             )
json_prompt = (
    "You are a data analyst API who analyzes emotional content in texts, and responds in JSON.  The JSON schema should include " +
    "{\n" +
    "\t'emotion_analysis': {\n" +
    "\t\t'Happiness': 'number (0-100)'\n" +
    "\t\t'Sadness': 'number (0-100)'\n" +
    "\t\t'Anger': 'number (0-100)'\n" +
    "\t\t'Fear': 'number (0-100)'\n" +
    "\t\t'Calmness': 'number (0-100)'\n"
    "\t}" +
    "}")

def describe_image(image_path, print_it=False):
    
    check = "TEST"
    img = load_image(image_path)
    
    while "Start".lower() not in check:

        image_chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user", 
                    "content": [
                        {"type": "text", "text": IMGprompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img}",
                            },
                        },
                    ],
                }
            ],
            model="llava-v1.5-7b-4096-preview",
        )
        check = image_chat_completion.choices[0].message.content.lower()
    
    if print_it == True:
        print(check)
    return check

def list_emotions(image_path, print_it = False):

    description = describe_image(image_path)
    
    text_chat_completion = client.chat.completions.create(
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": json_prompt
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": description
            }
        ],
        # The language model which will generate the completion.
        model="llama3-8b-8192",
        response_format={"type": "json_object"}
    )

    if print_it == True:
        print(text_chat_completion.choices[0].message.content)
        
    return json_to_dict(text_chat_completion.choices[0].message.content)

def json_to_dict(json_message):
    data = json.loads(json_message)
    return(data['emotion_analysis'])
    
print(list_emotions("C:\\beach.jpg"))