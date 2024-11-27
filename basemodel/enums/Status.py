from enum import Enum

class Status(str, Enum):
    operativo = 'operativo'
    inattivo = 'inattivo'
    