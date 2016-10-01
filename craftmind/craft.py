import json
import logging
import os

LOG = logging.getLogger(__name__)


class Craft(object):

    def __init__(self, directory):
        self.directory = directory
        self.users = self._read_json('usercache.json') or []

    @property
    def ops(self):
        return self._read_json('ops.json') or []

    @property
    def server_properties(self):
        try:
            path = os.path.join(self.directory, 'server.properties')
            return parse_properties(open(path, 'r').read())
        except Exception as e:
            LOG.exception(e)
            return None

    def user_stats(self, username):
        user = self._find_user_by_name(username)
        if not user:
            LOG.error("Failed to find id for user %s. Cannot load user stats.",
                      username)
            return {}
        return self._load_stats(user)

    def _read_json(self, relpath):
        try:
            path = os.path.join(self.directory, relpath)
            return json.load(open(path, 'r'))
        except Exception as e:
            LOG.exception(e)
            return None

    def _load_stats(self, user):
        user_id = user['uuid']
        path = os.path.join('world/stats/%s.json' % user_id)
        stats = self._read_json(path)
        if not stats:
            LOG.warning("No stats found for user %s [%s]", user['name'], user['uuid'])
        else:
            LOG.info("Loaded stats for user %s [%s]", user['name'], user['uuid'])
        return parse_user_stats(stats)

    def _find_user_by_name(self, username):
        for user in self.users:
            if user['name'] == username:
                return user


def parse_user_stats(data):
    result = {}
    for k, v in data.items():
        category, section = k.split('.', 1)
        if category not in result:
            result[category] = {}
        result[category][section] = v
    return result


def parse_properties(contents):
    result = []
    for line in contents.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        result.append(line.split('=', 1))
    result.sort(key=lambda x: x[0])
    return result
