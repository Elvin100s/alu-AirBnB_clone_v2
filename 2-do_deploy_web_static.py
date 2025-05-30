#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import env, put, run, local
import os
from datetime import datetime

# Set the hosts and user for deployment
env.user = 'ubuntu'
env.hosts = ['44.202.60.165', '44.202.132.51']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    
    Args:
        archive_path (str): Path to the archive file
        
    Returns:
        bool: True if all operations succeed, False otherwise
    """
    # Check if the archive file exists
    if not os.path.isfile(archive_path):
        return False
    
    try:
        # Extract filename from path and remove .tgz extension
        filename = os.path.basename(archive_path)
        name_no_ext = filename.replace('.tgz', '')
        release_path = "/data/web_static/releases/{}/".format(name_no_ext)
        tmp_path = "/tmp/{}".format(filename)
        
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, tmp_path)
        
        # Create the releases directory if it doesn't exist
        run("mkdir -p {}".format(release_path))
        
        # Uncompress the archive to the releases folder
        run("tar -xzf {} -C {}".format(tmp_path, release_path))
        
        # Delete the archive from the web server
        run("rm {}".format(tmp_path))
        
        # Move files from web_static subdirectory to the release directory
        run("mv {}web_static/* {} 2>/dev/null || true".format(
            release_path, release_path))
        
        # Remove the now empty web_static directory
        run("rm -rf {}web_static".format(release_path))
        
        # Delete the current symbolic link
        run("rm -rf /data/web_static/current")
        
        # Create new symbolic link
        run("ln -s {} /data/web_static/current".format(release_path))
        
        return True
        
    except:
        return False
