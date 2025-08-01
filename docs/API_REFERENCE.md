# API Reference

This document provides detailed information about the Python Automation Framework's internal APIs and modules.

## Core Modules

### ConfigManager

The `ConfigManager` class handles all configuration operations for the framework.

#### Class: `ConfigManager`

```python
from src.config_manager import ConfigManager

config = ConfigManager(config_path="config.ini")
```

#### Methods

##### `__init__(self, config_path: Optional[str] = None)`
Initialize the configuration manager.

**Parameters:**
- `config_path` (str, optional): Path to configuration file. Defaults to `config.ini` in project root.

**Example:**
```python
config = ConfigManager()  # Uses default path
config = ConfigManager("/path/to/custom/config.ini")  # Custom path
```

##### `get(self, section: str, key: str, fallback: Any = None) -> str`
Get a configuration value as string.

**Parameters:**
- `section` (str): Configuration section name
- `key` (str): Configuration key name
- `fallback` (Any): Default value if key not found

**Returns:**
- `str`: Configuration value

**Example:**
```python
base_url = config.get("OLLAMA", "base_url", "http://localhost:11434")
```

##### `get_int(self, section: str, key: str, fallback: int = 0) -> int`
Get a configuration value as integer.

##### `get_boolean(self, section: str, key: str, fallback: bool = False) -> bool`
Get a configuration value as boolean.

##### `get_float(self, section: str, key: str, fallback: float = 0.0) -> float`
Get a configuration value as float.

##### `set(self, section: str, key: str, value: str) -> None`
Set a configuration value.

##### `save_config(self) -> None`
Save current configuration to file.

---

### OllamaManager

The `OllamaManager` class handles all interactions with Ollama for AI-powered generation.

#### Class: `OllamaManager`

```python
from src.ollama_manager import OllamaManager
from src.config_manager import ConfigManager

config = ConfigManager()
ollama = OllamaManager(config)
```

#### Methods

##### `__init__(self, config: ConfigManager)`
Initialize the Ollama manager.

**Parameters:**
- `config` (ConfigManager): Configuration manager instance

##### `setup_ollama_models(self) -> None`
Ensures required Ollama models are available locally.

**Example:**
```python
ollama.setup_ollama_models()
```

##### `add_document_to_knowledge_base(self, file_path: str, document_content: str) -> None`
Add a document to the Chroma knowledge base.

**Parameters:**
- `file_path` (str): Original file path for metadata
- `document_content` (str): Extracted text content

**Example:**
```python
ollama.add_document_to_knowledge_base("doc.pdf", "Document content here...")
```

##### `query_knowledge_base(self, query: str, k: int = 4) -> List[str]`
Query the knowledge base for relevant documents.

**Parameters:**
- `query` (str): Search query
- `k` (int): Number of results to return

**Returns:**
- `List[str]`: List of relevant document contents

**Example:**
```python
results = ollama.query_knowledge_base("user authentication", k=3)
```

##### `generate_prompt(self, user_input: str, context: Optional[str] = None) -> str`
Generate a high-quality prompt based on user input.

**Parameters:**
- `user_input` (str): User's requirements or query
- `context` (str, optional): Additional context from knowledge base

**Returns:**
- `str`: Generated prompt

**Example:**
```python
prompt = ollama.generate_prompt("Test login functionality", context="Login docs...")
```

##### `generate_test_cases(self, prompt: str, testcase_level: str, testcase_type: str, count: int) -> List[Dict[str, Any]]`
Generate test cases based on a prompt.

**Parameters:**
- `prompt` (str): Input prompt for generation
- `testcase_level` (str): "Beginner", "Intermediate", or "Advanced"
- `testcase_type` (str): "Functional", "UI", "API", or "Mobile"
- `count` (int): Number of test cases to generate

**Returns:**
- `List[Dict[str, Any]]`: List of test case dictionaries

**Example:**
```python
test_cases = ollama.generate_test_cases(
    prompt="Test user login",
    testcase_level="Intermediate",
    testcase_type="Functional",
    count=5
)
```

##### `generate_test_script(self, test_case: Dict[str, Any], tool_selection: str, browser_selection: str) -> str`
Generate a test script from a test case.

**Parameters:**
- `test_case` (Dict): Test case dictionary
- `tool_selection` (str): Automation tool ("Selenium", "Playwright", etc.)
- `browser_selection` (str): Target browser ("Chrome", "Firefox", etc.)

**Returns:**
- `str`: Generated Python test script

**Example:**
```python
script = ollama.generate_test_script(
    test_case=test_cases[0],
    tool_selection="Selenium",
    browser_selection="Chrome"
)
```

---

