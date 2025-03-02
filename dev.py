import subprocess
import sys
import os

def run_tests():
    print("Running tests...")
    result = subprocess.run(["pytest", "tests"], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    if result.returncode != 0:
        print("Tests failed!")
        sys.exit(1)
    print("All tests passed!")

def run_linter():
    print("Running linter...")
    result = subprocess.run(["flake8", "."], capture_output=True, text=True)
    if result.stdout:
        print("Linter found issues:")
        print(result.stdout)
        sys.exit(1)
    print("Linting passed!")

def start_dev_server():
    print("Starting development server...")
    os.environ["DEBUG"] = "1"
    subprocess.run(["uvicorn", "app.main:app", "--reload"])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dev.py [test|lint|serve]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "test":
        run_tests()
    elif command == "lint":
        run_linter()
    elif command == "serve":
        start_dev_server()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: test, lint, serve")
        sys.exit(1)