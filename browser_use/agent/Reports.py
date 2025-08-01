import datetime

class HTMLLogger:
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, 'w') as f:
            f.write("""<html>
<head>
    <title>Log Report</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; }
        tr:nth-child(even){background-color: #f2f2f2;}
        th { background-color: #4CAF50; color: white; }
    </style>
</head>
<body>
    <h2>Application Log Report</h2>
    <table>
        <tr>
            <th>Timestamp</th>
            <th>Level</th>
            <th>Message</th>
        </tr>
""")

    def log(self, level, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = f"""        <tr>
            <td>{timestamp}</td>
            <td>{level}</td>
            <td>{message}</td>
        </tr>
"""
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(row)

    def close(self):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write("""    </table>
</body>
</html>""")

# --- Usage example ---
# logger = HTMLLogger('report.html')
# logger.log('INFO', 'Application started')
# logger.log('WARNING', 'This is a warning message')
# logger.log('ERROR', 'This is an error message')
# logger.close()
# --- Usage example ---
# logger = HTMLLogger('report.html')
# loggers.log('INFO', 'Application started')
# loggers.log('WARNING', 'This is a warning message')
# loggers.log('ERROR', 'This is an error message')
# loggers.close()
