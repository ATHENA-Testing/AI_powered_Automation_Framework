"""
Ollama Manager for Python Automation Framework
Handles interactions with Ollama for prompt, test case, and test script generation.
"""

import requests
import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

from src.config_manager import ConfigManager
from src.logger import log, LoggerMixin

class OllamaManager(LoggerMixin):
    """
    Manages Ollama interactions for various AI-powered generation tasks.
    """

    def __init__(self, config: ConfigManager):
        """
        Initializes the OllamaManager.

        Args:
            config: An instance of ConfigManager for accessing configuration settings.
        """
        self.config = config
        self.ollama_base_url = self.config.get("OLLAMA", "base_url")
        self.model_llama = self.config.get("OLLAMA", "model_llama")
        self.model_codellama = self.config.get("OLLAMA", "model_codellama")
        self.timeout = self.config.get_int("OLLAMA", "timeout")

        self.persist_directory = Path(self.config.get("CHROMADB", "persist_directory"))
        self.collection_name = self.config.get("CHROMADB", "collection_name")
        
        # Simple knowledge base storage (file-based for now)
        self.knowledge_base_path = self.persist_directory / "knowledge_base.json"
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize knowledge base
        self.knowledge_base = self._load_knowledge_base()
        
        self.logger.info(f"OllamaManager initialized with base URL: {self.ollama_base_url}")

    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load knowledge base from file"""
        if self.knowledge_base_path.exists():
            try:
                with open(self.knowledge_base_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading knowledge base: {e}")
        return {"documents": [], "embeddings": {}}

    def _save_knowledge_base(self):
        """Save knowledge base to file"""
        try:
            with open(self.knowledge_base_path, 'w') as f:
                json.dump(self.knowledge_base, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving knowledge base: {e}")

    def _check_ollama_connection(self) -> bool:
        """
        Checks if Ollama server is running and accessible.
        """
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                self.logger.info("Successfully connected to Ollama server.")
                return True
            else:
                self.logger.error(f"Ollama server returned status code: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"Failed to connect to Ollama server: {e}")
            self.logger.warning("Please ensure Ollama is running and the model is downloaded.")
            return False

    def _make_ollama_request(self, model: str, prompt: str, system_prompt: str = None) -> str:
        """
        Make a request to Ollama API
        """
        try:
            data = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            if system_prompt:
                data["system"] = system_prompt
            
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json=data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                self.logger.error(f"Ollama API error: {response.status_code}")
                return f"Error: Ollama API returned status {response.status_code}"
                
        except Exception as e:
            self.logger.error(f"Error making Ollama request: {e}")
            return f"Error: {str(e)}"

    def setup_ollama_models(self):
        """
        Ensures required Ollama models are available.
        """
        if not self._check_ollama_connection():
            self.logger.warning("Cannot check models - Ollama server not accessible")
            return
        
        # Check if models exist
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                
                if self.model_llama not in model_names:
                    self.logger.warning(f"Model {self.model_llama} not found. Please pull it with: ollama pull {self.model_llama}")
                
                if self.model_codellama not in model_names:
                    self.logger.warning(f"Model {self.model_codellama} not found. Please pull it with: ollama pull {self.model_codellama}")
                    
        except Exception as e:
            self.logger.error(f"Error checking models: {e}")

    def add_document_to_knowledge_base(self, file_path: str, document_content: str) -> None:
        """
        Adds a document's content to the knowledge base.

        Args:
            file_path: The original path of the document.
            document_content: The extracted text content of the document.
        """
        self.logger.info(f"Adding document {file_path} to knowledge base...")
        
        # Simple text chunking
        chunks = self._split_text(document_content)
        
        document_entry = {
            "file_path": file_path,
            "content": document_content,
            "chunks": chunks,
            "timestamp": datetime.now().isoformat(),
            "length": len(document_content)
        }
        
        self.knowledge_base["documents"].append(document_entry)
        self._save_knowledge_base()
        
        self.logger.info(f"Document {file_path} successfully added to knowledge base.")

    def _split_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Simple text splitting"""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap if end < len(text) else end
        return chunks

    def query_knowledge_base(self, query: str, k: int = 4) -> List[str]:
        """
        Queries the knowledge base for relevant documents.

        Args:
            query: The query string.
            k: The number of relevant documents to retrieve.

        Returns:
            A list of relevant document contents.
        """
        self.logger.info(f"Querying knowledge base for: {query}")
        
        # Simple keyword-based search (in a real implementation, you'd use embeddings)
        relevant_chunks = []
        query_lower = query.lower()
        
        for doc in self.knowledge_base["documents"]:
            for chunk in doc["chunks"]:
                if any(word in chunk.lower() for word in query_lower.split()):
                    relevant_chunks.append(chunk)
        
        # Return top k results
        return relevant_chunks[:k]

    def get_knowledge_base_info(self) -> Dict[str, Any]:
        """Get information about the knowledge base"""
        return {
            "doc_count": len(self.knowledge_base["documents"]),
            "total_chunks": sum(len(doc["chunks"]) for doc in self.knowledge_base["documents"])
        }

    def generate_prompt(self, user_input: str, context: Optional[str] = None) -> str:
        """
        Generates a high-quality prompt based on user input and optional context.

        Args:
            user_input: The user's initial input or query.
            context: Optional context from the knowledge base.

        Returns:
            The generated prompt string.
        """
        self.logger.info("Generating prompt...")
        
        system_prompt = (
            "You are an expert in generating high-quality prompts for test case and test script generation. "
            "Based on the user input and context, generate a detailed and clear prompt that can be used "
            "for creating comprehensive test cases."
        )
        
        prompt_text = f"User Input: {user_input}\n"
        if context:
            prompt_text += f"Context: {context}\n"
        prompt_text += "Generate a detailed prompt for test case generation:"
        
        try:
            response = self._make_ollama_request(self.model_llama, prompt_text, system_prompt)
            self.logger.info("Prompt generated successfully.")
            return response
        except Exception as e:
            self.logger.error(f"Failed to generate prompt: {e}")
            return f"Error generating prompt: {e}"

    def generate_test_cases(self, prompt: str, testcase_level: str, testcase_type: str, count: int) -> List[Dict[str, Any]]:
        """
        Generates test cases based on a prompt and specified criteria.

        Args:
            prompt: The prompt generated for test case generation.
            testcase_level: Level of test cases (Advanced/Intermediate/Beginner).
            testcase_type: Type of test cases (Functional, UI, API, Mobile).
            count: Number of test cases to generate.

        Returns:
            A list of dictionaries, each representing a test case.
        """
        self.logger.info(f"Generating {count} {testcase_level} {testcase_type} test cases...")

        system_prompt = (
            f"You are an expert QA engineer. Generate {count} test cases in JSON format. "
            f"The test cases should be {testcase_level} level and of type {testcase_type}. "
            "Each test case should have: id, title, description, preconditions (array), "
            "steps (array), expected_result, priority, and tags (array). "
            "Return only valid JSON array format."
        )
        
        prompt_text = f"Based on this prompt: {prompt}\n\nGenerate {count} test cases as a JSON array."
        
        try:
            response = self._make_ollama_request(self.model_llama, prompt_text, system_prompt)
            
            # Try to parse JSON response
            try:
                # Clean up the response to extract JSON
                json_start = response.find('[')
                json_end = response.rfind(']') + 1
                if json_start != -1 and json_end != 0:
                    json_str = response[json_start:json_end]
                    test_cases = json.loads(json_str)
                    self.logger.info("Test cases generated successfully.")
                    return test_cases
                else:
                    raise ValueError("No JSON array found in response")
            except (json.JSONDecodeError, ValueError) as e:
                self.logger.warning(f"Failed to parse JSON response: {e}")
                # Return a sample test case structure
                return self._generate_sample_test_cases(count, testcase_level, testcase_type)
                
        except Exception as e:
            self.logger.error(f"Failed to generate test cases: {e}")
            return self._generate_sample_test_cases(count, testcase_level, testcase_type)

    def _generate_sample_test_cases(self, count: int, level: str, test_type: str) -> List[Dict[str, Any]]:
        """Generate sample test cases when AI generation fails"""
        sample_cases = []
        for i in range(count):
            sample_cases.append({
                "id": f"TC_{i+1:03d}",
                "title": f"Sample {test_type} Test Case {i+1}",
                "description": f"This is a {level} level {test_type} test case for demonstration purposes.",
                "preconditions": ["System is accessible", "User has valid credentials"],
                "steps": [
                    "Navigate to the application",
                    "Perform the required action",
                    "Verify the result"
                ],
                "expected_result": "The action should complete successfully",
                "priority": "Medium",
                "tags": [test_type.lower(), level.lower(), "sample"]
            })
        return sample_cases

    def generate_test_script(self, test_case: Dict[str, Any], tool_selection: str, browser_selection: str) -> str:
        """
        Generates a test script in Python language based on a test case.

        Args:
            test_case: A dictionary representing the test case.
            tool_selection: The automation tool to use (e.g., Selenium, Playwright).
            browser_selection: The browser to target (e.g., Chrome, Firefox).

        Returns:
            The generated test script as a string.
        """
        self.logger.info(f"Generating test script for test case: {test_case.get('title', 'Untitled')}")

        system_prompt = (
            f"You are an expert in writing automated test scripts using {tool_selection} for {browser_selection}. "
            "Generate a complete Python test script with proper imports, setup, test methods, and teardown. "
            "Include error handling and best practices. Make the script executable and well-commented."
        )
        
        prompt_text = f"""
Generate a Python test script for:
Title: {test_case.get('title', '')}
Description: {test_case.get('description', '')}
Preconditions: {', '.join(test_case.get('preconditions', []))}
Steps: {' -> '.join(test_case.get('steps', []))}
Expected Result: {test_case.get('expected_result', '')}

Tool: {tool_selection}
Browser: {browser_selection}

Generate a complete Python test script:
"""

        try:
            response = self._make_ollama_request(self.model_codellama, prompt_text, system_prompt)
            self.logger.info("Test script generated successfully.")
            return response
        except Exception as e:
            self.logger.error(f"Failed to generate test script: {e}")
            return self._generate_sample_script(test_case, tool_selection, browser_selection)

    def _generate_sample_script(self, test_case: Dict[str, Any], tool: str, browser: str) -> str:
        """Generate a sample script when AI generation fails"""
        return f'''
# Test Script for: {test_case.get('title', 'Sample Test')}
# Generated for {tool} with {browser}

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test{test_case.get('id', 'Sample').replace('_', '')}:
    def __init__(self):
        self.driver = None
    
    def setup(self):
        """Setup test environment"""
        if "{browser.lower()}" == "chrome":
            self.driver = webdriver.Chrome()
        elif "{browser.lower()}" == "firefox":
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()  # Default
        
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
    
    def test_{test_case.get('id', 'sample').lower()}(self):
        """
        Test Case: {test_case.get('title', 'Sample Test')}
        Description: {test_case.get('description', 'Sample test description')}
        """
        try:
            # Test steps based on: {' -> '.join(test_case.get('steps', ['Sample step']))}
            
            # Step 1: Navigate to application
            self.driver.get("https://example.com")
            
            # Step 2: Perform test actions
            # Add your specific test logic here
            
            # Step 3: Verify results
            # Expected: {test_case.get('expected_result', 'Test should pass')}
            
            print("Test passed successfully!")
            return True
            
        except Exception as e:
            print(f"Test failed: {{e}}")
            return False
    
    def teardown(self):
        """Cleanup after test"""
        if self.driver:
            self.driver.quit()
    
    def run(self):
        """Run the complete test"""
        self.setup()
        try:
            result = self.test_{test_case.get('id', 'sample').lower()}()
            return result
        finally:
            self.teardown()

if __name__ == "__main__":
    test = Test{test_case.get('id', 'Sample').replace('_', '')}()
    test.run()
'''

# Example Usage (for testing purposes)
if __name__ == "__main__":
    # Assuming config.ini is in the parent directory
    current_dir = Path(__file__).parent
    config_path = current_dir.parent / "config.ini"
    
    # Initialize ConfigManager with the correct path
    from src.config_manager import ConfigManager
    cfg_manager = ConfigManager(config_path=str(config_path))
    ollama_manager = OllamaManager(cfg_manager)

    print("\n--- Ollama Manager Demo ---")
    
    # Check connection
    if ollama_manager._check_ollama_connection():
        print("✅ Ollama connection successful")
    else:
        print("❌ Ollama connection failed")
    
    # Add sample document
    sample_doc = "This is a sample document about user login functionality."
    ollama_manager.add_document_to_knowledge_base("sample.txt", sample_doc)
    
    # Query knowledge base
    results = ollama_manager.query_knowledge_base("login")
    print(f"Knowledge base query results: {len(results)} items found")
    
    print("\n--- Demo Complete ---")

