from flask import Flask, render_template, jsonify, request
import requests
import logging
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)

MAIN_API = "http://10.148.0.2:9000"

EVENT_LOGS = {}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def send_ticket_to_server(ticket_id):
    try:
        url = f"{MAIN_API}/v1/tickets/check-in/{ticket_id}"
        r = requests.post(url, timeout=5)
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def send_event_to_server(event_id):
    try:
        url = f"{MAIN_API}/v1/events/{event_id}"
        r = requests.get(url, timeout=5)
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/events/check-in/<event_id>")
def event_check_in(event_id):
    app.logger.info(f"[EVENT] check-in request: {event_id}")
    app_event_logs(event_id, f"[EVENT] check-in: {event_id}")

    result = send_event_to_server(event_id)

    if (
        not result
        or result.get("errors")
        or result.get("detail") == "Event not found"
    ):
        app.logger.warning(f"[EVENT] not found: {event_id}")
        app_event_logs(event_id,f"[EVENT] not found")
        return render_template("notfoundpage.html", event_id=event_id), 404

    app.logger.info(f"[EVENT] response: {result}")
    app_event_logs(event_id,f"[EVENT] response: {result}")

    summary = {
        "checkin_time": result["checked_in_date"],
        "user_id": result["user"],
        "ticket_type": result["ticket_types"][0]["name"],
        "ticket_id": result["ticket_types"][0]["ticket_id"],
    }

    return render_template(
        "event.html",
        summary=summary,
        raw=result,
        event_id=event_id,
    )


@app.route("/v1/tickets/check-in/<ticket_id>", methods=["POST"])
def ticket_check_in(ticket_id):
    app_event_logs(ticket_id,f"[TICKET] check-in request: {ticket_id}")

    result = send_ticket_to_server(ticket_id)

    if result.get("status") == "error":
        app.logger.info(f"[TICKET] failed: {result}")
        app_event_logs(ticket_id,f"[TICKET] failed: {result}")
    else:
        app.logger.info(f"[TICKET] success: {result}")
        app_event_logs(ticket_id,f"[TICKET] success: {result}")

    return jsonify(result)

def app_event_logs(event_id, message):
    EVENT_LOGS.setdefault(event_id, []).append(message)

@app.route("/events/logs/<event_id>")
def get_event_logs(event_id):
    return jsonify(EVENT_LOGS.get(event_id, []))