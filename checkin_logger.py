from datetime import datetime

EVENT_LOGS = {}

def log_checkin(event_id: str, ticket_id: str):
    if event_id not in EVENT_LOGS:
        EVENT_LOGS[event_id] = []

    EVENT_LOGS[event_id].append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ticket_id": ticket_id
    })


def get_event_logs(event_id: str):
    return EVENT_LOGS.get(event_id, [])