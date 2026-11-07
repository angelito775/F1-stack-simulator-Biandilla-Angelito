# Flask Stack and Queue Simulators

**Name:** Angelito Biandilla P.  
**Section:** BSIT WMT 4-2

This repository contains two independent Flask applications that demonstrate LIFO stack and FIFO queue operations.

## Requirements

- Python 3.9 or newer
- Flask (`pip install -r requirements.txt`)

## Stack Simulator

From the repository root, run:

```powershell
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

Use **Push**, **Pop**, **Peek**, and **Clear** to operate on the stack. The top item is shown first; popped values appear in the removed-items area.

## Queue Simulator

From the repository root, run:

```powershell
python queue-simulator\app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

Use **Enqueue**, **Dequeue**, **Peek**, and **Clear** to operate on the queue. Values are displayed from **Front** to **Rear**; dequeued values appear in the removed-items area.

Both apps keep data in the browser's signed Flask session. Set the `FLASK_SECRET_KEY` environment variable to use a persistent secret key across restarts; otherwise, a random development key is generated when the app starts.

Each app accepts nonblank values up to 24 characters and limits the structure to 20 values. The removed-items history keeps the 20 most recent removals and is reset by Clear.
