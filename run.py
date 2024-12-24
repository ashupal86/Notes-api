import os
import subprocess
import sys

        
def install_requirements():
    """Install dependencies from requirements.txt."""
    if os.path.exists('requirements.txt'):
        print("Activating virtual environment and installing dependencies...")

        # Activate the virtual environment and install dependencies
        activate_script = os.path.join('venv', 'Scripts', 'activate') if os.name == 'nt' else os.path.join('venv', 'bin', 'activate')
        
        # Run pip installation commands in the activated virtual environment
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip','--break-system-packages'])
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-cache-dir', '-r', 'requirements.txt','--break-system-packages'])

        print("Dependencies installed.")
    else:
        print("requirements.txt file not found. Please create it with the necessary dependencies.")



def main():
    """Main function to create virtual environment, install dependencies, and run the Flask app."""
    install_requirements()


if __name__ == "__main__":
    main()
