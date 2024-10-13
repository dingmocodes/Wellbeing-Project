from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
import boto3, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes


app = Flask(__name__, static_folder='static', template_folder='.')
CORS(app)  # Enable CORS for the whole app

# Create a Bedrock client with a specified AWS region
client = boto3.client('bedrock-runtime', region_name='us-west-2',
                      aws_access_key_id='access_key', 
                      aws_secret_access_key='secret_access_key', 
                      )

# Bedrock model configuration
model_id = "anthropic.claude-3-haiku-20240307-v1:0"
accept_header = "application/json"
content_type_header = "application/json"

@app.route('/')
def index():
    return render_template('website.html')

@app.route('/wellness_bot', methods=['POST'])
def wellness_bot():
    data = request.json
    user_query = data.get('query')

    # Example response
    response_data = {
        'result': f"Received your query: {user_query}"
    }

    return jsonify(response_data)


@app.route('/call_bedrock', methods=['POST'])
def call_bedrock():
    data = request.json
    user_response = data.get('user_response')  # Extract user's text input

    # Check if the user response is present
    if not user_response:
        return jsonify({"error": "User response is missing"}), 400

    # Bedrock API request body with anthropic_version and correct structure
    body = {
        "anthropic_version": "bedrock-2023-05-31",  # Required for Claude model
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_response
                    }
                ]
            }
        ]
    }

    try:
        # Invoke Bedrock model using Boto3
        response = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body).encode('utf-8')  # Encode body to bytes as required
        )

        # Decode the response body and print it for debugging
        model_response = json.loads(response['body'].read().decode('utf-8'))

        # Log the full response to see the actual structure
        print("Model Response: ", model_response)

        # Extract the model's response from the content array
        if "content" in model_response and len(model_response['content']) > 0:
            assistant_message = model_response['content'][0].get('text', 'No response')

            return jsonify({
                "message": "Success",
                "user_response": user_response,
                "model_output": assistant_message
            })
        else:
            return jsonify({
                "error": "Unexpected response structure",
                "full_response": model_response  # Include the full response for debugging
            }), 500

    except Exception as e:
        # Print detailed error message in the logs
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": "Failed to process request"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)