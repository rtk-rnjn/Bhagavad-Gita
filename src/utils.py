from __future__ import annotations

import os
import sys


def set_as_wallpaper(image_path: str) -> None:
    # TODO

    if os.name == "nt":
        import ctypes

        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, image_path, 3
        )

    if os.name == "posix":
        if sys.platform == "linux":
            os.system(
                f"gsettings set org.gnome.desktop.background picture-uri file://{image_path}"
            )

        elif sys.platform == "linux2":
            # Python 3
            os.system(
                f"qdbus org.kde.plasma-desktop /MainApplication org.kde.plasma-desktop.setWallpaper 0 {image_path} 6"
            )

        elif sys.platform == "darwin":
            os.system(
                f'osascript -e \'tell application "Finder" to set desktop picture to POSIX file "{image_path}"\''
            )

        raise NotImplementedError("Your OS is not supported")
