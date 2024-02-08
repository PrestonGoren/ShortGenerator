from openai import OpenAI
from dotenv import load_dotenv
import helpers.images as images
import helpers.video as video
import helpers.voiceover as voiceover
import helpers.script as script
import json
import sys
import os
import uuid
import time

start_time = time.time()

#load environment variables from .env file
load_dotenv()

#instantiate OpenAI client
client = OpenAI()

#if no command line prompt input is given, output error and exit
if len(sys.argv) < 2:
    print("Please provide a prompt")
    sys.exit()

#retrieve command line prompt input
prompt = sys.argv[1]

#if output directory does not exist, create one
if not os.path.exists("output"):
    os.makedirs("output")

#create unique id for this video's output
output_id = str(uuid.uuid4())

#create a folder in the output directory for this video
output_dir = f"output/{output_id}"
os.makedirs(output_dir)

#generate script
print("Generating script for prompt '" + prompt + "'...")
script.generate_script(client, prompt, output_dir)

#generate voiceovers
print("Generating voiceovers...")
voiceover.generate_voiceovers(client, f"{output_dir}/script.json", f"{output_dir}/voiceovers")

#generate images
print("Generating images...")
images.generate_images(client, f"{output_dir}/script.json", f"{output_dir}/images")

#combine into video
print("Combining into video...")
video.generate_video(output_dir)

end_time = time.time()
time_taken = end_time - start_time

print(f"Video generated in {time_taken} seconds")