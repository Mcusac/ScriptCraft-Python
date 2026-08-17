"""
Buy Once strategy.

A minimal baseline strategy that buys one wheat seed on the
first step and passes on every subsequent step.
"""


class BuyOnceStrategy:
    """Buy one wheat seed on the first step, then do nothing."""

    def decide(self, obs: dict) -> dict:
        """Return the actions for the current observation."""

        if obs.get("step", 0) == 0:
            return {
                "farmer": ["PASS"],
                "market": [["BUY_SEED", "WHEAT", 1]],
            }

        return {
            "farmer": ["PASS"],
            "market": [],
        }