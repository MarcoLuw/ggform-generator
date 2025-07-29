# Configuration for MCQ Form Generator

# Default form settings
DEFAULT_FORM_TITLE = "MCQ Quiz"
DEFAULT_FORM_DESCRIPTION = "Complete this quiz and receive immediate feedback with explanations."

# Scoring settings
POINTS_PER_QUESTION = 1
ENABLE_IMMEDIATE_FEEDBACK = True
SHOW_CORRECT_ANSWERS = True
COLLECT_EMAIL_ADDRESSES = False

# API settings
OAUTH_PORT = 50699
REQUEST_TIMEOUT = 30

# File paths (relative to project root)
CSV_FILE_PATH="material/reading.csv"
JSON_PATH_DIR="material/json"

QUESTIONS_DIR = "material/questions"
SOURCES_DIR = "material/sources"

# Form customization
QUIZ_INSTRUCTIONS = """
Instructions:
- Read each question carefully
- Select the best answer from the given options
- You will receive your score and explanations after submission
- Each question is worth 1 point
"""

# Date formats for form titles
DATE_FORMAT = "%d-%m-%Y"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M"
