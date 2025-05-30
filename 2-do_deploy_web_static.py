#!/usr/bin/python3
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

    filename = os.path.basename(archive_path)
    name_no_ext = filename.replace('.tgz', '')
    release_path = f"/data/web_static/releases/{name_no_ext}/"
    tmp_path = f"/tmp/{filename}"

    try:
        # Upload archive to /tmp/
        put(archive_path, tmp_path)

        # Create the release directory
        run(f"mkdir -p {release_path}")

        # Uncompress the archive to the release directory
        run(f"tar -xzf {tmp_path} -C {release_path}")

        # Delete the archive from the server
        run(f"rm {tmp_path}")

        # Move contents out of the web_static folder to release directory
        run(f"mv {release_path}web_static/* {release_path}")

        # Remove now-empty web_static folder
        run(f"rm -rf {release_path}web_static")

        # Delete the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run(f"ln -s {release_path} /data/web_static/current")

        print("New version deployed!")
        return True

    except Exception:
        return False
