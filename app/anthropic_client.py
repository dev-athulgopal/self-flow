from typing import Any, Dict, Tuple
import base64
import anthropic


def build_client(api_key: str) -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=api_key)


def encode_image_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def create_computer_use_request(
    client: anthropic.Anthropic,
    model: str,
    instruction_text: str,
    image_b64: str,
    media_type: str,
    display_size: Tuple[int, int],
    max_tokens: int = 512,
) -> Any:
    width, height = display_size
    return client.beta.messages.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instruction_text},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_b64,
                        },
                    },
                ],
            }
        ],
        tools=[{
            "type": "computer_20250124",
            "name": "computer",
            "display_width_px": width,
            "display_height_px": height,
            "display_number": 0,
        }],
        betas=["computer-use-2025-01-24"],
        max_tokens=max_tokens,
    )


