#!/usr/bin/python3
"""Fabric script that deploys an archive to web servers"""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['100.26.153.46', '52.201.211.87']


def do_deploy(archive_path):
    """Deploys an archive to the web servers"""
    if not os.path.isfile(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        archive_filename = archive_path.split("/")[-1]
        release_path = '/data/web_static/releases/{}'.format(
            archive_filename.split(".")[0])
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))
        run('rm /tmp/{}'.format(archive_filename))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_path))
        return True
