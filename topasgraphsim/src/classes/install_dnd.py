import ctypes
import os
import shutil
import site
import sys
import urllib.request


class InstallDnD:
    def __init__(self):

        self.install_success = False
        self.message = ""

        try:
            operating_system = sys.platform

            if "linux" in operating_system:
                operating_system = "linux-x64.tgz"

            if "darwin" in operating_system:
                operating_system = "osx-x64.tgz"

            if "win" in operating_system and "darwin" not in operating_system:
                if ctypes.sizeof(ctypes.c_voidp) == 4:
                    operating_system = "windows-x86.zip"
                else:
                    operating_system = "windows-x64.zip"

            package_paths = site.getsitepackages()
            tcl_path = os.path.join(package_paths[0], "tcl")
            site_path = package_paths[1]
            cur_dir = os.path.dirname(os.path.realpath(__file__))
            os.path.join(cur_dir, "..", "resources")

            tcl_link = (
                "https://github.com/petasis/tkdnd/releases/download/tkdnd-release-test-v2.9.2/tkdnd-2.9.2-"
                + f"{operating_system}"
            )
            urllib.request.urlretrieve(
                tcl_link,
                os.path.join(
                    os.path.join(cur_dir, "..", "resources", "temp"),
                    os.path.basename(tcl_link),
                ),
            )
            shutil.unpack_archive(
                os.path.join(
                    os.path.join(cur_dir, "..", "resources", "temp"),
                    os.path.basename(tcl_link),
                ),
                os.path.realpath(os.path.join(cur_dir, "..", "resources", "temp")),
            )
            os.remove(
                os.path.join(
                    os.path.join(cur_dir, "..", "resources", "temp"),
                    os.path.basename(tcl_link),
                )
            )
            shutil.move(
                os.path.join(
                    os.path.realpath(os.path.join(cur_dir, "..", "resources", "temp")),
                    os.listdir(
                        os.path.realpath(
                            os.path.join(cur_dir, "..", "resources", "temp")
                        )
                    )[0],
                ),
                tcl_path,
            )

            shutil.copytree(
                os.path.join(cur_dir, "..", "resources", "TkinterDnD2"),
                os.path.join(os.path.realpath(site_path), "TkinterDnD2"),
            )

            self.install_success = True
        except Exception as e:
            self.message = e
