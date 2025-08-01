"""
Report Generator for Python Automation Framework
Generates beautiful HTML reports from execution results.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import base64
import os

from src.config_manager import ConfigManager
from src.logger import log, LoggerMixin

class ReportGenerator(LoggerMixin):
    """
    Generates HTML reports from test execution results.
    """

    def __init__(self, config: ConfigManager):
        """
        Initializes the ReportGenerator.

        Args:
            config: An instance of ConfigManager for accessing configuration settings.
        """
        self.config = config
        self.reports_output = Path(self.config.get("PATHS", "reports_output"))
        self.reports_output.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("ReportGenerator initialized")

    def generate_html_report(self, execution_results: Dict[str, Any]) -> str:
        """
        Generates a comprehensive HTML report from execution results.

        Args:
            execution_results: Dictionary containing execution results for multiple test scripts.

        Returns:
            Path to the generated HTML report file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"execution_report_{timestamp}.html"
        report_path = self.reports_output / report_filename
        
        self.logger.info(f"Generating HTML report: {report_path}")
        
        # Calculate summary statistics
        total_tests = len(execution_results)
        passed_tests = sum(1 for result in execution_results.values() if result.get("status") == "PASSED")
        failed_tests = total_tests - passed_tests
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Generate HTML content
        html_content = self._generate_html_template(
            execution_results, 
            total_tests, 
            passed_tests, 
            failed_tests, 
            pass_rate,
            timestamp
        )
        
        # Write HTML file
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.logger.info(f"HTML report generated successfully: {report_path}")
        return str(report_path)

    def _generate_html_template(self, execution_results: Dict[str, Any], total_tests: int, 
                               passed_tests: int, failed_tests: int, pass_rate: float, 
                               timestamp: str) -> str:
        """
        Generates the HTML template for the report.
        """
        # Generate test results HTML
        test_results_html = self._generate_test_results_html(execution_results)
        
        # Generate charts data
        charts_data = self._generate_charts_data(execution_results, passed_tests, failed_tests)
        
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Automation Framework - Execution Report</title>
    <style>
        {self._get_css_styles()}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="header-content">
                <h1>🤖 Python Automation Framework</h1>
                <h2>Execution Report</h2>
                <p class="timestamp">Generated on: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
            </div>
        </header>

        <!-- Summary Section -->
        <section class="summary">
            <h3>📊 Execution Summary</h3>
            <div class="summary-cards">
                <div class="card total">
                    <div class="card-header">Total Tests</div>
                    <div class="card-value">{total_tests}</div>
                </div>
                <div class="card passed">
                    <div class="card-header">Passed</div>
                    <div class="card-value">{passed_tests}</div>
                </div>
                <div class="card failed">
                    <div class="card-header">Failed</div>
                    <div class="card-value">{failed_tests}</div>
                </div>
                <div class="card pass-rate">
                    <div class="card-header">Pass Rate</div>
                    <div class="card-value">{pass_rate:.1f}%</div>
                </div>
            </div>
        </section>

        <!-- Charts Section -->
        <section class="charts">
            <div class="chart-container">
                <h3>📈 Test Results Distribution</h3>
                <canvas id="resultsChart" width="400" height="200"></canvas>
            </div>
        </section>

        <!-- Test Results Section -->
        <section class="test-results">
            <h3>📋 Detailed Test Results</h3>
            {test_results_html}
        </section>

        <!-- Footer -->
        <footer class="footer">
            <p>Generated by Python Automation Framework | Report ID: {timestamp}</p>
        </footer>
    </div>

    <script>
        {self._get_javascript_code(charts_data)}
    </script>
