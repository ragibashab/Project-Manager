from flask import Flask, render_template, request, redirect, url_for, flash
from scraper import scrape_website
from filtering import filter_leads
from database import create_database, insert_lead, get_all_leads
from user import User, get_user, get_user_by_username, create_user_table, create_user
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

create_database()
create_user_table()

@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = get_user_by_username(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        create_user(username, hashed_password)
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        url = request.form.get("url")
        industry = request.form.get("industry")
        match_type = request.form.get("match_type")

        try:
            leads = scrape_website(url)
            if leads:
                for lead in leads:
                    lead["url"] = url
                    lead["industry"] = industry
                    insert_lead(lead)

                filters = {"industry": industry} if industry else {}
                filtered_leads = filter_leads(leads, filters, match_type)
                if filtered_leads:
                    return render_template("index.html", leads=filtered_leads)
                else:
                    return render_template("index.html", error="No leads found matching your criteria.")
            else:
                return render_template("index.html", error="Could not scrape the website.")
        except Exception as e:
            return render_template("index.html", error=f"An error occurred: {e}")

    return render_template("index.html", leads=[])

@app.route("/leads")
@login_required
def leads():
    all_leads = get_all_leads()
    return render_template("leads.html", leads=all_leads)

if __name__ == "__main__":
    app.run(debug=True)
