"""Manage Salesforce domain and Session ID."""

# For each active ARB in SF, see if an active ARB exists in Authorize.net, and if dates match (Jan 1 through Dec 31)
# Are there active ARBs in Authorize.net that are not recorded in SF?

import pathlib
import tempfile
from functools import lru_cache


SESSION_DIR = pathlib.Path(tempfile.gettempdir(), "aiosalesforce")


def destroy(session_path):
    with session_path.open("wb") as handle:
        handle.seek(150)
        handle.write(b"\0")
    session_path.unlink(True)


def destroy_all():
    for session_path in list_all():
        destroy(session_path)


def filepath(domain):
    return SESSION_DIR / f"{domain}.session"


def read(domain):
    return filepath(domain).read_text()


def list_all():
    return SESSION_DIR.glob("*.session")


def prompt():
    """Credential entry helper"""
    creds_json = input('Enter ["domain", "session_id"]: ')
    creds = json.loads(creds_json)
    return creds


def write(domain, session_id):
    filepath(domain).write_text(session_id)


def get_creds(domain, refresh=False):
    """Get credentials from file or input, and test"""
    sesspath = Path("logs") / "recent_session.json"
    pathlib.Path(tempfile.gettempdir()) / "sfsessions"

    creds = []
    if refresh:
        creds = input_creds()
        with sesspath.open("w") as handle:
            json.dump(creds, handle)
    else:
        try:
            with sesspath.open() as handle:
                creds = json.load(handle)
        except FileNotFoundError:
            creds = get_creds(True)
    return creds


@lru_cache(maxsize=4)
def sf_connect(api_version="48.0"):
    """Return a connection to SF org"""
    domain, sess_id = get_creds()
    connection = Salesforce(instance=domain, session_id=sess_id, version=api_version)
    try:
        connection.restful("")
    except SalesforceExpiredSession:
        get_creds(True)
        connection = sf_connect()
    return connection
