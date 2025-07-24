# Setup Guide for Google Forms MCQ Generator

## Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] Google Cloud account with billing enabled (free tier works)
- [ ] Google Forms API access

## Step-by-Step Setup

### 1. Google Cloud Setup

1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click "New Project" 
   - Enter project name (e.g., "MCQ Form Generator")
   - Click "Create"

2. **Enable Google Forms API**:
   - In your project, go to "APIs & Services" > "Library"
   - Search for "Google Forms API"
   - Click on it and press "ENABLE"

3. **Create OAuth Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - If prompted, configure OAuth consent screen first:
     - Choose "External" user type
     - Fill in app name and developer contact
     - Add your email to test users
   - For application type, select "Desktop application"
   - Give it a name (e.g., "MCQ Generator")
   - Click "Create"
   - Download the JSON file and save as `credentials.json` in project root

### 2. Project Setup

```bash
# 1. Navigate to project directory
cd ggform-generator

# 2. Create virtual environment (recommended)
python -m venv .venv

# 3. Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Copy environment template (optional)
copy .env.template .env
```

### 3. First Run

```bash
# Test the setup
python test.py

# Create your first form
python main.py material/questions/05-07-2025/1.json --title "My First Quiz"
```

### 4. Authentication Process

On first run:
1. Browser will open automatically
2. Sign in with Google account
3. Grant permissions to the app
4. `token.json` will be created automatically
5. Subsequent runs won't require browser authentication

## Troubleshooting Common Issues

### Error: "credentials.json not found"
- Download OAuth credentials from Google Cloud Console
- Ensure file is named exactly `credentials.json`
- Place in project root directory

### Error: "Google Forms API not enabled" 
- Go to Google Cloud Console
- Navigate to "APIs & Services" > "Library"
- Search and enable "Google Forms API"

### Error: "Access blocked: This app's request is invalid"
- Your OAuth consent screen needs to be properly configured
- Add your email to test users in OAuth consent screen
- Ensure redirect URI includes localhost

### Error: "Insufficient permissions"
- Check that your OAuth credentials have Forms API scope
- Re-download credentials if necessary

### Browser doesn't open for authentication
- Check firewall settings
- Try different port by modifying OAUTH_PORT in config
- Manually copy URL from terminal to browser

## Verification Steps

1. **Test API Connection**:
   ```bash
   python -c "from utils.gg_form_api import get_credentials; print('✅ Authentication works!' if get_credentials() else '❌ Authentication failed')"
   ```

2. **Validate Question Files**:
   ```bash
   python test.py
   ```

3. **Create Test Form**:
   ```bash
   python main.py material/questions/05-07-2025/1.json --title "Setup Test"
   ```

## File Structure Verification

```
ggform-generator/
├── credentials.json     ✅ (Your OAuth credentials)
├── token.json          ✅ (Auto-generated after first auth)
├── main.py             ✅ (Main application)
├── test.py             ✅ (Validation script)
├── requirements.txt    ✅ (Dependencies)
├── config.py           ✅ (Configuration)
└── utils/
    └── gg_form_api.py  ✅ (API wrapper)
```

## Success Indicators

- ✅ `python test.py` shows all validations pass
- ✅ First form creation shows URLs in terminal
- ✅ Form appears in your Google Drive
- ✅ Form functions as quiz with scoring
- ✅ Explanations appear after submission

## Need Help?

1. Run `python test.py` to diagnose issues
2. Check `credentials.json` exists and is valid JSON
3. Verify Google Forms API is enabled in your project
4. Ensure billing is enabled (free tier works)
5. Try deleting `token.json` and re-authenticating

---

**🎉 Once setup is complete, you're ready to create amazing MCQ forms!**
