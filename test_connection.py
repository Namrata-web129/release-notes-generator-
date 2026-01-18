import os
from dotenv import load_dotenv
from github import Github

# Load the keys from your .env file
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

def test_github():
    try:
        # Initialize the GitHub client
        g = Github(token)
        
        # Get the authenticated user
        user = g.get_user()
        print(f"✅ Success! Connected as: {user.login}")
        
        # List your first 3 repositories just to be sure
        print("Your recent repos:")
        for repo in user.get_repos()[:3]:
            print(f" - {repo.full_name}")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_github()