"""
Setup script for Job Application Crew - Simplified Version
"""

import subprocess
import sys
import os


def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        # Only install requests - no problematic dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True


def check_ollama():
    """Check if Ollama is available"""
    print("🔍 Checking Ollama availability...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running!")

            # Check if qwen2.5:7b is available
            models = response.json().get('models', [])
            model_names = [model['name'] for model in models]

            if 'qwen2.5:7b' in model_names:
                print("✅ qwen2.5:7b model is available!")
            else:
                print("⚠️  qwen2.5:7b model not found.")
                print("To install: ollama pull qwen2.5:7b")
                return False
        else:
            print("❌ Ollama is not responding properly")
            return False
    except ImportError:
        print("❌ Requests library not found. Installing...")
        install_requirements()
        return check_ollama()
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        print("Make sure Ollama is running with: ollama serve")
        return False

    return True


def main():
    """Main setup function"""
    print("🚀 Job Application Crew Setup (Simplified)")
    print("=" * 40)

    # Install requirements
    if not install_requirements():
        print("❌ Setup failed!")
        return

    # Check Ollama
    if not check_ollama():
        print("❌ Ollama setup incomplete!")
        print("\n🔧 To fix this:")
        print("1. Install Ollama from: https://ollama.ai/")
        print("2. Start Ollama: ollama serve")
        print("3. Install model: ollama pull qwen2.5:7b")
        print("4. Run this setup again")
        return

    print("\n🎉 Setup completed successfully!")
    print("✅ You can now run: python job_application_crew.py")


if __name__ == "__main__":
    main()

# run.py - Simple runner script
# !/usr/bin/env python3
"""
Simple runner for Job Application Crew
"""


def main():
    """Run the job application crew"""
    try:
        from job_application_crew import main as crew_main
        crew_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all files are in the same directory")
    except Exception as e:
        print(f"❌ Error running crew: {e}")


if __name__ == "__main__":
    main()