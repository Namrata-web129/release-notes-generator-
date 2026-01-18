# Python Project

This is a Python project with a virtual environment.

## Setup

1. Activate the virtual environment:
   - On Windows: `env\Scripts\activate`
   - On macOS/Linux: `source env/bin/activate`

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run your Python scripts.

## The Professional workflow

1. Create a clean environment: python -m venv env

2. Activate it: source env/Scripts/activate (or .\env\Scripts\activate on Windows)

3. Install the "Shopping List": pip install -r requirements.txt

## One Small Warning
1. Install Python on their system.

2. Create their own .env file with their own GITHUB_TOKEN and GEMINI_API_KEY, because for security reasons, you should never share your personal keys in your code or on GitHub.
## Troubleshooting

- If `python` command not found, ensure Python is installed and added to PATH.
- If activation fails, check the virtual environment path.

