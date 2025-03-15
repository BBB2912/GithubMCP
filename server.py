import json
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()
import os

mcp=FastMCP("GithubMCP")

USER_AGENT="GithubMCP-app/1.0"
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
GITHUB_API_URL = os.getenv("GITHUB_API_URL")

def get_headers():
        return {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"}
@mcp.tool()
async def list_repos(username: str = None):
        """
        Fetches public repositories of a user.
        
        Args:
            username: The GitHub username whose repositories need to be fetched.
        
        Returns:
            A list of public repositories associated with the user.
        """
        if username:
            url = f"{GITHUB_API_URL}/users/{username}/repos"  # Fetch public repos of a user
        else:
            url = f"{GITHUB_API_URL}/user/repos"  # Fetch both public and private repos for authenticated user
        response = requests.get(url, headers=get_headers())
        if response.status_code != 200:
            return {"error": "Failed to fetch repositories", "status_code": response.status_code}
        return response.json()

@mcp.tool()
async def get_repo_details(owner: str, repo: str):
    """
        Retrieves details of a repository.
        
        Args:
            owner: The GitHub username or organization that owns the repository.
            repo: The name of the repository.
        
        Returns:
            Detailed metadata about the repository, including description, stars, forks, and contributors.
        """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"
    response = requests.get(url, headers=get_headers())
    return response.json()
@mcp.tool()
async def create_repo(name: str, description: str, private: bool):
    """
    Creates a new GitHub repository.   
    Args:
        name (str): The name of the repository to be created.
        description (str): A short description of the repository.
        private (bool): A boolean indicating whether the repository should be private. 
    Returns:
        dict: A dictionary containing the repository details if created successfully, 
              or an error message if the request fails.
    
    Raises:
        HTTPError: If the GitHub API request returns an error.
    """
    url = f"{GITHUB_API_URL}/user/repos"
    data = {"name": name, "description": description, "private": private}
    response = requests.post(url, headers=get_headers(), json=data)
    return response.json()

@mcp.tool()
async def list_issues(owner: str, repo: str):
    """
    Retrieves a list of open issues in a GitHub repository.
    Args:
        owner (str): The GitHub username or organization that owns the repository.
        repo (str): The name of the repository.
    Returns:
        list: A list of dictionaries containing details about each open issue.
    
    Raises:
        HTTPError: If the GitHub API request fails.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues"
    response = requests.get(url, headers=get_headers())
    return response.json()

@mcp.tool()
async def create_issue(owner: str, repo: str, title: str, body: str):
    """
    Creates a new issue in a GitHub repository.
    Args:
        owner (str): The GitHub username or organization that owns the repository.
        repo (str): The name of the repository.
        title (str): The title of the issue.
        body (str): The detailed description of the issue. 
    Returns:
        dict: A dictionary containing issue details if created successfully, 
              or an error message if the request fails.
    
    Raises:
        HTTPError: If the GitHub API request fails.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues"
    data = {"title": title, "body": body}
    response = requests.post(url, headers=get_headers(), json=data)
    return response.json()

@mcp.tool()
async def list_pull_requests(owner: str, repo: str):
    """
    Retrieves a list of open pull requests in a GitHub repository. 
    Args:
        owner (str): The GitHub username or organization that owns the repository.
        repo (str): The name of the repository.
    Returns:
        list: A list of dictionaries containing details about each open pull request.
    
    Raises:
        HTTPError: If the GitHub API request fails.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
    response = requests.get(url, headers=get_headers())
    return response.json()

@mcp.tool()
async def merge_pull_request(owner: str, repo: str, pr_number: int):
    """
    Merges a pull request in a GitHub repository.  
    Args:
        owner (str): The GitHub username or organization that owns the repository.
        repo (str): The name of the repository.
        pr_number (int): The pull request number to be merged. 
    Returns:
        dict: A dictionary containing merge details if successful,
              or an error message if the request fails.
    
    Raises:
        HTTPError: If the GitHub API request fails.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}/merge"
    response = requests.put(url, headers=get_headers())
    return response.json()

@mcp.tool()
async def list_branches(owner: str, repo: str):
    """
    Retrieves all branches of a GitHub repository. 
    Args:
        owner (str): The GitHub username or organization that owns the repository.
        repo (str): The name of the repository.
    Returns:
        list: A list of dictionaries containing branch details.
    
    Raises:
        HTTPError: If the GitHub API request fails.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/branches"
    response = requests.get(url, headers=get_headers())
    return response.json()

@mcp.tool()
async def get_latest_commit(owner: str, repo: str, branch: str):
    """
    Fetches the latest commit on a specified branch of a GitHub repository.
    Args:
        owner (str): The GitHub username or organization that owns the repository.
        repo (str): The name of the repository.
        branch (str): The name of the branch to fetch the latest commit from.  
    Returns:
        dict: A dictionary containing commit details if successful,
              or an error message if the request fails.
    
    Raises:
        HTTPError: If the GitHub API request fails.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits/{branch}"
    response = requests.get(url, headers=get_headers())
    return response.json()

@mcp.tool()
async def list_contributors(owner: str, repo: str):
    """
    Retrieves a list of contributors for a GitHub repository.  
    Args:
        owner (str): The GitHub username or organization that owns the repository.
        repo (str): The name of the repository.
    Returns:
        list: A list of dictionaries containing contributor details.
    
    Raises:
        HTTPError: If the GitHub API request fails.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contributors"
    response = requests.get(url, headers=get_headers())
    return response.json()

@mcp.tool()
async def add_collaborator(owner: str, repo: str, username: str, permission: str):
    """
    Adds a collaborator to a GitHub repository.
    Args:
        owner (str): The GitHub username or organization that owns the repository.
        repo (str): The name of the repository.
        username (str): The GitHub username of the collaborator.
        permission (str): The level of permission to grant (e.g., "push", "pull", "admin").
    Returns:
        dict: A dictionary containing collaborator details if successful,
              or an error message if the request fails.
    
    Raises:
        HTTPError: If the GitHub API request fails.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/collaborators/{username}"
    data = {"permission": permission}
    response = requests.put(url, headers=get_headers(), json=data)
    return response.json() 
@mcp.tool()
async def create_file(owner: str, repo: str, path: str, content: str, message: str, branch: str = "main"):
    """
    Creates a new file in a GitHub repository.
    Args:
        owner: The GitHub username or organization that owns the repository.
        repo: The name of the repository.
        path: The file path where the new file should be created (e.g., "docs/readme.md").
        content: The content of the file in plain text (will be base64 encoded).
        message: The commit message describing the file creation.
        branch: The branch where the file should be created (default: "main").
    Returns:
        dict: File details if created successfully, or an error message.
    """
    import base64
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{path}"
    data = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
        "branch": branch
    }
    response = requests.put(url, headers=get_headers(), json=data)
    if response.status_code not in [200, 201]:
        return {"error": "Failed to create file", "status_code": response.status_code, "details": response.text}
    return response.json()
if __name__ == "__main__":
    mcp.run(transport="stdio")
    print("server is running")

