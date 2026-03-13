#!/usr/bin/env python3
"""
Aegis System Diagnostic Test
Tests all components to identify issues preventing the system from running.
"""

import sys
import os
from pathlib import Path

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def test_python_version():
    """Test Python version."""
    print_header("1. Python Version Check")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 9:
        print_success("Python version is compatible (3.9+)")
        return True
    else:
        print_error(f"Python 3.9+ required, found {version.major}.{version.minor}")
        return False

def test_dependencies():
    """Test if required dependencies are installed."""
    print_header("2. Dependency Check")
    
    required = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'pydantic': 'Pydantic',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'sklearn': 'Scikit-learn',
        'xgboost': 'XGBoost',
        'joblib': 'Joblib',
    }
    
    optional = {
        'tensorflow': 'TensorFlow (for deep learning models)',
        'boto3': 'Boto3 (for AWS integration)',
        'streamlit': 'Streamlit (for dashboard)',
    }
    
    all_installed = True
    
    print("\nRequired dependencies:")
    for module, name in required.items():
        try:
            __import__(module)
            print_success(f"{name} installed")
        except ImportError:
            print_error(f"{name} NOT installed")
            all_installed = False
    
    print("\nOptional dependencies:")
    for module, name in optional.items():
        try:
            __import__(module)
            print_success(f"{name} installed")
        except ImportError:
            print_warning(f"{name} not installed (optional)")
    
    return all_installed

def test_file_structure():
    """Test if required files and directories exist."""
    print_header("3. File Structure Check")
    
    required_paths = [
        'src/api/fastapi_app.py',
        'src/api/routers/gps.py',
        'src/api/routers/login.py',
        'src/api/routers/password.py',
        'src/api/routers/fraud.py',
        'src/api/routers/risk.py',
        'src/gps/score_gps.py',
        'src/login/score_login.py',
        'src/passwords/score_password.py',
        'src/fusion/risk_scoring.py',
        'requirements.txt',
    ]
    
    all_exist = True
    for path in required_paths:
        if Path(path).exists():
            print_success(f"{path}")
        else:
            print_error(f"{path} NOT FOUND")
            all_exist = False
    
    return all_exist

def test_model_files():
    """Test if model files exist."""
    print_header("4. Model Files Check")
    
    model_paths = [
        'models/gps/gps_isolation_forest.joblib',
        'models/gps/gps_gbm.joblib',
        'models/gps/gps_autoencoder.h5',
        'models/gps/gps_cnn_rnn.h5',
        'models/login/lanl_isolation_forest.joblib',
        'models/login/lanl_gbm_pseudo.joblib',
        'models/login/lanl_autoencoder.h5',
        'models/login/lanl_scaler.joblib',
        'models/login/lanl_meta.json',
    ]
    
    found = 0
    for path in model_paths:
        if Path(path).exists():
            print_success(f"{path}")
            found += 1
        else:
            print_warning(f"{path} not found (will use fallback)")
    
    print(f"\n{found}/{len(model_paths)} model files found")
    print_warning("Missing models will trigger rule-based fallbacks")
    return True  # Models are optional

def test_imports():
    """Test if core modules can be imported."""
    print_header("5. Module Import Check")
    
    modules_to_test = [
        ('src.api.fastapi_app', 'FastAPI App'),
        ('src.gps.score_gps', 'GPS Scoring'),
        ('src.login.score_login', 'Login Scoring'),
        ('src.passwords.score_password', 'Password Scoring'),
        ('src.fusion.risk_scoring', 'Risk Fusion'),
    ]
    
    all_imported = True
    
    # Add project root to path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    for module_path, name in modules_to_test:
        try:
            __import__(module_path)
            print_success(f"{name} ({module_path})")
        except Exception as e:
            print_error(f"{name} ({module_path}): {str(e)}")
            all_imported = False
    
    return all_imported

def test_routers():
    """Test if all routers can be imported."""
    print_header("6. Router Import Check")
    
    routers = [
        'src.api.routers.gps',
        'src.api.routers.login',
        'src.api.routers.password',
        'src.api.routers.fraud',
        'src.api.routers.risk',
    ]
    
    all_imported = True
    
    for router in routers:
        try:
            __import__(router)
            print_success(f"{router}")
        except Exception as e:
            print_error(f"{router}: {str(e)}")
            all_imported = False
    
    return all_imported

def test_frontend():
    """Test frontend setup."""
    print_header("7. Frontend Check")
    
    frontend_files = [
        'frontend/package.json',
        'frontend/app/page.tsx',
        'frontend/app/dashboard/page.tsx',
        'frontend/lib/api.ts',
        'frontend/lib/auth.ts',
    ]
    
    all_exist = True
    for path in frontend_files:
        if Path(path).exists():
            print_success(f"{path}")
        else:
            print_error(f"{path} NOT FOUND")
            all_exist = False
    
    # Check if node_modules exists
    if Path('frontend/node_modules').exists():
        print_success("Node modules installed")
    else:
        print_warning("Node modules not installed (run: cd frontend && npm install)")
    
    return all_exist

def main():
    """Run all tests."""
    print(f"\n{BLUE}🛡️  AEGIS SYSTEM DIAGNOSTIC TEST{RESET}")
    
    results = {
        'Python Version': test_python_version(),
        'Dependencies': test_dependencies(),
        'File Structure': test_file_structure(),
        'Model Files': test_model_files(),
        'Module Imports': test_imports(),
        'Router Imports': test_routers(),
        'Frontend': test_frontend(),
    }
    
    # Summary
    print_header("SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print_success("\n✓ All tests passed! System should be ready to run.")
        print("\nTo start the system:")
        print("  Backend:  python3 -m uvicorn src.api.fastapi_app:app --reload --port 8000")
        print("  Frontend: cd frontend && npm run dev")
    else:
        print_error("\n✗ Some tests failed. Fix the issues above before running.")
        print("\nQuick fixes:")
        if not results['Dependencies']:
            print("  1. Install dependencies: pip3 install -r requirements.txt")
        if not results['Frontend']:
            print("  2. Install frontend deps: cd frontend && npm install")
    
    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
