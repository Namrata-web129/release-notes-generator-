import os
import sys
import time
import threading
import itertools
from datetime import datetime
from dotenv import load_dotenv
from github import Github, Auth, GithubException
from google import genai

load_dotenv()

# Setup Clients
auth = Auth.Token(os.getenv("GITHUB_TOKEN"))
github_client = Github(auth=auth)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class Spinner:
    def __init__(self, message="Thinking..."):
        self.message = message
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.stop_running = threading.Event()
        self.spin_thread = threading.Thread(target=self._animate)

    def _animate(self):
        while not self.stop_running.is_set():
            sys.stdout.write(f"\r{next(self.spinner)} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)

    def start(self):
        self.spin_thread.start()

    def stop(self, success=True):
        self.stop_running.set()
        self.spin_thread.join()
        # CLEAN-PRINT: Overwrite the line with spaces to erase "Thinking..." completely
        sys.stdout.write("\r" + " " * (len(self.message) + 15) + "\r")
        if success:
            sys.stdout.write("✅ Analysis Completes\n")
        sys.stdout.flush()

def get_comprehensive_data(repo_name):
    print(f"📡 Analyzing {repo_name}...")
    repo = github_client.get_repo(repo_name)
    
    try:
        last_release = repo.get_latest_release()
        since_date = last_release.created_at
        print(f"📅 Last release was on: Changes since {since_date.strftime('%Y-%m-%d %H:%M')}")
    except:
        print("⚠️  Notice: No release tag found. Analyzing full history...")
        since_date = datetime(2000, 1, 1) 

    # Combined PR and Commit Data
    commits = repo.get_commits(since=since_date)
    commit_data = [f"Commit: {c.commit.message.split('\n')[0]}" for c in commits]
    
    pulls = repo.get_pulls(state='closed', sort='updated', direction='desc')
    pr_data = [f"PR #{p.number}: {p.title}" for p in pulls if p.merged and p.merged_at > since_date]
    
    return commit_data + pr_data

import time

def generate_professional_notes(data_list):
    loading = Spinner("Gemini is structuring technical release notes...")
    loading.start()
    
    # We will try up to 3 times if we hit a rate limit
    max_retries = 3
    for attempt in range(max_retries):
        try:
            prompt = f"..." # (Your existing prompt here)
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            loading.stop()
            return response.text
        except Exception as e:
            if "429" in str(e):
                # If we hit the limit, wait 20 seconds and try again
                time.sleep(20) 
                continue
            else:
                loading.stop()
                raise e
    loading.stop()
    return "⚠️ Error: AI Rate limit exceeded. Please try again in a few minutes."

def push_to_github(repo_name, content):
    print(f"🚀 Sync: Initializing GitHub upload...")
    repo = github_client.get_repo(repo_name)
    file_name = "RELEASE_NOTES.md"
    
    # Technical One-Word Mapping
    ERROR_MAP = {
        401: "AUTH",      # Bad Token
        403: "ACL",       # No Write Permission (Access Control List)
        404: "RESOURCE",  # Repo Not Found (Often a permission mask)
        422: "LOGIC",     # Data validation error
        500: "REMOTE"     # GitHub is down
    }

    try:
        try:
            contents = repo.get_contents(file_name)
            repo.update_file(contents.path, "docs: update release notes", content, contents.sha)
            print("✨ Result: Remote file updated successfully.")
        except GithubException as e:
            if e.status == 404:
                repo.create_file(file_name, "docs: initial release notes", content)
                print("✨ Result: Remote file created successfully.")
            else:
                raise e
    except GithubException as e:
        cause = ERROR_MAP.get(e.status, "SYSTEM")
        print(f"\n❌ GITHUB SYNC FAILED")
        print(f"Category: {cause}")
        
        # Technical Logic for 404
        if e.status == 404:
            
            print("Note💡: GitHub also returns 404 for private repos if your token lacks access.")
        else:
            print(f"Reason:  {e.data.get('message', 'Unexpected error')} (HTTP {e.status})")
            
        print("💾 Status: Local build saved to disk, but remote push was skipped.")

if __name__ == "__main__":
    print("\n" + "—"*45)
    print("      PROFESSIONAL RELEASE AUTOMATOR")
    print("—"*45 + "\n")
    
    target = input("Target Repository (user/repo): ").strip()
    
    if target:
        try:
            raw_data = get_comprehensive_data(target)
            final_md = generate_professional_notes(raw_data if raw_data else ["Documentation update"])
            
            with open("RELEASE_NOTES.md", "w", encoding="utf-8") as f:
                f.write(final_md)
            print("💾 Local: Build saved to disk.")
            
            push_to_github(target, final_md)
            print("\n🎉 Your professional release notes are live! ")
        except Exception as e:
            print(f"\n❌ System Error: {e}")