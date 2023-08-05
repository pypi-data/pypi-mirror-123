# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
#    _                ___ ___   _____       _             _           _
#   /_\  _ _ ___ __ _|_  | _ ) |_   _|__ __| |_  _ _  ___| |___  __ _(_)___ ___
#  / _ \| '_/ -_) _` |/ // _ \   | |/ -_) _| ' \| ' \/ _ \ / _ \/ _` | / -_|_-<
# /_/ \_\_| \___\__,_/___\___/   |_|\___\__|_||_|_||_\___/_\___/\__, |_\___/__/
#                                                               |___/
"""Build packages to be submitted to Area28."""
import logging


# current version
__version__ = '0.5.0'

# enable logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# try use colored logs
try:
    import coloredlogs

    coloredlogs.install(level='DEBUG', logger=log)
except ImportError:
    coloredlogs = None
    log.warning('for better logging, please pip install coloredlogs')
