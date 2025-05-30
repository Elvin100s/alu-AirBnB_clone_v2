#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import env, put, run
import os

env.user = 'ubuntu'
env.hosts = ['44.202.60.165', '44.202.132.51']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Uploads the archive to /tmp/ on the server, decompresses it into
    /data/web_static/releases/<archive filename without extension>/,
    deletes the archive from /tmp/, deletes the old symbolic link
    /data/web_static/current, and creates a new symbolic link to the
    new release folder.

    Args:
        archive_path (str): The path to the archive to deploy.

    Returns:
        bool: True if all operations succeed, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False

    try:
        # Extract filename and name without extension
        filename = os.path.basename(archive_path)
        name_no_ext = filename.replace('.tgz', '')
        release_path = "/data/web_static/releases/{}/".format(name_no_ext)
        tmp_path = "/tmp/{}".format(filename)

        # Upload archive to /tmp/
        put(archive_path, tmp_path)

        # Create the release directory
        run("mkdir -p {}".format(release_path))

        # Uncompress the archive to the release directory
        run("tar -xzf {} -C {}".format(tmp_path, release_path))

        # Delete the archive from the server
        run("rm {}".format(tmp_path))

        # Move contents from web_static subdirectory to release directory
        run("mv {}web_static/* {}".format(release_path, release_path))

        # Remove the now-empty web_static subdirectory
        run("rm -rf {}web_static".format(release_path))

        # Delete the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create new symbolic link to the new release
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True

    except Exception:
        return False
