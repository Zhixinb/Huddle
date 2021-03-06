from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from huddle.router import Router
from huddle.workspace import Workspace, Permission
from apscheduler.schedulers.background import BackgroundScheduler
from flask_talisman import Talisman
import os
import sys
import json
import ast
import redis
import signal
import atexit
import pickle

IS_HEROKU = os.environ.get('IS_HEROKU', False)
# TTL is 12h in prod
REDIS_TTL_S = 60*60*12 if IS_HEROKU else 0
db = None
if IS_HEROKU:
    redis_url = os.getenv('REDISTOGO_URL', None)
    db = redis.from_url(redis_url)

# initialize Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# use talisman for SSL if in prod
talisman = Talisman(app) if IS_HEROKU else None

socketio = SocketIO(app, cors_allowed_origins=["http://localhost:8080", "https://robin-dev.d1jfi0qjq3gsdb.amplifyapp.com", "https://main.d1jfi0qjq3gsdb.amplifyapp.com"])
ROOM_NAMESPACE = 'ROOM/'
ROUTER_NAMESPACE = 'ROUTER/'
ROOMS = {}  # dict to track active workspaces
ROUTERS = {}  # dict to track routers

def get_user_rooms(rooms, uid):
    return [room_key for room_key,
                 workspace in rooms.items() if workspace.has_access(uid)]

@socketio.on('create')
def on_create(data):
    """Create a workspace"""
    uid = data['uid']
    ws = Workspace(uid)
    room = ws.workspace_id
    ROOMS[room] = ws
    ROUTERS[room] = Router()
    join_room(room)
    user_room = get_user_rooms(ROOMS, uid)
    emit('created_room', {'rooms': user_room})

    # Debug
    # print("create is called on server:" + str(user_room), file=sys.stderr)
    # print("create is called by user:" + data['sid'], file=sys.stderr)
    # for index, r in enumerate(list(ROOMS.values())):
    #     print(str(index) + ":" + json.dumps(r.to_json()), file=sys.stderr)

@socketio.on('get_rooms')
def on_get_rooms(data):
    uid = data['uid']
    user_room = get_user_rooms(ROOMS, uid)
    emit('created_room', {'rooms': user_room})

@socketio.on('join')
def on_join(data):
    """Join a workspace"""
    uid = data['uid']
    room = data['room']
    sid = data['sid']
    if room in ROOMS:
        # add user and rebroadcast workspace object
        join_room(room)
        ws = ROOMS[room]
        ws.users.add(uid, sid)
        send(ws.to_json(), room=room)

        router = ROUTERS[room]
        room_data = router.get_state()

        emit('update_slides_result', {
             'new_state': room_data})

    else:
        emit('error', {'error': 'Unable to join room. Room does not exist: ' + room})


@socketio.on('leave')
def on_leave(data):
    uid = data['uid']
    room = data['room']
    if room in ROOMS:
        # remove player and rebroadcast game object
        leave_room(room)
        ws = ROOMS[room]
        ws.users.remove(uid)
        send(ws.to_json(), room=room)


@socketio.on('change')
def on_change(data):
    """Change a workspace"""
    key = data['key']
    text = data['text']
    uid = data['uid']
    room = data['room']
    if room in ROOMS:
        ws = ROOMS[room]
        router = ROUTERS[room]

    # BASIC FLOW:
    #


@socketio.on('get_share_state')
def on_get_share_state(data):
    uid = data['uid']
    room = data['room']

    if room in ROOMS:
        ws = ROOMS[room]

        if uid in ROOMS[room].user_perms:
            emit('share_state_result', {'whitelist': ws.get_user_perms(),
                                        'global_share_state': ws.global_share_state,
                                        'can_share': ws.get_can_share(uid),
                                        'permission_map': Workspace.getPermissionDict(),
                                        'role': ws.get_role(uid)})
        else:
            emit('share_state_result', {'whitelist': [],
                                        'global_share_state': {},
                                        'can_share': ws.get_can_share(uid),
                                        'permission_map': Workspace.getPermissionDict(),
                                        'role':  ws.get_role(uid)})


@socketio.on('get_enter_room_perm')
def on_get_enter_room_perm(data):
    uid = data['uid']
    room = data['room']
    if room in ROOMS and (uid in ROOMS[room].user_perms or ROOMS[room].global_share_state is not Permission.PERM_DENIED):
        emit('enter_room_perm_result', {'result': True})
    else:
        emit('enter_room_perm_result', {'result': False})


