"""
Optional emoji-enhanced logging formatter.

Extends Utf8Formatter with level-based emoji prefixing.
This module is intentionally isolated so the core logging
system remains clean and dependency-free.
"""

import logging

from layers.layer_1_tools.level_0_infra.level_0.formatter import Utf8Formatter


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

        # Only prefix if no emoji already present
        if not any(ch in message[:3] for ch in self.KNOWN_EMOJIS):
            prefix = self.LEVEL_EMOJI.get(record.levelname.lower(), "")
            record.msg = prefix + message

        return super().format(record)