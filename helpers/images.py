from openai import OpenAI
import base64
import json
import os

def load_prompts(filepath):
    # Load the json content
    prompts = []
    with open(filepath, 'r') as file: 
        script_json = json.load(file)
        for scene_num, scene in script_json.items():
            prompts.append(scene['image'])

    return prompts

def generate_images(client, script_filepath, output_dir):

    prompts = load_prompts(script_filepath)

    #generate output directory if it doesn't already exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #for loop that makes png file for each prompt and generates image + writes it to file
    for i, prompt in enumerate(prompts, start=1):
        image_path = os.path.join(output_dir, f'image_{i}.png')
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            response_format="b64_json",
            n=1,
        )

        image_data = base64.b64decode(response.data[0].b64_json)
        with open(image_path, 'wb') as file:
            file.write(image_data)




