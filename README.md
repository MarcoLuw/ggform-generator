# Google Forms MCQ Generator

This project creates Google Forms multiple-choice quizzes from JSON question data with automatic assessment and scoring capabilities. It includes utilities for processing vocabulary data from CSV files and generating questions via LLM prompts.

## Features

- ✅ **Automated MCQ Form Creation**: Convert JSON question files to Google Forms
- 📊 **Assessment & Scoring**: Automatic grading with point values
- 💡 **Explanations**: Detailed feedback shown after form submission
- 🔄 **Batch Processing**: Handle multiple question files at once
- 📝 **CSV to JSON Processing**: Convert vocabulary CSV files to organized JSON format
- 📅 **Date-based Organization**: Automatically organize vocabulary by date
- 🤖 **LLM Question Generation**: Generate MCQ questions using AI prompts
- 🎯 **IELTS Ready**: Designed for IELTS vocabulary and reading comprehension

## Prerequisites

1. **Google Cloud Project**: Set up a Google Cloud project with Forms API enabled
2. **OAuth Credentials**: Download `credentials.json` from Google Cloud Console
3. **Python 3.12+**: Required for the application
4. **LLM Access**: ChatGPT, Claude, or other LLM for question generation (optional)

## Installation

1. **Clone/Download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Forms API**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the Google Forms API
   - Create OAuth 2.0 credentials (Desktop application)
   - Download the credentials and save as `credentials.json` in the project root

## Complete Workflow

### Step 1: Process CSV Data to JSON

The `data_handler.py` module processes vocabulary data from CSV files into organized JSON files.

#### CSV File Requirements

Your CSV file must contain the following columns (case-sensitive):

| Column Name | Required | Description | Example |
|-------------|----------|-------------|---------|
| `Vocabulary` | Yes | The vocabulary word/phrase | "procrastination" |
| `Meaning` | No | Definition of the word | "delaying or postponing tasks" |
| `Collocation` | No | Common word combinations | "chronic procrastination" |
| `Context` | No | Example sentence or usage context | "His procrastination led to missed deadlines" |
| `IPA` | No | International Phonetic Alphabet notation | "/proʊˌkræs.tɪˈneɪ.ʃən/" |
| `Time` | No | Date when the vocabulary was noted | "05/07/2025" |

#### Sample CSV Format

```csv
Vocabulary,Meaning,Collocation,Context,IPA,Time
procrastination,delaying or postponing tasks,chronic procrastination,His procrastination led to missed deadlines,/proʊˌkræs.tɪˈneɪ.ʃən/,05/07/2025
vibrant,energetic and exciting,vibrant city,The vibrant city attracted many tourists,,09/07/2025
supplement,add to make larger or better,supplement income,She supplements her income with freelance work,/ˈsʌp.lə.ment/,05/07/2025
```

#### Process CSV Data

```bash
# Process CSV to JSON files organized by date
python utils/data_handler.py
```

This creates structured JSON files in `material/sources/` organized by date:

```
material/sources/
├── 05-07-2025/
│   ├── 1.json (first 20 vocabulary entries)
│   ├── 2.json (next 20 vocabulary entries)
│   └── ...
├── 09-07-2025/
│   ├── 1.json
│   └── ...
```

### Step 2: Generate Questions with LLM

#### Copy Vocabulary Data for LLM Prompt

1. **Copy JSON content**: Take the content from any generated JSON file (e.g., `material/sources/05-07-2025/1.json`)

2. **Open prompt template**: Navigate to `docs/questionGeneratedPrompt.md`

3. **Paste vocabulary data**: Replace the placeholder content with your vocabulary JSON data

4. **Use the prompt**: Copy the entire prompt content and paste it into your preferred LLM (ChatGPT, Claude, etc.)

#### Example LLM Prompt Usage

```markdown
# docs/questionGeneratedPrompt.md

You're a senior English teacher, do the tasks listed in Task section

User prompt:
- I have a vocabulary list in JSON format

Task:
- Provide a context which contains the list of english vocabulary which is noted in a json format
- Generate MCQs based on the content from the attached context

[PASTE YOUR VOCABULARY JSON HERE]

Instruction:
- Read the content, generate the MCQs based on it
- If there are any words which are not eligible to make a question, bypass them
- You can provide more information to enrich the MCQs, such as meanings, context (example to use the word), so on
- The final objective of question bank is to make the words more understandable, effectively know how to use it, and impressive to remember

Output Format:
- A json with questions with 4 answers, including 1 correct answer
```

