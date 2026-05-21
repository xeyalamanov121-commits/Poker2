import socketio
import eventlet
import random

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

rooms = {}

class GameRoom:
    def __init__(self):
        self.players = {}
        self.max_players = 6

@sio.event
def connect(sid, environ):
    print(f"Connected: {sid}")

@sio.event
def create_room(sid, data):
    room_id = f"POKER{random.randint(1000,9999)}"
    rooms[room_id] = GameRoom()
    sio.enter_room(sid, room_id)
    rooms[room_id].players[sid] = {"name": data["name"], "chips": 10000}
    sio.emit("room_created", {"room_id": room_id, "name": data["name"]}, to=sid)

@sio.event
def join_room(sid, data):
    room_id = data["room_id"]
    if room_id in rooms and len(rooms[room_id].players) < 6:
        sio.enter_room(sid, room_id)
        rooms[room_id].players[sid] = {"name": data["name"], "chips": 10000}
        sio.emit("update_players", {"players": list(rooms[room_id].players.values())}, room=room_id)
    else:
        sio.emit("error", {"msg": "Otaq tapılmadı və ya dolu!"}, to=sid)

@sio.event
def disconnect(sid):
    for rid, room in list(rooms.items()):
        if sid in room.players:
            del room.players[sid]
            sio.emit("update_players", {"players": list(room.players.values())}, room=rid)
            if not room.players:
                del rooms[rid]
            break

if __name__ == '__main__':
    print("Server işləyir → http://localhost:5000")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
