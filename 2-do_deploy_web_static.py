from fabric.api import env, put, run
import os

env.user = 'ubuntu'
env.hosts = ['44.202.60.165', '44.202.132.51']

def do_deploy(archive_path):
    """Deploys an archive to the web servers."""
    if not os.path.isfile(archive_path):
        return False

    try:
        filename = archive_path.split("/")[-1]
        name_no_ext = filename.split(".")[0]
        release_path = f"/data/web_static/releases/{name_no_ext}/"
        tmp_path = f"/tmp/{filename}"

        # Upload the archive to /tmp/
        put(archive_path, tmp_path)

        # Remove existing release folder if it exists to avoid mv conflict
        run(f"rm -rf {release_path}")
        run(f"mkdir -p {release_path}")

        # Uncompress the archive to the release directory
        run(f"tar -xzf {tmp_path} -C {release_path}")

        # Move the contents out of the web_static folder
        run(f"mv {release_path}web_static/* {release_path}")

        # Remove the now-empty web_static folder
        run(f"rm -rf {release_path}web_static")

        # Delete the archive from the server
        run(f"rm {tmp_path}")

        # Delete the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run(f"ln -s {release_path} /data/web_static/current")

        print("New version deployed!")
        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
