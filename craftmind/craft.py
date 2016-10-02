import json
import logging
import os

from nbt.nbt import NBTFile

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

    @property
    def level_data(self):
        return self._read_nbt('world/level.dat') or {}

    def user_comparison(self, *usernames):
        def add_user_data(result, user_stats, name):
            """Insert the data into result as follows:

                data looks like {<category>: {<stat>: <val>}}
                result looks like {<category>: {<stat>: {<name>: <val>}}}
            """
            for category, data in user_stats.items():
                if category not in result:
                    result[category] = {}

                for stat, val in data.items():
                    if stat not in result[category]:
                        result[category][stat] = {}

                    result[category][stat][name] = val

        result = {}
        for name in usernames:
            userdata = self.user_stats(name)
            if not userdata:
                LOG.error("Failed to compile user comparison data for %s", usernames)
                return {}

            add_user_data(result, userdata, name)
        return result

    def player_comparison(self, *usernames):
        def add_player_data(result, data, name):
            """
            {<stat>: {<name>: <val>}}
            """
            for key, val in data.items():
                if key not in result:
                    result[key] = {}
                if key == 'Inventory':
                    result[key][name] = Inventory(val)
                elif key == 'Attributes':
                    result[key][name] = {x['Name']: x['Base'] for x in val}
                else:
                    result[key][name] = val

        result = {}
        for name in usernames:
            playerdata = self.player_data(name)
            if not playerdata:
                LOG.error("Failed to compile player comparison data for %s", usernames)
                return {}

            add_player_data(result, playerdata, name)
        return result

    def user_stats(self, username):
        user = self._find_user_by_name(username)
        if not user:
            return {}
        return self._load_stats(user)

    def player_data(self, username):
        user = self._find_user_by_name(username)
        if not user:
            return {}
        return self._load_player_data(user)

    def _read_nbt(self, relpath):
        try:
            path = os.path.join(self.directory, relpath)
            with open(path, 'rb') as f:
                return NBTFile(fileobj=f)
        except Exception as e:
            LOG.exception(e)
            return None

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
            LOG.error("No stats found for user %s [%s]", user['name'], user['uuid'])
        else:
            LOG.info("Loaded stats for user %s [%s]", user['name'], user['uuid'])
        return parse_user_stats(stats)

    def _load_player_data(self, user):
        user_id = user['uuid']
        path = os.path.join('world/playerdata/%s.dat' % user_id)
        data = self._read_nbt(path)
        if not data:
            LOG.error("No player data found for user %s [%s]", user['name'], user['uuid'])
        else:
            LOG.info("Loaded player data for user %s [%s]", user['name'], user['uuid'])
        return data or {}

    def _find_user_by_name(self, username):
        for user in self.users:
            if user['name'] == username:
                return user
        LOG.error("Failed to find id for user %s. Cannot load user stats.",
                  username)

class Inventory(object):

    def __init__(self, raw):
        self.entries = []
        self.headers = set()
        for item in raw:
            # prepare the data
            #  - copy enchantment from the tags to a top-level key
            #  - remove the tags (too messy to display)
            item = dict(item)
            item['ench'] = item.get('tag', {}).get('ench', [{}])[0].get('lvl', '')
            if 'tag' in item:
                del item['tag']

            # make sure headers and row values are in the right order
            items = sorted(item.items(), key=lambda x: x[0], reverse=True)
            self.entries.append([v for _, v in items])
            self.headers.update([k for k, v in items])

        self.headers = list(self.headers)
        self.headers.sort(reverse=True)

        # detect errors
        for e in self.entries:
            if len(e) != len(self.headers):
                LOG.error("Inventory row %s has a different number of values "
                          "than there are headers, %s", e, self.headers)


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