### BrowserAutomationAgent

The `BrowserAutomationAgent` class handles web automation using Browser-Use AI Agent.

#### Class: `BrowserAutomationAgent`

```python
from src.browser_agent import BrowserAutomationAgent
from src.config_manager import ConfigManager

config = ConfigManager()
browser_agent = BrowserAutomationAgent(config)
```

#### Methods

##### `__init__(self, config: ConfigManager)`
Initialize the browser automation agent.

##### `execute_script(self, script_content: str, test_case_id: str = "unknown") -> Dict[str, Any]`
Execute a Python test script using Browser-Use AI Agent.

**Parameters:**
- `script_content` (str): Python script to execute
- `test_case_id` (str): Identifier for logging and reporting

**Returns:**
- `Dict[str, Any]`: Execution results with status, logs, and screenshots

**Example:**
```python
result = browser_agent.execute_script(
    script_content="agent.navigate('https://example.com')",
    test_case_id="TC_001"
)
```

**Return Structure:**
```python
{
    "status": "PASSED" | "FAILED",
    "error_message": str | None,
    "logs": List[Dict[str, str]],
    "screenshots": List[str],
    "log_file": str
}
```

##### `direct_execute_browser_action(self, action_script: str) -> Dict[str, Any]`
Execute a direct browser action.

**Parameters:**
- `action_script` (str): Single browser action command

**Returns:**
- `Dict[str, Any]`: Execution results

---

### FileProcessor

The `FileProcessor` class handles extraction of text content from various file formats.

#### Class: `FileProcessor`

```python
from src.file_processor import FileProcessor
from src.config_manager import ConfigManager

config = ConfigManager()
processor = FileProcessor(config)
```

#### Methods

##### `extract_text_from_file(self, file_path: str) -> str`
Extract text content from a file.

**Parameters:**
- `file_path` (str): Path to the file to process

**Returns:**
- `str`: Extracted text content

**Supported Formats:**
- PDF (.pdf)
- Text (.txt)
- Word Documents (.doc, .docx)
- Excel Spreadsheets (.xlsx, .xls)
- CSV (.csv)

**Example:**
```python
content = processor.extract_text_from_file("document.pdf")
```

##### `get_file_info(self, file_path: str) -> Dict[str, Any]`
Get information about a file.

**Returns:**
```python
{
    "name": str,
    "extension": str,
    "size_bytes": int,
    "size_mb": float,
    "created": float,
    "modified": float,
    "is_supported": bool
}
```

##### `validate_file(self, file_path: str) -> Dict[str, Any]`
Validate a file for processing.

**Returns:**
```python
{
    "is_valid": bool,
    "file_info": Dict,
    "errors": List[str],
    "warnings": List[str]
}
```

##### `batch_process_files(self, file_paths: List[str]) -> Dict[str, Any]`
Process multiple files in batch.

---

### GitManager

The `GitManager` class handles Git operations for version control.

#### Class: `GitManager`

```python
from src.git_manager import GitManager
from src.config_manager import ConfigManager

config = ConfigManager()
git_manager = GitManager(config)
```

#### Methods

##### `get_status(self) -> str`
Get the current Git repository status.

**Returns:**
- `str`: Formatted status information

##### `get_modified_files(self) -> List[str]`
Get list of modified files.

**Returns:**
- `List[str]`: List of modified file paths

##### `commit_files(self, file_paths: List[str], commit_message: str) -> str`
Commit specified files.

**Parameters:**
- `file_paths` (List[str]): Files to commit
- `commit_message` (str): Commit message

**Returns:**
- `str`: Commit hash

##### `push_changes(self, remote_name: str = "origin", branch_name: str = None) -> None`
Push committed changes to remote repository.

##### `auto_commit_on_success(self) -> str`
Perform automatic commit when all tests pass.

---

### ReportGenerator

The `ReportGenerator` class generates HTML reports from execution results.

#### Class: `ReportGenerator`

```python
from src.report_generator import ReportGenerator
from src.config_manager import ConfigManager

config = ConfigManager()
report_gen = ReportGenerator(config)
```

#### Methods

##### `generate_html_report(self, execution_results: Dict[str, Any]) -> str`
Generate a comprehensive HTML report.

**Parameters:**
- `execution_results` (Dict): Dictionary of execution results

**Returns:**
- `str`: Path to generated HTML report

**Example:**
```python
report_path = report_gen.generate_html_report({
    "TC_001": {
        "status": "PASSED",
        "logs": [...],
        "screenshots": [...]
    }
})
```

---

## Data Structures

### Test Case Structure