#### Save LLM Generated Questions

1. **Get LLM Response**: The LLM will generate MCQ questions in JSON format
2. **Save to Questions Folder**: Copy the generated JSON and save it to `material/questions/` or any location you prefer
3. **Organize by Date**: Recommended to organize questions by date for better management

Example question file structure:
```
material/questions/
├── 05-07-2025/
│   ├── vocabulary_quiz_1.json
│   ├── vocabulary_quiz_2.json
└── 09-07-2025/
    ├── vocabulary_quiz_1.json
```

### Step 3: Create Google Forms

#### Basic Usage

```bash
# Create form from specific JSON question file
python main.py material/questions/05-07-2025/vocabulary_quiz_1.json

# Create form with custom title
python main.py material/questions/05-07-2025/vocabulary_quiz_1.json --title "IELTS Vocabulary Quiz"

# Create form with title and description
python main.py path/to/your/questions.json --title "Reading Test" --description "Test your comprehension skills"
```

#### Direct Python Usage

```python
from main import MCQFormGenerator

generator = MCQFormGenerator()
result = generator.create_mcq_form_from_json(
    json_file_path="material/questions/05-07-2025/vocabulary_quiz_1.json",
    form_title="My Quiz",
    form_description="Quiz description"
)

print(f"Form URL: {result['response_url']}")
```

## Data Formats

### Vocabulary JSON (from data_handler)

```json
[
    {
        "Vocabulary": "procrastination",
        "Meaning": "delaying or postponing tasks",
        "Collocation": "chronic procrastination",
        "Context": "His procrastination led to missed deadlines",
        "IPA": "/proʊˌkræs.tɪˈneɪ.ʃən/",
        "Time": "05/07/2025"
    }
]
```

### Question JSON (from LLM)

Your question files should follow this structure:

```json
[
  {
    "question": "What does 'procrastination' mean in the context: 'His procrastination led to missed deadlines'?",
    "options": {
      "option-1": "Working very quickly and efficiently",
      "option-2": "Delaying or postponing something you need to do",
      "option-3": "Doing multiple tasks at the same time",
      "option-4": "Planning carefully before starting work"
    },
    "correct_option": "option-2",
    "explanation": "Procrastination means delaying or postponing something you need to do, often until the last minute."
  }
]
```

#### Required Fields:
- `question`: The question text
- `options`: Object with option-1, option-2, option-3, option-4
- `correct_option`: The key of the correct option (e.g., "option-2")
- `explanation`: Feedback text shown after submission

## File Structure

```
ggform-generator/
├── main.py                         # Main application script
├── requirements.txt                # Python dependencies
├── run.bat                         # Windows batch script for easy execution
├── config/
│   ├── config.py                  # Application configuration
│   └── settings.yaml              # YAML settings file
├── core/
│   ├── __init__.py
│   └── config.py                  # Core configuration module
├── creds/
│   ├── credentials.json           # Google OAuth credentials (you provide)
│   └── token.json                 # Auto-generated auth token
├── docs/
│   ├── setup.md                   # Setup documentation
│   └── questionGeneratedPrompt.md # LLM prompt template for question generation
├── tests/
│   └── test_create_gg_form.py     # Test scripts
├── utils/
│   ├── __init__.py
│   ├── gg_form_api.py             # Google Forms API wrapper
│   └── data_handler.py            # CSV to JSON processing
├── material/
│   ├── Road to Ielts Again - Reading.csv  # Source vocabulary CSV
│   ├── questions/                 # Generated MCQ questions (from LLM)
│   │   ├── 05-07-2025/
│   │   ├── 09-07-2025/
│   │   └── ...
│   └── sources/                   # Processed JSON vocabulary (from data_handler)
│       ├── 05-07-2025/
│       ├── 09-07-2025/
│       └── ...
```

## Detailed Workflow Example

### Complete End-to-End Process

1. **Prepare Your Data**:
   ```bash
   # Place your vocabulary CSV in material/
   # Configure CSV_FILE_PATH in config/config.py
   ```

