from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3
import os




# Create databases###############################################
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT,
UNIQUE(username));""")

cursor.execute("""CREATE TABLE IF NOT EXISTS info(
user_id INTEGER PRIMARY KEY,
about TEXT,
tags TEXT,
pfp TEXT,
social1 TEXT,
social2 TEXT,
social3 TEXT,
FOREIGN KEY (user_id) REFERENCES users(user_id)
);"""
)

cursor.execute("""CREATE TABLE IF NOT EXISTS match_handler(
user_id INTEGER PRIMARY KEY,
accepted TEXT,
sent TEXT,
FOREIGN KEY (user_id) REFERENCES users(user_id)
);"""
)

###Account Initialisers
try:
    cursor.execute("""INSERT INTO users(username, password) VALUES 
    (?, ?);""", ("admin", "admin"))
    cursor.execute("""INSERT INTO info(about, tags, pfp) VALUES 
    (?, ?, ?);""", ("about admin", "gamer, admin", "default.jpg"))
    cursor.execute("""INSERT INTO match_handler(accepted, sent) VALUES 
    (?, ?);""", ("0,", "0,"))

    cursor.execute("""INSERT INTO users(username, password) VALUES                  
    (?, ?);""", ("kyan", "admin"))
    cursor.execute("""INSERT INTO info(about, tags, pfp) VALUES 
    (?, ?, ?);""", ("about kyan", "gamer, kyan", "kyan.png"))
    cursor.execute("""INSERT INTO match_handler(accepted, sent) VALUES 
    (?, ?);""", ("0,", "0,"))

    cursor.execute("""INSERT INTO users(username, password) VALUES               
    (?, ?);""", ("jenson", "admin"))
    cursor.execute("""INSERT INTO info(about, tags, pfp) VALUES 
    (?, ?, ?);""", ("about jenson", "gamer, jenson", "jenson.png"))
    cursor.execute("""INSERT INTO match_handler(accepted, sent) VALUES 
    (?, ?);""", ("0,", "0,"))

    cursor.execute("""INSERT INTO users(username, password) VALUES 
    (?, ?);""", ("alex", "admin"))
    cursor.execute("""INSERT INTO info(about, tags, pfp) VALUES 
    (?, ?, ?);""", ("about alex", "gamer, alex", "alex.png"))
    cursor.execute("""INSERT INTO match_handler(accepted, sent) VALUES 
    (?, ?);""", ("0,", "0,"))

    cursor.execute("""INSERT INTO users(username, password) VALUES 
    (?, ?);""", ("lily", "admin"))
    cursor.execute("""INSERT INTO info(about, tags, pfp) VALUES 
    (?, ?, ?);""", ("about lily", "gamer, lily", "lily.png"))
    cursor.execute("""INSERT INTO match_handler(accepted, sent) VALUES 
    (?, ?);""", ("0,", "0,"))

    cursor.execute("""INSERT INTO users(username, password) VALUES 
    (?, ?);""", ("noah", "admin"))
    cursor.execute("""INSERT INTO info(about, tags, pfp) VALUES 
    (?, ?, ?);""", ("about noah", "gamer, noah", "noah.png"))
    cursor.execute("""INSERT INTO match_handler(accepted, sent) VALUES 
    (?, ?);""", ("0,", "0,"))

    cursor.execute("""INSERT INTO users(username, password) VALUES 
    (?, ?);""", ("mason", "admin"))
    cursor.execute("""INSERT INTO info(about, tags, pfp) VALUES 
    (?, ?, ?);""", ("about mason", "gamer, mason", "mason.png"))
    cursor.execute("""INSERT INTO match_handler(accepted, sent) VALUES 
    (?, ?);""", ("0,", "0,"))
except sqlite3.IntegrityError:

    print("Admin user already exists")

conn.commit()
conn.close()

################################################################
app = Flask(__name__)
app.secret_key = "secret_key"

# Folder to store uploaded images
UPLOAD_FOLDER = 'static/pfps'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html") # RENAME TO INDEX.html

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT password FROM users WHERE username = ?""", (username,))
        check = cursor.fetchone()

        print(check)
        conn.commit()
        conn.close()
        if check is None or password != check[0]:
            return render_template("login.html", error="Username or Password is incorrect")
        elif password == check[0]:
            session["user"] = username
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("""SELECT user_id FROM users WHERE username = ?""", (username,))
            user_id = cursor.fetchone()
            session["user_id"] = user_id[0]
            print(user_id[0])
            conn.commit()
            conn.close()

            return redirect(url_for("profile"))
        return render_template("login.html")
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if len(username) <= 8:
            return render_template("register.html", error="Username too short") 
        if len(username) >= 20:
            return render_template("register.html", error="Username too long")
        if len(password) <= 8:
            return render_template("register.html", error="Password too short")
        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            #insert user and pass
            cursor.execute("""INSERT INTO users(username, password) VALUES 
            (?, ?);""", (username, password))
            #insert placeholder for about and tags
            cursor.execute("""INSERT INTO info(about,tags, pfp) VALUES 
            (?, ?, ?);""", ('aboutplaceholder', 'tagplaceholder', 'default.jpg'))
            #insert match_handler   
            cursor.execute("""INSERT INTO match_handler(accepted, sent) VALUES 
    (?, ?);""", ("0,", "0,"))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            return render_template("register.html", error="Username already exists")

    return render_template("register.html")

