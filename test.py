import subprocess
import sys

def install_flask_cors():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask-cors"])
        print("flask-cors installed successfully!")
    except subprocess.CalledProcessError:
        print("Error installing flask-cors")

if __name__ == "__main__":
    install_flask_cors()