#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to your web servers"""
from fabric.api import env
from fabric.operations import local
from os.path import exists
from datetime import datetime

env.hosts = ['100.26.153.46', '52.201.211.87']
env.user = "ubuntu"


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

def do_deploy(archive_path):
    """Deploys an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        archive_filename = archive_path.split("/")[-1]
        folder_name = "/data/web_static/releases/{}".format(
            archive_filename.split(".")[0])
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, folder_name))

        run("mv {}/web_static/* {}".format(folder_name, folder_name))
        run("rm -rf {}/web_static".format(folder_name))
        run("rm /tmp/{}".format(archive_filename))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_name))
        print("New version deployed!")
        return True
    except Exception as e:
        return False

def deploy():
    """Creates and distributes an archive to your web servers"""
    archive_path = do_pack()

    if not archive_path:
        return False

    return do_deploy(archive_path)
