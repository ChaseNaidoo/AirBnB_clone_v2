#!/usr/bin/python3
"""Fabric script that deletes out-of-date archives"""
from fabric.api import env, run, local
from fabric.operations import put
from datetime import datetime
from os.path import exists
from operator import itemgetter

env.hosts = ['100.26.153.46', '52.201.211.87']
env.user = "ubuntu"


def do_clean(number=0):
    """Deletes out-of-date archives from the versions and releases"""
    number = int(number)

    local_archives = local("ls -1t versions", capture=True).split("\n")
    if number <= 1:
        local_archives_to_keep = local_archives[:1]
    else:
        local_archives_to_keep = local_archives[:number]

    for archive in local_archives:
        if archive not in local_archives_to_keep:
            local("rm -f versions/{}".format(archive))

    releases = run("ls -1t /data/web_static/releases").split("\n")
    releases_to_keep = sorted(releases, key=lambda x: datetime.strptime(
        x.split("_")[-1], "%Y%m%d%H%M%S"), reverse=True)[:number]

    for release in releases:
        if release not in releases_to_keep:
            run("rm -rf /data/web_static/releases/{}".format(release))
