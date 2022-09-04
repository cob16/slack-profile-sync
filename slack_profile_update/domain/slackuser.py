from dataclasses import dataclass


@dataclass
class SlackUser:
    user_id: str
    team_id: str
    token: str = None
    app_id: str = None

    def __hash__(self):
        return hash((self.user_id, self.team_id))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.team_id == other.team_id and self.user_id == other.user_id
