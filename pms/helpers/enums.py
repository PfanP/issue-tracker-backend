
from core.helpers.enums import ChoiceEnum

__author__ = 'Ashraful'


class IssueStatusEnum(ChoiceEnum):
    NEW = 0
    IN_PROGRESS = 1
    ON_HOLD = 2
    AWAITING_QA = 3
    QA_VERIFIED = 4
    CLOSE = 5
    ARCHIVE = 6


class IssueTrackerEnum(ChoiceEnum):
    BUG = 0
    FEATURE = 1
    SUPPORT = 2


class IssuePriorityEnum(ChoiceEnum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3


class ActionEnum(ChoiceEnum):
    CREATE = 0
    RETRIEVE = 1
    UPDATE = 2
    DELETE = 3
