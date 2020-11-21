#!/usr/bin/env python3

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

import RPi.GPIO as GPIO


LOG = logging.getLogger(__name__)


class FireplaceIsFucked(Exception):
    pass


class Fireplace:
    """Control Fireplace via custom RPi HAT constructed by Mr Aijay Adams 👨🏻‍🦰
    - Will wrap all GPIO calls into Threads so we don't block"""

    def __init__(self, workers: int = 2) -> None:
        GPIO.setmode(GPIO.BOARD)
        self.loop = asyncio.get_running_loop()
        self.thread_pool = ThreadPoolExecutor(max_workers=workers)

    def __del__(self) -> None:
        GPIO.cleanup()

    async def fire_lit(self) -> bool:
        """Is the fire on?"""
        return False

    async def turn_off(self) -> None:
        """Turn on the fireplace"""
        ...

    async def turn_on(self) -> None:
        """Turn on the fireplace"""
        ...
