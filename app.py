from urllib.parse import urlparse
from flask import Flask, render_template, request

app = Flask(__name__)
submissions = []


def is_valid_url(url):
    p = urlparse(url.strip())
    return p.scheme in ("http", "https") and "." in p.netloc


@app.route("/", methods=["GET", "POST"])
def index():
    errors = []
    message = ""
    status = 200

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        reg_no = request.form.get("reg_no", "").strip()
        title = request.form.get("title", "").strip()
        url = request.form.get("url", "").strip()

        if not name:
            errors.append("Name is required")
            if not reg_no:
             errors.append("Registration number is required")
        if not title:
            errors.append("Assignment title is required")
        if not url:
            errors.append("Submission URL is required")
        elif not is_valid_url(url):
            errors.append("Submission URL is invalid")

        if errors:
            status = 400
        else:
            submissions.append(
                {"name": name, "reg_no": reg_no, "title": title, "url": url}
            )
            message = "Submission saved"

    return render_template(
        "index.html", errors=errors, message=message, submissions=submissions
    ), status


if __name__ == "__main__":
    app.run(debug=True)