# Secret Key Setup

## Security Warning
The `SECRET_KEY` in `settings.py` is now configured to use environment variables for security.

## Setup Instructions

### For Development (Quick Start)
The current setup will work with the fallback key, but it's **not secure for production**.

### For Production (Recommended)

1. **Generate a new secret key:**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Set it as an environment variable:**

   **Windows (PowerShell):**
   ```powershell
   $env:DJANGO_SECRET_KEY="your-generated-secret-key-here"
   ```

   **Windows (Command Prompt):**
   ```cmd
   set DJANGO_SECRET_KEY=your-generated-secret-key-here
   ```

   **Linux/Mac:**
   ```bash
   export DJANGO_SECRET_KEY="your-generated-secret-key-here"
   ```

3. **Or create a `.env` file** (recommended):
   - Create a `.env` file in the project root
   - Add: `DJANGO_SECRET_KEY=your-generated-secret-key-here`
   - Install `python-decouple` or use `python-dotenv` to load it automatically

## Current Configuration
The `settings.py` file now uses:
```python
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fallback-key-for-dev-only")
```

This means:
- ✅ It will use the environment variable if set
- ⚠️ Falls back to the insecure key only for development
- 🔒 **Never commit the actual secret key to git**