@app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for("index"))

@app.route('/profile')
def profile():
    if "user" in session:
        user_id = session.get("user_id")
        print(session)
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
        """SELECT * 
        FROM info
        WHERE user_id = (SELECT user_id FROM users WHERE username = ?);""", (session["user"],)
        )
        about = cursor.fetchone()

        cursor.execute(
        """SELECT pfp 
        FROM info
        WHERE user_id = (SELECT user_id FROM users WHERE username = ?);""", (session["user"],)
        )

        pfp = cursor.fetchone()
        print(pfp)
        cursor.execute(
        """SELECT tags FROM info
           WHERE user_id = (SELECT user_id FROM users WHERE username = ?);""", (session["user"],)
        )
        tags = cursor.fetchone()[0].split(",")
        recc = []
        for tag in tags:
            cursor.execute(
            """SELECT users.username, info.* FROM info
            JOIN users
            ON users.user_id = info.user_id
            WHERE tags LIKE ? AND info.user_id <> ?;""", (f"%{tag}%",user_id)
            )
            recc.append(cursor.fetchall())

        recc_set = []
        for tag in recc:
            for id in tag:
                recc_set.append(id)
                if len(list(set(list(recc_set)))) > 5:
                    break

        recc_set = list(set(list(recc_set)))

        cursor.execute("""SELECT user_id
                       FROM match_handler
                       WHERE sent LIKE ?;
                       """, (f"%{user_id},%", ))
        sent = cursor.fetchall()

        sent_ids = [item[0] for item in sent]

        cursor.execute("""SELECT social1 FROM info WHERE user_id = ?""", (user_id,))
        social1 = cursor.fetchone()
        cursor.execute("""SELECT social2 FROM info WHERE user_id = ?""", (user_id,))
        social2 = cursor.fetchone()
        cursor.execute("""SELECT social3 FROM info WHERE user_id = ?""", (user_id,))
        social3 = cursor.fetchone()
        socials = [social1, social2, social3]
        conn.commit()
        conn.close()


        print(recc_set)
        return render_template("profile.html", username=session["user"], about=about[1], tags=about[2], pfp=f"/static/pfps/{pfp[0]}", user_data=recc_set, sent=sent_ids, socials=socials) 

@app.route('/profile2/<user>')
def profile2(user):
    if "user" in session:
        user_id = session.get('user_id')
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            """SELECT accepted
            FROM match_handler
            WHERE user_id = ?;""", (user_id,)
            )
            
        acc = cursor.fetchone()
        cursor.execute(
            """SELECT accepted
            FROM match_handler
            WHERE user_id = ?;""", (user_id,)
            )
        sent = cursor.fetchone()
        match_list = []
        
        for i in acc[0].split(','):
            if i in sent[0].split(','):
                match_list.append(i)
                print(match_list)
        if user in match_list:
            print(user)
            
            cursor.execute(
            """SELECT info.*, users.username
            FROM info
            JOIN users
            ON info.user_id = users.user_id
            WHERE info.user_id = ?;""", (user,)
            )

            about = cursor.fetchone()
            print(about)
            cursor.execute(
            """SELECT pfp 
            FROM info
            WHERE user_id = ?;""", (user,)
            )

            pfp = cursor.fetchone()
            print(pfp)

            cursor.execute("""SELECT social1 FROM info WHERE user_id = ?""", (user,))
            social1 = cursor.fetchone()
            cursor.execute("""SELECT social2 FROM info WHERE user_id = ?""", (user,))
            social2 = cursor.fetchone()
            cursor.execute("""SELECT social3 FROM info WHERE user_id = ?""", (user,))
            social3 = cursor.fetchone()
            socials = [social1, social2, social3]
            conn.commit()
            conn.close()

            return render_template("profile2.html", username=about[7], about=about[1], tags=about[2], pfp=f"/static/pfps/{pfp[0]}", socials=socials)
        else:
            conn.commit()
            conn.close()
            return "Not Matched"
    else:
        return "login fail"
