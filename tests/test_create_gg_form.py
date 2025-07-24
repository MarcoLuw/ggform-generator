#!/usr/bin/env python3
"""
Test script to validate JSON question files and test form creation.
"""

import os
import json
import sys
from pathlib import Path


def validate_question_format(question_data, index):
    """Validate a single question's format."""
    errors = []
    
    # Check required fields
    required_fields = ['question', 'options', 'correct_option', 'explanation']
    for field in required_fields:
        if field not in question_data:
            errors.append(f"Missing required field: {field}")
    
    # Check options format
    if 'options' in question_data:
        options = question_data['options']
        required_options = ['option-1', 'option-2', 'option-3', 'option-4']
        
        for opt in required_options:
            if opt not in options:
                errors.append(f"Missing option: {opt}")
            elif not isinstance(options[opt], str) or not options[opt].strip():
                errors.append(f"Empty or invalid option: {opt}")
    
    # Check correct_option
    if 'correct_option' in question_data:
        correct_opt = question_data['correct_option']
        if correct_opt not in ['option-1', 'option-2', 'option-3', 'option-4']:
            errors.append(f"Invalid correct_option: {correct_opt}")
    
    # Check question text
    if 'question' in question_data:
        if not isinstance(question_data['question'], str) or not question_data['question'].strip():
            errors.append("Question text is empty or invalid")
    
    # Check explanation
    if 'explanation' in question_data:
        if not isinstance(question_data['explanation'], str) or not question_data['explanation'].strip():
            errors.append("Explanation is empty or invalid")
    
    return errors


def validate_json_file(file_path):
    """Validate a JSON file containing questions."""
    print(f"🔍 Validating: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    if not isinstance(data, list):
        print(f"❌ Root element must be a list of questions")
        return False
    
    if len(data) == 0:
        print(f"❌ No questions found in file")
        return False
    
    print(f"📊 Found {len(data)} questions")
    
    all_valid = True
    for i, question in enumerate(data, 1):
        errors = validate_question_format(question, i)
        if errors:
            print(f"❌ Question {i} errors:")
            for error in errors:
                print(f"   - {error}")
            all_valid = False
        else:
            print(f"✅ Question {i}: Valid")
    
    if all_valid:
        print(f"✅ File validation passed!")
    else:
        print(f"❌ File validation failed!")
    
    return all_valid


def test_sample_questions():
    """Test with sample question data."""
    print("🧪 Testing with sample question data...\n")
    
    sample_questions = [
        {
            "question": "What is the capital of France?",
            "options": {
                "option-1": "London",
                "option-2": "Berlin", 
                "option-3": "Paris",
                "option-4": "Madrid"
            },
            "correct_option": "option-3",
            "explanation": "Paris is the capital city of France, known for landmarks like the Eiffel Tower."
        },
        {
            "question": "Which programming language is this project written in?",
            "options": {
                "option-1": "Java",
                "option-2": "Python",
                "option-3": "JavaScript", 
                "option-4": "C++"
            },
            "correct_option": "option-2",
            "explanation": "This MCQ form generator is written in Python, using Google Forms API."
        }
    ]
    
    # Test validation
    for i, question in enumerate(sample_questions, 1):
        errors = validate_question_format(question, i)
        if errors:
            print(f"❌ Sample question {i} has errors:")
            for error in errors:
                print(f"   - {error}")
        else:
            print(f"✅ Sample question {i}: Valid")
    
    # Create temporary file and test form creation
    temp_file = "temp_test_questions.json"
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(sample_questions, f, indent=2, ensure_ascii=False)
        
        print(f"\n📝 Created temporary test file: {temp_file}")
        print("🚀 To test form creation, run:")
        print(f"   python main.py {temp_file} --title 'Test Quiz'")
        
    except Exception as e:
        print(f"❌ Error creating test file: {e}")
    finally:
        # Clean up
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print(f"🧹 Cleaned up temporary file")
            except:
                pass


def main():
    """Main test function."""
    print("=== MCQ Form Generator Test Suite ===\n")
    
    # Test 1: Validate existing question files
    questions_dir = Path("material/questions")
    if questions_dir.exists():
        print("1️⃣ Testing existing question files...\n")
        
        json_files = list(questions_dir.rglob("*.json"))
        if json_files:
            for json_file in json_files[:3]:  # Test first 3 files
                validate_json_file(json_file)
                print()
        else:
            print("No JSON files found in questions directory")
    else:
        print("Questions directory not found, skipping file validation")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Test with sample data
    print("2️⃣ Testing with sample data...\n")
    test_sample_questions()
    
    print(f"\n🎉 Test suite completed!")


if __name__ == "__main__":
    main()
