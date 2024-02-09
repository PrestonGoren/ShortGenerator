# ShortGenerator

This project uses generative AI to create a short video from a single prompt.


This diagram details the flow of information from your initial prompt to the resulting video:
![mermaid-diagram-2024-02-09-143320](https://github.com/PrestonGoren/ShortGenerator/assets/80135054/d095bd05-76f4-4b69-8fae-be20e8b43d6f)

## Installation

Clone the repository
```bash
git clone "https://github.com/PrestonGoren/ShortGenerator.git"
```
If you want to use a virtual environment (recommended) run
```bash
python3 -m venv venv
source venv/bin/activate
```
Install the required dependencies
```bash
pip install -r "requirements.txt"
```
Navigate to the `.env` file and add your OpenAI key to the `OPENAI_API_KEY` field

## Usage/Examples

In the project folder, run:
```python
python3 script.py "Your prompt here"
```
An "output" directory will be generated with your output.

### Example
Here is an example output generated from the input "make a video about how the dolphin collective has been secretly taking over the world":


https://github.com/PrestonGoren/ShortGenerator/assets/80135054/cb6d8785-c29a-46a5-ad17-70772e04b3f2


## License

[MIT](https://choosealicense.com/licenses/mit/)


## TODO

upload example generated videos ✅


installation instructions ✅


usage instructions ✅


diagram showing how everything connects ✅


calculate token usage/cost for each video


more granular calculations for time taken (time taken for script, time taken for voiceovers, etc)

