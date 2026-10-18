

class AstarNode:
    def __init__(self, state: list, g_score, h_score, parent=None):
        self.state = state
        self.f_score = g_score + h_score
        self.g_score = g_score
        self.h_score = h_score
        self.parent = parent

    def __lt__(self, other):
        # note: this breaks ties using the larger g_score (distance to node) as this usually means
        # that we are closer to the goal
        return self.g_score > other.g_score if self.f_score == other.f_score else self.f_score < other.f_score

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)
        