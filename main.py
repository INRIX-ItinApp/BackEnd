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
app = Flask(__name__, template_folder="app/templates", static_url_path="/static")
# By adding CORS(app), you are telling Flask to include CORS headers in responses. The flask_cors extension will add headers such as Access-Control-Allow-Origin: *, allowing requests from any origin.
# This way, when your frontend makes requests to your Flask server, the server will respond with the appropriate CORS headers, and the browser will permit the requests. Since the frontend and backend are on the same origin (domain), you won't encounter CORS issues.
# For more info on CORS goto: https://www.bannerbear.com/blog/what-is-a-cors-error-and-how-to-fix-it-3-ways/
CORS(app)


# This is the route that will serve your index.html template
@app.route("/")
def index():
    return render_template("index.html")


# This is the route that will help you get the token and return it as a JSON response
@app.route("/getToken", methods=["GET"])
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


@app.route("/findRoute", methods=["POST"])
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


@app.route("/getRoute", methods=["POST"])
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
@app.route("/ask_openai", methods=["POST"])
def ask_openai():
    print("hello!")
    user_input = request.json.get("question")
    user_input = (
        user_input
        + """
    I gave you a starting location and list of locations I want to go to.

    I might have given you vague descriptions of locations like "I want to go grocery shopping." in which case, just find an establishment for grocery shopping near the area that won't take too much time to drive to, and gimme its coordinates.

    Please gimme all possible pairs of start point and destination (coordinates) to travel from one place to the next. All possibilities of itinerary. 

    For example, when I say:
    "Hey I'm at Stevens Court apartment in UW. I want to go to dicks burger, go grocery shopping, and go to a bar."


    Please output:
    [
        [(47.655548, -122.3048987), (47.6612705, -122.3133457), (47.6610986, -122.2984852), (47.6603733, -122.3130995)],
        [(47.655548, -122.3048987), (47.6612705, -122.3133457), (47.6603733, -122.3130995), (47.6610986, -122.2984852)],
        [(47.655548, -122.3048987), (47.6610986, -122.2984852), (47.6612705, -122.3133457), (47.6603733, -122.3130995)],
        [(47.655548, -122.3048987), (47.6610986, -122.2984852), (47.6603733, -122.3130995), (47.6612705, -122.3133457)],
        [(47.655548, -122.3048987), (47.6603733, -122.3130995), (47.6612705, -122.3133457), (47.6610986, -122.2984852)],
        [(47.655548, -122.3048987), (47.6603733, -122.3130995), (47.6610986, -122.2984852), (47.6612705, -122.3133457)],
        [(47.655548, -122.3048987), (47.6612705, -122.3133457), (47.6603733, -122.3130995), (47.6610986, -122.2984852)],
        [(47.655548, -122.3048987), (47.6612705, -122.3133457), (47.6610986, -122.2984852), (47.6603733, -122.3130995)],
        [(47.655548, -122.3048987), (47.6603733, -122.3130995), (47.6612705, -122.3133457), (47.6610986, -122.2984852)],
        [(47.655548, -122.3048987), (47.6603733, -122.3130995), (47.6610986, -122.2984852), (47.6612705, -122.3133457)],
        [(47.655548, -122.3048987), (47.6610986, -122.2984852), (47.6603733, -122.3130995), (47.6612705, -122.3133457)],
        [(47.655548, -122.3048987), (47.6610986, -122.2984852), (47.6612705, -122.3133457), (47.6603733, -122.3130995)],
        [(47.655548, -122.3048987), (47.6603733, -122.3130995), (47.6610986, -122.2984852), (47.6612705, -122.3133457)],
        [(47.655548, -122.3048987), (47.6603733, -122.3130995), (47.6612705, -122.3133457), (47.6610986, -122.2984852)],
        [(47.655548, -122.3048987), (47.6610986, -122.2984852), (47.6603733, -122.3130995), (47.6612705, -122.3133457)],
        [(47.655548, -122.3048987), (47.6610986, -122.2984852), (47.6612705, -122.3133457), (47.6603733, -122.3130995)],
        [(47.655548, -122.3048987), (47.6612705, -122.3133457), (47.6610986, -122.2984852), (47.6603733, -122.3130995)],
        [(47.655548, -122.3048987), (47.6612705, -122.3133457), (47.6603733, -122.3130995), (47.6610986, -122.2984852)],
        [(47.655548, -122.3048987), (47.6612705, -122.3133457), (47.6603733, -122.3130995), (47.6610986, -122.2984852)],
        [(47.655548, -122.3048987), (47.6612705, -122.3133457), (47.6610986, -122.2984852), (47.6603733, -122.3130995)],
        [(47.655548, -122.3048987), (47.6603733, -122.3130995), (47.6610986, -122.2984852), (47.6612705, -122.3133457)],
        [(47.655548, -122.3048987), (47.6603733, -122.3130995), (47.6612705, -122.3133457), (47.6610986, -122.2984852)],
        [(47.655548, -122.3048987), (47.6610986, -122.2984852), (47.6612705, -122.3133457), (47.6603733, -122.3130995)],
        [(47.655548, -122.3048987), (47.6610986, -122.2984852), (47.6603733, -122.3130995), (47.6612705, -122.3133457)]
    ]
    In your response, like this above I just want a big array of X subarrays. X is the amount of permutations for travelling plans btw.
    For example if there are 3 locations, there should be 6 permutations thus 6 subarrays. If 4 locations, should be 24 permutations, thus 24 subarrays.
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
