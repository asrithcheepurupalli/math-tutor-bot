"""
Setup script for Math Tutor Bot
Handles initial setup, dependency checks, and configuration
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_system_dependencies():
    """Check for system-level dependencies"""
    print("\n🔍 Checking system dependencies...")
    
    dependencies_ok = True
    
    # Check for Tesseract OCR
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, check=True)
        version_line = result.stdout.split('\n')[0]
        print(f"✅ Tesseract OCR: {version_line}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Tesseract OCR not found")
        print("   Please install Tesseract OCR:")
        if platform.system() == "Darwin":  # macOS
            print("   brew install tesseract")
        elif platform.system() == "Linux":
            print("   sudo apt-get install tesseract-ocr")
        elif platform.system() == "Windows":
            print("   Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        dependencies_ok = False
    
    # Check for git (optional but useful)
    try:
        result = subprocess.run(['git', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Git: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Git not found (optional)")
    
    return dependencies_ok

def setup_virtual_environment():
    """Set up Python virtual environment"""
    print("\n🐍 Setting up virtual environment...")
    
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        # Create virtual environment
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✅ Virtual environment created")
        
        # Get activation command
        if platform.system() == "Windows":
            activate_cmd = ".venv\\Scripts\\activate"
        else:
            activate_cmd = "source .venv/bin/activate"
        
        print(f"📝 To activate: {activate_cmd}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    
    # Determine pip command
    if platform.system() == "Windows":
        pip_cmd = ".venv\\Scripts\\pip"
    else:
        pip_cmd = ".venv/bin/pip"
    
    try:
        # Upgrade pip first
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
        print("✅ pip upgraded")
        
        # Install requirements
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Python dependencies installed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment_file():
    """Set up environment configuration file"""
    print("\n⚙️  Setting up environment configuration...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        # Copy example to .env
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            dst.write(src.read())
        print("✅ .env file created from template")
        print("📝 Please edit .env file with your API keys and configuration")
        return True
    else:
        print("❌ .env.example not found")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ["logs", "generated_videos", "temp"]
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {dir_name}")
        else:
            print(f"✅ Directory exists: {dir_name}")

def setup_git_hooks():
    """Set up git hooks (optional)"""
    print("\n🔗 Setting up git hooks...")
    
    if not Path(".git").exists():
        print("⚠️  Not a git repository, skipping git hooks")
        return
    
    hooks_dir = Path(".git/hooks")
    pre_commit_hook = hooks_dir / "pre-commit"
    
    if pre_commit_hook.exists():
        print("✅ Pre-commit hook already exists")
        return
    
    # Create a simple pre-commit hook for code quality
    hook_content = """#!/bin/sh
# Math Tutor Bot pre-commit hook

echo "Running pre-commit checks..."

# Check Python syntax
python -m py_compile bot.py ai_solver.py video_generator.py
if [ $? -ne 0 ]; then
    echo "❌ Python syntax errors found"
    exit 1
fi

# Run black formatter (if available)
if command -v black &> /dev/null; then
    black --check --diff .
    if [ $? -ne 0 ]; then
        echo "⚠️  Code formatting issues found. Run 'black .' to fix."
        echo "Committing anyway..."
    fi
fi

echo "✅ Pre-commit checks passed"
"""
    
    try:
        with open(pre_commit_hook, 'w') as f:
            f.write(hook_content)
        
        # Make executable
        os.chmod(pre_commit_hook, 0o755)
        print("✅ Pre-commit hook created")
        
    except Exception as e:
        print(f"⚠️  Failed to create pre-commit hook: {e}")

def verify_setup():
    """Verify the setup is working"""
    print("\n🔍 Verifying setup...")
    
    # Check if we can import main modules
    try:
        # Add current directory to Python path
        sys.path.insert(0, '.')
        
        # Try importing main modules
        print("   Testing imports...")
        
        # Test basic imports
        import dotenv
        print("   ✅ python-dotenv")
        
        import telegram
        print("   ✅ python-telegram-bot")
        
        import openai
        print("   ✅ openai")
        
        import PIL
        print("   ✅ Pillow")
        
        import cv2
        print("   ✅ opencv-python")
        
        print("✅ All imports successful")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Please check your virtual environment and requirements.txt")
        return False

def show_next_steps():
    """Show next steps to the user"""
    print("\n" + "=" * 60)
    print("🎉 Setup completed! Next steps:")
    print("=" * 60)
    
    print("\n1. Activate virtual environment:")
    if platform.system() == "Windows":
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    
    print("\n2. Configure your .env file:")
    print("   - Add your Telegram bot token")
    print("   - Add your OpenAI or Gemini API key")
    print("   - Configure other settings as needed")
    
    print("\n3. Test the components:")
    print("   python test_components.py")
    
    print("\n4. Run the bot:")
    print("   python bot.py")
    
    print("\n5. For WhatsApp integration:")
    print("   python whatsapp_bot.py")
    
    print("\n📚 Documentation:")
    print("   See README.md for detailed instructions")
    
    print("\n🆘 Need help?")
    print("   Check the logs/ directory for error details")
    print("   Review the .env.example file for configuration options")

def main():
    """Main setup function"""
    print("=" * 60)
    print("🧮 Math Tutor Bot Setup")
    print("=" * 60)
    
    setup_steps = [
        ("Python version", check_python_version),
        ("System dependencies", check_system_dependencies),
        ("Virtual environment", setup_virtual_environment),
        ("Python dependencies", install_python_dependencies),
        ("Environment file", setup_environment_file),
        ("Directories", create_directories),
        ("Git hooks", setup_git_hooks),
        ("Setup verification", verify_setup)
    ]
    
    failed_steps = []
    
    for step_name, step_func in setup_steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        try:
            if not step_func():
                failed_steps.append(step_name)
        except Exception as e:
            print(f"❌ Error in {step_name}: {e}")
            failed_steps.append(step_name)
    
    print("\n" + "=" * 60)
    
    if failed_steps:
        print("⚠️  Setup completed with issues:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\nPlease resolve these issues before running the bot.")
    else:
        print("✅ Setup completed successfully!")
    
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error during setup: {e}")
        sys.exit(1)
