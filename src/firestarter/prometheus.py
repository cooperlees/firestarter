#!/usr/bin/env python3

import asyncio
from aiohttp import web
from socket import getfqdn
from time import time


PROMETHEUS_TEMPLATE = """\
# HELP fireplace_status Is the fireplace running (bool)
# TYPE fireplace_status gauge
fireplace_status{hostname="%s"} %i %i

# HELP fireplace_coroutines Number of current running asyncio coroutines
# TYPE fireplace_coroutines gauge
fireplace_coroutines{hostname="%s"} %i %i
"""


async def stats(request: web.Request) -> web.Response:
    hostname = getfqdn()
    state = await request.app["fireplace"].lit()
    stat_time = int(time())
    formatted_metrics = PROMETHEUS_TEMPLATE % (
        hostname,
        stat_time,
        int(state),
        hostname,
        stat_time,
        len(asyncio.all_tasks()),
    )
    return web.Response(text=formatted_metrics)
