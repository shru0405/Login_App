# Login_App 
A user registration system with Python(Flask), MySql and React. Users can register and login and view dashboards.

SETUP and STEPS:

1). Form Design — Design a login and registration form with React.

2). Templates — Create Flask templates with HTML and Python.

3). Basic Validation — Validating form data that is sent to the server (username, password, and email).

4). Session Management — Initialize sessions and store retrieved database results.

5). MySQL Queries — Select and insert records from/in our database table.

6). Routes — Routing will allow us to point our URL's to our functions.

RUNNING THE APP LOCALLY:

1.Set up  development environment:

    Install Node.js
    Install npm (Node Package Manager): npm is included with Node.js, so once you install Node.js, npm will be available.

2.Create a React.js app:

    Open a terminal and run the following commands:

    npx create-react-app my-login-app
    cd my-login-app

3.Install required dependencies:

    Install additional dependencies needed for the login functionality:

    npm install axios react-router-dom

4.Create the login page:

    Replace the content of src/App.js with your login page component code. Create separate components for login and other related functionalities.

5.Set up a Python backend:

    Create a Python virtual environment:

    python -m venv venv

6.Activate the virtual environment:

    On Windows: venv\Scripts\activate
    On macOS/Linux: source venv/bin/activate

7.Install Flask and Flask-CORS:

    pip install Flask Flask-CORS

8.Create the Python backend:

    Create a new file, e.g, app.py, and set up a basic Flask app with endpoints for handling user authentication.

9.Set up MySQL database:

    Install MySQL and create a database for your application.
    Install the MySQL Python connector:

    pip install mysql-connector-python

10.Connect React.js to Python backend:

    Update your React.js code to make API requests to your Python backend.

11.Run the applications:

    Start your Flask backend by running:
    python app.py

12.Start React.js app by running:

    npm start

13.Access the app:

    Open your web browser and navigate to http://localhost:3000 to see your React.js app in action.

CREATING A PROFILE PAGE:
The profile page is where the user can go to view their username, password, and email.

PASSWORD RESET:
Password change can be achieved with sending tokens to the user email id.
   
User Requests Password Reset:
1. Create an endpoint on your server (backend) to handle password reset requests. The client (React app) should send a request to this endpoint with the user's email.

2. Generate Token:
 When a password reset request is received, generate a unique token associated with the user's account. This token will be used to verify the password reset request.

3. Send Email with Token:
Send an email to the user containing a link with the generated token. The link should point to a password reset page in your React app.

4. Reset Password Page:
Create a page in your React app where users can enter a new password. This page should be accessible via the link provided in the email.

5. Verify Token:
When the user clicks on the link, extract the token from the URL and send it to the server to verify its validity. Ensure that the token hasn't expired and matches the one generated for the user.

6. Update Password:
 If the token is valid, allow the user to update their password on the password reset page.

This can be accomplished using Axios to make the API call. The axios.post method is used to send a POST request to the server with the new password. The server end must be able to handle the request and update the database.

import React, { useState } from 'react';
import axios from 'axios';

const PasswordResetPage = ({ match }) => {
  const [password, setPassword] = useState('');

  const handlePasswordReset = async () => {
    try {
      // Send a request to the server to update the password
      // Use match.params.token to get the token from the URL
      const response = await axios.post(`/api/reset-password/${match.params.token}`, {
        password: password,
      });

      // Handle the response as needed
      console.log('Password reset successful:', response.data);
    } catch (error) {
      console.error('Password reset failed:', error.response.data);
      // Handle errors, e.g., show an error message to the user
    }
  };

  return (
    <div>
      <h2>Password Reset</h2>
      <label>New Password:</label>
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handlePasswordReset}>Reset Password</button>
    </div>
  );
};

export default PasswordResetPage;

