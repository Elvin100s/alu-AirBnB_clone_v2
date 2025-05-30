from fabric.api import env, run, put, local
from datetime import datetime
import os

env.hosts = ['44.202.60.165', '44.202.132.51']
env.user = 'ubuntu'

def do_pack():
    """Generates a .tgz archive from web_static contents"""
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = f"versions/web_static_{timestamp}.tgz"
        local(f"tar -cvzf {archive_name} web_static")
        return archive_name
    except Exception:
        return None

def do_deploy(archive_path):
    """Distributes archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]
        release_path = f"/data/web_static/releases/{folder_name}/"

        put(archive_path, '/tmp/')
        run(f"mkdir -p {release_path}")
        run(f"tar -xzf /tmp/{file_name} -C {release_path}")
        run(f"rm /tmp/{file_name}")
        run(f"mv {release_path}web_static/* {release_path}")
        run(f"rm -rf {release_path}web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {release_path} /data/web_static/current")
        print("New version deployed!")
        return True
    except Exception:
        return False

def deploy():
    """Creates and distributes archive to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
