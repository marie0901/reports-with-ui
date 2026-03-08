"""Report plugin implementations."""

from .casino_ret import CasinoRetPlugin
from .awol import AWOLPlugin
from .slot import SlotPlugin
from .awol_casino_ret import AWOLCasinoRetPlugin

__all__ = ["CasinoRetPlugin", "AWOLPlugin", "SlotPlugin", "AWOLCasinoRetPlugin"]
