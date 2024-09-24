import requests
import random
from datetime import datetime, timedelta

def get_random_repos(language, code_string=None, commit_search=None):
    base_url = "https://api.github.com/search/repositories"
    
    # Calculate the date 6 months ago
    six_months_ago = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
    
    # Construct the query
    query = f"language:{language} stars:>=20 pushed:>{six_months_ago}"
    
    if code_string:
        query += f" {code_string} in:file"
    
    params = {
        "q": query,
        "sort": "updated",
        "order": "desc",
        "per_page": 100
    }
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return []
    
    repos = response.json()["items"]
    
    # Filter repos based on commit search if provided
    if commit_search:
        filtered_repos = []
        for repo in repos:
            commits_url = f"{repo['url']}/commits"
            commits_params = {"since": six_months_ago}
            commits_response = requests.get(commits_url, params=commits_params, headers=headers)
            
            if commits_response.status_code == 200:
                commits = commits_response.json()
                if any(commit_search.lower() in commit['commit']['message'].lower() for commit in commits):
                    filtered_repos.append(repo)
        repos = filtered_repos
    
    # Randomly select up to 5 repos
    selected_repos = random.sample(repos, min(5, len(repos)))
    
    return selected_repos

def main():
    language = input("Enter the programming language to filter by: ")
    code_string = input("Enter a code string to search for (optional, press Enter to skip): ")
    commit_search = input("Enter a string to search in commit messages (optional, press Enter to skip): ")
    
    if not code_string:
        code_string = None
    if not commit_search:
        commit_search = None
    
    repos = get_random_repos(language, code_string, commit_search)
    
    if repos:
        print(f"\nFound {len(repos)} random repositories:")
        for repo in repos:
            print(f"\nName: {repo['name']}")
            print(f"Description: {repo['description']}")
            print(f"URL: {repo['html_url']}")
            print(f"Stars: {repo['stargazers_count']}")
            print(f"Last pushed: {repo['pushed_at']}")
    else:
        print("No repositories found matching the criteria.")

if __name__ == "__main__":
    main()

