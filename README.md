# JARVIS Personal AI Assistant

A simple Python desktop chat assistant powered by Google's Gemini API.

## Security first
The API key you previously pasted into chat may be exposed. Revoke that key in Google AI Studio and create a new one. Do not put the key directly in `main.py`, upload `.env` to GitHub, or share screenshots containing it.

## Requirements
- Python 3.10 or newer
- Internet connection
- A Gemini API key from Google AI Studio

## Setup

### Windows
1. Install Python from https://www.python.org/downloads/ (enable “Add Python to PATH”).
2. Extract this project folder.
3. Open Command Prompt in the folder.
4. Create a virtual environment and install dependencies:

   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. Copy `.env.example` to a new file named `.env`.
6. Open `.env` and replace the placeholder with your NEW key:

   ```text
   GEMINI_API_KEY=your_new_key_here
   ```

7. Run the app:

   ```bat
   python main.py
   ```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your new key
python main.py
```

## Notes
- This is a text-chat desktop starter. It does not yet include voice input/output, wake-word detection, or desktop command execution.
- Conversation history is kept in memory for the current app session only.
- Never execute arbitrary commands suggested by an AI without reviewing them.
- If you see a model or quota error, check current model availability and usage in Google AI Studio.
