# Python Automation Framework

A comprehensive AI-powered automation framework that integrates Ollama for intelligent test case and script generation, Browser-Use AI Agent for web execution, and provides a beautiful Streamlit interface for seamless workflow management.

## 🚀 Features

### Core Capabilities
- **AI-Powered Generation**: Uses Ollama (Llama 3.1 8B) for intelligent prompt and test case generation
- **Smart Test Script Creation**: Automated test script generation using Codellama
- **Browser Automation**: Browser-Use AI Agent for intelligent web execution
- **Knowledge Base**: Chroma Vector DB for document embeddings and contextual retrieval
- **Beautiful UI**: Modern Streamlit interface with futuristic design
- **Git Integration**: Automatic version control and push operations
- **HTML Reports**: Comprehensive execution reports with screenshots and logs

### Supported File Formats
- **Documents**: PDF, TXT, DOC, DOCX
- **Spreadsheets**: XLSX, XLS, CSV
- **Test Scripts**: Python, JSON, Text formats

### Automation Tools
- **Browser-Use AI Agent**: Intelligent web automation
- **Selenium**: Traditional web automation (planned)
- **Playwright**: Modern web automation (planned)
- **Appium**: Mobile automation (planned)

## 📁 Project Structure

```
python_automation_framework/
├── src/                           # Source code
│   ├── __init__.py               # Package initialization
│   ├── main.py                   # Main Streamlit application
│   ├── config_manager.py         # Configuration management
│   ├── logger.py                 # Logging configuration
│   ├── ollama_manager.py         # Ollama AI integration
│   ├── browser_agent.py          # Browser-Use AI Agent
│   ├── file_processor.py         # File processing utilities
│   ├── git_manager.py            # Git operations
│   └── report_generator.py       # HTML report generation
├── config/                       # Configuration files
├── data/                         # Input data files
├── docs/                         # Documentation
├── tests/                        # Test files
├── reports/                      # Generated HTML reports
├── testcase_generator/           # Generated test cases
├── testscript_generator/         # Generated test scripts
├── knowledgebase/                # Vector DB and embeddings
├── logs/                         # Execution logs
├── screenshots/                  # Captured screenshots
├── requirements.txt              # Python dependencies
├── config.ini                    # Configuration settings
├── todo.md                      # Development progress
└── README.md                    # This documentation
```

## 🛠️ Installation and Setup

### Prerequisites
- Python 3.11 or higher
- Ollama installed and running
- Git (for version control)
- Chrome browser (for web automation)

### Step 1: Clone or Download the Framework
```bash
# If you have the zip file, extract it
unzip python_automation_framework.zip
cd python_automation_framework

# Or clone from repository
git clone <repository-url>
cd python_automation_framework
```

### Step 2: Install Python Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Install and Setup Ollama
```bash
# Install Ollama (visit https://ollama.ai for platform-specific instructions)
# For Linux/macOS:
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull required models (in a new terminal)
ollama pull llama3.1:8b
ollama pull codellama:latest
```

### Step 4: Configure the Framework
Edit `config.ini` to match your environment:

```ini
[OLLAMA]
base_url = http://localhost:11434
model_llama = llama3.1:8b
model_codellama = codellama:latest

[BROWSER]
default_browser = chrome
headless = false
capture_screenshots = true

[PATHS]
testcase_output = ./testcase_generator
testscript_output = ./testscript_generator
reports_output = ./reports
```

