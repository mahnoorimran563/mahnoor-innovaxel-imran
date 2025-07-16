URL Shortener API — Flask Project

This is a simple Flask-based API to shorten URLs. It supports:

1. Creating a short link
2. Retrieving the original link
3. Updating the link
4. Deleting it
5. Viewing access stats

---> How to Run the Project

1. Install the required libraries:

pip install -r requirements.txt

2. Start the Flask server:

python app.py

3. Open this URL in your browser:

http://127.0.0.1:5000/

You can use the browser OR Postman to test everything.

---> API Endpoints

1. POST /shorten – Create a short link

2. GET /shorten/<shortCode> – Get original URL

3. PUT /shorten/<shortCode> – Update the link

4. DELETE /shorten/<shortCode> – Delete the link

5. GET /shorten/<shortCode>/stats – Get usage stats

---> Frontend

A simple HTML page is provided in templates/index.html

Open it in a browser to test all features visually.

---> Tools Used

1. Python
2. Flask
3. SQLite
4. HTML + JavaScript