</body>
</html>
"""
        return html_template

    def _generate_test_results_html(self, execution_results: Dict[str, Any]) -> str:
        """
        Generates HTML for individual test results.
        """
        results_html = []
        
        for script_id, result in execution_results.items():
            status = result.get("status", "UNKNOWN")
            status_class = "passed" if status == "PASSED" else "failed"
            status_icon = "✅" if status == "PASSED" else "❌"
            
            # Process logs
            logs_html = self._generate_logs_html(result.get("logs", []))
            
            # Process screenshots
            screenshots_html = self._generate_screenshots_html(result.get("screenshots", []))
            
            # Error message
            error_message = result.get("error_message", "")
            error_html = f'<div class="error-message"><strong>Error:</strong> {error_message}</div>' if error_message else ""
            
            result_html = f"""
            <div class="test-result {status_class}">
                <div class="test-header">
                    <h4>{status_icon} {script_id}</h4>
                    <span class="status-badge {status_class}">{status}</span>
                </div>
                
                {error_html}
                
                <div class="test-details">
                    <div class="detail-section">
                        <h5>📝 Execution Logs</h5>
                        <div class="logs-container">
                            {logs_html}
                        </div>
                    </div>
                    
                    {screenshots_html}
                </div>
            </div>
            """
            results_html.append(result_html)
        
        return "\n".join(results_html)

    def _generate_logs_html(self, logs: List[Dict[str, Any]]) -> str:
        """
        Generates HTML for execution logs.
        """
        if not logs:
            return "<p class='no-data'>No logs available</p>"
        
        logs_html = []
        for log_entry in logs:
            timestamp = log_entry.get("timestamp", "")
            level = log_entry.get("level", "INFO")
            message = log_entry.get("message", "")
            
            level_class = level.lower()
            logs_html.append(f"""
                <div class="log-entry {level_class}">
                    <span class="log-timestamp">{timestamp}</span>
                    <span class="log-level">{level}</span>
                    <span class="log-message">{message}</span>
                </div>
            """)
        
        return "\n".join(logs_html)

    def _generate_screenshots_html(self, screenshots: List[str]) -> str:
        """
        Generates HTML for screenshots.
        """
        if not screenshots:
            return ""
        
        screenshots_html = ["<div class='detail-section'><h5>📸 Screenshots</h5><div class='screenshots-container'>"]
        
        for screenshot_path in screenshots:
            if os.path.exists(screenshot_path):
                # Convert image to base64 for embedding
                try:
                    with open(screenshot_path, "rb") as img_file:
                        img_data = base64.b64encode(img_file.read()).decode()
                        img_name = os.path.basename(screenshot_path)
                        
                        screenshots_html.append(f"""
                            <div class="screenshot">
                                <img src="data:image/png;base64,{img_data}" alt="{img_name}" onclick="openModal(this)">
                                <p class="screenshot-name">{img_name}</p>
                            </div>
                        """)
                except Exception as e:
                    screenshots_html.append(f"<p class='error'>Error loading screenshot: {screenshot_path}</p>")
            else:
                screenshots_html.append(f"<p class='error'>Screenshot not found: {screenshot_path}</p>")
        
        screenshots_html.append("</div></div>")
        return "\n".join(screenshots_html)

    def _generate_charts_data(self, execution_results: Dict[str, Any], passed_tests: int, failed_tests: int) -> Dict[str, Any]:
        """
        Generates data for charts.
        """
        return {
            "pieChart": {
                "labels": ["Passed", "Failed"],
                "data": [passed_tests, failed_tests],
                "colors": ["#4CAF50", "#F44336"]
            }
        }

    def _get_css_styles(self) -> str:
        """
        Returns CSS styles for the HTML report.
        """
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header h2 {
            color: #555;
            font-size: 1.8em;
            margin-bottom: 10px;
        }

        .timestamp {
            color: #777;
            font-size: 1.1em;
        }

        .summary {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        .summary h3 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
        }

        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }

        .card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .card.passed {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        }

        .card.failed {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        }

        .card.pass-rate {
            background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
        }

        .card-header {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .card-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
        }

        .charts {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        .chart-container {
            text-align: center;
        }

        .chart-container h3 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
        }

        .test-results {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        .test-results h3 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
        }

        .test-result {
            border: 2px solid #ddd;
            border-radius: 10px;
            margin-bottom: 20px;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .test-result:hover {
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }

        .test-result.passed {
            border-color: #4CAF50;
        }

        .test-result.failed {
            border-color: #F44336;
        }

        .test-header {
            background: #f8f9fa;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .test-result.passed .test-header {
            background: #e8f5e8;
        }

        .test-result.failed .test-header {
            background: #fde8e8;
        }

        .test-header h4 {
            margin: 0;
            color: #333;
        }

        .status-badge {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }

        .status-badge.passed {
            background: #4CAF50;
            color: white;
        }

        .status-badge.failed {
            background: #F44336;
            color: white;
        }

        .error-message {
            background: #ffebee;
            border-left: 4px solid #F44336;
            padding: 15px 20px;
            color: #c62828;
        }

        .test-details {
            padding: 20px;
        }

        .detail-section {
            margin-bottom: 20px;
        }

        .detail-section h5 {
            color: #555;
            margin-bottom: 10px;
            font-size: 1.1em;
        }

        .logs-container {
            background: #f8f9fa;
            border-radius: 5px;
            padding: 15px;
            max-height: 300px;
            overflow-y: auto;
        }

        .log-entry {
            display: flex;
            gap: 10px;
            padding: 5px 0;
            border-bottom: 1px solid #eee;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }

        .log-entry:last-child {
            border-bottom: none;
        }

        .log-timestamp {
            color: #666;
            min-width: 180px;
        }

        .log-level {
            min-width: 60px;
            font-weight: bold;
        }

        .log-level.info {
            color: #2196F3;
        }

        .log-level.error {
            color: #F44336;
        }

        .log-level.warning {
            color: #FF9800;
        }

        .log-message {
            flex: 1;
        }

        .screenshots-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }

        .screenshot {
            text-align: center;
        }

        .screenshot img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            cursor: pointer;
            transition: transform 0.3s ease;
        }

        .screenshot img:hover {
            transform: scale(1.05);
        }

        .screenshot-name {
            margin-top: 5px;
            font-size: 0.8em;
            color: #666;
        }

        .no-data {
            color: #999;
            font-style: italic;
            text-align: center;
            padding: 20px;
        }

        .error {
            color: #F44336;
            font-style: italic;
        }

        .footer {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            color: #666;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        /* Modal for screenshot viewing */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
        }

        .modal-content {
            margin: 5% auto;
            display: block;
            max-width: 90%;
            max-height: 80%;
        }

        .close {
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .summary-cards {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .card-value {
                font-size: 2em;
            }
        }
        """

    def _get_javascript_code(self, charts_data: Dict[str, Any]) -> str:
        """
        Returns JavaScript code for interactive charts.
        """
        return f"""
        // Initialize charts
        document.addEventListener('DOMContentLoaded', function() {{
            // Pie chart for test results
            const ctx = document.getElementById('resultsChart').getContext('2d');
            new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: {json.dumps(charts_data['pieChart']['labels'])},
                    datasets: [{{
                        data: {json.dumps(charts_data['pieChart']['data'])},
                        backgroundColor: {json.dumps(charts_data['pieChart']['colors'])},
                        borderWidth: 2,
                        borderColor: '#fff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                            labels: {{
                                padding: 20,
                                font: {{
                                    size: 14
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }});

        // Modal functionality for screenshots
        function openModal(img) {{
            const modal = document.createElement('div');
            modal.className = 'modal';
            modal.innerHTML = `
                <span class="close">&times;</span>
                <img class="modal-content" src="${{img.src}}" alt="${{img.alt}}">
            `;
            document.body.appendChild(modal);
            modal.style.display = 'block';

            modal.querySelector('.close').onclick = function() {{
                document.body.removeChild(modal);
            }};

            modal.onclick = function(event) {{
                if (event.target === modal) {{
                    document.body.removeChild(modal);
                }}
            }};
        }}
        """

