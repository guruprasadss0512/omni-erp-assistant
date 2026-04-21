import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
ORG_ID = os.getenv("ZOHO_ORG_ID")

ACCOUNTS_URL = "https://accounts.zoho.in/oauth/v2/token"
API_BASE_URL = "https://www.zohoapis.in/inventory/v1"

def get_access_token():
    """Uses the Refresh Token to get a temporary Access Token."""
    payload = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token"
    }
    response = requests.post(ACCOUNTS_URL, data=payload)
    data = response.json()
    if "access_token" in data:
        return data["access_token"]
    else:
        raise Exception(f"Failed to get access token: {data}")

def get_inventory():
    """Fetches all items and their current stock levels."""
    access_token = get_access_token()
    url = f"{API_BASE_URL}/items"
    headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
    params = {"organization_id": ORG_ID}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        items = response.json().get("items", [])
        inventory_data = []
        for item in items:
            inventory_data.append({
                "item_name": item.get("name"),
                "sku": item.get("sku"),
                "stock_on_hand": item.get("stock_on_hand"),
                "item_id": item.get("item_id")
            })
        return inventory_data
    return None

def adjust_stock(item_id: str, quantity_change: int, reason: str = "Omni-ERP Assistant Update"):
    """Adjusts the stock level of an item by creating an Inventory Adjustment."""
    access_token = get_access_token()
    url = f"{API_BASE_URL}/inventoryadjustments"
    
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }
    
    params = {"organization_id": ORG_ID}
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    payload = {
        "adjustment_type": "quantity",
        "date": today,
        "reason": reason,
        "line_items": [
            {
                "item_id": item_id,
                "quantity_adjusted": quantity_change
            }
        ]
    }
    
    response = requests.post(url, headers=headers, params=params, json=payload)
    data = response.json()
    
    if data.get("code") == 0:  # Zoho returns code 0 for success
        return True
    else:
        print(f"Error adjusting stock: {data.get('message')}")
        return False

# --- TESTING BLOCK ---
if __name__ == "__main__":
    print("Testing Zoho ERP Integration (Read & Write)...")
    try:
        # 1. Read Current Stock
        inventory = get_inventory()
        target_item_id = None
        
        if inventory:
            print("\n✅ Current Inventory:")
            for item in inventory:
                print(f" - {item['item_name']} (SKU: {item['sku']}): {item['stock_on_hand']} in stock.")
                # Look for your specific book
                if item['sku'] == "TTP001":
                    target_item_id = item['item_id']
            
            # 2. Write (Adjust) Stock
            if target_item_id:
                print("\nInitiating stock adjustment: Deducting 2 units from TTP001...")
                # We pass -2 to reduce stock. Pass +2 to add stock.
                success = adjust_stock(target_item_id, -2)
                
                if success:
                    print("✅ Stock adjusted successfully in Zoho!")
                    
                    # 3. Verify the change
                    print("\nVerifying new stock level...")
                    updated_inventory = get_inventory()
                    for item in updated_inventory:
                        if item['sku'] == "TTP001":
                            print(f"🎉 New Stock Level for {item['item_name']}: {item['stock_on_hand']}")
            else:
                print("Could not find SKU: TTP001 to adjust.")
                
    except Exception as e:
        print(f"\n❌ ERROR: {e}")