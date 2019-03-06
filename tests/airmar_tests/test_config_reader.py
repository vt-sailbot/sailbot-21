import unittest
from unittest.mock import MagicMock

import os
from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial
from src.hardware.pin import make_pin

from src.airmar.config_reader import read_pin_config
from src.airmar.config_reader import read_interval
from src.airmar.config_reader import read_port_config


class AirmarConfigReaderTests(unittest.TestCase):
    """Tests methods in RC Config Reader"""

    def setUp(self):
        """Sets up path of test config.yaml for each test method"""
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_read_pin_config(self):
        """Tests read_pin_config"""
        Adafruit_BBIO.UART.setup = MagicMock(name='Adafruit.BBIO.UART.setup')

        mock_pins = read_pin_config(mock_bbio=Adafruit_BBIO, path=self.path)
        pins = read_pin_config(path=self.path)

        assert pins["WIND"].pin_name == "P0_0"
        assert mock_pins["WIND"].pin_name == "P0_0"

        assert pins["BOAT"].pin_name == "P0_1"
        assert mock_pins["BOAT"].pin_name == "P0_1"

    def test_read_interval(self):
        """Tests read_interval"""
        assert read_interval(path=self.path) == "50 / 1000"

    def test_read_port_config(self):
        """Tests read_port_config"""
        ports = read_port_config(path=self.path)
        mock_ports = read_port_config(path=self.path, mock_port=serial)

        assert mock_ports["WIND"].port_name == "/dev/tty01"
        assert ports["WIND"].port_name == "/dev/tty01"

        assert mock_ports["BOAT"].port_name == "/dev/tty04"
        assert ports["BOAT"].port_name == "/dev/tty04"
