import os
from flask import Flask, render_template, request, redirect, url_for
import markdown

app = Flask(__name__)

PAGES_FOLDER = "pages"

# Create pages folder if not exists
if not os.path.exists(PAGES_FOLDER):
    os.makedirs(PAGES_FOLDER)


def get_files():
    return sorted([f for f in os.listdir(PAGES_FOLDER) if f.endswith(".md")])


@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        files=get_files(),
        current_page=None
    )


@app.route("/page/<name>")
def view_page(name):
    path = os.path.join(PAGES_FOLDER, name)

    if not os.path.exists(path):
        return "Page not found"

    with open(path, "r", encoding="utf-8") as f:
        html = markdown.markdown(
            f.read(),
            extensions=["fenced_code", "tables"]
        )

    return render_template(
        "view.html",
        content=html,
        name=name,
        files=get_files(),
        current_page=name
    )


@app.route("/edit/<name>", methods=["GET", "POST"])
def edit_page(name):
    path = os.path.join(PAGES_FOLDER, name)

    if request.method == "POST":
        with open(path, "w", encoding="utf-8") as f:
            f.write(request.form["content"])
        return redirect(url_for("view_page", name=name))

    content = ""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

    return render_template(
        "edit.html",
        name=name,
        content=content,
        files=get_files(),
        current_page=name
    )


@app.route("/delete/<name>")
def delete_page(name):
    path = os.path.join(PAGES_FOLDER, name)
    if os.path.exists(path):
        os.remove(path)
    return redirect(url_for("dashboard"))


@app.route("/create", methods=["POST"])
def create_page():
    name = request.form.get("name")

    if not name.endswith(".md"):
        name += ".md"

    path = os.path.join(PAGES_FOLDER, name)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {name.replace('.md','')}\n\nStart writing here...")

    return redirect(url_for("edit_page", name=name))


if __name__ == "__main__":
    app.run(debug=True)
