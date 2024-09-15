
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

file = open("token.txt", "r")
apikey = file.read()
file.close()

client = Groq(
    # This is the default and can be omitted
    api_key=apikey,
)

IMGprompt = ("Describe in great detail the facial expresions and body language of the largest and most prevalent person in the image. Also, start every description by saying START:")
# TXTprompt = ("Using the following description of a scenario, please provide a ranked listing of the emotions present in the people in image, by using the following format (keep in mind neutral does not mean happy, and yelling faces are angry): \n" +
#              "Happiness: x%\n" +
#              "Anger: x%\n" +
#              "Fear: x%\n" +
#              "Calmness: x%\n"
#              )
json_prompt = (
    "You are a data analyst API who analyzes emotional content in scenario descriptions, and responds in JSON. The JSON schema must include " +
    "{\n" +
    "\t'Happiness': 'number (0-100)'\n" +
    "\t'Anger': 'number (0-100)'\n" +
    "\t'Fear': 'number (0-100)'\n" +
    "\t'Calmness': 'number (0-100)'\n"
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
    string = str(json_message)
    #print("x", string)
    try:
        dict = eval(string) #fuck
        if 'Happiness' not in dict or 'Anger' not in dict or 'Fear' not in dict or 'Calmness' not in dict:
            return None
        return dict
    except:
        return None