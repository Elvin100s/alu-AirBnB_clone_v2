#!/usr/bin/python3
"""
Fabric script to pack and deploy web_static folder to web servers.
"""

from fabric.api import env, put, run, local
import os
from datetime import datetime

env.user = 'ubuntu'
env.hosts = ['44.202.60.165', '44.202.132.51']

def do_pack():
    """
    Create a .tgz archive from the web_static folder.
    Returns the archive path if successful, None otherwise.
    """
    local("mkdir -p versions")
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(now)
    print("Packing web_static to {}".format(archive_path))
    result = local("tar -czf {} web_static".format(archive_path))
    if result.succeeded:
        return archive_path
    return None


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
        print("Archive path does not exist:", archive_path)
        return False

    try:
        filename = os.path.basename(archive_path)
        name_no_ext = filename.replace('.tgz', '')
        release_path = "/data/web_static/releases/{}/".format(name_no_ext)
        tmp_path = "/tmp/{}".format(filename)

        print("Uploading archive:", archive_path)
        put(archive_path, tmp_path)

        print("Creating release directory:", release_path)
        run("mkdir -p {}".format(release_path))

        print("Extracting archive to release directory")
        run("tar -xzf {} -C {}".format(tmp_path, release_path))

        print("Deleting archive from /tmp/")
        run("rm {}".format(tmp_path))

        print("Moving contents from web_static to release directory")
        run("mv {}web_static/* {}".format(release_path, release_path))

        print("Removing now empty web_static directory")
        run("rm -rf {}web_static".format(release_path))

        print("Setting permissions")
        run("chmod -R 755 {}".format(release_path))

        print("Removing old symbolic link")
        run("rm -rf /data/web_static/current")

        print("Creating new symbolic link")
        run("ln -s {} /data/web_static/current".format(release_path))

        print("Verifying symbolic link:")
        run("ls -l /data/web_static/current")

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed:", e)
        return False


def deploy():
    """
    Packs and deploys the web_static folder to web servers.
    Returns True if all operations succeed, False otherwise.
    """
    archive_path = do_pack()
    if archive_path is None:
        print("Packing failed.")
        return False
    return do_deploy(archive_path)
