import os
import json
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Constants for the Gemini API
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
API_KEY = "AIzaSyDfbmswHN2wk0cNmosFut9WAnwbO8zosjs"  # Replace with your actual API key

def call_gemini_api(input_text):
    try:
        headers = {
            "Content-Type": "application/json",
        }

        # Correcting the payload structure according to the API request
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": input_text  # The prompt for generating content
                        }
                    ]
                }
            ]
        }

        # Adding the API key in the query parameters
        params = {"key": API_KEY}

        # Sending POST request
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload)

        # Log the response status code and body for debugging
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        if response.status_code == 200:
            data = response.json()
            # Handling the response from the Gemini API
            if "candidates" in data and len(data["candidates"]) > 0:
                generated_text = data["candidates"][0]["content"]["parts"][0]["text"]
                return generated_text
            else:
                return "No valid response from Gemini API."
        else:
            return f"Error: {response.status_code}, {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

test_input = "Tell me a joke."
generated_content = call_gemini_api(test_input)
print(generated_content)

# Route to serve the form page
@app.route("/")
def index():
    return render_template("index.html")

# Route to fetch trends from the mock server and generate posts
@app.route("/generate", methods=["POST"])
def generate():
    try:
        # Fetching trends from the mock server
        response = requests.get("http://127.0.0.1:5000/1.1/trends/place.json")
        trends_data = response.json()[0]["trends"]

        trend_posts = []

        # Generate post for the first trend only
        trend = trends_data[0]  # Using only the first trend
        trend_name = trend.get("name")
        
        if trend_name:
            # Prepare the prompt
            prompt = f"Create a social media post for {trend_name} for the GoFR company."
            
            # Call Gemini API
            generated_content = call_gemini_api(prompt)

            if "error" in generated_content:
                return jsonify({"error": generated_content}), 500  # Return error if any

            # Return the generated content for the trend
            trend_posts.append({
                "trend": trend_name,
                "post": generated_content
            })

        return jsonify({"generated_posts": trend_posts})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to save content to a file
@app.route("/save", methods=["POST"])
def save_content():
    content = request.json.get("content")
    if not content:
        return jsonify({"error": "Content is required"}), 400
    
    try:
        # Ensure that the file is in the right path, or you can use a specific folder
        with open("generated_content.txt", "a") as f:
            f.write(content + "\n")
        return jsonify({"message": "Content saved successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to handle modify (re-generate content based on new prompt)
@app.route("/modify", methods=["POST"])
def modify():
    try:
        new_prompt = request.json.get('new_prompt')
        if not new_prompt:
            return jsonify({"error": "New prompt is required"}), 400

        # Fetch trends again (to use in modified prompt)
        response = requests.get("http://127.0.0.1:5000/1.1/trends/place.json")
        trends_data = response.json()[0]["trends"]

        trend = trends_data[0]  # Using the first trend
        trend_name = trend.get("name")

        if trend_name:
            updated_prompt = f"{new_prompt} and the trend {trend_name}"
            generated_content = call_gemini_api(updated_prompt)

            if "error" in generated_content:
                return jsonify({"error": generated_content}), 500  # Return error if any

            return jsonify({"generated_content": generated_content})
        else:
            return jsonify({"error": "Trend name not found."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
