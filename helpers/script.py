from openai import OpenAI
import json
import os

def generate_script(client, prompt, output_dir):
    response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": """
        You are a short form video creator that will create the script and scene descriptions for a short form (30-60 second) online video. 
        Based on the given topic / idea / concept, you will write the script for the video and provide image descriptions that will be fed to an image generation model to provide the visual component of the video. 
        For each sentence of the script provide an accompanying image description. Output in the following json format:
    {     
        "scene1": {
            "sentence": "sentence1",
            "image":"image for sentence1"
        },
        "scene2": {
            "sentence": "sentence2",
            "image":"image for sentence2"
        }    
    }"""},
        {"role": "user", "content": prompt}
    ]
    )

    json_content = json.loads(response.choices[0].message.content)

    with open(f"{output_dir}/script.json", 'w') as json_file:
        json.dump(json_content, json_file, indent=4)
        print("Script written to script.json")
    