from agents.leadership import TilotmaAgent


def test_tilotma_describe():
    agent = TilotmaAgent()
    summary = agent.describe()
    assert summary["name"] == "tilotma"