@socketio.on('set_global_share_state')
def on_set_global_share_state(data):
    uid = data['uid']
    room = data['room']
    state = data['new_state']
    if room in ROOMS and uid in ROOMS[room].user_perms:
        ROOMS[room].global_share_state = Permission.VIEWER if state else Permission.PERM_DENIED
        emit('set_global_share_state_result', {
             'result': ROOMS[room].global_share_state}, room=room)
    else:
        emit('error', {'error': 'Unable to update share state'})

# TODO: server-side permission checks for add/remove, modify whitelist
# TODO: broadcast to changed listing user if they are in the room about their role


@socketio.on('update_whitelist')
def on_update_whitelist(data):
    uid = data['uid']
    room = data['room']
    action = data['action']
    if room in ROOMS and uid in ROOMS[room].user_perms:
        listing = data['listing']
        ws = ROOMS[room]

        role_uid = str(listing['uid'])
        if action == 'add':
            ws.user_perms[role_uid] = Permission(int(listing['perm']))
        elif action == 'remove':
            del ws.user_perms[str(listing['uid'])]
        emit('update_whitelist_result', {'whitelist': ws.get_user_perms(),
                                         'global_share_state': ws.global_share_state,
                                         'can_share': ws.get_can_share(uid),
                                         'permission_map': Workspace.getPermissionDict(),
                                         'target_uid': role_uid,
                                         'new_role': ws.get_role(role_uid),
                                         'new_can_share': ws.get_can_share(role_uid)}, room=room)
    else:
        emit('error', {'error': 'Unable to update whitelist'})


@socketio.on('new_slide')
def on_new_slide(data):
    uid = data['uid']
    room = data['room']
    if room in ROOMS:
        router = ROUTERS[room]
        router.add_new_slide()
        room_data = router.get_state()

        emit('update_slides_result', {
             'new_state': room_data}, room=room)
    else:
        emit('error', {'error': 'Unable to update slides states'})


@socketio.on('update_slides')
def on_update_slides(data):
    uid = data['uid']
    room = data['room']
    state = data['new_state']
    if room in ROOMS:
        router = ROUTERS[room]
        router.update_state(state)

        emit('update_slides_result', {
             'new_state': state}, room=room)
    else:
        emit('error', {'error': 'Unable to update slides states'})

@socketio.on('update_component_id')
def on_update_component_id(data):
    uid = data['uid']
    room = data['room']
    s_id = data['s_id']
    c_id = data['c_id']
    if room in ROOMS:
        router = ROUTERS[room]
        changes = data['changes']
        router.update_component_id(s_id, c_id, changes)
        room_data = router.get_state()
        
        emit('update_slides_result', {
            'new_state': room_data,
            's_id': s_id}, room=room)

    else:
        emit('error', {'error': 'Unable to update widget states'})

@socketio.on('update_component_id_batch')
def on_update_component_id_batch(data):
    uid = data['uid']
    room = data['room']
    s_id = data['s_id']
    if room in ROOMS:
        router = ROUTERS[room]
        changes = data['changes']
        for key in changes:
            router.update_component_id(s_id, key, changes[key])
        room_data = router.get_state()
        
        emit('update_slides_result', {
            'new_state': room_data,
            's_id': s_id}, room=room)

    else:
        emit('error', {'error': 'Unable to batch update widget states'})

@socketio.on('new_component')
def on_new_component(data):
    uid = data['uid']
    room = data['room']
    component = data['component']
    if room in ROOMS:
        router = ROUTERS[room]
        router.add_new_component(component)
        room_data = router.get_state()

        emit('update_slides_result', {
            'new_state': room_data}, room=room)

    else:
        emit('error', {'error': 'Unable to create new widget'})


@socketio.on('new_connection')
def on_new_connection(data):
    uid = data['uid']
    room = data['room']
    if room in ROOMS:
        router = ROUTERS[room]
        router.add_new_connection(
            data['s_id'], data['c_id0'], data['c_id1'], data['signal'], data['slot'], data['expression'])
        room_data = router.get_state()

        emit('update_slides_result', {
            'new_state': room_data,
            's_id': data['s_id']}, room=room)
    else:
        emit('error', {'error': 'Unable to create new connection'})

