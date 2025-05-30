#!/usr/bin/python3
from fabric.api import env, put, run
import os

env.user = 'ubuntu'
env.hosts = ['44.202.60.165', '44.202.132.51']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path (str): Path to the archive file.

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
        put(archive_path, tmp_path)
        run(f"mkdir -p {release_path}")
        run(f"tar -xzf {tmp_path} -C {release_path}")
        run(f"rm {tmp_path}")
        run(f"mv {release_path}web_static/* {release_path}")
        run(f"rm -rf {release_path}web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {release_path} /data/web_static/current")
        return True
    except Exception:
        return False
