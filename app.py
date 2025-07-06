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

# @app.route("/blogs/<section>/<slug>")
# def blog(section, slug):
#     valid_sections = ["inspirations", "reviews", "notes", "fundamentals"]
#     if section not in valid_sections:
#         abort(404)

#     filepath = os.path.join("blog_posts", section, f"{slug}.md")
#     if not os.path.exists(filepath):
#         abort(404)

#     post = frontmatter.load(filepath)
#     content_html = markdown2.markdown(post.content)
#     # print(f"Looking for: blog_posts/{section}/{slug}.md")
#     return render_template("blog_post.html", title=post['title'], date=post['date'], section=post['section'], content=content_html)

@app.route("/blogs/<section>/<slug>")
def blog(section, slug):
    valid_sections = ["inspirations", "reviews", "notes", "fundamentals"]
    if section not in valid_sections:
        abort(404)

    filepath = os.path.join("blog_posts", section, f"{slug}.md")
    if not os.path.exists(filepath):
        print(f"Missing file: {filepath}")  # Debug line
        abort(404)

    post = frontmatter.load(filepath)
    content_html = markdown2.markdown(post.content)
    return render_template(
        "blog_post.html",
        title=post.get("title", "Untitled"),
        date=post.get("date", "Unknown date"),
        section=post.get("section", section),
        content=content_html
    )

@app.route("/blogs/<section>/")
def blog_section_index(section):
    valid_sections = ["inspirations", "reviews", "notes", "fundamentals"]
    if section not in valid_sections:
        abort(404)

    root = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(root, "blog_posts", section)

    if not os.path.exists(folder_path):
        abort(404)

    posts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            slug = filename[:-3]  # remove .md
            filepath = os.path.join(folder_path, filename)
            post = frontmatter.load(filepath)
            posts.append({
                "title": post.get("title", slug),
                "date": post.get("date", ""),
                "slug": slug
            })

    # Sort by date (optional)
    posts.sort(key=lambda x: x["date"], reverse=True)

    return render_template("blog_index.html", section=section, posts=posts)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)