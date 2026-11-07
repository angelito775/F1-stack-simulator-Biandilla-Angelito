"""Flask web interface for the queue simulator."""
import os
import secrets
from pathlib import Path

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from queue_model import Queue

APP_DIR = Path(__file__).resolve().parent
app = Flask(
    __name__,
    root_path=str(APP_DIR),
    template_folder=str(APP_DIR / "templates"),
    static_folder=str(APP_DIR / "static"),
)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)
MAX_ITEMS = 20
MAX_VALUE_LENGTH = 24
MAX_REMOVED = 20


@app.route("/")
def index():
    queue = Queue(session.get("queue_items", []))
    return render_template(
        "index.html",
        items=queue.items,
        size=queue.size(),
        removed=session.get("queue_removed", []),
        highlight=session.get("queue_highlight", False),
    )


@app.route("/queue", methods=["POST"])
def operate():
    action = request.form.get("action", "")
    value = request.form.get("value", "").strip()
    queue = Queue(session.get("queue_items", []))
    removed = list(session.get("queue_removed", []))
    highlight = False

    if action == "enqueue":
        if not value:
            flash("Enter a value before enqueueing it.", "danger")
        elif len(value) > MAX_VALUE_LENGTH:
            flash(f"Values must be {MAX_VALUE_LENGTH} characters or fewer.", "danger")
        elif queue.size() >= MAX_ITEMS:
            flash(f"The queue can hold at most {MAX_ITEMS} values.", "danger")
        else:
            queue.enqueue(value)
            flash(f"Enqueued {value} at the rear of the queue.", "success")
    elif action == "dequeue":
        value = queue.dequeue()
        if value is None:
            flash("The queue is empty; there is nothing to dequeue.", "danger")
        else:
            removed.insert(0, value)
            removed = removed[:MAX_REMOVED]
            flash(f"Dequeued {value} from the front of the queue.", "info")
    elif action == "peek":
        value = queue.peek()
        if value is None:
            flash("The queue is empty; there is nothing to peek at.", "danger")
        else:
            highlight = True
            flash(f"Front of the queue: {value}.", "info")
    elif action == "clear":
        queue.clear()
        removed.clear()
        flash("The queue and removed items have been cleared.", "success")
    else:
        flash("Choose a valid queue operation.", "danger")

    session["queue_items"] = queue.items
    session["queue_removed"] = removed
    session["queue_highlight"] = highlight
    return redirect(url_for("index"))


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run()
