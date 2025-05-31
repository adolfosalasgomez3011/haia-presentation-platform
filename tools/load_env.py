import os

def load_env_file():
    """Load environment variables from .env file"""
    try:
        # Look for .env in parent folder (main project folder)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        env_path = os.path.join(parent_dir, '.env')
        
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if line and not line.startswith('#') and not line.startswith('//'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key] = value
            print(f"✅ Environment variables loaded from {env_path}")
            return True
        else:
            print(f"⚠️ .env file not found at {env_path}")
            return False
    except Exception as e:
        print(f"❌ Error loading .env file: {e}")
        return False

if __name__ == "__main__":
    load_env_file()
    print(f"FRED_API_KEY: {'Set' if os.getenv('FRED_API_KEY') else 'Not set'}")
    print(f"ALPHA_VANTAGE_KEY: {'Set' if os.getenv('ALPHA_VANTAGE_KEY') else 'Not set'}")
    print(f"OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")