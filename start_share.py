from pyngrok import ngrok
import time

# Basic config - works best if user adds a token later
# ngrok.set_auth_token("YOUR_TOKEN") 

try:
    # Open a HTTP tunnel on the default port 8000
    public_url = ngrok.connect(8000).public_url
    print("\n" + "="*50)
    print(f"  👉 YOUR PUBLIC LINK: {public_url}")
    print("="*50 + "\n")
    print("Keep this script running to keep the link active!")
    
    # Keep the script running
    while True:
        time.sleep(1)
except Exception as e:
    print(f"Error starting ngrok: {e}")
    print("\nNOTE: If you see an error about 'auth token', you need to sign up at ngrok.com (free) and run:")
    print("ngrok config add-authtoken <YOUR_TOKEN>")
