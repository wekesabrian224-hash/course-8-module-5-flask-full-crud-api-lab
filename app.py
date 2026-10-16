from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


def find_event(event_id):
    # Return the Event with this id, or None if it doesn't exist
    for event in events:
        if event.id == event_id:
            return event
    return None


# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    new_id = max((e.id for e in events), default=0) + 1
    event = Event(new_id, data["title"])
    events.append(event)
    return jsonify(event.to_dict()), 201


# PATCH /events/<id> - Update the title of an event
@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    event = find_event(id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json(silent=True)
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    event.title = data["title"]
    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    event = find_event(id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return "", 204  # 204 No Content: success, empty body


if __name__ == "__main__":
    app.run(debug=True)