2. **Process CSV to JSON**:
   ```bash
   python utils/data_handler.py
   # Output: material/sources/[date]/1.json, 2.json, etc.
   ```

3. **Generate Questions with LLM**:
   ```bash
   # Copy content from material/sources/05-07-2025/1.json
   # Paste into docs/questionGeneratedPrompt.md
   # Copy the full prompt to ChatGPT/Claude
   # Save LLM response as material/questions/05-07-2025/quiz1.json
   ```

4. **Create Google Forms**:
   ```bash
   python main.py material/questions/05-07-2025/quiz1.json --title "IELTS Vocabulary Quiz"
   ```

5. **Share and Use**:
   ```
   Form created successfully!
   Response URL: https://docs.google.com/forms/d/e/1FAIpQL.../viewform
   ```

## Assessment Features

The generated forms include:

1. **Automatic Scoring**: Each question worth 1 point
2. **Immediate Feedback**: Explanations shown after submission
3. **Quiz Mode**: Proper Google Forms quiz configuration
4. **Correct Answer Revelation**: Students see correct answers after submission

## Authentication Flow

1. **First Run**: Browser opens for Google OAuth consent
2. **Token Storage**: `token.json` created automatically
3. **Subsequent Runs**: Uses stored token (no browser needed)

## Error Handling

The application handles:
- ❌ Missing credentials files
- ❌ Invalid JSON format
- ❌ Network connection issues  
- ❌ Google API errors
- ❌ Invalid question data
- ❌ CSV parsing errors
- ❌ Missing vocabulary fields

## Command Line Options

```bash
# Data processing
python utils/data_handler.py

# Form generation
python main.py <json_file> [options]

Arguments:
  json_file              Path to JSON questions file

Options:
  --title, -t           Custom form title
  --description, -d     Form description
  --help, -h           Show help message
```

## Example Output

```
=== DATA PROCESSING ===
Loaded 150 vocabulary entries
Processing complete! Generated JSON files for 150 vocabulary entries.

=== LLM QUESTION GENERATION ===
1. Copy vocabulary from: material/sources/05-07-2025/1.json
2. Use prompt in: docs/questionGeneratedPrompt.md
3. Save LLM output to: material/questions/05-07-2025/quiz1.json

=== FORM CREATION SUMMARY ===
Form Title: IELTS Vocabulary Quiz
Questions Added: 20/20
Form ID: 1a2b3c4d5e6f7g8h9i0j
Edit URL: https://docs.google.com/forms/d/1a2b3c4d5e6f7g8h9i0j/edit
Response URL: https://docs.google.com/forms/d/e/1FAIpQL.../viewform
Assessment: Enabled with explanations after submission
```

## Troubleshooting

### Common Issues:

1. **"credentials.json not found"**
   - Download OAuth credentials from Google Cloud Console
   - Place file in project root directory

2. **"Permission denied" errors**
   - Ensure Google Forms API is enabled in your Google Cloud project
   - Check OAuth scopes in credentials

3. **"Invalid JSON" errors**
   - Validate your question JSON files from LLM
   - Ensure all required fields are present
   - Check JSON syntax with online validators

4. **CSV processing errors**
   - Check CSV file format and column headers
   - Ensure `Vocabulary` column contains data

5. **LLM prompt issues**
   - Make sure to copy the complete vocabulary JSON data
   - Use the exact prompt format from `docs/questionGeneratedPrompt.md`
   - Verify LLM response matches the required JSON structure

6. **Network/API errors**
   - Check internet connection
   - Verify Google Cloud project is active

## Tips for Better Results

### For LLM Question Generation:
- Process vocabulary in smaller chunks (20 entries max) for better LLM responses
- Review and edit LLM-generated questions before creating forms
- Save different question sets for the same vocabulary to create multiple quizzes
- Use specific prompts for different question types (meaning, usage, context, etc.)

### For Google Forms:
- Use descriptive titles and descriptions for better student engagement
- Test forms before sharing with students
- Consider creating multiple shorter quizzes rather than one long quiz

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

This project is for educational purposes. Follow Google's Terms of Service for Forms API usage.

---

**Happy Quiz Creating! 🎉**