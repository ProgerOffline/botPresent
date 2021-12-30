#-*- coding: utf-8 -*-

from . import messages
from . import commands
from . import reply_buttons


def setup(dp) -> None:
    commands.setup(dp)
    reply_buttons.setup(dp)
    messages.setup(dp)