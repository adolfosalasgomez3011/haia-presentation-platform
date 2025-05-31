import autogen
import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 AutoGen Google Support Test")
print("=" * 40)

print(f"📦 AutoGen version: {autogen.__version__}")

# Check if AutoGen has Google support
try:
    from autogen.oai import GoogleGenAIClient
    print("✅ GoogleGenAIClient found in AutoGen")
except ImportError as e:
    print(f"❌ GoogleGenAIClient not found in AutoGen: {e}")

# Check available OAI clients
try:
    from autogen import oai
    print(f"📋 Available OAI modules: {dir(oai)}")
except Exception as e:
    print(f"❌ Could not check OAI modules: {e}")

# Test Gemini API key
gemini_key = os.getenv("GEMINI_API_KEY")  # Changed from GOOGLE_API_KEY
if gemini_key:
    print(f"✅ Gemini API key present")
    print(f"🔑 API key starts with: {gemini_key[:10]}...")
    print(f"📏 API key length: {len(gemini_key)} characters")
else:
    print("❌ GEMINI_API_KEY not found in environment")

# Test OpenAI key (for comparison)
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    print(f"✅ OpenAI API key also present")
else:
    print("❌ OPENAI_API_KEY not found")

print("\n🧪 Testing Google configuration...")

# Test basic Google config
try:
    config = {
        "model": "gemini-1.5-pro",
        "api_key": gemini_key,  # Changed from google_key
        "api_type": "google"
    }
    print("✅ Config dictionary created successfully")
    
    # Try to create a simple agent with Google config
    from autogen import ConversableAgent
    test_agent = ConversableAgent(
        name="test",
        llm_config={"config_list": [config]},
        human_input_mode="NEVER"
    )
    print("✅ Test agent created successfully")
    
except Exception as e:
    print(f"❌ Config test failed: {e}")
    print(f"❌ Error type: {type(e)}")

print("\n" + "=" * 40)
print("Test completed!")