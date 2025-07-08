# Chatroom-web-application

# Goals
After learning flask and concepts of API and backend development, it’s time to create a web application. I decided to build a simple chatroom application with user authentication. So people can make their own accounts and chat to each other.

# Objectives
Users can register to the site and log in to their accounts. They can manage their accounts and change some simple informations. In the profile tab the user can change the profile photo, password and email address for account recovery. It’s also possible to remove the photo or log out from an account or even delete that. In the discover tab, global chat is available that means all of the users can talk to each other. Since realtime updates are important in a chatroom, this part is created by simple socket programming using a flask extension called flask socketio in the server side and javascript’s socket.io in the client side.
There is no sign of database handling or using an RDBMS in this project. All of the user’s data stores in text and CSV files.
I used flask to structure backend and APIs, pandas for some data manipulation, flask socketio for receiving and sending data in the backend, flask mail for sending forgotten password to user’s email address and also HTML, CSS & some Javascript for frontend development.

# Challenges & Solutions
I’ve had some challenges in creating and styling some widgets in HTML and CSS since I’m not an expert. However, the most challenging part for me was development of the chatroom. At first I was trying to avoid socket programming, because I had no experience before. Therefore I stored every message from user into a text file and then read its contents in the frontend and show them all. The problem of this method is that it doesn’t support realtime updates in the browser and users have to reload the page manually every second. Then I tried to update the contents of the page every second using setInterval() function in javascript. For almost unknown reasons it didn’t work in this specific case. I also tried to reload the page every second which wasn’t a good idea at all. Therefore the last way was to use socket programming. After hours of reading documents and watching youtube videos and of course getting help from ChatGPT finally I created the most simple chatroom with realtime updates.

# CONCLUSION
The project was a great experience for me. In the future I would like to create some more web apps with flask like a to-do list app or an online shop or a trivia game. I expect from myself to use SQL databases in the next projects.
