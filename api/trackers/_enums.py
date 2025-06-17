from enum import Enum

class TrackerObjectType(str, Enum):
    TRACKER = "tracker"
    TRACKER_VISIT = "tracker_visit"
    LIST = "list"

class SortBy(str, Enum):
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    VISIT_COUNT = "visitCount"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"