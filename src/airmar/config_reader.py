import yaml
import os

from src.hardware.pin import make_pin
from src.hardware.port import make_port


def read_pin_config(mock_bbio=None, path=None):
    """Reads the pin configuration from config.yml and returns matching pin 
    dictionary"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        if mock_bbio is None:
            pins = {
                "WIND": make_pin(conf["pins"]["WIND"]),
                "BOAT": make_pin(conf["pins"]["BOAT"])
            }
        else:
            pins = {
                "WIND": make_pin(conf["pins"]["WIND"], mock_lib=mock_bbio.UART),
                "BOAT": make_pin(conf["pins"]["BOAT"], mock_lib=mock_bbio.UART)
            }
    return pins


def read_interval(path=None):
    """Reads the read interval from config.yml"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        interval = conf["read interval"]

    return interval


def read_port_config(mock_port=None, path=None):
    """ Reads the settings for serial port communication from config.yml and 
    returns matching port dictionary"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        if mock_port is None:
            ports = {
                "WIND": make_port(conf["ports"]["WIND"]),
                "BOAT": make_port(conf["ports"]["BOAT"])
            }
        else:
            ports = {
                "WIND": make_port(conf["ports"]["WIND"], mock_port=mock_port.Serial),
                "BOAT": make_port(conf["ports"]["BOAT"], mock_port=mock_port.Serial)
            }
    return ports
