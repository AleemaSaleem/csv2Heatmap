from flask import Flask, request, jsonify
from firebase2firebase import process_device_data,get_phosphorus_color,get_Conductivity_color,get_nitrogen_color,get_moisture_color,get_ph_color,get_potassium_color



# Initialize Flask app
app = Flask(__name__)

# Route to process and save image data
@app.route('/process_data', methods=['POST'])
def process_data():
    try:
        # Extract device ID from the request payload
        payload = request.json
        device_id = payload.get('device_id')
        devices=[device_id]
        if not device_id:
            return jsonify({'error': 'Device ID is required'}), 400
        attributes = ['phosphor', 'conductivity', 'nitrogen', 'moisture', 'pH','potassium']
        color_functions = {
        'phosphor': get_phosphorus_color,
        'conductivity': get_Conductivity_color,
        'nitrogen': get_nitrogen_color,
        'moisture' : get_moisture_color,
        'pH' : get_ph_color,
        'potassium' : get_potassium_color
        }
        process_device_data(devices, attributes, color_functions)   

        return jsonify({'message': 'Image processed and uploaded successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
