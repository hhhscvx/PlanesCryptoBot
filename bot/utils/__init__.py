from .logger import logger
from .schemas import Profile


import os

if not os.path.exists(path="sessions"):
    os.mkdir(path="sessions")