# Example Usage (for testing purposes)
if __name__ == "__main__":
    # Assuming config.ini is in the parent directory
    current_dir = Path(__file__).parent
    config_path = current_dir.parent / "config.ini"
    
    # Initialize ConfigManager with the correct path
    cfg_manager = ConfigManager(config_path=str(config_path))
    report_generator = ReportGenerator(cfg_manager)

    # Create sample execution results
    sample_results = {
        "TC_001_Login": {
            "status": "PASSED",
            "error_message": None,
            "logs": [
                {"timestamp": "2024-01-15 10:30:00", "level": "INFO", "message": "Starting test execution"},
                {"timestamp": "2024-01-15 10:30:05", "level": "INFO", "message": "Navigated to login page"},
                {"timestamp": "2024-01-15 10:30:10", "level": "INFO", "message": "Entered credentials"},
                {"timestamp": "2024-01-15 10:30:15", "level": "INFO", "message": "Login successful"}
            ],
            "screenshots": [],
            "log_file": "/path/to/log/file.json"
        },
        "TC_002_Search": {
            "status": "FAILED",
            "error_message": "Element not found: search button",
            "logs": [
                {"timestamp": "2024-01-15 10:35:00", "level": "INFO", "message": "Starting search test"},
                {"timestamp": "2024-01-15 10:35:05", "level": "ERROR", "message": "Search button not found"},
                {"timestamp": "2024-01-15 10:35:06", "level": "ERROR", "message": "Test failed"}
            ],
            "screenshots": [],
            "log_file": "/path/to/log/file2.json"
        }
    }

    print("\n--- Generating Sample HTML Report ---")
    report_path = report_generator.generate_html_report(sample_results)
    print(f"Report generated: {report_path}")
    print("\n--- Report Generation Demo Complete ---")

