class EntityInfo:
    name: str
    codex: str
    filename_lua: str

    def __init__(self, name, codex, filename_lua):
        self.name = name
        self.codex = codex
        self.filename_lua = filename_lua
