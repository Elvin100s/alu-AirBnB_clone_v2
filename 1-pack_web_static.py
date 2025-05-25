#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        # Create versions folder if it doesn't exist
        if not os.path.exists("versions"):
            local("mkdir -p versions")

        # Create timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_{}.tgz".format(timestamp)

        # Compress web_static directory
        print("Packing web_static to {}".format(archive_name))
        result = local("tar -cvzf {} web_static".format(archive_name))

        # Check if archive was created successfully
        if result.succeeded:
            archive_size = os.path.getsize(archive_name)
            print("web_static packed: {} -> {}Bytes".format(
                archive_name, archive_size))
            return archive_name
        return None
    except Exception as e:
        return None