### Step 5: Launch the Application
```bash
streamlit run src/main.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 User Guide

### 1. Embedding & Knowledge Base Section

This section allows you to build a knowledge base from your documents and text inputs.

**Text Input:**
1. Enter text content in the text area
2. Click "Add Text to Knowledge Base"
3. The text will be processed and stored with embeddings

**File Upload:**
1. Click "Browse files" to select documents
2. Supported formats: PDF, TXT, DOC, DOCX, XLSX, XLS
3. Click "Process [filename]" for each uploaded file
4. Files are automatically added to the knowledge base

**Knowledge Base Benefits:**
- Contextual test case generation
- Intelligent prompt enhancement
- Historical information retention
- Regression testing support

### 2. Query Knowledge Base Section

Search and retrieve information from your knowledge base.

**How to Use:**
1. Enter your query in the search box
2. Adjust the number of results (1-10)
3. Click "Search Knowledge Base"
4. Review relevant document excerpts

**Use Cases:**
- Find existing test scenarios
- Retrieve application documentation
- Discover related functionality
- Context gathering for test generation

### 3. Prompt Generation Section

Generate high-quality prompts for test case creation using AI.

**Process:**
1. Enter your testing requirements or user story
2. Choose whether to use knowledge base context
3. Click "Generate Prompt"
4. Review and use the generated prompt

**Tips:**
- Be specific about the functionality to test
- Include user roles and scenarios
- Mention expected behaviors
- Use knowledge base context for better results

### 4. Test Case Generator Section

Create comprehensive test cases using AI-powered generation.

**Input Methods:**
- **Use Generated Prompt**: Utilizes the prompt from previous section
- **Upload Document**: Process a document directly for test case generation
- **Direct Input**: Enter requirements manually

**Advanced Options:**
- **Test Case Level**: Beginner, Intermediate, Advanced
- **Test Case Type**: Functional, UI, API, Mobile
- **Count**: Number of test cases to generate (1-20)

**Generated Output:**
- JSON format with structured test case data
- Table view for easy reading
- Downloadable files (JSON and TXT formats)

**Test Case Structure:**
```json
{
  "id": "TC_001",
  "title": "User Login Validation",
  "description": "Verify user can login with valid credentials",
  "preconditions": ["User account exists", "Application is accessible"],
  "steps": ["Navigate to login page", "Enter credentials", "Click login"],
  "expected_result": "User successfully logs in",
  "priority": "High",
  "tags": ["smoke", "functional", "login"]
}
```

### 5. Test Script Generator Section

Convert test cases into executable automation scripts.

**Input Selection:**
- Select from generated test cases
- Upload test case files (JSON/TXT)

**Tool Configuration:**
- **Automation Tool**: Selenium, Playwright, RestAssured, Appium
- **Browser/Platform**: Chrome, Firefox, Safari, Edge, iOS, Android

**Generated Scripts:**
- Python-based automation code
- Well-commented and structured
- Framework-specific implementations
- Best practices included

**Script Features:**
- Error handling
- Wait strategies
- Element identification
- Assertion methods
- Logging integration

### 6. Executor Section

Execute test scripts using Browser-Use AI Agent or other automation tools.

**Script Input:**
- Select from generated scripts
- Upload script files
- Enter scripts directly

**Execution Options:**
- **Execution Tool**: Browser-Use AI Agent, Selenium, Appium
- **Headless Mode**: Run without GUI
- **Capture Screenshots**: Save execution screenshots
- **Capture Logs**: Detailed execution logging

**Execution Results:**
- Status: PASSED/FAILED
- Execution logs with timestamps
- Screenshots at key steps
- Error messages and stack traces
- Downloadable log files

### 7. Reports Section

Generate beautiful HTML reports from execution results.

**Report Features:**
- Executive summary with pass/fail statistics
- Interactive charts and graphs
- Detailed test results with logs
- Embedded screenshots
- Professional styling
- Downloadable HTML format

**Report Sections:**
- **Summary**: Total tests, pass rate, execution time
- **Charts**: Visual representation of results
- **Detailed Results**: Individual test outcomes
- **Screenshots**: Captured during execution
- **Logs**: Complete execution traces

### 8. Git Integration Section

Manage version control and collaborate with team members.

**Repository Management:**
- Check Git status
- View modified files
- Select files for commit
- Custom commit messages

**Automated Operations:**
- Auto-commit on successful test execution
- Automatic push to remote repository
- Branch management
- Commit history tracking

**Best Practices:**
- Regular commits after test creation
- Descriptive commit messages
- Branch-based development
- Automated backups

## 🔧 Configuration Guide

### Ollama Configuration
```ini
[OLLAMA]
base_url = http://localhost:11434    # Ollama server URL
model_llama = llama3.1:8b           # Model for prompt/test generation
model_codellama = codellama:latest   # Model for script generation
timeout = 300                       # Request timeout in seconds
```

### Browser Configuration
```ini
[BROWSER]
default_browser = chrome            # Default browser for automation
headless = false                   # Run browser in headless mode
capture_screenshots = true         # Capture screenshots during execution
screenshot_path = ./screenshots    # Screenshot storage path
implicit_wait = 10                 # Implicit wait timeout
page_load_timeout = 30            # Page load timeout
```

### Path Configuration
```ini
[PATHS]
testcase_output = ./testcase_generator     # Test case storage
testscript_output = ./testscript_generator # Test script storage
reports_output = ./reports                 # Report storage
logs_output = ./logs                      # Log file storage
data_input = ./data                       # Input data storage
```

### Git Configuration
```ini
[GIT]
auto_commit = true                         # Enable auto-commit
auto_push = false                         # Enable auto-push
commit_message_template = "Automated commit: {timestamp}"
```

### Logging Configuration
```ini
[LOGGING]
level = INFO                              # Log level
format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
file_path = ./logs/framework.log          # Log file path
```

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. Ollama Connection Issues
**Problem**: "Failed to connect to Ollama server"

**Solutions:**
- Ensure Ollama is installed and running: `ollama serve`
- Check if models are downloaded: `ollama list`
- Verify base_url in config.ini matches Ollama server
- Check firewall settings

#### 2. Model Download Issues
**Problem**: "Model not found" or slow model pulling

**Solutions:**
- Pull models manually: `ollama pull llama3.1:8b`
- Check internet connection
- Ensure sufficient disk space
- Try alternative model versions

#### 3. Browser Automation Issues
**Problem**: Browser fails to start or crashes

**Solutions:**
- Install/update Chrome browser
- Check browser driver compatibility
- Try headless mode: set `headless = true` in config.ini
- Verify browser permissions

#### 4. File Processing Issues
**Problem**: "Unsupported file format" or extraction errors

**Solutions:**
- Check supported formats: PDF, TXT, DOC, DOCX, XLSX, XLS, CSV
- Ensure files are not corrupted
- Try converting to supported format
- Check file permissions

#### 5. Memory Issues
**Problem**: Out of memory errors during processing

**Solutions:**
- Reduce batch size for file processing
- Close unnecessary applications
- Increase system RAM
- Process files individually

#### 6. Git Integration Issues
**Problem**: Git operations fail

**Solutions:**
- Initialize Git repository: `git init`
- Configure Git user: `git config user.name "Your Name"`
- Check repository permissions
- Verify remote repository access

#### 7. Streamlit Issues
**Problem**: UI doesn't load or crashes

**Solutions:**
- Check Python version (3.11+ required)
- Reinstall dependencies: `pip install -r requirements.txt`
- Clear Streamlit cache: `streamlit cache clear`
- Check port availability (8501)

#### 8. Performance Issues
**Problem**: Slow response times

**Solutions:**
- Use smaller AI models for faster processing
- Enable headless browser mode
- Reduce screenshot capture frequency
- Optimize knowledge base size

### Error Codes and Messages

| Error Code | Message | Solution |
|------------|---------|----------|
| OLLAMA_001 | Connection timeout | Check Ollama server status |
| BROWSER_001 | WebDriver not found | Install/update browser driver |
| FILE_001 | Unsupported format | Use supported file types |
| GIT_001 | Repository not initialized | Run `git init` |
| CONFIG_001 | Configuration file missing | Check config.ini exists |

### Performance Optimization

#### System Requirements
- **Minimum**: 8GB RAM, 4 CPU cores, 10GB disk space
- **Recommended**: 16GB RAM, 8 CPU cores, 50GB disk space
- **Optimal**: 32GB RAM, 16 CPU cores, 100GB SSD

#### Optimization Tips
1. **Use SSD storage** for better I/O performance
2. **Enable headless mode** for faster browser automation
3. **Limit concurrent executions** to prevent resource exhaustion
4. **Regular cleanup** of logs and screenshots
5. **Optimize model selection** based on accuracy vs speed needs

## 🔒 Security Considerations

### Data Privacy
- All processing happens locally
- No data sent to external services (except Ollama models)
- Knowledge base stored locally
- Screenshots and logs contain sensitive information

### Best Practices
- Regular backup of knowledge base
- Secure storage of configuration files
- Access control for generated reports
- Regular security updates

### Compliance
- GDPR compliant (local processing)
- No external data transmission
- Audit trail through Git integration
- Configurable data retention

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Install development dependencies
4. Make changes and test thoroughly
5. Submit pull request

### Code Standards
- Follow PEP 8 for Python code
- Add docstrings for all functions
- Include unit tests for new features
- Update documentation as needed

### Testing
- Run unit tests: `pytest tests/`
- Test UI functionality manually
- Verify cross-platform compatibility
- Performance testing for large datasets

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Ollama Team** for the excellent local LLM platform
- **Browser-Use Team** for the AI-powered browser automation
- **Streamlit Team** for the amazing web app framework
- **Open Source Community** for the various libraries and tools

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the configuration guide
- Consult the user guide

---

**Happy Testing! 🚀**

# AI_Powered_Automation_FrameWork
