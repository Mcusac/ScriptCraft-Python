"""
Basic Kaggriculture agent.

Layer 3 adapter for the Buy Once strategy.
"""

from kaggle_environments import make

from ..layer_2_strategy.buy_once import BuyOnceStrategy


strategy = BuyOnceStrategy()


def agent(obs: dict) -> dict:
    """Kaggriculture entry point."""

    return strategy.decide(obs)


env = make("kaggriculture", configuration={"episodeSteps": 200})
env.run([agent, "random"])
env.render(mode="ipython", width=800, height=800)
