"""Flask web interface for the stack simulator."""
import os
import secrets

# TODO P1: Extend the imports with render_template, request, redirect,
# url_for, session, and flash. Import secrets and the completed Stack class.
from flask import Flask, flash, redirect, render_template, request, session, url_for

from stack_model import Stack

app = Flask(__name__)
# TODO P2: Set SECRET_KEY for the session and flash messages.
# This lesson uses short fictional stack values on localhost.
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)
MAX_ITEMS = 20
MAX_VALUE_LENGTH = 24
MAX_REMOVED = 20


@app.route("/")
def index():
    # TODO P3: Replace this temporary response with render_template.
    # Start by displaying the static index.html through Flask.
    # TODO P6: Restore stack values from session, reverse for display,
    # and pass items, size, popped, and highlight to the template.
    stack = Stack(session.get("stack_items", []))
    return render_template(
        "index.html",
        items=list(reversed(stack.items)),
        size=stack.size(),
        removed=session.get("stack_removed", []),
        highlight=session.get("stack_highlight", False),
    )


@app.route("/stack", methods=["POST"])
def operate():
    # TODO P4: Read action and value from request.form. Strip the value.
    # TODO P7: Restore the Stack and removed-item history from session.
    # TODO P8: Implement Push, Pop, Peek, and Clear with feedback.
    # Push accepts 1-24 characters and at most 20 current items.
    # Pop and Peek must handle an empty stack. Clear resets both lists.
    # Keep only the 20 most recently removed values.
    # TODO P9: Reassign session values, then redirect to the index route.
    # Use a peek flag when highlighting the top item.
    action = request.form.get("action", "")
    value = request.form.get("value", "").strip()
    stack = Stack(session.get("stack_items", []))
    removed = list(session.get("stack_removed", []))
    highlight = False

    if action == "push":
        if not value:
            flash("Enter a value before pushing it onto the stack.", "danger")
        elif len(value) > MAX_VALUE_LENGTH:
            flash(f"Values must be {MAX_VALUE_LENGTH} characters or fewer.", "danger")
        elif stack.size() >= MAX_ITEMS:
            flash(f"The stack can hold at most {MAX_ITEMS} values.", "danger")
        else:
            stack.push(value)
            flash(f"Pushed {value} onto the stack.", "success")
    elif action == "pop":
        value = stack.pop()
        if value is None:
            flash("The stack is empty; there is nothing to pop.", "danger")
        else:
            removed.insert(0, value)
            removed = removed[:MAX_REMOVED]
            flash(f"Popped {value} from the stack.", "info")
    elif action == "peek":
        value = stack.peek()
        if value is None:
            flash("The stack is empty; there is nothing to peek at.", "danger")
        else:
            highlight = True
            flash(f"Top of the stack: {value}.", "info")
    elif action == "clear":
        stack.clear()
        removed.clear()
        flash("The stack and removed items have been cleared.", "success")
    else:
        flash("Choose a valid stack operation.", "danger")

    session["stack_items"] = stack.items
    session["stack_removed"] = removed
    session["stack_highlight"] = highlight
    return redirect(url_for("index"))


@app.route("/contact")
def contact():
    # TODO P5: Render contact.html as a placeholder landing page.
    # A validated contact form belongs to a later lesson.
    return render_template("contact.html")


if __name__ == "__main__":
    app.run()