@socketio.on('remove_connection')
def on_remove_connection(data):
    uid = data['uid']
    room = data['room']
    if room in ROOMS:
        router = ROUTERS[room]
        router.remove_connection(
            data['s_id'], data['c_id0'], data['c_id1'], data['signal'], data['slot'])
        room_data = router.get_state()

        emit('update_slides_result', {
            'new_state': room_data,
            's_id': data['s_id']}, room=room)
    else:
        emit('error', {'error': 'Unable to remove connection'})

@socketio.on('remove_component')
def on_remove_component(data):
    uid = data['uid']
    room = data['room']
    sid = data['s_id']
    cid = data['c_id']
    if room in ROOMS:
        router = ROUTERS[room]
        router.remove_component(sid, cid)
        room_data = router.get_state()

        emit('update_slides_result', {
            'new_state': room_data,
            's_id': sid, 'c_id': cid}, room=room)
    else:
        emit('error', {'error': 'Unable to remove component'})

@socketio.on('remove_slide')
def on_remove_slide(data):
    uid = data['uid']
    room = data['room']
    sid = data['s_id']
    if room in ROOMS:
        router = ROUTERS[room]
        router.remove_slide(sid)
        room_data = router.get_state()

        emit('update_slides_result', {
            'new_state': room_data}, room=room)
    else:
        emit('error', {'error': 'Unable to remove slide'})

@socketio.on('upload_json')
def on_upload_json(data):
    uid = data['uid']
    room = data['room']

    if room in ROOMS:
        router = ROUTERS[room]
        slides_file = data['slides_file']
        dict_str = slides_file.decode("UTF-8")
        decoded_data = ast.literal_eval(dict_str)

        # print(type(decoded_data))
        # print(decoded_data)

        router.update_state(decoded_data)
        room_data = router.get_state()

        emit('update_slides_result', {
            'new_state': room_data}, room=room)
             
    else:
        emit('error', {'error': 'Unable to upload json file'})

# If user is the owner, then room is deleted from memory and db, else user is removed from the room's access
@socketio.on('deleteWorkspace')
def on_delete_workspace(data):
    uid = data['uid']
    room = data['room']

    if room in ROOMS:
        ws = ROOMS[room]
        perm = ws.get_user_perm(uid)
        
        if perm is Permission.OWNER:
            # remove the room from ROOMS, ROUTERS, and DB
            ROOMS.pop(room, None)
            ROUTERS.pop(room, None)

            # Deleting from DB has race condition with background scheduler for backing up ROOMS and ROUTERS to db
            # can be avoid if removing scheduler after able to detect SIGTERM for backup only on exit, or watch dicts and backup on change
            if IS_HEROKU:
                db.delete(ROOM_NAMESPACE + room, ROUTER_NAMESPACE + room)
        else:
            # remove uid from user_perms
            ws.remove_user_perm(uid)

        user_room = get_user_rooms(ROOMS, uid)
        emit('created_room', {'rooms': user_room})       
             
    else:
        emit('error', {'error': 'Unable to delete/remove access of workspace'})

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def save_game_state(namespace, room, state):
    if IS_HEROKU:
        db.setex(namespace + room, REDIS_TTL_S, pickle.dumps(state))
    # print("saving -- key:" + namespace + room + ", value:" + str(pickle.dumps(state)))

def handle_exit():
    # if IS_HEROKU:
        # Clear db
        # db.flushdb()
        # save dicts
    for room in ROOMS:
        save_game_state(ROOM_NAMESPACE, room, ROOMS[room])
    for room in ROUTERS:
        save_game_state(ROUTER_NAMESPACE, room, ROUTERS[room])

def load_from_db():
    if IS_HEROKU:
        for key in db.scan_iter():
            key = str(key, 'utf-8', 'ignore')
            if key.startswith(ROOM_NAMESPACE):
                room = remove_prefix(key, ROOM_NAMESPACE)
                ROOMS[room] = pickle.loads(db.get(key))
            elif key.startswith(ROUTER_NAMESPACE):
                room = remove_prefix(key, ROUTER_NAMESPACE)
                ROUTERS[room] = pickle.loads(db.get(key))     
        # print("loading -- ROOMS:" + str(ROOMS))
        # print("loading -- ROUTERS:" + str(ROUTERS))

if __name__ == '__main__':
    # currently no way to detect SIGNTERM or SIGKILL from Heroku when dyno restarts during redeployment
    # atexit, signal.signal do not work with current setup
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=handle_exit, trigger="interval", seconds=10)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    if IS_HEROKU:
        load_from_db()    

    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
