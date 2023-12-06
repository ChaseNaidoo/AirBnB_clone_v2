#!/usr/bin/python3
"""Fabric script that generates a .tgz archive"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    local("mkdir -p versions")

    now = datetime.utcnow()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second
    )
    result = local("tar -cvzf versions/{} web_static"
                   .format(archive_name), capture=True)

    if result.failed:
        return None
    else:
        archive_path = os.path.join("versions", archive_name)
        return archive_path
