🚀 Professional Release Automator
An AI-powered tool that analyzes GitHub commits and Pull Requests to generate structured, professional release notes. It automatically categorizes changes into Features, Fixes, Docs, and Breaking Changes.

🛠️ Setup Instructions
1. Clone the Repository
Bash
  git clone https://github.com/your-username/your-repo-name.git
  cd your-repo-name

2. Configure Environment Variables
   To protect your privacy, the .env file is excluded from this repository.
   Locate the .env.example file.
   Create a copy named .env.
Fill in your personal API keys:
  Plaintext
  # .env file
  GITHUB_TOKEN=your_github_personal_access_token
  GEMINI_API_KEY=your_google_gemini_api_key

3. Install Dependencies
It is recommended to use a virtual environment:
Bash
  # Create and activate environment
  python -m venv env
  source env/Scripts/activate  # Windows: .\env\Scripts\activate

  # Install libraries
  pip install -r requirements.txt

🚀 Usage
Run the main script to generate and sync your release notes:
Bash
  python generate_notes.py
  Enter the Repository: Type the user/repo (e.g., Namrata-Web/ClipBar).

AI Analysis: The system will fetch all changes since the last release.
Local Save: A RELEASE_NOTES.md file is created in your folder.
GitHub Sync: The script attempts to push the notes directly to the repository.

⚠️ Troubleshooting Errors
The tool uses a One-Word Cause system to help you diagnose issues quickly:

[AUTH]: Your GitHub token is invalid or expired.
[ACL]: Your token works, but you don't have "Write" permissions for that specific repository.
[RESOURCE]: The repository name is mistyped or the repo is private.
[QUOTA]: You have exceeded the Gemini API free tier limits (wait 60 seconds).
