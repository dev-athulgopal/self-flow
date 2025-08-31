# Self-Flow 🤖

**AI-Powered Desktop Automation using Claude AI**

Self-Flow is a Python-based desktop automation tool that leverages Claude AI to understand natural language instructions and execute computer actions automatically. It can perform mouse movements, clicks, typing, keyboard shortcuts, and more based on your verbal commands.

## 🏗️ Architecture

### Core Components

```
self-flow/
├── main.py                 # Main entry point and orchestration
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── logger.py          # Logging setup
│   ├── display.py         # Screen capture and display utilities
│   ├── anthropic_client.py # Claude AI API integration
│   ├── executor.py        # Action execution engine
│   └── ui.py             # User interface and input handling
├── requirements.txt       # Python dependencies
└── README.md
```

### Architecture Flow

```
User Input → Screenshot Capture → Claude AI Analysis → Action Execution → Feedback
     ↓              ↓                    ↓              ↓              ↓
Natural Language → Screen State → AI Understanding → Computer Actions → Results
```

### Key Design Principles

- **Modular Design**: Each component has a single responsibility
- **Error Handling**: Robust error handling with retry mechanisms
- **Logging**: Comprehensive logging for debugging and monitoring
- **Configuration**: Environment-based configuration management
- **Safety**: Built-in failsafe mechanisms for automation actions

## 🚀 Features

### Available Actions

| Action | Description | Parameters |
|--------|-------------|------------|
| `left_click` | Left mouse click | `{"coordinate": [x, y]}` |
| `right_click` | Right mouse click | `{"coordinate": [x, y]}` |
| `double_click` | Double mouse click | `{"coordinate": [x, y]}` |
| `move` | Move cursor | `{"coordinate": [x, y]}` |
| `type` | Type text | `{"text": "your text"}` |
| `key` | Press single key | `{"key": "enter"}` |
| `key_combination` | Press key combo | `{"keys": ["cmd", "c"]}` |
| `scroll` | Scroll up/down | `{"direction": "down", "amount": 3}` |
| `drag` | Drag and drop | `{"start_coordinate": [x1, y1], "end_coordinate": [x2, y2]}` |
| `wait` | Wait for duration | `{"duration": 1.0}` |

### AI Capabilities

- **Visual Understanding**: Analyzes screenshots to understand context
- **Natural Language Processing**: Interprets human-like instructions
- **Smart Action Planning**: Determines optimal sequence of actions
- **Context Awareness**: Maintains understanding of current screen state

## 📋 Prerequisites

- Python 3.8+
- macOS (currently optimized for macOS)
- Anthropic API key
- Internet connection for AI processing

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dev-athulgopal/self-flow.git
   cd self-flow
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env  # If available
   # Or create .env file manually:
   echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Getting Your Anthropic API Key

1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

## 🎯 Usage

### Basic Usage

1. **Start the application**
   ```bash
   python main.py
   ```

2. **Provide instructions**
   - Type natural language commands like:
     - "Click the login button"
     - "Type 'Hello World' in the text field"
     - "Open the file menu and select 'Save'"
     - "Scroll down to see more content"

3. **Watch automation happen**
   - The AI will analyze your screen
   - Execute the requested actions
   - Provide feedback on completion

### Example Commands

```
"Click the blue button in the top right corner"
"Type my email address in the username field"
"Press Command+S to save the document"
"Scroll down to see the bottom of the page"
"Right-click on the file and select 'Delete'"
"Drag the image from the left panel to the right panel"
```

### Safety Features

- **Failsafe**: Move mouse to top-left corner to stop automation
- **Coordinate Validation**: All coordinates are validated against screen bounds
- **Retry Logic**: Actions are retried up to 2 times on failure
- **Error Handling**: Graceful error handling with detailed logging

## 🔧 Advanced Configuration

### Custom System Prompts

Modify the system prompt in `app/config.py` to customize AI behavior:

```python
DEFAULT_SYSTEM_PROMPT = """Your custom instructions here..."""
```

### Logging Configuration

Adjust logging levels in `app/logger.py`:

```python
logging.basicConfig(level=logging.INFO)  # Change to DEBUG for more detail
```

### Action Parameters

Customize action behavior in `app/executor.py`:

```python
# Adjust retry attempts
max_retries: int = 3

# Modify timing delays
time.sleep(0.5)  # Increase for slower systems
```

## 🐛 Troubleshooting

### Common Issues

1. **Permission Denied Errors**
   - Ensure you have accessibility permissions enabled
   - Grant permissions to Terminal/IDE in System Preferences

2. **API Key Issues**
   - Verify your `.env` file exists and contains the correct API key
   - Check that the API key is valid and has sufficient credits

3. **Action Failures**
   - Check the logs for detailed error information
   - Ensure the target elements are visible on screen
   - Verify coordinates are within screen bounds

4. **Performance Issues**
   - Reduce screenshot frequency if needed
   - Adjust timing delays in the executor
   - Check your internet connection for AI processing

### Debug Mode

Enable detailed logging by modifying the logger level:

```python
# In app/logger.py
logging.basicConfig(level=logging.DEBUG)
```

## 📚 API Reference

### Main Functions

- `main()`: Application entry point
- `process_single_instruction()`: Process user input and execute actions
- `execute_tool_use_actions()`: Execute AI-generated actions

### Configuration

- `Settings`: Configuration dataclass
- `load_settings()`: Load configuration from environment

### Action Execution

- `execute_action_with_retry()`: Execute action with retry logic
- `validate_coordinate()`: Validate screen coordinates
- `validate_action_parameters()`: Validate action parameters

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for Claude AI
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for desktop automation
- [Python-dotenv](https://github.com/theskumar/python-dotenv) for environment management

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/dev-athulgopal/self-flow/issues) page
2. Review the logs for error details
3. Create a new issue with detailed information

---

**⚠️ Disclaimer**: This tool automates computer actions. Use responsibly and ensure you have proper permissions for any actions performed on your system.
