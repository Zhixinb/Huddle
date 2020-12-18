"""Object for tracking workspace status"""
from datetime import datetime
import time
import random
import math
import string
import os
from huddle import users

class Permission:
    OWNER = 0
    CAN_EDIT = 1
    CAN_VIEW = 2

class Workspace(object):
    workspace_ids = set()

    # pylint: disable=too-many-instance-attributes
    """Object for tracking game stats"""
    def __init__(self, host, permission="host-only"):
        self.permission = permission
        self.workspace_id = self.generate_workspace_id()
        self.date_created = datetime.now()
        self.date_modified = self.date_created
        self.users = users.Users()
        self.user_perms = {}

        # gererate board
        self.generate_workspace(host)

    def to_json(self):
        """Serialize object to JSON"""
        return {
            "workspace_id": self.workspace_id,
            "users": self.users.as_dict(),
            "date_created": str(self.date_created),
            "date_modified": str(self.date_modified),
            "user_perms" : self.user_perms
        }

    def generate_workspace(self, host):
        # TODO: Initialize workspace
        self.user_perms[host] =  Permission.OWNER
        return

    def add_user(self, sid, param):
        """Add username to user array"""
        self.users.add(sid, param)

    def remove_user(self, sid):
        """Remove username to user array"""
        self.users.remove(sid)

    def has_access(self, sid):
        return sid in self.user_perms

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