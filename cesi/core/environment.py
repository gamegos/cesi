class Environment:
    def __init__(self, name, members_string=""):
        self.name = name
        self.members = list(map(str.strip, members_string.split(",")))

    def set_members(self, members):
        self.members = members

    def serialize(self):
        return {"name": self.name, "members": self.members}
