from enum import Enum


class RunMode(str, Enum):
    GLOBAL = "global"
    SINGLE_DOMAIN = "single_domain"
    DOMAIN = "domain"
    CUSTOM = "custom"