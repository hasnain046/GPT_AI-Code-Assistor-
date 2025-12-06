# GPT-4 API Setup Guide

## Step 1: Get Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to **API Keys** section
4. Click **"Create new secret key"**
5. Copy your API key (starts with `sk-`)

## Step 2: Configure the API Key

### Method 1: Edit config.py (Recommended)
```python
# In config.py, replace:
OPENAI_API_KEY = "sk-your-actual-api-key-here"
# With your real API key:
OPENAI_API_KEY = "sk-proj-abc123..."
```

### Method 2: Environment Variable
```bash
# Set environment variable
export OPENAI_API_KEY="sk-proj-abc123..."
```

## Step 3: Test the Connection

1. Start the backend:
```bash
python backend.py
```

2. Open the application in browser
3. Try the "Explain Code" or "Fix with GPT-4" features

## API Usage & Costs

- **GPT-4**: ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
- **GPT-4 Turbo**: ~$0.01 per 1K input tokens, ~$0.03 per 1K output tokens

## Troubleshooting

### "GPT-4 API key not configured"
- Check your API key in `config.py`
- Ensure it starts with `sk-`

### "GPT-4 API error: 401"
- Invalid API key
- Check if key is correct and active

### "GPT-4 API error: 429"
- Rate limit exceeded
- Wait and try again or upgrade plan

### "GPT-4 API timeout"
- Network issue or slow response
- Check internet connection

## Security Notes

- Never commit API keys to version control
- Add `config.py` to `.gitignore`
- Use environment variables in production
- Monitor API usage regularly