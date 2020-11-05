from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, join_room, emit, send
from huddle.workspace import Workspace
import sys
import json

# initialize Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
ROOMS = {} # dict to track active workspaces

@socketio.on('create')
def on_create(data):
    """Create a workspace"""
    sid = data['sid']
    ws = Workspace(sid, permission="host-only")
    room = ws.workspace_id
    ROOMS[room] = ws
    join_room(room)
    user_room = [room_key for room_key, workspace in ROOMS.items() if workspace.has_user(sid)]
    emit('created_room', {'rooms': user_room})
    
    # Debug
    # print("create is called on server:" + room, file=sys.stderr)
    # print("create is called by user:" + data['sid'], file=sys.stderr)
    # for index, r in enumerate(list(ROOMS.values())):
    #     print(str(index) + ":" + json.dumps(r.to_json()), file=sys.stderr)

@socketio.on('join')
def on_join(data):
    """Join a workspace"""
    sid = data['sid']
    room = data['room']
    if room in ROOMS:
        # add user and rebroadcast workspace object
        join_room(room)
        ws = ROOMS[room]
        ws.users.add(sid, {"credential" : "mockCredential"})
        send(ws.to_json(), room=room)
    else:
        emit('error', {'error': 'Unable to join room. Room does not exist.'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)