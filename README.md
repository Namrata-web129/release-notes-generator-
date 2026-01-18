# 🚀 Professional Release Automator

An AI-powered tool that analyzes GitHub commits and Pull Requests to generate structured release notes.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

### 2. Configure Environment Variables
To protect your privacy, the `.env` file is excluded from this repository. Locate the `.env.example` file and create a copy named `.env`.

**Fill in your keys in this format:**

```plaintext
# .env file (This is configuration, not code)
GITHUB_TOKEN=your_github_personal_access_token
GEMINI_API_KEY=your_google_gemini_api_key

### 3. Install Dependencies
It is recommended to use a virtual environment to avoid dependency conflicts. Follow these steps in your terminal:

```bash
# Create a virtual environment
python -m venv env

# Activate the environment
# Windows:
.\env\Scripts\activate

# Mac/Linux:
source env/bin/activate

# Install all required libraries
pip install -r requirements.txt

---

## 🚀 Usage

### 1. Run the Generator
Run the main script to generate and sync your release notes:

```bash
python generate_notes.py



