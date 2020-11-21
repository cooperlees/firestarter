#!/usr/bin/env python3
# Copyright (c) 2014-present, Facebook, Inc.

import logging
from os import environ

from aiohttp import web

# Uncomment when I can actually build on a Raspberry Pi
# from firestarter.fp import Fireplace, FireplaceIsFucked


LOG = logging.getLogger(__name__)
ROOT_HTML = r"""<html><body><h1>Firestarter Coming Soon</h1></body></html>"""


async def index(request: web.Request) -> web.Response:
    return web.Response(text=ROOT_HTML)


async def serve() -> web.Application:
    log_level = logging.DEBUG if "DEBUG" in environ else logging.INFO
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s (%(filename)s:%(lineno)d)",
        level=log_level,
    )

    app = web.Application()
    app.router.add_get("/", index)
    LOG.debug("Finished setting up routes")
    return app


if __name__ == "__main__":
    LOG.error("This module is designed to run via gunicorn")
