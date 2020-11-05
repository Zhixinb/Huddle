import json
import random

class Users(object):
  def __init__(self):
    self.reset()

  def add(self, sid, param):
    self.users[sid] = param

  def remove(self, sid):
    if sid in self.users:
      del self.users[sid]

  def has_user(self, sid):
    return sid in self.users.keys()

  def reset(self):
    self.users = {}

  def as_dict(self):
    return {
      "users": self.users
    }
