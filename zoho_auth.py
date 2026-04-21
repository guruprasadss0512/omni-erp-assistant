import requests

# Fill these in!
CLIENT_ID = "1000.19SS97YUP3Q6TVB2M8ROD6VTOGMG9F"
CLIENT_SECRET = "4e077a0f2075d85bcd5973aaa933342ed85d332db0"
GRANT_TOKEN = "1000.e48dbc7534ff32a0a7b0794383dfdcaa.2405c6b0fa4840f8741e1bc8b8111d66"
REDIRECT_URI = "http://localhost:8000/callback"

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