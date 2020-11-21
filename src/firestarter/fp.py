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

    PIN_SENSE_STATE = 2
    PIN_TOGGLE_STATE = 3

    def __init__(self, workers: int = 2) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_SENSE_STATE, GPIO.IN)

        # Get Fireplace State before messing with the toggle pin.
        initial_state = self.fire_lit()

        # PIN_TOGGLE_STATE is LOW by default, but I'm not sure what the 
        # GPIO library will do when it moves it to mode OUTPUT, so best be sure it 
        # stays LOW and didnt' toggle the state during init. 
        GPIO.setup(PIN_TOGGLE_STATE, GPIO.OUT)
        GPIO.output(PIN_TOGGLE_STATE, GPIO.LOW)

        self.turn.on() if initial_state else self.turn_off()

        self.loop = asyncio.get_running_loop()
        self.thread_pool = ThreadPoolExecutor(max_workers=workers)

    def __del__(self) -> None:
        GPIO.cleanup()

    async def fire_lit(self) -> bool:
        """Is the fire on?"""
        return GPIO.input(PIN_SENSE_STATE)

    async def _toggle_state(self) -> None:
        """Toggle the state of the fireplace"""
        ...
        GPIO.output(PIN_TOGGLE_STATE, GPIO.HIGH)
        await asyncio.sleep(0.1)
        GPIO.output(PIN_TOGGLE_STATE, GPIO.LOW)

    async def turn_off(self) -> None:
        """Turn on the fireplace"""
        self._toggle_state() if self.fire_lit()

    async def turn_on(self) -> None:
        """Turn on the fireplace"""
        self._toggle_state() if not self.fire_lit()
