"""
Optional emoji-enhanced logging formatter (core L1).

Extends Utf8Formatter with level-based emoji prefixing.
"""

import logging

from scriptcraft.layers.layer_0_core.level_0.runtime.formatters import Utf8Formatter


class EmojiFormatter(Utf8Formatter):
    """Formatter that prepends emojis based on log level."""

    LEVEL_EMOJI = {
        "debug":    "🔍 ",
        "info":     "📝 ",
        "warning":  "⚠️ ",
        "error":    "❌ ",
        "critical": "💥 ",
    }

    KNOWN_EMOJIS = frozenset("🔍📝⚠️❌💥🚀✅🎯📊📁🔧💡🎉🏁")

    def format(self, record: logging.LogRecord) -> str:
        message = str(record.msg)

        if not any(ch in message[:3] for ch in self.KNOWN_EMOJIS):
            prefix = self.LEVEL_EMOJI.get(record.levelname.lower(), "")
            record.msg = prefix + message

        return super().format(record)
