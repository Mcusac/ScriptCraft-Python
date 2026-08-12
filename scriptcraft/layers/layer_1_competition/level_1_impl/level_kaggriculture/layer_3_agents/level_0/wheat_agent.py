"""
Basic wheat farming Kaggriculture agent.

Layer 3 adapter for the Wheat strategy.
"""

from kaggle_environments import make

from ..layer_2_strategy.level_0.wheat import WheatStrategy


strategy = WheatStrategy()


def agent(obs: dict) -> dict:
    """Kaggriculture entry point."""

    return strategy.decide(obs)

env = make("kaggriculture", configuration={"episodeSteps": 200})
env.run([agent, "random"])
env.render(mode="ipython", width=800, height=800)
