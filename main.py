#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.11"
# dependencies = ["raylib"]
# ///

from src.game import *
from src.context import Context

if __name__ == "__main__":
    start_game()
