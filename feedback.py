from dataclasses import dataclass
from enum import Enum

class FeedbackType(Enum):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    UP = "up"
    DOWN = "down"


@dataclass
class Feedback:
    gender: FeedbackType
    affiliation: FeedbackType
    devil_fruit: FeedbackType
    haki: FeedbackType
    last_bounty: FeedbackType
    height: FeedbackType
    origin: FeedbackType
    first_arc: FeedbackType

    def __str__(self):
        return str({k: v.value for k, v in self.__dict__.items()})
