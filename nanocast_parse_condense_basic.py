import requests
from comfyui.core.node import Node, Input, Output

class NanocastParseCondenseBasic(Node):
    def __init__(self):
        super().__init__()
        self.api_endpoint = "http://localhost:8000/api"
        self.api_key = "sk-5f806ca081db4f6abc88e89532e50624"

    @Input("text")
    def parse_and_condense(self, text):
        prompt = (
            f"Here is some news feed content: {text}\n"
            "You will create a 1-minute narration summary of this article. "
            "Highlight 30 prompts that will generate images relating to this story. "
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

    @Output("narration")
    def get_narration_output(self):
        return self.parse_and_condense[0]

    @Output("image_prompts")
    def get_image_prompts_output(self):
        return self.parse_and_condense[1]

# Register the node with ComfyUI
node = NanocastParseCondenseBasic()
ComfyUI.register_node(node)
