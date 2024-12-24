import os
import subprocess
import sys
import venv

def create_virtualenv():
    """Create a virtual environment if it doesn't exist."""
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        venv.create('venv', with_pip=True)
        print("Virtual environment created.")

def install_requirements():
    """Install dependencies from requirements.txt."""
    if os.path.exists('requirements.txt'):
        print("Installing dependencies...")
        subprocess.check_call(['python3', '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call(['python3', '-m', 'pip', 'install','--no-cache-dir', '-r', 'requirements.txt'])
        print("Dependencies installed.")
    else:
        print("requirements.txt file not found. Please create it with the necessary dependencies.")


def main():
    """Main function to create virtual environment, install dependencies, and run the Flask app."""
    create_virtualenv()
    install_requirements()

if __name__ == "__main__":
    main()
