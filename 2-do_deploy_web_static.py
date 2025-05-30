#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import env, put, run
import os

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
    # Return False if file doesn't exist
    if not os.path.isfile(archive_path):
        return False
    
    try:
        # Get filename and name without extension
        filename = os.path.basename(archive_path)
        name_no_ext = filename.split('.')[0]
        
        # Define paths
        tmp_path = "/tmp/{}".format(filename)
        release_path = "/data/web_static/releases/{}/".format(name_no_ext)
        
        # Upload archive to /tmp/
        put(archive_path, tmp_path)
        
        # Create release directory
        run("mkdir -p {}".format(release_path))
        
        # Extract archive
        run("tar -xzf {} -C {}".format(tmp_path, release_path))
        
        # Delete archive from server
        run("rm {}".format(tmp_path))
        
        # Handle web_static subdirectory if it exists
        web_static_dir = "{}web_static".format(release_path)
        run("if [ -d {} ]; then mv {}/* {} && rm -rf {}; fi".format(
            web_static_dir, web_static_dir, release_path, web_static_dir))
        
        # Remove current symbolic link
        run("rm -rf /data/web_static/current")
        
        # Create new symbolic link
        run("ln -s {} /data/web_static/current".format(release_path))
        
        return True
        
    except:
        return False
