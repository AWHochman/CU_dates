This is my final project for CS 1998 (Intro to Backend Development). I
created and deployed the backend for a dating app. The API specification
is written in a .md file within the project; I tried to make it similar to
specifications we have been given in this course. Other than that I've
listed below a feature that satisfies each requirement to try and make
grading easier.

Server IP: http://34.75.199.194/ (No longer runnning)

One-to-many relationship:  
    &nbsp;&nbsp;&nbsp;- Each user in the User table can be associated with many matches from the Match table  
Many-to-many relationship:  
    &nbsp;&nbsp;&nbsp;- Each user in the User table can be associated with many communities from the Community table and each community can be associated with many users (can see nested serialization in their serialize methods)  
Create route:  
    &nbsp;&nbsp;&nbsp;- POST /api/users/ creates a user  
Retrieve route:  
    &nbsp;&nbsp;&nbsp;- GET /api/users/ retrieves all of the users  
Update route:  
    &nbsp;&nbsp;&nbsp;- POST /api/users/{id}/browse/ if a match already exists in the Match table between the two users specified in the request then the accepted field of the match is updated to the value specified in the request  
Delete route:  
    &nbsp;&nbsp;&nbsp;- DELETE /api/users/{id}/ deletes a users
