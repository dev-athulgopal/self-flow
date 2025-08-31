#!/usr/bin/env python3
"""Self Flow - Desktop automation using Claude AI."""

from app.config import load_settings
from app.logger import setup_logger
from app.display import get_primary_display_size, take_screenshot
from app.anthropic_client import build_client, create_computer_use_request, encode_image_to_base64
from app.executor import execute_tool_use_actions
from app.ui import get_user_instruction, should_quit, display_loop_header


def process_single_instruction(client, settings, display_size, logger) -> bool:
    """Process a single user instruction and return success status."""
    try:
        # Get instruction from user
        logger.info("Requesting user instruction")
        instruction_text = get_user_instruction()
        
        if not instruction_text:
            return True  # Continue loop, no instruction provided
        
        if should_quit(instruction_text):
            logger.info("User requested to quit")
            return False  # Exit loop
        
        logger.info("User instruction received: '%s'", instruction_text)
        
        # Take screenshot of current screen
        logger.info("Capturing current screen state")
        screenshot_path = take_screenshot()
        logger.info("Screenshot captured: %s", screenshot_path)
        
        # Encode screenshot and send to Claude
        logger.info("Preparing request for Claude AI")
        img_b64 = encode_image_to_base64(screenshot_path)
        logger.info("Image encoded for transmission")
        
        # Send request to Claude
        logger.info("Sending request to Claude AI")
        response = create_computer_use_request(
            client=client,
            model="claude-sonnet-4-20250514",
            instruction_text=instruction_text,
            image_b64=img_b64,
            media_type="image/png",
            display_size=display_size,
            system_prompt=settings.system_prompt,
            max_tokens=settings.max_tokens,
        )
        
        logger.info("Claude AI response received successfully")
        
        # Execute actions
        logger.info("Starting action execution phase")
        actions_executed = execute_tool_use_actions(response, display_size)
        
        if actions_executed > 0:
            logger.info("Automation completed successfully. Executed %s action(s).", actions_executed)
        else:
            logger.info("No actions were executed.")
        
        return True  # Continue loop
        
    except Exception as e:
        logger.exception("Error processing instruction: %s", e)
        print(f"Error: {e}")
        print("Continuing with next instruction...")
        return True  # Continue loop despite error


def main() -> None:
    """Main entry point for Self Flow automation."""
    logger = setup_logger("self_flow")
    logger.info("Starting Self Flow automation")
    
    try:
        # Load settings and build client
        logger.info("Loading application configuration")
        settings = load_settings()
        logger.info("Configuration loaded successfully")
        
        logger.info("Building Anthropic client")
        client = build_client(settings.anthropic_api_key)
        logger.info("Anthropic client ready")
        
        # Get display information
        logger.info("Detecting display configuration")
        display_size = get_primary_display_size()
        logger.info("Display configuration: %sx%s", *display_size)
        
        # Display loop header
        display_loop_header()
        
        # Main loop for processing instructions
        instruction_count = 0
        while True:
            instruction_count += 1
            logger.info("Processing instruction #%s", instruction_count)
            
            # Process the instruction
            should_continue = process_single_instruction(client, settings, display_size, logger)
            
            if not should_continue:
                break
            
            print(f"\nInstruction #{instruction_count} completed. Ready for next instruction...")
        
        logger.info("Self Flow automation session completed. Processed %s instructions.", instruction_count)
        print(f"\nSession completed! Processed {instruction_count} instructions.")
        
    except Exception as e:
        logger.exception("Fatal error during automation: %s", e)
        print(f"Fatal Error: {e}")
        raise


if __name__ == "__main__":
    main()
