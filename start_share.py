from pyngrok import ngrok
import time
import requests

# Basic config - works best if user adds a token later
# ngrok.set_auth_token("YOUR_TOKEN") 

def check_backend():
    try:
        response = requests.get("http://localhost:8000/stats", timeout=2)
        return response.status_code == 200
    except:
        return False

print("\n🚀 PREPARING LIVE SHARE LINK...")

if not check_backend():
    print("⚠️  WARNING: Backend server (run_app.bat) is NOT running.")
    print("👉 Please start 'run_app.bat' first, then run this script.")
    print("-" * 50)

try:
    # Open a HTTP tunnel on the default port 8000
    public_url = ngrok.connect(8000).public_url
    print("\n" + "="*60)
    print("  ✅ SUCCESS! YOUR APP IS NOW LIVE ON THE INTERNET")
    print(f"  🔗 LINK: {public_url}")
    print("="*60 + "\n")
    print("📢 INSTRUCTIONS FOR HACKATHON:")
    print("1. Keep this terminal open.")
    print("2. Keep the 'run_app.bat' terminal open.")
    print("3. Copy the link above and share it with the judges.")
    print("4. If you close this terminal, the link will stop working.")
    
    # Keep the script running
    while True:
        time.sleep(1)
except Exception as e:
    print(f"❌ Error starting ngrok: {e}")
    print("\n💡 TIP: If you haven't set up ngrok before, you need a free token:")
    print("1. Sign up at https://ngrok.com/ (Free)")
    print("2. Run: ngrok config add-authtoken <YOUR_TOKEN>")
