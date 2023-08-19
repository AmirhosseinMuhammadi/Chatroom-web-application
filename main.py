from flask import Flask , render_template
from flask import redirect , request , url_for , session
from flask_socketio import SocketIO, emit
from flask_mail import Mail , Message
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "1234"
socketio = SocketIO(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yaghuduk@gmail.com'
app.config['MAIL_PASSWORD'] = 'idgjfnlyglrswvyk'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login" , methods = ["POST" , "GET"])
def login():
    if "username" not in session:
        message = ""
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            file = open("users.txt")
            t = 0
            for line in file:
                if username == line.strip().split(" ")[0]:
                    t += 1
                    if password == line.strip().split(" ")[1]:
                        session["username"] = username
                        return redirect("/discover")
                    else:
                        #return "<script>alert('Invalid password.');window.location.href = '/login';</script>"
                        message = "Invalid password."

            if t == 0:
                #return "<script>alert('You do not have an account. Try to sign up first.');window.location.href = '/login';</script>"
                message = "You don't have an account. Try to sign up first."
            
            file.close()

        return render_template("login.html" , message = message)
    else:
        return redirect("/discover")

@app.route("/sign-up" , methods = ["POST" , "GET"])
def register():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        t = 0
        file = open("users.txt" , "r+")
        for line in file:
            if username == line.strip().split(" ")[0]:
                t += 1
        
        if t == 0:
            file.write(f"{username} {password}" + "\n")
            file.close()

            userInfo = {"username" : [username] , 
                        "password" : [password] , 
                        "profile photo" : ["profile.png"] ,
                        "email" : ["empty"]}
            newUser = open(f"{username}.csv" , "a")
            pd.DataFrame(userInfo).to_csv(newUser)
            newUser.close()
            
            return "<script>alert('Done! You can login now.');window.location.href = '/login';</script>"
        else:
            #return "<script>alert('Username already taken. Try another.');window.location.href = '/sign-up';</script>"
            message = "Username already taken. Try another."

    return render_template("sign up.html" , message = message)


@app.route("/discover" , methods = ["GET" , "POST"])
def discover():
    if "username" in session:
        return render_template("discover.html")
    else:
        return "You don't have access to this page"
    

@app.route("/profile" , methods = ["GET" , "POST"])
def profile():
    if "username" in session:
        df = pd.read_csv(f"{session['username']}.csv")
        profilePhoto = f"static/{df['profile photo'][0]}"
        email = df["email"][0]
        if request.method == "POST":
            if request.files["file"].filename != "":
                f = request.files["file"]
                f.save(f"static/{session['username']}.png")
                df["profile photo"][0] = f"{session['username']}.png"
                df.to_csv(f"{session['username']}.csv")
            if request.form["newpass"] != "" and request.form["newpass"] == request.form["secondnewpass"]:
                df["password"][0] = request.form["newpass"]
                df.to_csv(f"{session['username']}.csv")
                with open("users.txt" , "r") as file:
                    inputFilelines = file.readlines()
                    with open("users.txt" , "w") as file:
                        for line in inputFilelines:
                            if line.strip().split(" ")[0] != session["username"]:
                                file.write(line)
                file.close()
                file = open("users.txt" , "a+")
                file.write(f"{df['username'][0]} {request.form['newpass']}" + "\n")
                file.close()
            
            if request.form["email"] != "":
                df["email"][0] = request.form["email"]
                df.to_csv(f"{session['username']}.csv")
            
            if request.form["newpass"] != "" and request.form["newpass"] != request.form["secondnewpass"]:
                return "<script>alert('Your passwords are not the same');window.location.href = '/profile';</script>"

            return redirect("/profile")
        return render_template("profile.html" , profilePhoto = profilePhoto , email = email)
    else:
        return "You don't have access to this page"
    
@app.route("/remove-photo")
def removePhoto():
    if "username" in session:
        df = pd.read_csv(f"{session['username']}.csv")
        if df["profile photo"][0] != "profile.png":
            os.remove(f"static/{df['profile photo'][0]}")
            df["profile photo"][0] = "profile.png"
            df.to_csv(f"{session['username']}.csv")
        return redirect("/profile")

    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/delete-account")
def delete():
    if "username" in session:
        df = pd.read_csv(f"{session['username']}.csv")
        if df["profile photo"][0] != "profile.png":
            os.remove(f"static/{session['username']}.png")
        os.remove(f"{session['username']}.csv")
        with open("users.txt" , "r") as file:
            inputFilelines = file.readlines()
            with open("users.txt" , "w") as file:
                for line in inputFilelines:
                    if line.strip().split(" ")[0] != session["username"]:
                        file.write(line)

        session.clear()
        file.close()
        return "<script>alert('Your account has been deleted successfully');window.location.href = '/login';</script>"
    else:
        return redirect(url_for("login"))


@app.route("/recovery" , methods = ["GET" , "POST"])
def recovery():
    if "username" not in session:
        message = ""
        if request.method == "POST":
            email = request.form["email"]
            file = open("users.txt")
            t = 0
            users = []
            for line in file:
                users.append(f"{line.strip().split(' ')[0]}.csv")
                if line.strip().split(" ")[0] == email:
                        t = 1
                        msg = Message('Restore your account', sender = 'yaghuduk@gmail.com', recipients = [email])
                        msg.body = f"Your username is {line.strip().split(' ')[0]} and your password is {line.strip().split(' ')[1]}. Keep them safe."
                        mail.send(msg)
                        return "<script>alert('We sent you an email. Check it and login to your account');window.location.href = '/login';</script>"
                
                if t == 0:
                    count = 0
                    for user in users:
                        df = pd.read_csv(user)
                        if df["email"][0] == email:
                            count = 1
                            msg = Message('Restore your account', sender = 'yaghuduk@gmail.com', recipients = [email])
                            msg.body = f"Your username is {df['username'][0]} and your password is {df['password'][0]}. Keep them safe."
                            mail.send(msg)
                            break
                    
                    if count == 0:
                        message = "There are no accounts created with this email."

                    else:
                        return "<script>alert('We sent you an email. Check it and login to your account');window.location.href = '/login';</script>"
                    
        return render_template("recovery.html" , message = message)
    
    else:
        return redirect(url_for("discover"))


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('message')
def handle_message(message):
    df = pd.read_csv(f"{session['username']}.csv")
    emit('message', f"static/{df['profile photo'][0]}-{session['username']} : {message}", broadcast=True)

if __name__ == "__main__":
    app.run(debug=True)