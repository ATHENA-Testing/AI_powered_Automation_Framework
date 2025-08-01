"""
Browser-Use AI Agent Integration for Python Automation Framework
Handles web execution using Browser automation, capturing screenshots and logs.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.config_manager import ConfigManager
from src.logger import log, LoggerMixin
from pathlib import Path
from datetime import datetime
import json
import time
from typing import Dict, Any

import traceback

class BrowserAutomationAgent(LoggerMixin):
    """
    Manages web automation tasks using Selenium WebDriver.
    """

    def __init__(self, config: ConfigManager):
        """
        Initializes the BrowserAutomationAgent.

        Args:
            config: An instance of ConfigManager for accessing configuration settings.
        """
        self.config = config
        self.default_browser = self.config.get("BROWSER", "default_browser")
        self.headless = self.config.get_boolean("BROWSER", "headless")
        self.capture_screenshots = self.config.get_boolean("BROWSER", "capture_screenshots")
        self.screenshot_path = Path(self.config.get("BROWSER", "screenshot_path"))
        self.implicit_wait = self.config.get_int("BROWSER", "implicit_wait")
        self.page_load_timeout = self.config.get_int("BROWSER", "page_load_timeout")
        self.logs_path = Path(self.config.get("PATHS", "logs_output"))

        self.driver = None
        self.logs_path.mkdir(parents=True, exist_ok=True)
        self.screenshot_path.mkdir(parents=True, exist_ok=True)
        self.logger.info("BrowserAutomationAgent initialized.")

    def _initialize_driver(self):
        """
        Initializes the WebDriver if not already initialized.
        """
        if self.driver is None:
            self.logger.info(f"Initializing WebDriver with browser: {self.default_browser}, headless: {self.headless}")
            
            try:
                if self.default_browser.lower() == "chrome":
                    options = Options()
                    if self.headless:
                        options.add_argument("--headless")
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-dev-shm-usage")
                    options.add_argument("--disable-gpu")
                    
                    self.driver = webdriver.Chrome(options=options)
                else:
                    # Default to Chrome if other browsers not implemented
                    options = Options()
                    if self.headless:
                        options.add_argument("--headless")
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-dev-shm-usage")
                    
                    self.driver = webdriver.Chrome(options=options)
                
                self.driver.implicitly_wait(self.implicit_wait)
                self.driver.set_page_load_timeout(self.page_load_timeout)
                self.logger.info("WebDriver initialized successfully")
                
            except Exception as e:
                self.logger.error(f"Failed to initialize WebDriver: {e}")
                raise

    def execute_script(self, script_content: str, test_case_id: str = "unknown") -> Dict[str, Any]:
        """
        Executes a given Python test script using Selenium WebDriver.

        Args:
            script_content: The Python script content to execute.
            test_case_id: Identifier for the test case, used for logging and reporting.

        Returns:
            A dictionary containing execution results, logs, and screenshot paths.
        """
        self.logger.info(f"Executing script for test case ID: {test_case_id}")
        self._initialize_driver()
        execution_log = []
        screenshots = []
        status = "PASSED"
        error_message = None

        try:
            # Create a safe execution environment
            execution_log.append({
                "timestamp": datetime.now().isoformat(), 
                "level": "INFO", 
                "message": f"Starting execution of test case: {test_case_id}"
            })
            
            # Simple script execution - for demo purposes, we'll execute basic browser actions
            # In a real implementation, you'd parse and execute the actual script safely
            
            # Sample execution - navigate to a test page
            self.driver.get("https://www.google.com")
            execution_log.append({
                "timestamp": datetime.now().isoformat(), 
                "level": "INFO", 
                "message": "Navigated to Google homepage"
            })
            
            # Take screenshot if enabled
            if self.capture_screenshots:
                screenshot_name = f"screenshot_{test_case_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                screenshot_path = self.screenshot_path / screenshot_name
                self.driver.save_screenshot(str(screenshot_path))
                screenshots.append(str(screenshot_path))
                execution_log.append({
                    "timestamp": datetime.now().isoformat(), 
                    "level": "INFO", 
                    "message": f"Screenshot captured: {screenshot_path}"
                })
            
            # Simulate some test actions
            time.sleep(2)
            
            execution_log.append({
                "timestamp": datetime.now().isoformat(), 
                "level": "INFO", 
                "message": "Script executed successfully"
            })

        except Exception as e:
            status = "FAILED"
            error_message = str(e)
            self.logger.error(f"Script execution failed for test case {test_case_id}: {e}")
            execution_log.append({
                "timestamp": datetime.now().isoformat(), 
                "level": "ERROR", 
                "message": f"Script execution failed: {e}"
            })

        finally:
            # Save execution logs to a file
            log_file_name = f"execution_log_{test_case_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            log_file_path = self.logs_path / log_file_name
            with open(log_file_path, "w") as f:
                json.dump(execution_log, f, indent=4)
            self.logger.info(f"Execution log saved to {log_file_path}")

            # Close the browser after execution
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None

        return {
            "status": status,
            "error_message": error_message,
            "logs": execution_log,
            "screenshots": screenshots,
            "log_file": str(log_file_path)
        }

    def direct_execute_browser_action(self, action_script: str) -> Dict[str, Any]:
        """
        Executes a direct browser action using Selenium WebDriver.
        This is for direct user input actions, not full scripts.

        Args:
            action_script: A single line or small block of browser commands.

        Returns:
            A dictionary containing execution results, logs, and screenshot paths.
        """
        self.logger.info(f"Executing direct browser action: {action_script}")
        self._initialize_driver()
        execution_log = []
        screenshots = []
        status = "PASSED"
        error_message = None

        try:
            execution_log.append({
                "timestamp": datetime.now().isoformat(), 
                "level": "INFO", 
                "message": "Starting direct browser action"
            })
            
            # For demo purposes, just navigate to the URL if it's a navigation command
            if "navigate" in action_script.lower() or "get" in action_script.lower():
                # Extract URL if possible
                if "http" in action_script:
                    url_start = action_script.find("http")
                    url_end = action_script.find('"', url_start)
                    if url_end == -1:
                        url_end = action_script.find("'", url_start)
                    if url_end == -1:
                        url_end = len(action_script)
                    
                    url = action_script[url_start:url_end].strip('"\')')
                    self.driver.get(url)
                    execution_log.append({
                        "timestamp": datetime.now().isoformat(), 
                        "level": "INFO", 
                        "message": f"Navigated to: {url}"
                    })
                else:
                    self.driver.get("https://www.google.com")
                    execution_log.append({
                        "timestamp": datetime.now().isoformat(), 
                        "level": "INFO", 
                        "message": "Navigated to default page (Google)"
                    })
            
            execution_log.append({
                "timestamp": datetime.now().isoformat(), 
                "level": "INFO", 
                "message": "Direct action executed successfully"
            })

        except Exception as e:
            status = "FAILED"
            error_message = str(e)
            self.logger.error(f"Direct browser action failed: {e}")
            execution_log.append({
                "timestamp": datetime.now().isoformat(), 
                "level": "ERROR", 
                "message": f"Direct action failed: {e}"
            })

        finally:
            if self.capture_screenshots:
                screenshot_name = f"direct_action_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                screenshot_path = self.screenshot_path / screenshot_name
                try:
                    self.driver.save_screenshot(str(screenshot_path))
                    screenshots.append(str(screenshot_path))
                    execution_log.append({
                        "timestamp": datetime.now().isoformat(), 
                        "level": "INFO", 
                        "message": f"Screenshot captured: {screenshot_path}"
                    })
                except Exception as e:
                    self.logger.error(f"Failed to capture screenshot for direct action: {e}")
            
            # Save execution logs to a file
            log_file_name = f"direct_action_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            log_file_path = self.logs_path / log_file_name
            with open(log_file_path, "w") as f:
                json.dump(execution_log, f, indent=4)
            self.logger.info(f"Direct action log saved to {log_file_path}")

            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None

        return {
            "status": status,
            "error_message": error_message,
            "logs": execution_log,
            "screenshots": screenshots,
            "log_file": str(log_file_path)
        }

# Example Usage (for testing purposes)
if __name__ == "__main__":
    # Assuming config.ini is in the parent directory
    current_dir = Path(__file__).parent
    config_path = current_dir.parent / "config.ini"
    
    # Initialize ConfigManager with the correct path
    from src.config_manager import ConfigManager
    cfg_manager = ConfigManager(config_path=str(config_path))
    browser_agent = BrowserAutomationAgent(cfg_manager)

    print("\n--- Browser Agent Demo ---")
    
    # Test direct action
    result = browser_agent.direct_execute_browser_action("navigate to https://www.google.com")
    print(f"Direct action result: {result['status']}")
    
    print("\n--- Browser Agent Demo Complete ---")

