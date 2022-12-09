"""Settings.py, general settings for yt-watch-history-analyzer."""

from pathlib import Path

__all__ = [
    "CONFIG_FILE",
    "TOKEN_PICKLE_FILE",
]

######################
##### cfg paths ######
######################

CONFIG_DIR = Path("/home/paul/repos/yt-watch-history-analyzer/yt_watch_history_analyzer/config")
# CONFIG_FILE = "config.yaml"
CONFIG_FILE = CONFIG_DIR / "config.yaml" 
TOKEN_PICKLE_FILE = CONFIG_DIR / "token.pickle"
