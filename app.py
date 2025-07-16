from flask import Flask, render_template, request
from scraper import scrape_website
from filtering import filter_leads

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        industry = request.form.get("industry")

        leads = scrape_website(url)
        if leads:
            filters = {"industry": industry} if industry else {}
            filtered_leads = filter_leads(leads, filters)
            return render_template("index.html", leads=filtered_leads)
        else:
            return render_template("index.html", error="Could not scrape the website.")

    return render_template("index.html", leads=[])

if __name__ == "__main__":
    app.run(debug=True)
