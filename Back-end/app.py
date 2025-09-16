from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore 

# Import our custom modules
from services.analysis_service import run_analysis  # type: ignore
from ml.roof_detector import calculate_roof_area_from_image #type: ignore

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS for all routes, allowing our front-end to connect
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze_potential():
    """
    API endpoint to handle the analysis request from the front-end.
    """
    try:
        # Get data from the form. We use request.form because the request
        # will be 'multipart/form-data' due to the file upload.
        dwellers = int(request.form.get('dwellers', 4))
        open_space = float(request.form.get('space', 20))
        lat = float(request.form.get('lat', 29.3803))
        lng = float(request.form.get('lng', 79.4636))

        roof_area = 0
        # Check if the roof photo was uploaded
        if 'roof_photo' in request.files and request.files['roof_photo'].filename != '':
            image_file = request.files['roof_photo']
            # Get area from our ML model placeholder
            roof_area = calculate_roof_area_from_image(image_file)
            if roof_area is None:
                return jsonify({"error": "Could not process the uploaded image."}), 400
        else:
            # If no photo, use the manually entered roof area
            roof_area = float(request.form.get('roof_area', 150))
        
        # --- Fetch External Data (Placeholder) ---
        # TODO: In a real app, you would make API calls to weather and GIS services here
        # using the lat and lng. For now, we'll use static mock data.
        location_data = {
            "avgAnnualRainfall": 1470, # mm
            "principalAquifer": "Fissured Rock",
            "depthToGroundwater": "10-20 meters"
        }

        # --- Run the Core Analysis ---
        analysis_results = run_analysis(roof_area, dwellers, open_space, location_data)

        # Return the results as JSON
        return jsonify(analysis_results)

    except Exception as e:
        # Basic error handling
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal server error occurred. Please check the data and try again."}), 500


if __name__ == '__main__':
    # Run the app in debug mode for development
    # It will be accessible at http://127.0.0.1:5000
    app.run(debug=True, port=5000)