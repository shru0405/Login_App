# Login_App 
A user registration system with Python(Flask), MySql and React. Users can register and login and view dashboards.

SETUP and STEPS:

1). Form Design — Design a login and registration form with React.

2). Templates — Create Flask templates with HTML and Python.

3). Basic Validation — Validating form data that is sent to the server (username, password, and email).

4). Session Management — Initialize sessions and store retrieved database results.

5). MySQL Queries — Select and insert records from/in our database table.

6). Routes — Routing will allow us to point our URL's to our functions.

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

      // Handle the response accordingly
      console.log(response.data); // You can handle success or error responses here

    } catch (error) {
      // Handle errors (e.g., network issues, server errors)
      console.error('Error resetting password:', error);
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

