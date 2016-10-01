Overview
--------

Craftmind is a tiny read-only dashboard for your Minecraft server.

Features,

- [x] Show server properties [`server.properties`]
- [x] List players [`usercache.json`]
- [x] List server operators [`ops.json`]
- [x] Show aggregate player statistics [`world/stats/*.json`]
- [x] Display world data [`world/level.dat`]
- [ ] Show banned ips [`banned-ips.json`]
- [ ] Show banned players [`banned-players.json`]
- [ ] Show player whitelist [`whitelist.json`]
- [ ] ???

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

This starts a multiprocess HTTP server (gunicorn) suitable for a small number
of concurrent users. You may open your browser and go to
`http://<server-location>:52425` to view the dashboard.

For development, you may prefer Flask's built-in server and debugging support.
Flask's native server can be started with:

    python craftmind/app.py
