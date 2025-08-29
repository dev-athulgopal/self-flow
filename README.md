## Self Flow

Automate desktop actions with Anthropic computer-use and Python. Provide a screenshot and a natural-language instruction (e.g., "Click on calendar"); the app requests an action plan from Claude and optionally moves your cursor to the returned coordinates for verification.

### Features
- Vision + instruction request to Anthropic Messages (computer-use beta)
- Dynamically uses your primary display resolution
- Safe local executor (moves mouse with pyautogui)
- Structured logging and modular design

### Requirements
- Python 3.10+
- macOS (tested) with Accessibility permission for your terminal/Python to control the mouse
- Anthropic API key with access to computer-use beta

### Quick Start
1. Clone and install
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment
```bash
echo 'ANTHROPIC_API_KEY=your_key_here' > .env
```

3. Provide an input image
- Place a screenshot at `input.png` in the project root, or change the default path in `app/config.py`.

4. Run
```bash
python main.py
```

You should see:
- A response printed from the Anthropic API, including a `tool_use` block with a `coordinate` like `[x, y]`.
- The mouse will move to that location (no click) and log a confirmation.

### How It Works
- `main.py` wires the flow: load config → build client → encode image → call model → execute returned action.
- `app/config.py` loads settings from `.env`.
- `app/logger.py` provides consistent, human-friendly logs.
- `app/display.py` returns your primary display (width, height) via `pyautogui.size()` with fallback.
- `app/anthropic_client.py` prepares the request: mixed text + image content and the `computer` tool declaration.
- `app/executor.py` looks for `tool_use` blocks and moves the mouse to the requested coordinates.

### Model & Tools
- Model: `claude-sonnet-4-20250514` (adjust if your account uses a different identifier)
- Tools: `computer_20250124` with the `display_width_px` and `display_height_px` set dynamically

### Permissions (macOS)
If the cursor does not move:
- System Settings → Privacy & Security → Accessibility → enable for your Terminal (or IDE) and for the Python binary inside `venv`.

### Customize
- Change the instruction text in `main.py` (e.g., "Click on calendar").
- Add support for more actions (double-click, typing, key presses) in `app/executor.py` by mapping additional `action` values.
- Point to a different screenshot path in `.env` or by editing `app/config.py`.

### Troubleshooting
- No movement: confirm Accessibility permission and look for logs.
- Schema errors: ensure the `type` fields (`text`, `image`) match the SDK version and you have the correct beta flag: `betas=["computer-use-2025-01-24"]`.
- Blurry UI: increase virtual display size (it uses your primary display size by default).

### Development
Run formatters/linters of your choice; repository includes a `.gitignore` tuned for Python.

### Security Notes
- Your `ANTHROPIC_API_KEY` should be stored in `.env` (already gitignored).
- The executor only moves the mouse by default. Be careful before enabling actions that click or type automatically.

### License
MIT


