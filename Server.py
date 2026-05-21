import socketio
import eventlet
import os
import random

sio = socketio.Server(cors_allowed_origins="*", async_mode='eventlet')
app = socketio.WSGIApp(sio)

rooms = {}

class GameRoom:
    def __init__(self):
        self.players = {}

@sio.event
def connect(sid, environ):
    print(f"Connected: {sid}")

@sio.event
def create_room(sid, data):
    room_id = f"POKER{random.randint(1000,9999)}"
    rooms[room_id] = GameRoom()
    sio.enter_room(sid, room_id)
    rooms[room_id].players[sid] = {"name": data.get("name", "Vanqa"), "chips": 10000}
    sio.emit("room_created", {"room_id": room_id}, to=sid)

@sio.event
def join_room(sid, data):
    room_id = data.get("room_id")
    if room_id in rooms and len(rooms[room_id].players) < 6:
        sio.enter_room(sid, room_id)
        rooms[room_id].players[sid] = {"name": data.get("name", "Player"), "chips": 10000}
        sio.emit("update_players", {"players": list(rooms[room_id].players.values())}, room=room_id)
    else:
        sio.emit("error", {"msg": "Otaq tapılmadı!"}, to=sid)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Server {port} portunda işləyir...")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', port)), app)
