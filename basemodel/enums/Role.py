from enum import Enum

class Role(str, Enum):
    admin = 'admin'
    operator = 'operator'