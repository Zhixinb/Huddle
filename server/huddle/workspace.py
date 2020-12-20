"""Object for tracking workspace status"""
from datetime import datetime
import time
import random
import math
import string
import os
from enum import IntEnum
from huddle import users

class Permission(IntEnum):
    OWNER = 0
    EDITOR = 1
    VIEWER = 2
    PERM_DENIED = 3

class Workspace(object):
    workspace_ids = set()

    # pylint: disable=too-many-instance-attributes
    """Object for tracking game stats"""
    def __init__(self, host, permission=Permission.OWNER):
        self.date_created = datetime.now()
        self.date_modified = self.date_created

        self.workspace_id = self.generate_workspace_id()
        self.users = users.Users()
        self.user_perms = {}
        # self.global_share_state = Permission.PERM_DENIED

        # initialize workspace
        self.generate_workspace(host)

    def to_json(self):
        """Serialize object to JSON"""
        return {
            "workspace_id": self.workspace_id,
            "users": self.users.as_dict(),
            "date_created": str(self.date_created),
            "date_modified": str(self.date_modified),
            "user_perms" : self.user_perms,
            "global_share_state": self.global_share_state
        }

    def generate_workspace(self, host):
        self.user_perms[host] =  Permission.OWNER
        self.global_share_state = Permission.PERM_DENIED # SHOULD BE DENIED, testing

    def add_user(self, sid, param):
        """Add username to user array"""
        self.users.add(sid, param)

    def remove_user(self, sid):
        """Remove username to user array"""
        self.users.remove(sid)

    def has_access(self, sid):
        return sid in self.user_perms

    def get_user_perms(self):
        return [{"uid": uid, "perm": perm} for (uid, perm) in self.user_perms.items()]
    
    def get_user_perm(self, uid):
        if (uid in self.user_perms):
            return self.user_perms[uid]
        else:
            return self.global_share_state
    
    def get_role(self, uid):
        perm = self.get_user_perm(uid)
        return Permission(perm).name

    @classmethod
    def generate_workspace_id(cls):
        """Generate a random workspace ID"""
        id_length = 5

        candidate_id = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase) for _ in range(id_length))
        
        if candidate_id in Workspace.workspace_ids:
            return generate_workspace_id()
        else:
            return candidate_id

    @classmethod
    def getPermissionDict(cls):
        return {permission.name:permission.value for permission in Permission}

    def regenerate_id(self):
        self.workspace_id = self.generate_workspace_id()

    def uptime(self):
        # 2018-08-12 10:12:25.700528
        fmt = '%Y-%m-%d %H:%M:%S'
        d1 = self.date_created
        d2 = self.date_modified
        # Convert to Unix timestamp
        d1_ts = time.mktime(d1.timetuple())
        d2_ts = time.mktime(d2.timetuple())
        return round(float(d2_ts-d1_ts) / 60, 2)