from enum import Enum

class Status(str, Enum):
    admin = 'admin'
    operator = 'operator'