import json
from flask import Flask, render_template, jsonify, request
from app.utils.auth_utils import get_token
from flask_cors import CORS
from app.functions.route_functions import find_route_fetch
from app.functions.route_functions import get_route_fetch
from dotenv import load_dotenv
from openai import OpenAI
import os
from flask import Flask, render_template, jsonify, request
from app.utils.auth_utils import get_token
from flask_cors import CORS
import re
import json

load_dotenv()
OPENAI_KEY = os.environ.get("MY_GPT_KEY_TWO")
client = OpenAI(api_key=OPENAI_KEY)


# Create the Flask app with the template folder specified that will contain your index.html and static folder which will contain your JavaScript files
application = Flask(
    __name__, template_folder="app/templates", static_url_path="/static"
)
# By adding CORS(app), you are telling Flask to include CORS headers in responses. The flask_cors extension will add headers such as Access-Control-Allow-Origin: *, allowing requests from any origin.
# This way, when your frontend makes requests to your Flask server, the server will respond with the appropriate CORS headers, and the browser will permit the requests. Since the frontend and backend are on the same origin (domain), you won't encounter CORS issues.
# For more info on CORS goto: https://www.bannerbear.com/blog/what-is-a-cors-error-and-how-to-fix-it-3-ways/
CORS(application)


# This is the route that will serve your index.html template
@application.route("/")
def index():
    return render_template("index.html")


# This is the route that will help you get the token and return it as a JSON response
@application.route("/getToken", methods=["GET"])
def display_token():
    # This makes the call to the get_token function in the auth_utils.py file
    response, status_code = get_token()
    # If the request is successful, return the token
    if status_code == 200:
        api_token = response
        return jsonify({"message": api_token})
    # If the request fails, return the error message
    else:
        return jsonify({"message": response})


@application.route("/findRoute", methods=["POST"])
def findRoute():
    record = request.get_json()
    pointA: str = record.get("pointA")
    pointB: str = record.get("pointB")
    pointC: str = record.get("pointC")
    pointD: str = record.get("pointD")
    bearerToken: str = record.get("bearerToken")
    response, status_code = find_route_fetch(
        pointA, pointB, pointC, pointD, bearerToken
    )
    if status_code == 200:
        return response


@application.route("/getRoute", methods=["POST"])
def getRoute():
    record = request.get_json()
    route_id: str = record.get("route_id")
    bearerToken: str = record.get("bearerToken")
    response, status_code = get_route_fetch(route_id, bearerToken)
    if status_code == 200:
        return response
    else:
        return "request failed"


# Route to interact with the OpenAI Assistant
@application.route("/ask_openai", methods=["POST"])
def ask_openai():
    print("hello!")
    user_input = request.json.get("question")
    user_input = (
        user_input
        + """
Provide an array of coordinates for each destination based on the given starting location and list of destinations. When descriptions are vague (e.g., 'grocery shopping'), select a nearby establishment and include its coordinates. The output should be a simple array of coordinate pairs, each representing a distinct destination including the starting point.

Example request:
'I'm at Stevens Court apartment in UW. My destinations are Dicks Burger, a grocery store, and a bar.'

Expected output:
An array of coordinate pairs. The first pair should represent the Stevens Court apartment in UW, followed by coordinates for Dicks Burger, a nearby grocery store, and a bar.

Note: The response from the chatbot should be exclusively the array of coordinates, without any additional text or explanations.

        """
    )
    print(user_input)
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": user_input}],
        )
        # Extract the message content
        message_content = response.choices[0].message.content
        print("layer3")
        # Use regular expressions to find the JSON array within the message content
        # We're looking for the pattern that starts with '[' and ends with ']', inclusive
        print("preprocessing", message_content)
        json_array_str = re.search(r"\[\s*\[.*?\]\s*\]", message_content, re.DOTALL)
        print("post-processing", json_array_str)
        print("layer4")
        if json_array_str:
            print("layer5")
            json_array_str = json_array_str.group(0)
            print("JSON String Before Parsing:", json_array_str)
            return json_array_str
        else:
            return jsonify({"error": "Could not find the array in the response"})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    application.run(host="0.0.0.0", port=port)