@app.route('/check')
def check():    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM users""")
    data = cursor.fetchall()
    cursor.execute("""SELECT * FROM info""")
    data2 = cursor.fetchall()
    cursor.execute("""SELECT * FROM match_handler""")
    data3 = cursor.fetchall()
    conn.commit()
    conn.close()
    return data + data2 + data3
#Setting routes
@app.route('/settings/aboutme')
def settings_aboutme():
    if "user" in session:
        return render_template('settings_aboutme.html')
    return redirect(url_for("login"))

@app.route('/settings/changeinfo')
def settings_changeinfo():
    if "user" in session:
        user_id = session.get("user_id")
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT social1 FROM info WHERE user_id = ?""", (user_id,))
        social1 = cursor.fetchone()
        cursor.execute("""SELECT social2 FROM info WHERE user_id = ?""", (user_id,))
        social2 = cursor.fetchone()
        cursor.execute("""SELECT social3 FROM info WHERE user_id = ?""", (user_id,))
        social3 = cursor.fetchone()
        conn.commit()
        conn.close()
        return render_template("settings_changeinfo.html", social1=social1, social2=social2, social3=social3)
    return redirect(url_for("login"))
# Updaters 
@app.route('/settings/aboutme/update_aboutme', methods=["POST"])
def update_aboutme():
    if "user" in session:
        aboutme = request.form['aboutme']

        tags = request.form['tags']
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        if aboutme:
            cursor.execute("""
            UPDATE info 
            SET
            about = ?
            WHERE user_id = ?;""", (aboutme, session["user_id"])
            )

        if tags:
            cursor.execute("""
            UPDATE info 
            SET
            tags = ?
            WHERE user_id = ?;""", (tags, session["user_id"])
            )

        
        conn.commit()
        conn.close()

        return profile()
    return redirect(url_for("login"))


@app.route('/settings/changeinfo/update_changeinfo', methods=["POST"])
def update_changeinfo():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        social1 = request.form['social1']
        social2 = request.form['social2']
        social3 = request.form['social3']
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        
        #insert user and pass pfp socials
        cursor.execute("""
                UPDATE info
                SET social1 = ?
                WHERE user_id = ?;
                """, (social1, session["user_id"]))

        cursor.execute("""
                UPDATE info
                SET social2 = ?
                WHERE user_id = ?;
                """, (social2, session["user_id"]))
        
        cursor.execute("""
                UPDATE info
                SET social3 = ?
                WHERE user_id = ?;
                """, (social3, session["user_id"]))
        
        if username:
            try:
                cursor.execute("""
                UPDATE users
                SET username = ?
                WHERE user_id = ?;
                """, (username, session["user_id"]))
                session["user"] = username
            except sqlite3.IntegrityError:
                print(f"Username {username} already exists")
                
        if password:
            cursor.execute("""
            UPDATE users
            SET password = ?
            WHERE user_id = ?;
            """, (password, session["user_id"]))


        if 'pfp' in request.files:
            file = request.files['pfp']
            if file.filename != '':
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                cursor.execute("""
                            UPDATE info
                            SET pfp = ?
                            WHERE user_id = ?;
                            """, (file.filename, session["user_id"]))        
        conn.commit()
        conn.close()
        return profile()
    return profile()    


@app.route("/find")
def find():
    if "user" in session:
        user_id = int(session.get("user_id"))
        print(session)
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
        """SELECT * 
        FROM info
        WHERE user_id <> ? ;""", (user_id,)
        )
        user_data = cursor.fetchall()

        cursor.execute("""SELECT username
                       FROM users
                       WHERE user_id <> ?
                       ORDER BY user_id ASC;""", (user_id,))
        names = cursor.fetchall()

        cursor.execute("""SELECT user_id
                       FROM match_handler
                       WHERE sent LIKE ?;
                       """, (f"%{user_id},%", ))
        sent = cursor.fetchall()

        sent_ids = [item[0] for item in sent]
        print(f"sent {sent_ids}")
        conn.commit()
        conn.close()
        print(f"user data {user_data} names {names}")
        return render_template("find.html", user_data=user_data, names=names, sent=sent_ids)

    else:
        return "login fail"
    
