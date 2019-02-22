"""Collects all AIs into one dictionary for easy search later"""
from .test_hover import test_hover
from .test_linear_move import test_linear_move
from .user_command import user_command

AIS = {
    "test_hover": test_hover,
    "test_linear_move": test_linear_move,
    "user_command": user_command
}