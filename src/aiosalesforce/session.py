"""Manage Salesforce domain and Session ID."""

import json
import pathlib
import tempfile

SESSION_DIR = pathlib.Path(tempfile.gettempdir(), "aiosalesforce")


def destroy(session_path):
    """Zero fill and delete specified session file.

    Args:
        session_path: path to session file
    """
    with session_path.open("wb") as handle:
        handle.seek(150)
        handle.write(b"\0")
    session_path.unlink(True)


def destroy_all():
    """Destroy all session files found."""
    for session_path in list_all():
        destroy(session_path)


def file_path(domain):
    """Get path to session file for this domain.

    Args:
        domain: Salesforce domain for API access

    Returns:
        Path to file
    """
    return SESSION_DIR / f"{domain}.session"


def read(domain):
    """Get Session ID for this domain.

    Args:
        domain: Salesforce domain for API access

    Returns:
        Session ID
    """
    return file_path(domain).read_text()


def list_all():
    """List all session files.

    Returns:
        List of file paths
    """
    return SESSION_DIR.glob("*.session")


def prompt():
    """Credential entry helper.

    Returns:
        credentials
    """
    credentials_json = input('Enter ["domain", "session_id"]: ')
    credentials = json.loads(credentials_json)
    return credentials


def write(domain, session_id):
    """Create/update session file with Session ID.

    Args:
        domain: Salesforce domain for API access
        session_id: the Salesforce Session ID to be recorded
    """
    file_path(domain).write_text(session_id)
