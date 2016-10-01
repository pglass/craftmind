Overview
--------

Craftmind is a tiny read-only dashboard for your Minecraft server.

Features,

- [x] Show server properties [`server.properties`]
- [x] List players [`usercache.json`]
- [x] List server operators [`ops.json`]
- [x] Show aggregate player statistics [`world/stats/*.json`]
- [x] Compare player statistics
- [x] Display world data [`world/level.dat`]
- [ ] Show banned ips [`banned-ips.json`]
- [ ] Show banned players [`banned-players.json`]
- [ ] Show player whitelist [`whitelist.json`]
- [ ] ???

Supported Minecraft versions

- [ ] 1.10
- [ ] 1.9
- [x] 1.8
- [ ] 1.7
- [ ] 1.6
- [ ] 1.5
- [ ] 1.4
- [ ] 1.3
- [ ] 1.2
- [ ] 1.1
- [ ] 1.0

Other versions than those checked above may work but are not tested.

Quickstart
----------

Craftmind works by reading files from your Minecraft server directory, so the
Craftmind server must be started on the same machine as your Minecraft server.

Craftmind is a [Flask](http://flask.pocoo.org/) app, so you will need python
and pip installed.

On Linux,

    $ git clone git@github.com:pglass/craftmind.git
    $ cd craftmind
    $ pip install -r requirements.txt
    $ make start

**NOTE**: Craftmind assumes your Minecraft server data directory is
`/home/minecraft`. Changing this directory currently requires editing the code.

This starts a multiprocess HTTP server (gunicorn) suitable for a small number
of concurrent users. You may open your browser and go to
`http://<server-location>:52425` to view the dashboard.

For development, you may prefer Flask's built-in server and debugging support.
Flask's native server can be started with:

    python craftmind/app.py
