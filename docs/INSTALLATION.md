# Installation Guide

This guide provides detailed instructions for installing and setting up the Python Automation Framework on different operating systems.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: 3.11 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space minimum, 50GB recommended
- **Internet**: Required for initial setup and model downloads

### Recommended Requirements
- **RAM**: 16GB or higher
- **CPU**: 8 cores or higher
- **Storage**: SSD with 50GB+ free space
- **GPU**: Optional, for faster AI model processing

## Pre-Installation Steps

### 1. Install Python 3.11+

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and check "Add Python to PATH"
3. Verify installation: `python --version`

#### macOS
```bash
# Using Homebrew (recommended)
brew install python@3.11

# Or download from python.org
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv
```

### 2. Install Git
#### Windows
Download and install from [git-scm.com](https://git-scm.com/)

#### macOS
```bash
brew install git
```

#### Linux
```bash
sudo apt install git
```

### 3. Install Chrome Browser
Download and install Google Chrome from [google.com/chrome](https://www.google.com/chrome/)

## Framework Installation

### Method 1: From ZIP File (Recommended)

1. **Extract the Framework**
```bash
unzip python_automation_framework.zip
cd python_automation_framework
```

2. **Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### Method 2: From Git Repository

1. **Clone Repository**
```bash
git clone <repository-url>
cd python_automation_framework
```

2. **Follow steps 2-3 from Method 1**

## Ollama Installation and Setup

### 1. Install Ollama

#### Windows
1. Download Ollama from [ollama.ai](https://ollama.ai/)
2. Run the installer
3. Ollama will start automatically

#### macOS
```bash
# Using Homebrew
brew install ollama

# Or download from ollama.ai
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Start Ollama Service

#### Windows
Ollama starts automatically. If not, run:
```cmd
ollama serve
```

#### macOS/Linux
```bash
# Start as service
ollama serve

# Or start in background
nohup ollama serve > ollama.log 2>&1 &
```

### 3. Download Required Models

Open a new terminal and run:
```bash
# Download Llama 3.1 8B model (required)
ollama pull llama3.1:8b

# Download CodeLlama model (required)
ollama pull codellama:latest

# Verify models are installed
ollama list
```

**Note**: Model downloads can take 30-60 minutes depending on internet speed.

## Configuration

### 1. Basic Configuration

Edit `config.ini` file:

```ini
[OLLAMA]
base_url = http://localhost:11434
model_llama = llama3.1:8b
model_codellama = codellama:latest
timeout = 300

[BROWSER]
default_browser = chrome
headless = false
capture_screenshots = true

[PATHS]
testcase_output = ./testcase_generator
testscript_output = ./testscript_generator
reports_output = ./reports
logs_output = ./logs
```

### 2. Advanced Configuration

For production environments, consider:

#### Performance Optimization
```ini
[BROWSER]
headless = true  # Faster execution
implicit_wait = 5  # Reduce wait times
```

#### Security Settings
```ini
[LOGGING]
level = WARNING  # Reduce log verbosity
```

#### Resource Management
```ini
[OLLAMA]
timeout = 600  # Increase for large documents
```

## Verification

### 1. Test Python Environment
```bash
python --version  # Should show 3.11+
pip list  # Should show installed packages
```

### 2. Test Ollama
```bash
ollama list  # Should show downloaded models
curl http://localhost:11434/api/tags  # Should return JSON
```

### 3. Test Framework
```bash
# Activate virtual environment if not already active
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Run the application
streamlit run src/main.py
```

The application should open at `http://localhost:8501`

## Troubleshooting Installation

### Common Issues

#### 1. Python Version Issues
**Problem**: "Python 3.11 required"
**Solution**: 
```bash
# Check version
python --version

# Install correct version or use specific command
python3.11 -m venv venv
```

#### 2. Permission Errors
**Problem**: Permission denied during installation
**Solution**:
```bash
# Linux/macOS
sudo pip install -r requirements.txt

# Or use user installation
pip install --user -r requirements.txt
```

#### 3. Ollama Connection Issues
**Problem**: Cannot connect to Ollama
**Solution**:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

#### 4. Model Download Failures
**Problem**: Model download interrupted
**Solution**:
```bash
# Resume download
ollama pull llama3.1:8b

# Check available space
df -h  # Linux/macOS
dir  # Windows
```

#### 5. Port Conflicts
**Problem**: Port 8501 already in use
**Solution**:
```bash
# Use different port
streamlit run src/main.py --server.port 8502

# Or kill existing process
lsof -ti:8501 | xargs kill  # Linux/macOS
netstat -ano | findstr :8501  # Windows
```

### Environment-Specific Issues

#### Windows-Specific
- **Long Path Issues**: Enable long path support in Windows
- **Antivirus**: Add framework folder to exclusions
- **PowerShell**: May need to enable script execution

#### macOS-Specific
- **Xcode Tools**: Install if compilation errors occur
- **Homebrew**: Update if package installation fails
- **Permissions**: May need to allow Chrome automation

#### Linux-Specific
- **Dependencies**: Install system packages for PDF processing
- **Display**: Set DISPLAY variable for GUI applications
- **Permissions**: Ensure user has necessary permissions

## Post-Installation Setup

### 1. Initialize Git Repository
```bash
cd python_automation_framework
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 2. Create Initial Commit
```bash
git add .
git commit -m "Initial setup of Python Automation Framework"
```

### 3. Set Up Remote Repository (Optional)
```bash
git remote add origin <your-repository-url>
git push -u origin master
```

### 4. Test All Components

1. **Upload a test document** in the Embedding section
2. **Generate a prompt** in the Prompt Generation section
3. **Create test cases** in the Test Case Generator
4. **Generate a script** in the Test Script Generator
5. **Execute the script** in the Executor section
6. **Generate a report** in the Reports section

## Performance Optimization

### 1. System Optimization
```bash
# Increase file descriptor limits (Linux/macOS)
ulimit -n 4096

# Set environment variables for better performance
export PYTHONUNBUFFERED=1
export STREAMLIT_SERVER_HEADLESS=true
```

### 2. Model Optimization
- Use smaller models for faster processing if accuracy allows
- Consider quantized models for resource-constrained environments
- Cache frequently used prompts

### 3. Browser Optimization
- Enable headless mode for production
- Reduce screenshot frequency
- Use browser profiles for consistent state

## Security Considerations

### 1. Network Security
- Run Ollama on localhost only
- Use firewall rules to restrict access
- Consider VPN for remote access

### 2. Data Security
- Encrypt sensitive test data
- Regular backup of knowledge base
- Secure storage of configuration files

### 3. Access Control
- Use proper user permissions
- Implement authentication for production
- Audit trail through Git integration

## Maintenance

### 1. Regular Updates
```bash
# Update Python packages
pip install --upgrade -r requirements.txt

# Update Ollama models
ollama pull llama3.1:8b
ollama pull codellama:latest
```

### 2. Cleanup
```bash
# Clean up old logs
find logs/ -name "*.log" -mtime +30 -delete

# Clean up old screenshots
find screenshots/ -name "*.png" -mtime +7 -delete

# Clean up old reports
find reports/ -name "*.html" -mtime +30 -delete
```

### 3. Backup
```bash
# Backup knowledge base
tar -czf knowledgebase_backup.tar.gz knowledgebase/

# Backup configuration
cp config.ini config.ini.backup
```

## Next Steps

After successful installation:

1. **Read the User Guide** for detailed usage instructions
2. **Review Configuration Options** for customization
3. **Explore Example Workflows** to understand capabilities
4. **Set Up Monitoring** for production environments
5. **Configure Backups** for important data

For additional help, refer to the main README.md file or create an issue in the repository.

