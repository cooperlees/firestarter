#!/usr/bin/env python3

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

import RPi.GPIO as GPIO


GPIO.setwarnings(True)
LOG = logging.getLogger(__name__)


class Fireplace:
    """Control Fireplace via custom RPi HAT constructed by Mr Aijay Adams 👨🏻‍🦰
    - Will wrap all GPIO calls into Threads so we don't block"""

    # Have all instances share lock + thread pool
    # Expect to have Web interface + prometheus stats use access to GPIO
    lock = asyncio.Lock()
    thread_pool = ThreadPoolExecutor(max_workers=2)

    PIN_TOGGLE_STATE = 2
    PIN_SENSE_STATE = 3

    def __init__(self) -> None:
        self.loop = asyncio.get_running_loop()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN_SENSE_STATE, GPIO.IN)

        # PIN_TOGGLE_STATE is LOW by default, but I'm not sure what the
        # GPIO library will do when it moves it to mode OUTPUT
        # Best be sure it stays HIGH and didn't toggle the state during init
        GPIO.setup(self.PIN_TOGGLE_STATE, GPIO.OUT)
        GPIO.output(self.PIN_TOGGLE_STATE, GPIO.HIGH)

    def on_exit(self) -> None:
        """Function to use with atexit or some form of program exit cleanup"""
        GPIO.cleanup()

    async def _toggle_state(self) -> None:
        """Toggle the state of the fireplace - Use an async lock to ensure
        only 1 thing is try to play with the toggle at once #monogamy"""
        async with self.lock:
            self.loop.run_in_executor(
                self.thread_pool,
                GPIO.output,
                self.PIN_TOGGLE_STATE,
                GPIO.LOW,
            )
            await asyncio.sleep(0.1)
            self.loop.run_in_executor(
                self.thread_pool,
                GPIO.output,
                self.PIN_TOGGLE_STATE,
                GPIO.HIGH,
            )

    async def lit(self) -> bool:
        """Is the fire on?"""
        return bool(
            await self.loop.run_in_executor(
                self.thread_pool,
                GPIO.input,
                self.PIN_SENSE_STATE,
            )
        )

    async def turn_off(self) -> None:
        """Turn on the fireplace"""
        if await self.lit():
            await self._toggle_state()

    async def turn_on(self) -> None:
        """Turn on the fireplace"""
        if not await self.lit():
            await self._toggle_state()
