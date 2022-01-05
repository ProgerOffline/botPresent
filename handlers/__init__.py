#-*- coding: utf-8 -*-

from . import messages
from . import commands
from . import states
from . import buttons


def setup(dp, bot) -> None:
    states.setup(dp, bot)
    buttons.setup(dp)
    commands.setup(dp, bot)
    messages.setup(dp)