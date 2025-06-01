#!/usr/bin/python3
from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime

# Server configuration
env.hosts = ['44.202.60.165', '44.202.132.51']
env.user = 'ubuntu'  # The username you use to SSH
env.key_filename = '~/.ssh/school'  # Path to your private key

def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ on server
        put(archive_path, '/tmp/')

        # Extract filename and create target directory
        file_name = archive_path.split('/')[-1]
        base_name = file_name.replace('.tgz', '')
        release_path = f'/data/web_static/releases/{base_name}'

        # Create directory and extract archive
        run(f'mkdir -p {release_path}')
        run(f'tar -xzf /tmp/{file_name} -C {release_path}')

        # Move files and clean up
        run(f'mv {release_path}/web_static/* {release_path}/')
        run(f'rm -rf {release_path}/web_static')
        run(f'rm /tmp/{file_name}')

        # Update symbolic link
        run('rm -rf /data/web_static/current')
        run(f'ln -s {release_path} /data/web_static/current')

        print("New version deployed!")
        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
