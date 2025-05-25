#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime

env.hosts = ['54.157.32.137', '52.55.249.213']  # Replace with your server IPs
env.user = 'ubuntu'  # Replace with your username
env.key_filename = '~/.ssh/id_rsa'  # Replace with your SSH key path


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract archive filename without extension
        archive_filename = archive_path.split('/')[-1]
        archive_name = archive_filename.split('.')[0]
        release_path = '/data/web_static/releases/{}'.format(archive_name)

        # Create target directory
        run('mkdir -p {}'.format(release_path))

        # Uncompress the archive
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))

        # Remove the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move files from web_static subfolder to release path
        run('mv {}/web_static/* {}'.format(release_path, release_path))

        # Remove the empty web_static directory
        run('rm -rf {}/web_static'.format(release_path))

        # Delete the old symbolic link
        run('rm -rf /data/web_static/current')

        # Create new symbolic link
        run('ln -s {} /data/web_static/current'.format(release_path))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False
