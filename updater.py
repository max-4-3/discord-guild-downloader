import os
import subprocess
import sys

def check_git_installed():
    """Check if Git is installed."""
    try:
        subprocess.run(['git', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_python_installed():
    """Check if Python is installed."""
    return sys.version_info.major >= 3

def check_dependencies():
    """Check if required dependencies are installed."""
    dependencies = ['git']
    for dependency in dependencies:
        if dependency == 'git' and not check_git_installed():
            print("Error: Git is not installed. Please install Git to continue.")
            return False
    return True

def update_repository(repo_path):
    """Update the Git repository."""
    try:
        subprocess.run(['git', '-C', repo_path, 'pull'], check=True)
        print("Repository updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating repository: {e}")

def main():
    """Main function to check dependencies and update the project."""
    repo_path = '.'  # Set this to your project path if needed.

    if not check_dependencies():
        return

    print("All dependencies are satisfied. Proceeding to update the project...")
    update_repository(repo_path)

if __name__ == "__main__":
    if not check_python_installed():
        print("Error: Python 3 is required. Please install Python 3 to continue.")
    else:
        main()
