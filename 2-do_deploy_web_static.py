#!/usr/bin/python3
"""Fabric script that deploys an archive to web servers"""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['100.26.153.46', '52.201.211.87']


def do_deploy(archive_path):
    """Deploys an archive to the web servers"""
    if not os.path.isfile(archive_path):
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, f"/tmp/{file}").failed:
        return False
    if run(f"rm -rf /data/web_static/releases/{name}/").failed or \
       run(f"mkdir -p /data/web_static/releases/{name}/").failed or \
       run(f"tar -xzf /tmp/{file} -C /data/web_static/releases/{name}/").failed or \
       run(f"rm /tmp/{file}").failed or \
       run(f"mv /data/web_static/releases/{name}/web_static/* /data/web_static/releases/{name}/").failed or \
       run(f"rm -rf /data/web_static/releases/{name}/web_static").failed or \
       run("rm -rf /data/web_static/current").failed or \
       run(f"ln -s /data/web_static/releases/{name}/ /data/web_static/current").failed:
        return False

    return True
