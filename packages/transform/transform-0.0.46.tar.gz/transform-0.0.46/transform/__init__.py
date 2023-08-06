from transform.mql import MQLClient

__version__ = "0.0.46"
PACKAGE_NAME = "transform"

# mql gets imported if user is already authenticated
try:
    mql = MQLClient()
except Exception as e:  # noqa: D
    mql = None
