from flask import Flask, render_template, request, abort
import numpy as np
import os
import frontmatter
import markdown2



app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = None
    if request.method == "POST":
        try:
            dBm = float(request.form["dBm"])  #dBm
            result = np.round(10**(dBm/10), 4)           #mW
        except ValueError:
            result = "Invalid input"
    return render_template("calculator.html", result=result)

# @app.route("/blogs/<section>")
# def blog_section(section):
#     titles = {
#         "inspirations": "Inspirations",
#         "reviews": "Technology Reviews",
#         "notes": "Technical Notes",
#         "fundamentals": "Fundamentals"
#     }
#     title = titles.get(section, "Blog Section")
#     return f"<h2>{title} blog coming soon!</h2>"

@app.route("/blogs/<section>/<slug>")
def blog(section, slug):
    valid_sections = ["inspirations", "reviews", "notes", "fundamentals"]
    if section not in valid_sections:
        abort(404)

    filepath = os.path.join("blog_posts", section, f"{slug}.md")
    if not os.path.exists(filepath):
        abort(404)

    post = frontmatter.load(filepath)
    content_html = markdown2.markdown(post.content)
    return render_template("blog_post.html", title=post['title'], date=post['date'], section=post['section'], content=content_html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)