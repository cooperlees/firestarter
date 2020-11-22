#!/usr/bin/env python3
# Copyright (c) 2014-present, Facebook, Inc.

import atexit
import logging
from datetime import datetime
from os import environ

from aiohttp import web

from firestarter.fp import Fireplace


SIXTYNINE_ASCII = r"""\
.------..------.
|6.--. ||9.--. |
| (\/) || :/\: |
| :\/: || (__) |
| '--'6|| '--'9|
`------'`------'
"""
LOG = logging.getLogger(__name__)
HTMLTEMPLATE = """\
<html>
<head><title>Mother Fucking Fireplace</title><head>
<body>
    <h1>Firestarter v6.9</h1>
    <p>Fireplace is <strong>{status}</strong> @ {date}</p>
    <p>
        <form action="{action}" method="POST" id="toggle_form"></form>
        <button type="submit" form="toggle_form" value="{value}">{value}</button>
    </p>
    <!-- TODO: Add sweet 1999 GIF of fireplace on or off -->
    <p><a href="/">HOME</a></p>
</body>
</html>
"""


async def _generate_response_html(request: web.Request) -> str:
    fp = request.app["fireplace"]
    lit = await fp.lit()
    status = "ON" if lit else "OFF"
    date = datetime.now().strftime("%a %b %d %Y %H:%M:%S")
    action = "/turn_off" if status == "ON" else "/turn_on"
    value = "Turn Fireplace Off" if status == "ON" else "Turn Fireplace On"
    return HTMLTEMPLATE.format(status=status, date=date, action=action, value=value)


async def index(request: web.Request) -> web.Response:
    formatted_html = await _generate_response_html(request)
    return web.Response(text=formatted_html, content_type="text/html")


async def change_state(request: web.Request) -> web.Response:
    fp = request.app["fireplace"]
    if "turn_on" in str(request.rel_url).lower():
        await fp.turn_on()
    else:
        await fp.turn_off()

    # TODO: Add support for header to request JSON return
    formatted_html = await _generate_response_html(request)
    return web.Response(text=formatted_html, content_type="text/html")


async def sixtynine(request: web.Request) -> web.Response:
    return web.Response(text=SIXTYNINE_ASCII)


async def serve() -> web.Application:
    log_level = logging.DEBUG if "DEBUG" in environ else logging.INFO
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s (%(filename)s:%(lineno)d)",
        level=log_level,
    )

    app = web.Application()
    app["fireplace"] = Fireplace()
    atexit.register(app["fireplace"].on_exit)

    app.router.add_get("/", index)
    app.router.add_post("/69", sixtynine)
    app.router.add_post("/sixtynine", sixtynine)
    app.router.add_post("/turn_off", change_state)
    app.router.add_post("/turn_on", change_state)

    LOG.debug("Finished setting up routes")
    return app


if __name__ == "__main__":
    LOG.error("This module is designed to run via gunicorn")
