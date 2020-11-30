#!/usr/bin/env python3
# Copyright (c) 2014-present, Facebook, Inc.

import atexit
import logging
from datetime import datetime
from os import environ
from pathlib import Path
from typing import Tuple

import basicauth
from aiohttp import web

from firestarter.fp import Fireplace
from firestarter.prometheus import stats


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
    <p>Hello {user}, you are visiting from {ip}</p>
    <p>Fireplace is <strong>{status}</strong> @ {date}</p>
    <p>
        <form action="{action}" method="POST" id="toggle_form"></form>
        <button type="submit" form="toggle_form" value="{value}">{value}</button>
    </p>
    <p><img src="{img_src}"></p>
    <p><a href="/">HOME</a></p>
</body>
</html>
"""
IMAGES_DIR = Path("/var/www/images")


async def _get_user_and_ip(
    request: web.Request, ip_header: str = "X-Forwarded-For"
) -> Tuple[str, str]:
    user = "Unauthed"
    ip = str(request.remote)
    if "Authorization" in request.headers:
        user, _ = basicauth.decode(request.headers["Authorization"])
        if ip_header in request.headers and request.headers[ip_header]:
            ip = request.headers[ip_header]

    return (user, ip)


async def _generate_response_html(request: web.Request, user: str, ip: str) -> str:
    fp = request.app["fireplace"]
    lit = await fp.lit()
    status = "ON" if lit else "OFF"
    date = datetime.now().strftime("%a %b %d %Y %H:%M:%S")
    action = "/turn_off" if lit else "/turn_on"
    value = "Turn Fireplace Off" if lit else "Turn Fireplace On"
    img_src = "/images/fireplace_on.gif" if lit else "/images/fireplace_off.jpg"
    return HTMLTEMPLATE.format(
        status=status,
        date=date,
        action=action,
        value=value,
        img_src=str(img_src),
        user=user,
        ip=ip,
    )


async def index(request: web.Request) -> web.Response:
    user, ip = await _get_user_and_ip(request)
    formatted_html = await _generate_response_html(request, user, ip)
    return web.Response(text=formatted_html, content_type="text/html")


async def change_state(request: web.Request) -> web.Response:
    fp = request.app["fireplace"]
    user, ip = await _get_user_and_ip(request)
    if "turn_on" in str(request.rel_url).lower():
        LOG.info(f"{user} from {ip} turned fireplace ON")
        await fp.turn_on()
    else:
        LOG.info(f"{user} from {ip} turned fireplace OFF")
        await fp.turn_off()

    # TODO: Add support for header to request JSON return
    formatted_html = await _generate_response_html(request, user, ip)
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
    app.router.add_get("/metrics", stats)
    app.router.add_get("/stats", stats)
    app.router.add_get("/probe", stats)
    app.router.add_post("/69", sixtynine)
    app.router.add_post("/sixtynine", sixtynine)
    app.router.add_post("/turn_off", change_state)
    app.router.add_post("/turn_on", change_state)
    app.router.add_static("/images", IMAGES_DIR)

    LOG.debug("Finished setting up routes")
    return app


if __name__ == "__main__":
    LOG.error("This module is designed to run via gunicorn")
