from openai import OpenAI
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import json
import os

def load_sentences(filepath):
    # Load the json content
    sentences = []
    with open(filepath, 'r') as file: 
        script_json = json.load(file)
        for scene_num, scene in script_json.items():
            sentences.append(scene['sentence'])

    return sentences

def generate_voiceovers(client, script_filepath, output_dir):

    sentences = load_sentences(script_filepath)

    #generate output directory if it doesn't already exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #for loop that makes voiceover mp3 file for each sentence and generates voiceover + streams it to file
    for i, sentence in enumerate(sentences, start=1):
        voiceover_path = os.path.join(output_dir, f'voiceover_{i}.mp3')
        response = client.audio.speech.create(
            model="tts-1-hd",
            voice="onyx",
            input=sentence,
            speed=1.2
        )
        # Stream the response to a file
        response.stream_to_file(voiceover_path)       

        #use pydub to trim silence from start and end of audio file
        audio = AudioSegment.from_file(voiceover_path, format="mp3")
        non_silence_ranges = detect_nonsilent(audio, min_silence_len=100, silence_thresh=-50)

        if non_silence_ranges:
            start_trim = non_silence_ranges[0][0]
            end_trim = non_silence_ranges[-1][1]
            trimmed_audio = audio[start_trim:end_trim]

            # Overwrite the original file with the trimmed audio
            trimmed_audio.export(voiceover_path, format="mp3")

        #print(f'Generated voiceover for sentence {i}: {voiceover_path}')