```python
{
    "id": str,                    # Unique identifier
    "title": str,                 # Test case title
    "description": str,           # Detailed description
    "preconditions": List[str],   # Prerequisites
    "steps": List[str],           # Test steps
    "expected_result": str,       # Expected outcome
    "priority": str,              # Priority level
    "tags": List[str]            # Associated tags
}
```

### Execution Result Structure

```python
{
    "status": str,               # "PASSED" or "FAILED"
    "error_message": str | None, # Error details if failed
    "logs": List[Dict[str, str]], # Execution logs
    "screenshots": List[str],     # Screenshot file paths
    "log_file": str              # Log file path
}
```

### Log Entry Structure

```python
{
    "timestamp": str,    # ISO format timestamp
    "level": str,        # Log level (INFO, ERROR, WARNING)
    "message": str       # Log message
}
```

## Error Handling

### Exception Types

#### `ConfigurationError`
Raised when configuration issues occur.

```python
try:
    config = ConfigManager("invalid_path.ini")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

#### `OllamaConnectionError`
Raised when Ollama server is not accessible.

#### `FileProcessingError`
Raised when file processing fails.

#### `BrowserAutomationError`
Raised when browser automation fails.

### Error Codes

| Code | Description | Module |
|------|-------------|---------|
| CONF_001 | Configuration file not found | ConfigManager |
| OLLAMA_001 | Connection timeout | OllamaManager |
| OLLAMA_002 | Model not found | OllamaManager |
| BROWSER_001 | WebDriver initialization failed | BrowserAgent |
| FILE_001 | Unsupported file format | FileProcessor |
| GIT_001 | Repository not initialized | GitManager |

## Logging

### Logger Configuration

```python
from src.logger import log, LoggerMixin

# Direct logging
log.info("Information message")
log.error("Error message")
log.warning("Warning message")

# Using mixin in classes
class MyClass(LoggerMixin):
    def my_method(self):
        self.logger.info("Method called")
```

### Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General information about program execution
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical errors that may cause program termination

## Configuration Reference

### Complete Configuration Schema

```ini
[OLLAMA]
base_url = http://localhost:11434
model_llama = llama3.1:8b
model_codellama = codellama:latest
timeout = 300

[CHROMADB]
persist_directory = ./knowledgebase
collection_name = automation_knowledge
embedding_model = all-MiniLM-L6-v2

[BROWSER]
default_browser = chrome
headless = false
capture_screenshots = true
screenshot_path = ./screenshots
implicit_wait = 10
page_load_timeout = 30

[PATHS]
testcase_output = ./testcase_generator
testscript_output = ./testscript_generator
reports_output = ./reports
logs_output = ./logs
data_input = ./data

[GIT]
auto_commit = true
auto_push = false
commit_message_template = "Automated commit: {timestamp}"

[LOGGING]
level = INFO
format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
file_path = ./logs/framework.log

[UI]
theme = dark
page_title = Python Automation Framework
page_icon = 🤖
layout = wide
```

## Extension Points

### Custom File Processors

```python
from src.file_processor import FileProcessor

class CustomFileProcessor(FileProcessor):
    def __init__(self, config):
        super().__init__(config)
        self.supported_formats['.custom'] = self._extract_from_custom
    
    def _extract_from_custom(self, file_path: str) -> str:
        # Custom extraction logic
        pass
```

### Custom Report Generators

```python
from src.report_generator import ReportGenerator

class CustomReportGenerator(ReportGenerator):
    def generate_pdf_report(self, execution_results):
        # Custom PDF generation logic
        pass
```

### Custom Browser Agents

```python
from src.browser_agent import BrowserAutomationAgent

class CustomBrowserAgent(BrowserAutomationAgent):
    def execute_mobile_script(self, script_content):
        # Custom mobile automation logic
        pass
```

## Performance Considerations

### Memory Management

- Use generators for large file processing
- Implement pagination for large result sets
- Clear browser cache regularly
- Optimize vector database queries

### Concurrency

- Use thread pools for parallel file processing
- Implement queue-based execution for multiple tests
- Consider async operations for I/O bound tasks

### Caching

- Cache frequently used prompts
- Store processed file contents temporarily
- Implement result caching for repeated queries

## Security Guidelines

### Input Validation

- Validate all user inputs
- Sanitize file paths
- Check file types and sizes
- Validate configuration values

### Data Protection

- Encrypt sensitive configuration data
- Secure temporary file storage
- Implement access controls
- Regular security audits

### Network Security

- Use HTTPS for external connections
- Validate SSL certificates
- Implement rate limiting
- Monitor network traffic

This API reference provides the foundation for extending and customizing the Python Automation Framework. For specific implementation examples, refer to the source code and unit tests.

