import os
from dotenv import load_dotenv
from github import Github, Auth

load_dotenv()
auth = Auth.Token(os.getenv("GITHUB_TOKEN"))
g = Github(auth=auth)

def get_recent_activity(repo_name):
    print(f"--- Connecting to {repo_name} ---")
    repo = g.get_repo(repo_name)
    
    data_for_ai = []
    
    # 1. Try to get Pull Requests safely
    print(f"Checking for Pull Requests...")
    pulls = repo.get_pulls(state='all', sort='created', direction='desc')
    
    count = 0
    for pr in pulls:
        if count >= 10: break # Stop after 10
        line = f"PR #{pr.number}: {pr.title}"
        print(f"✅ Found: {line}")
        data_for_ai.append(line)
        count += 1

    # 2. If no PRs were found, get Commits instead
    if len(data_for_ai) == 0:
        print("No PRs found. Fetching recent commits...")
        commits = repo.get_commits()
        
        count = 0
        for c in commits:
            if count >= 10: break
            msg = c.commit.message.split('\n')[0]
            print(f"✅ Commit: {msg}")
            data_for_ai.append(msg)
            count += 1

    return data_for_ai

if __name__ == "__main__":
    REPO = "Namrata-web129/cleartracker-hub"
    results = get_recent_activity(REPO)
    
    if results:
        print(f"\n--- Success! Found {len(results)} items ---")
    else:
        print("\n--- No activity found in this repository ---")