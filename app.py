from flask import Flask,render_template, request
import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app= Flask(__name__)
    #app.debug = True  # Set debug mode explicitly
    client = MongoClient(os.getenv("MONGODB_URI"))

    app.db = client.Microblog
    #entries=[]

    @app.route("/", methods= ["GET","POST"])
    def home():
    
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            #entries.append((entry_content,formatted_date))
            app.db.entries.insert_one({"content": entry_content,"date": formatted_date})

        entries_with_dates=[
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]


        return render_template("home.html",entries=entries_with_dates)




    #if __name__ == "__main__":
        #app.run(debug=True)  # Pass debug=True here too

    return app
