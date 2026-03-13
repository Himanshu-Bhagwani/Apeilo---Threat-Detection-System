# TensorFlow Compatibility Fix

## Issue
TensorFlow 2.20.0 crashes on macOS with Python 3.9.6 (Abort trap: 6).

## Root Cause
- Python 3.9 is no longer officially supported by TensorFlow 2.20+
- macOS LibreSSL compatibility issues
- The system has graceful fallbacks, so TensorFlow is optional

## Solutions

### Option 1: Use Without TensorFlow (Recommended for Quick Start)
The system is designed to work without TensorFlow using rule-based fallbacks:

```bash
# Remove TensorFlow from requirements
pip uninstall tensorflow -y

# System will automatically use fallback models
./start_apelio.sh
```

**Impact**: GPS and Login deep learning models (Autoencoder, CNN-RNN) won't be available, but Isolation Forest and GBM models will still work with rule-based scoring.

### Option 2: Upgrade Python (Best Long-term Solution)
```bash
# Install Python 3.10+ using Homebrew
brew install python@3.10

# Create new virtual environment with Python 3.10
python3.10 -m venv .venv
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Start system
./start_aegis.sh
```

### Option 3: Use TensorFlow 2.13 (Compatible with Python 3.9)
```bash
# Edit requirements.txt
# Change: tensorflow>=2.13.0
# To:     tensorflow==2.13.1

# Reinstall
pip install tensorflow==2.13.1

# Start system
./start_aegis.sh
```

### Option 4: Make TensorFlow Truly Optional
Edit `requirements.txt` to make TensorFlow optional:

```txt
# Deep Learning (optional - system has fallbacks)
# tensorflow>=2.13.0  # Uncomment if you want deep learning models
```

## Current Status
✅ Core system works without TensorFlow
✅ Startup script updated to handle TensorFlow gracefully
✅ All ML models (Isolation Forest, GBM) work fine
⚠️ Deep learning models (Autoencoder, CNN-RNN) require TensorFlow

## Testing Without TensorFlow
```bash
# Test backend startup
python3 -m uvicorn src.api.fastapi_app:app --host 127.0.0.1 --port 8000

# Test GPS scoring (will use fallback)
curl -X POST http://localhost:8000/gps/score \
  -H "Content-Type: application/json" \
  -d '{"trajectory": [{"latitude": 37.7749, "longitude": -122.4194}]}'

# Test login scoring (will use fallback)
curl -X POST http://localhost:8000/login/score \
  -H "Content-Type: application/json" \
  -d '{"user_deg": 5, "comp_deg": 3}'
```

## Verification
The diagnostic test shows:
- ✅ Python 3.9.6 installed
- ✅ FastAPI, Uvicorn, scikit-learn, pandas, numpy working
- ✅ All model files present
- ✅ All routers import successfully
- ⚠️ TensorFlow crashes on import (non-critical)

## Recommendation
For immediate use: **Proceed without TensorFlow**. The system is fully functional with rule-based fallbacks and traditional ML models (Isolation Forest, GBM).

For production: **Upgrade to Python 3.10+** for full TensorFlow support.
