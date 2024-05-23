import os
import requests
from dotenv import load_dotenv
from comfyui.core.node import Node, Input, Output

# Load environment variables from a .env file
load_dotenv()

class NanocastOllamaBasic(Node):
    def __init__(self):
        super().__init__()
        self.api_endpoint = "http://localhost:8000/api"
        self.api_key = os.getenv("API_KEY")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True, 
                    "dynamicPrompts": False, 
                    "default": "Enter text here"
                }),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("narration", "image_prompts")
    FUNCTION = "parse_and_condense"
    CATEGORY = "Text Processing"

    def parse_and_condense(self, text):
        prompt = (
            f"Here is some news feed content: {text}\n"
            "You will create a narrative summary/script of this article. 1 article runs from Title to the next title. "
            "Highlight 15-30 prompts that will generate images relating to this story. "
            "Split these two outputs into 'narration' and 'image_prompts'."
        )

        response = requests.post(
            self.api_endpoint,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"text": prompt, "task": "parse_and_condense"}
        )

        if response.status_code == 200:
            result = response.json()
            narration = result.get("narration", "Error: No narration output.")
            image_prompts = result.get("image_prompts", "Error: No image prompts output.")
        else:
            narration = "Error: Unable to parse and condense text."
            image_prompts = "Error: Unable to generate image prompts."

        return narration, image_prompts

def register():
    node = NanocastOllamaBasic()
    ComfyUI.register_node(node)

NODE_CLASS_MAPPINGS = {
    "NanocastOllamaBasic": NanocastOllamaBasic
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NanocastOllamaBasic": "Ollama Parse and Condense"
}
