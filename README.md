Overview
--------

Craftmind is a tiny read-only dashboard for your Minecraft server.

Features,

- [x] Show `server.properties` values
- [x] List players and server operators
- [x] Show aggregate player statistics (achievements, etc)
- [ ] Show banned ips
- [ ] Show player whitelist
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

Then open your browser and go to `http://<server-location>:52425`
