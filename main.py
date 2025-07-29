"""
Main script to create Google Forms MCQ quizzes with assessment and scoring.
This script leverages gg_form_api.py to create forms from JSON question data.
"""

import os
import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.gg_form_api import get_credentials, SERVICE_ENDPOINT
import requests

# Import configuration
try:
    from config.config import *
except ImportError:
    # Fallback configuration if config.py is not found
    POINTS_PER_QUESTION = 1
    ENABLE_IMMEDIATE_FEEDBACK = True
    SHOW_CORRECT_ANSWERS = True
    COLLECT_EMAIL_ADDRESSES = False
    REQUEST_TIMEOUT = 30
    DEFAULT_FORM_DESCRIPTION = "Complete this quiz and receive immediate feedback with explanations."


class MCQFormGenerator:
    def __init__(self):
        self.credentials = None
        self.headers = None
        
    def authenticate(self):
        """Authenticate and set up headers for API requests."""
        self.credentials = get_credentials()
        self.headers = {
            'Authorization': f'Bearer {self.credentials.token}',
            'Content-Type': 'application/json'
        }
        
    def load_questions(self, json_file_path):
        """Load questions from JSON file."""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                questions = json.load(f)
            print(f"Loaded {len(questions)} questions from {json_file_path}")
            return questions
        except FileNotFoundError:
            print(f"Error: Question file {json_file_path} not found.")
            return []
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {json_file_path}: {e}")
            return []
    
    def create_quiz_form(self, title, description=""):
        """Create a new Google Form configured as a quiz."""
        # Step 1: Create basic form with title only
        form_data = {
            "info": {
                "title": title
            }
        }
        
        try:
            response = requests.post(f'{SERVICE_ENDPOINT}/v1/forms', 
                                   headers=self.headers, 
                                   json=form_data,
                                   timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            form = response.json()
            form_id = form['formId']
            
            # Step 2: Update form with description and quiz settings if needed
            if description:
                update_data = {
                    "requests": [{
                        "updateFormInfo": {
                            "info": {
                                "description": description
                            },
                            "updateMask": "description"
                        }
                    }]
                }
                
                update_response = requests.post(
                    f'{SERVICE_ENDPOINT}/v1/forms/{form_id}:batchUpdate',
                    headers=self.headers,
                    json=update_data,
                    timeout=REQUEST_TIMEOUT
                )
                update_response.raise_for_status()
            
            print(f"Quiz form created successfully!")
            print(f"Form ID: {form['formId']}")
            print(f"Edit URL: https://docs.google.com/forms/d/{form['formId']}/edit")
            print(f"Response URL: {form['responderUri']}")
            return form
        except requests.exceptions.RequestException as e:
            print(f"Error creating form: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None
    
    def convert_option_key_to_index(self, option_key):
        """Convert option key (option-1, option-2, etc.) to zero-based index."""
        try:
            return int(option_key.split('-')[1]) - 1
        except (IndexError, ValueError):
            return 0
    
    def add_all_questions_batch(self, form_id, questions):
        """Add all questions in a single batch request to avoid index conflicts."""
        # Prepare all question requests
        requests_list = []
        
        for i, question_data in enumerate(questions):
            # Prepare options for Google Forms
            options = []
            correct_option_index = None
            
            # Convert options to list format expected by Google Forms
            for key in ['option-1', 'option-2', 'option-3', 'option-4']:
                if key in question_data['options']:
                    options.append({"value": question_data['options'][key]})
                    
                    # Check if this is the correct option
                    if key == question_data['correct_option']:
                        correct_option_index = len(options) - 1
            
            # Create question request
            question_request = {
                "createItem": {
                    "item": {
                        "title": question_data['question'],
                        "description": "",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "grading": {
                                    "pointValue": POINTS_PER_QUESTION,
                                    "correctAnswers": {
                                        "answers": [{"value": options[correct_option_index]["value"]}]
                                    },
                                    "whenRight": {
                                        "text": "Correct! " + question_data.get('explanation', 'Well done!')
                                    },
                                    "whenWrong": {
                                        "text": question_data.get('explanation', 'Please review the explanation.')
                                    }
                                },
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": options
                                }
                            }
                        }
                    },
                    "location": {"index": i}
                }
            }
            requests_list.append(question_request)
        
        # Send all questions in one batch
        batch_data = {"requests": requests_list}
        
        try:
            response = requests.post(
                f'{SERVICE_ENDPOINT}/v1/forms/{form_id}:batchUpdate',
                headers=self.headers,
                json=batch_data,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            print(f"Successfully added all {len(questions)} questions in batch!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error adding questions in batch: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return False

    def add_mcq_question(self, form_id, question_data, question_index):
        """Add a multiple choice question to the form with correct answer and feedback."""
        # Prepare options for Google Forms
        options = []
        correct_option_index = None
        
        # Convert options to list format expected by Google Forms
        for key in ['option-1', 'option-2', 'option-3', 'option-4']:
            if key in question_data['options']:
                options.append({"value": question_data['options'][key]})
                
                # Check if this is the correct option
                if key == question_data['correct_option']:
                    correct_option_index = len(options) - 1
        
        # Create the question item
        question_item = {
            "requests": [{
                "createItem": {
                    "item": {
                        "title": question_data['question'],
                        "description": "",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "grading": {
                                    "pointValue": POINTS_PER_QUESTION,
                                    "correctAnswers": {
                                        "answers": [{"value": options[correct_option_index]["value"]}]
                                    },
                                    "whenRight": {
                                        "text": "Correct! " + question_data.get('explanation', 'Well done!')
                                    },
                                    "whenWrong": {
                                        "text": question_data.get('explanation', 'Please review the explanation.')
                                    }
                                },
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": options
                                }
                            }
                        }
                    },
                    "location": {"index": question_index}
                }
            }]
        }
        
        try:
            response = requests.post(
                f'{SERVICE_ENDPOINT}/v1/forms/{form_id}:batchUpdate',
                headers=self.headers,
                json=question_item,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            print(f"Added question {question_index + 1}: {question_data['question'][:50]}...")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error adding question {question_index + 1}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return False
    
    def configure_quiz_settings(self, form_id):
        """Configure quiz settings for assessment and feedback."""
        settings_update = {
            "requests": [{
                "updateSettings": {
                    "settings": {
                        "quizSettings": {
                            "isQuiz": True
                        }
                    },
                    "updateMask": "quizSettings.isQuiz"
                }
            }]
        }
        
        try:
            response = requests.post(
                f'{SERVICE_ENDPOINT}/v1/forms/{form_id}:batchUpdate',
                headers=self.headers,
                json=settings_update,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            print("Quiz settings configured successfully!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error configuring quiz settings: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return False
    
    def create_mcq_form_from_json(self, json_file_path, form_title=None, form_description=""):
        """Main method to create a complete MCQ form from JSON data."""
        # Authenticate
        self.authenticate()
        if not self.credentials:
            print("Authentication failed!")
            return None
        
        # Load questions
        questions = self.load_questions(json_file_path)
        if not questions:
            return None
        
        # Generate form title if not provided
        if not form_title:
            filename = Path(json_file_path).stem
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            form_title = f"MCQ Quiz - {filename} ({timestamp})"
        
        # Create the form
        form = self.create_quiz_form(form_title, form_description)
        if not form:
            return None
        
        form_id = form['formId']
        
        # Configure quiz settings FIRST (before adding questions with grading)
        print("Configuring quiz settings...")
        if not self.configure_quiz_settings(form_id):
            print("Warning: Failed to configure quiz settings")
        
        # Add all questions in batch to avoid index conflicts
        print(f"Adding {len(questions)} questions in batch...")
        if self.add_all_questions_batch(form_id, questions):
            success_count = len(questions)
            print(f"Successfully added all {success_count} questions!")
        else:
            success_count = 0
            print("Failed to add questions. Trying individual approach as fallback...")
            
            # Fallback: Add questions one by one
            for i, question_data in enumerate(questions):
                if self.add_mcq_question(form_id, question_data, i):
                    success_count += 1
        
        # Quiz settings already configured above
        
        print(f"\n=== FORM CREATION SUMMARY ===")
        print(f"Form Title: {form_title}")
        print(f"Questions Added: {success_count}/{len(questions)}")
        print(f"Form ID: {form_id}")
        print(f"Edit URL: https://docs.google.com/forms/d/{form_id}/edit")
        print(f"Response URL: {form['responderUri']}")
        print(f"Assessment: Enabled with explanations after submission")
        
        return {
            'form_id': form_id,
            'edit_url': f"https://docs.google.com/forms/d/{form_id}/edit",
            'response_url': form['responderUri'],
            'questions_added': success_count,
            'total_questions': len(questions)
        }
    
    def create_combined_mcq_form_from_multiple_json(self, json_file_paths, form_title=None, form_description=""):
        """Create a single MCQ form combining questions from multiple JSON files."""
        # Authenticate
        self.authenticate()
        if not self.credentials:
            print("Authentication failed!")
            return None
        
        # Load and combine all questions
        combined_questions = []
        file_info = []
        
        for json_file_path in json_file_paths:
            questions = self.load_questions(json_file_path)
            if questions:
                combined_questions.extend(questions)
                filename = Path(json_file_path).stem
                file_info.append(f"{filename} ({len(questions)} questions)")
            else:
                print(f"Warning: No questions loaded from {json_file_path}")
        
        if not combined_questions:
            print("No questions found in any of the provided files!")
            return None
        
        # Generate form title if not provided
        if not form_title:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            form_title = f"Combined MCQ Quiz ({len(json_file_paths)} files, {len(combined_questions)} questions) - {timestamp}"
        
        # Add file info to description
        files_summary = "Sources: " + " | ".join(file_info)
        if form_description:
            form_description = f"{form_description}\n\n{files_summary}"
        else:
            form_description = files_summary
        
        # Create the form
        form = self.create_quiz_form(form_title, form_description)
        if not form:
            return None
        
        form_id = form['formId']
        
        # Configure quiz settings
        print("Configuring quiz settings...")
        if not self.configure_quiz_settings(form_id):
            print("Warning: Failed to configure quiz settings")
        
        # Add all questions in batch
        print(f"Adding {len(combined_questions)} questions from {len(json_file_paths)} files in batch...")
        if self.add_all_questions_batch(form_id, combined_questions):
            success_count = len(combined_questions)
            print(f"Successfully added all {success_count} questions!")
        else:
            success_count = 0
            print("Failed to add questions. Trying individual approach as fallback...")
            
            # Fallback: Add questions one by one
            for i, question_data in enumerate(combined_questions):
                if self.add_mcq_question(form_id, question_data, i):
                    success_count += 1
        
        print(f"\n=== COMBINED FORM CREATION SUMMARY ===")
        print(f"Form Title: {form_title}")
        print(f"Source Files: {len(json_file_paths)}")
        for i, file_path in enumerate(json_file_paths, 1):
            print(f"  {i}. {file_path}")
        print(f"Questions Added: {success_count}/{len(combined_questions)}")
        print(f"Form ID: {form_id}")
        print(f"Edit URL: https://docs.google.com/forms/d/{form_id}/edit")
        print(f"Response URL: {form['responderUri']}")
        print(f"Assessment: Enabled with explanations after submission")
        
        return {
            'form_id': form_id,
            'edit_url': f"https://docs.google.com/forms/d/{form_id}/edit",
            'response_url': form['responderUri'],
            'questions_added': success_count,
            'total_questions': len(combined_questions),
            'source_files': json_file_paths
        }


def main():
    """Main function to handle command line arguments and create forms."""
    parser = argparse.ArgumentParser(description='Create a single Google Forms MCQ quiz from one or multiple JSON data files')
    parser.add_argument('json_files', nargs='?', help='Path(s) to JSON file(s) containing questions. Use comma-separated for multiple files: file1.json,file2.json')
    parser.add_argument('--title', '-t', help='Form title (optional)')
    parser.add_argument('--description', '-d', default='', help='Form description (optional)')
    parser.add_argument('--directory', '-r', help='Directory path containing JSON files. All JSON files in the directory will be combined into one form')
    
    args = parser.parse_args()
    
    # Check if either json_files or directory is provided
    if not args.json_files and not args.directory:
        print("Error: You must provide either JSON files or a directory path.")
        print("Usage examples:")
        print("  python main.py file1.json,file2.json")
        print("  python main.py -r /path/to/directory")
        return 1
    
    # If directory is provided, get all JSON files from it
    if args.directory:
        if not os.path.exists(args.directory):
            print(f"Error: Directory '{args.directory}' does not exist.")
            return 1
        
        if not os.path.isdir(args.directory):
            print(f"Error: '{args.directory}' is not a directory.")
            return 1
        
        # Find all JSON files in the directory
        json_files_in_dir = []
        for file in os.listdir(args.directory):
            if file.lower().endswith('.json'):
                json_files_in_dir.append(os.path.join(args.directory, file))
        
        if not json_files_in_dir:
            print(f"Error: No JSON files found in directory '{args.directory}'.")
            return 1
        
        # Sort files for consistent ordering
        json_file_paths = sorted(json_files_in_dir)
        print(f"Found {len(json_file_paths)} JSON files in directory '{args.directory}':")
        for i, file_path in enumerate(json_file_paths, 1):
            print(f"  {i}. {os.path.basename(file_path)}")
        
    else:
        # Parse multiple file paths from command line argument
        json_file_paths = [path.strip() for path in args.json_files.split(',')]
    
    # Validate all JSON file paths
    missing_files = []
    for file_path in json_file_paths:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"Error: The following files do not exist:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return 1
    
    # Create form generator
    generator = MCQFormGenerator()
    
    total_files = len(json_file_paths)
    
    if total_files == 1:
        # Single file - use the single file method
        print(f"Creating form from single file: {json_file_paths[0]}")
        
        result = generator.create_mcq_form_from_json(
            json_file_path=json_file_paths[0],
            form_title=args.title,
            form_description=args.description
        )
    else:
        # Multiple files - combine into one form
        if args.directory:
            print(f"Combining {total_files} JSON files from directory '{args.directory}' into one form...")
        else:
            print(f"Combining {total_files} files into one form...")
        
        result = generator.create_combined_mcq_form_from_multiple_json(
            json_file_paths=json_file_paths,
            form_title=args.title,
            form_description=args.description
        )
    
    if result:
        print(f"\n✅ Form created successfully!")
        return 0
    else:
        print(f"\n❌ Form creation failed!")
        return 1


if __name__ == "__main__":
    # Example usage without command line args
    if len(sys.argv) == 1:
        print("=== MCQ Form Generator ===")
        print("\nUsage examples:")
        print("python main.py material/questions/05-07-2025/1.json")
        print("python main.py material/questions/05-07-2025/1.json,material/questions/05-07-2025/2.json")
        print("python main.py material/questions/05-07-2025/1.json --title 'IELTS Reading Quiz'")
        print("python main.py file1.json,file2.json,file3.json --title 'Combined Quiz' --description 'Test your knowledge'")
        print("python main.py -r material/questions/05-07-2025/ --title 'Directory Quiz'")
        print("python main.py --directory material/questions/05-07-2025/")
        
        # For demonstration, use the provided file
        default_file = "material/questions/05-07-2025/1.json"
        if os.path.exists(default_file):
            print(f"\n🔄 Creating form using default file: {default_file}")
            generator = MCQFormGenerator()
            result = generator.create_mcq_form_from_json(
                json_file_path=default_file,
                form_title="IELTS Vocabulary Quiz",
                form_description="Test your English vocabulary knowledge with this comprehensive quiz. You'll receive immediate feedback and explanations after submission."
            )
        else:
            print(f"\n❌ Default file {default_file} not found!")
    else:
        sys.exit(main())
