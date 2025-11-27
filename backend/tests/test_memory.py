from memory.project_memory import ProjectMemory


def test_project_memory_upsert(tmp_path, monkeypatch):
    storage = tmp_path / "project.json"
    monkeypatch.chdir(tmp_path)
    memory = ProjectMemory()
    memory.upsert_project("abc", {"name": "Demo"})
    assert memory.get_project("abc")["name"] == "Demo"

