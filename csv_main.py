from flask import Flask, request, jsonify
import pandas as pd
from new_csv2firebase import upload_csv_to_firebase_and_store_url, process_device_data, get_phosphorus_color, get_Conductivity_color, get_nitrogen_color, get_moisture_color, get_ph_color, get_potassium_color  # Update with your actual module

# Initialize Flask app
app = Flask(__name__)

# Function to fetch data from CSV
def fetch_data_from_csv(csv_file):
    try:
        data = pd.read_csv(csv_file)
        return data
    except Exception as e:
        return str(e)

# Function to process the device data and create heatmap
def process_and_create_heatmap(csv_file_new):
    # Fetch data from the CSV file
    data = fetch_data_from_csv(csv_file_new)
    
    if isinstance(data, str):  # If an error message was returned from fetch_data_from_csv
        return {"error": data}
    
    # Define attributes and color functions
    attributes = ['phosphor', 'conductivity', 'nitrogen', 'moisture', 'pH', 'potassium']
    color_functions = {
        'phosphor': get_phosphorus_color,
        'conductivity': get_Conductivity_color,
        'nitrogen': get_nitrogen_color,
        'moisture': get_moisture_color,
        'pH': get_ph_color,
        'potassium': get_potassium_color
    }
    
    # Process the device data and create heatmaps
    result = process_device_data(data, attributes, color_functions)
    
    return {"message": result}

@app.route('/process_csv', methods=['POST'])
def process_csv():
    # Get the file from the request
    csv_file = None
    for file_key in request.files:
        csv_file = request.files[file_key]
        break  # Only pick the first file uploaded

    # Check if a file is uploaded
    if not csv_file:
        return jsonify({"error": "CSV file is required."}), 400

    # Check if the file has a valid name
    if csv_file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    # Get the custom file name from the form (optional)
    custom_filename = request.form.get('custom_filename', csv_file.filename)

    # Get the custom file name from the form (optional)
    custom_filename = request.form.get('custom_filename', csv_file.filename)

    # Save the file locally with the custom filename
    csv_file_path = f"{custom_filename}"
    csv_file.save(csv_file_path)
    
    upload_csv_to_firebase_and_store_url(csv_file_path, folder_name="csv_files")
    # Process the file and create heatmap
    result = process_and_create_heatmap(csv_file_path)
    
    if "error" in result:
        return jsonify(result), 500
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)



