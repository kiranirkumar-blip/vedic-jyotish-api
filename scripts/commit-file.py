from github import Github
import base64
import os

# Inputs passed from GitHub Action
token = os.getenv("GH_TOKEN")
repo_name = os.getenv("REPO_NAME")
file_path = os.getenv("FILE_PATH")          # Local file inside repo
target_path = os.getenv("TARGET_PATH")      # Path where it should be stored in repo
commit_message = os.getenv("COMMIT_MESSAGE")

# Authenticate
github = Github(token)
repo = github.get_repo(repo_name)

# Read file content
with open(file_path, "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

try:
    # If file exists, update it
    contents = repo.get_contents(target_path)
    repo.update_file(
        contents.path,
        commit_message,
        encoded,
        contents.sha
    )
    print("✅ File updated successfully")

except Exception:
    # If file does not exist, create it
    repo.create_file(
        target_path,
        commit_message,
        encoded
    )
    print("✅ File created successfully")
