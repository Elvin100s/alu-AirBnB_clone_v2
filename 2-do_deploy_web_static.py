#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['44.202.60.165', '44.202.132.51']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    
    Args:
        archive_path (str): Path to the archive file
        
    Returns:
        bool: True if all operations completed successfully, False otherwise
    """
    if not exists(archive_path):
        return False
    
    try:
        # Extract filename and base name
        file_name = archive_path.split("/")[-1]
        base_name = file_name.replace(".tgz", "")
        
        # Remote paths
        tmp_path = "/tmp/{}".format(file_name)
        release_path = "/data/web_static/releases/{}".format(base_name)
        
        # Upload archive
        put(archive_path, tmp_path)
        
        # Create release directory
        run("mkdir -p {}".format(release_path))
        
        # Extract archive
        run("tar -xzf {} -C {}".format(tmp_path, release_path))
        
        # Clean up archive
        run("rm {}".format(tmp_path))
        
        # Move files and clean up
        run("mv {}/web_static/* {}".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))
        
        # Update symlink
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))
        
        return True
    except Exception as e:
        return False
