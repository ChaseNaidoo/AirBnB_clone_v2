#!/usr/bin/python3
"""Fabric script that deploys an archive to web servers"""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['100.26.153.46', '52.201.211.87']


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
