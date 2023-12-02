# INRIX_Hack_Client_Server_Flask_Demo
This repository will guide you through the process of creating a Flask server/backend app, developing APIs, setting up a frontend Vanilla JavaScript application, and making a simple API call. The goal is to demonstrate how to seamlessly integrate and exchange data between the frontend and backend applications.


# Client Server Flask App - INRIX HACK 2023

## Overview
This repository contains the source code for a Flask web application developed for INRIX HACK 2023. The application serves as a client-server demo example to help you get started with client-server interactions using Flask and Bootstrap.

## Links
If you wish to see an ExpressJS example for the same project goto: [ExpressJS code example](https://github.com/INRIX-Aashay-Motiwala/INRIX_Hack_Client_Server_ExpressJS_Demo)



## Features
- **Home Page**: A simple home page with Bootstrap styling.
- You can click the GetToken button in the navbar after hosting this app locally to print the token on the html page
- **GetToken Endpoint**: Access the `/getToken` endpoint to receive a JSON response with the Auth Token.
  

## Prerequisites
- Python 3.x
- Virtualenv (optional but recommended - helps to download all the libraries required at once)

## Setup Instructions

1. **Clone the Repository:**
    ```bash
    git clone git@github.com:<YOUR USER NAME>/INRIX_Hack_Client_Server_Demo.git
    cd INRIX_Hack_Client_Server_Demo
    ```

2. **Create a Virtual Environment (Optional):**
    ```bash
    pip3 install virtualenv
    virtualenv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**
    ```bash
    pip3 install -r requirements.txt
    ```
4. !!! Make sure to paste your INRIX APP_ID and HASH_TOKEN in app/utils/auth_utils.py i.e. [here](https://github.com/INRIX-Aashay-Motiwala/INRIX_Hack_Client_Server_Demo/blob/7058cd0d5c7a482a93ac7a6efeef68428fcab106/app/utils/auth_utils.py#L3) before you run your application

## Running the Application

1. **Start the Flask App:**
    ```bash
    python main.py 
    ```
    Make sure to be in the same directory where you have your main.py file

2. **Access the App:**
    Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

3. **Explore the App:**
    - Click on the "GetToken" link in the navigation bar to fetch and display the API token dynamically.
    
## File Structure
- **app.py:** Flask application script.
- **templates/:** HTML templates for the web pages.
- **static/:** Static files (CSS, JS).
---

If you want to learn how to parse a JSON Dataset goto [Example](https://github.com/INRIX-Aashay-Motiwala/INRIX_Hack_Client_Server_Demo/blob/main/json_parser_example.py)

**Happy Hacking!**
