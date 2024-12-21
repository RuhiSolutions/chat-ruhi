from flask import Flask, request, jsonify
import pandas as pd
import requests
from io import BytesIO

app = Flask(__name__)

# Direct download link for your Google Sheet
GOOGLE_DRIVE_FILE_LINK = "https://docs.google.com/uc?id=1xumBvTyfwbXRZiS_vw7I3xy0LQv-rIyh&export=download"

def load_excel_from_drive():
    # Fetch the Google Sheet as a file
    response = requests.get(GOOGLE_DRIVE_FILE_LINK)
    if response.status_code == 200:
        # Read the file into a pandas DataFrame
        excel_data = pd.read_excel(BytesIO(response.content))
        return excel_data
    else:
        raise Exception("Failed to fetch the file from Google Drive.")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').strip()
    
    # Extract product code from the user's message
    product_code = user_message.upper()
    
    try:
        # Load the Excel data
        df = load_excel_from_drive()
        
        # Search for the product code
        product_info = df[df['Product Code'] == product_code]
        
        if not product_info.empty:
            response = {
                "Product Name": product_info.iloc[0]['Product Name'],
                "Stock": product_info.iloc[0]['Stock'],
                "Price": product_info.iloc[0]['Price']
            }
        else:
            response = {"error": "Product code not found. Please check the code and try again."}
    
    except Exception as e:
        response = {"error": f"An error occurred: {str(e)}"}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
