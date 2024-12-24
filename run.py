import os
import subprocess
import sys
import os
import zipfile
import urllib.request
import subprocess

# URL to the SQLite tools zip file
sqlite_url = "https://www.sqlite.org/2024/sqlite-tools-linux-x64-3470200.zip"
download_dir = "/tmp/sqlite_download"  # Directory to download the zip file
extract_dir = "/usr/local/sqlite"  # Directory to extract SQLite tools

def download_sqlite():
    """Download the SQLite tools zip file."""
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    zip_path = os.path.join(download_dir, "sqlite-tools-linux-x64-3470200.zip")

    # Download SQLite tools zip
    print(f"Downloading SQLite tools from {sqlite_url}...")
    urllib.request.urlretrieve(sqlite_url, zip_path)
    print("Download complete.")

    return zip_path

def extract_sqlite(zip_path):
    """Extract the downloaded SQLite tools zip file."""
    print("Extracting SQLite tools...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"SQLite tools extracted to {extract_dir}.")

def add_to_path():
    """Add SQLite binaries to the system PATH."""
    bin_path = os.path.join(extract_dir, "sqlite-tools-linux-x64-3470200")
    
    # Add SQLite binary directory to PATH (for current session)
    os.environ["PATH"] += os.pathsep + bin_path
    print(f"SQLite tools added to PATH: {bin_path}")

def verify_installation():
    """Verify SQLite installation by checking its version."""
    print("Verifying SQLite installation...")
    result = subprocess.run(['sqlite3', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode == 0:
        print(f"SQLite version: {result.stdout.decode().strip()}")
    else:
        print("SQLite installation failed.")

        
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
    """Main function to download, extract, and install SQLite."""
    zip_path = download_sqlite()
    extract_sqlite(zip_path)
    add_to_path()
    verify_installation()


if __name__ == "__main__":
    main()
