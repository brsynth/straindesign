from __future__ import absolute_import, print_function

from uuid import uuid4

try:
    from IPython import display
except ImportError:
    pass

import logging
import os
from base64 import b64encode

from cameobrs import util

ASSETS = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))

SEARCHING_IMAGE_FILE = os.path.join(ASSETS, "searching.gif")
with open(SEARCHING_IMAGE_FILE, "rb") as f:
    SEARCHING_IMAGE = b64encode(f.read()).decode("utf-8").replace("\n", "")

# LOADING_IMAGE_FILE = os.path.join(ASSETS, "loading_wave.gif")
LOADING_IMAGE_FILE = os.path.join(ASSETS, "searching.gif")
with open(LOADING_IMAGE_FILE, "rb") as f:
    LOADING_IMAGE = b64encode(f.read()).decode("utf-8").replace("\n", "")

logger = logging.getLogger(__name__)


def notice(message):
    if util.in_ipnb():
        display.HTML("<span>%s</span>" % message)
    else:
        print(message)


def bold(message):
    if util.in_ipnb():
        display.HTML("<strong>%s</strong>" % message)
    else:
        print("\033[1m" + message + "\033[0m")


def searching():
    if util.in_ipnb():
        identifier = str(uuid4())
        display.HTML(
            """
        <img class="loading" id="%s" style="margin:auto; text-align:center;" src="data:image/gif;base64,%s"/>
        """
            % (identifier, SEARCHING_IMAGE)
        )
        return identifier
    else:
        logger.debug("loading only works on Jupyter notebooks")


def loading():
    if util.in_ipnb():
        identifier = str(uuid4())
        display.HTML(
            """
        <img class="loading" id="%s" style="margin:auto; text-align:center;" src="data:image/gif;base64,%s"/>
        """
            % (identifier, LOADING_IMAGE)
        )
        return identifier
    else:
        logger.debug("loading only works on Jupyter notebooks")


def stop_loader(identifier):
    if util.in_ipnb():
        display.Javascript(
            """
        jQuery("#%s").remove();
        """
            % identifier
        )
    else:
        logger.debug("loading only works on Jupyter notebooks")


def delta():
    if util.in_ipnb():
        return "&Delta;"
    else:
        return b"\xce\x94".decode("utf-8")


def knockin():
    if util.in_ipnb():
        return "+"
    else:
        return "+"


def upreg(coeff):
    if util.in_ipnb():
        return "&uarr;%.3f" % coeff
    else:
        return b"\xe2\x86\x91".decode("utf-8") + "%.3f" % coeff


def downreg(coeff):
    if util.in_ipnb():
        return "&darr;%.3f" % coeff
    else:
        return b"\xe2\x86\x93".decode("utf-8") + "%.3f" % coeff
