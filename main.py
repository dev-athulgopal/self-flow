from app.config import load_settings
from app.logger import setup_logger
from app.display import get_primary_display_size
from app.anthropic_client import build_client, encode_image_to_base64, create_computer_use_request
from app.executor import execute_tool_use_actions


def main() -> None:
    logger = setup_logger("self_flow")
    try:
        settings = load_settings()
        client = build_client(settings.anthropic_api_key)
        img_b64 = encode_image_to_base64(settings.default_image_path)
        display_size = get_primary_display_size()
        response = create_computer_use_request(
            client=client,
            model="claude-sonnet-4-20250514",
            instruction_text="Click on calendar",
            image_b64=img_b64,
            media_type="image/png",
            display_size=display_size,
        )
        logger.info("Request sent successfully.")
        print(response)
        execute_tool_use_actions(response)
    except Exception as e:
        logger.exception("Fatal error: %s", e)


if __name__ == "__main__":
    main()