@app.route('/matches')
def matches():
    if "user" in session:
        user_id = int(session.get("user_id"))
        print("MATCHES")
        ### Get Matches
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT user_id
                       FROM match_handler
                       WHERE accepted LIKE ?;
                       """, (f"%{user_id},%",))
        sent = cursor.fetchall()
        sent_ids = [str(item[0]) for item in sent]
        print(sent_ids)
        cursor.execute("""
                       SELECT accepted  
                       FROM match_handler
                       WHERE user_id LIKE ?;
                       """, (user_id, ))
        accepted = cursor.fetchall()
        print(accepted)
        if accepted:
            accepted_ids = accepted[0][0].split(",")
        else:
            accepted_ids=[]
        match_ids = []
        for id in sent_ids:
            if id in accepted_ids:
                match_ids.append(id)
        ###
        ### Get Matches DATA
        placeholders = ','.join('?' for _ in match_ids)

        # Execute the query with the correct number of placeholders
        cursor.execute(
            f"SELECT * FROM info WHERE user_id IN ({placeholders});",
            match_ids
        )
        user_data = cursor.fetchall()
        print(user_data)

        cursor.execute(
            f"""
            SELECT username
            FROM users
            WHERE user_id IN ({placeholders})
            ORDER BY user_id ASC;
            """,
            match_ids
        )

        names = cursor.fetchall()

        print(f" {sent_ids}, accepted{accepted_ids}, {match_ids}")
        conn.commit()
        conn.close()
        return render_template('matches.html', user_data=user_data, names=names, sent=match_ids)

    else:
        return "login fail"


#Sent - Pending
#Received - Requests
@app.route('/matches/requests')
def matches_requests():
    if "user" in session:
        user_id = int(session.get("user_id"))
        print("MATCHES")
        ### Get Matches
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT user_id
                       FROM match_handler
                       WHERE accepted LIKE ? and sent NOT LIKE ?
                       """, (f"%,{user_id},%", f"%,{user_id},%"))
        match_ids = [str(item[0]) for item in cursor.fetchall()]
        ###
        ### Get Matches DATA
        placeholders = ','.join('?' for _ in match_ids)

        ### Execute the query with the correct number of placeholders
        cursor.execute(
            f"SELECT * FROM info WHERE user_id IN ({placeholders});", 
            match_ids
        )
        user_data = cursor.fetchall()
        print(user_data)

        cursor.execute(
            f"""
            SELECT username
            FROM users
            WHERE user_id IN ({placeholders})
            ORDER BY user_id ASC;
            """,
            match_ids
        )

        names = cursor.fetchall()

        conn.commit()
        conn.close()
        return render_template('matches_requests.html', user_data=user_data, names=names, sent=match_ids)

    else:
        return "login fail"
    

@app.route('/match_request/<receiver>')
def match_request(receiver):
    if "user" in session:
        user_id = int(session.get("user_id"))
        print(session)
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
        """
        UPDATE match_handler
        SET sent = sent || ?
        WHERE user_id = ?;""", ((f"{user_id},"), receiver,)
        )
        
        cursor.execute(
        """
        UPDATE match_handler
        SET accepted = accepted || ?
        WHERE user_id = ?;""", (f"{receiver}," ,user_id,)
        )

        conn.commit()
        conn.close()
        return redirect(url_for('find'))


    else:
        return "login fail"
    
@app.route('/matches/pending')
def matches_pending():
    if "user" in session:
        user_id = int(session.get("user_id"))
        print("MATCHES")
        ### Get Matches
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
                        SELECT accepted, sent FROM match_handler WHERE user_id = ?;""", (user_id,))
        
        ids = cursor.fetchall()
        accepted = (ids[0][0]).split(',')
        sent = (ids[0][1]).split(',')
        print(accepted, sent)
        pending = []

        for id in accepted:
            if id not in sent:
                pending.append(id)

        

        pending_str = ','.join(pending)


        cursor.execute(f"""
                    SELECT info.*, users.username
                    FROM info
                    JOIN users ON users.user_id = info.user_id
                    WHERE info.user_id IN ({pending_str}) ;""")
                
        
        user_data = cursor.fetchall()
        print(user_data)
        conn.commit()
        conn.close()
        return render_template('matches_pending.html', user_data=user_data, names=user_data, sent=pending)

    else:
        return "login fail"

if __name__ == '__main__':
    app.run(port=2222, debug=True)