import requests

# Change .in to .com if your account is not on the Indian data center
url = "https://accounts.zoho.in/oauth/v2/token"

payload = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "code": GRANT_TOKEN
}

response = requests.post(url, data=payload)
data = response.json()

if "refresh_token" in data:
    print("\n✅ SUCCESS! Here is your Refresh Token. Guard this with your life:")
    print(f"REFRESH_TOKEN={data['refresh_token']}\n")
    print("Add this to your .env file immediately.")
else:
    print("\n❌ Error generating token. Your Grant Token may have expired.")
    print(data)