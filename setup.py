#!/usr/bin/env python3
"""
music production setup
- checks installed commands and rpm packages before installing
- installs available packages from enabled fedora repositories
- downloads and installs the official SnapTune Linux release from GitHub
- creates the LMMS asset folders
- does not remove or overwrite existing projects, presets, or plugins

usage:
    python3 setup.py
    python3 setup.py --check
    python3 setup.py --all
    python3 setup.py --packages
    python3 setup.py --snaptune
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

GITHUB_API = "https://api.github.com/repos/NicoFerni/snaptune/releases/latest"
GITHUB_PAGE = "https://github.com/NicoFerni/snaptune/releases"

# Each entry is: rpm package name -> command used to check whether the app exists.
# Some optional package names can vary by Fedora release/repository. Missing packages
# are reported and skipped rather than causing the entire setup to fail.
PACKAGES = {
    "lmms": "lmms",
    "hydrogen": "hydrogen",
    "guitarix": "guitarix",
    "easyeffects": "easyeffects",
    "calf": "calf",
    "lv2-calf-plugins": None,
    "lv2-x42-plugins": None,
    "ladspa-autotalent-plugins": None,
    "pavucontrol": "pavucontrol",
    "qpwgraph": "qpwgraph",
    "fluidsynth": "fluidsynth",
    "fluid-soundfont-gm": None,
    "fluid-soundfont-gs": None,
    "pipewire-jack-audio-connection-kit": None,
    "cmake": "cmake",
    "ninja-build": "ninja",
    "git": "git",
}

# Ardour's package name has differed across distributions/releases.
ARDOUR_CANDIDATES = ("ardour9", "ardour")

APP_COMMANDS = {
    "LMMS": "lmms",
    "Hydrogen": "hydrogen",
    "Guitarix": "guitarix",
    "EasyEffects": "easyeffects",
    "Ardour": "ardour9 or ardour",
    "REAPER": "reaper",
    "SnapTune standalone": "SnapTune",
}

HOME = Path.home()
LMMS_ASSETS = HOME / "Music" / "LMMS" / "LMMS-assets"
SNAPTUNE_CONFIG = HOME / ".config" / "SnapTune"


def run(command: list[str], *, check: bool = False, capture: bool = False):
    """Run a system command without using a shell."""
    try:
        return subprocess.run(
            command,
            check=check,
            text=True,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None,
        )
    except FileNotFoundError:
        return None


def is_fedora() -> bool:
    try:
        data = Path("/etc/os-release").read_text(encoding="utf-8").lower()
        return "fedora" in data
    except OSError:
        return False


def rpm_installed(package: str) -> bool:
    result = run(["rpm", "-q", package], capture=True)
    return bool(result and result.returncode == 0)


def package_available(package: str) -> bool:
    # dnf info checks enabled repositories and does not install anything.
    result = run(["dnf", "-q", "info", package], capture=True)
    if not result or result.returncode != 0:
        return False
    output = (result.stdout or "") + (result.stderr or "")
    return "Available Packages" in output or "Installed Packages" in output or "Name" in output


def check_report() -> None:
    print("\n=== application command check ===")
    for name, command in APP_COMMANDS.items():
        if name == "Ardour":
            found = shutil.which("ardour9") or shutil.which("ardour")
        elif name == "SnapTune standalone":
            found = shutil.which("SnapTune") or (HOME / ".local/bin/SnapTune").exists()
        else:
            found = shutil.which(command)
        print(f"[{'found' if found else 'not found'}] {name}: {found or command}")

    print("\n=== rpm package check ===")
    for package in PACKAGES:
        print(f"[{'installed' if rpm_installed(package) else 'not installed'}] {package}")

    print("\n=== plugin folder check ===")
    for path in (HOME / ".vst3", HOME / ".lv2"):
        print(f"[{'exists' if path.exists() else 'not found'}] {path}")

    print("\n=== LMMS asset folders ===")
    for folder in ("Drumkits", "Presets", "Samples", "Soundfonts"):
        path = LMMS_ASSETS / folder
        print(f"[{'exists' if path.exists() else 'not found'}] {path}")


def install_packages() -> None:
    if not is_fedora():
        print("This installer is written for Fedora. Package installation was skipped.")
        return
    if not shutil.which("dnf"):
        print("dnf was not found. Cannot install Fedora packages.")
        return

    print("\nChecking Fedora packages. Already-installed packages will be skipped.")
    to_install: list[str] = []

    for package in PACKAGES:
        if rpm_installed(package):
            print(f"[already installed] {package}")
        elif package_available(package):
            print(f"[available] {package}")
            to_install.append(package)
        else:
            print(f"[not found in enabled repositories] {package} (skipping)")

    # Ardour is handled separately because the package name can vary.
    ardour_found = False
    for candidate in ARDOUR_CANDIDATES:
        if rpm_installed(candidate):
            print(f"[already installed] {candidate}")
            ardour_found = True
            break
    if not ardour_found:
        for candidate in ARDOUR_CANDIDATES:
            if package_available(candidate):
                print(f"[available] {candidate}")
                to_install.append(candidate)
                ardour_found = True
                break
    if not ardour_found:
        print("[not found] Ardour package (check your enabled Fedora repositories)")

    if not to_install:
        print("\nNo Fedora packages need installing.")
        return

    print("\nThe following packages will be installed:")
    for package in to_install:
        print(f"  - {package}")
    print("\nFedora may ask for your password through sudo.")
    answer = input("Continue with package installation? [y/N]: ").strip().lower()
    if answer not in ("y", "yes"):
        print("Package installation cancelled.")
        return

    # dnf is invoked once to reduce repeated package-manager operations.
    result = run(["sudo", "dnf", "install", "-y", *to_install])
    if result is None or result.returncode != 0:
        print("One or more packages could not be installed. Review the dnf output above.")
    else:
        print("Package installation command completed.")


def create_lmms_folders() -> None:
    print(f"\nPreparing LMMS asset folders under: {LMMS_ASSETS}")
    for folder in ("Drumkits", "Presets", "Samples", "Soundfonts"):
        path = LMMS_ASSETS / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"[ready] {path}")
    print("Existing files in these folders are left untouched.")


def github_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "fedora-music-production-setup",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def safe_extract(tar: tarfile.TarFile, destination: Path) -> None:
    """Extract only paths that remain inside destination."""
    base = destination.resolve()
    for member in tar.getmembers():
        target = (destination / member.name).resolve()
        if target != base and base not in target.parents:
            raise RuntimeError(f"Unsafe path in archive; refusing to extract: {member.name}")
        if member.issym() or member.islnk():
            raise RuntimeError(f"Archive contains a link; refusing to extract: {member.name}")
    tar.extractall(destination)


def install_snaptune() -> None:
    print("\n=== SnapTune GitHub installer ===")
    target = HOME / ".local/bin/SnapTune"
    vst3 = HOME / ".vst3/SnapTune.vst3"
    lv2 = HOME / ".lv2/SnapTune.lv2"

    if target.exists() and vst3.exists() and lv2.exists():
        print("SnapTune standalone, VST3, and LV2 paths already exist.")
        answer = input("Check GitHub for an update and reinstall the latest release? [y/N]: ").strip().lower()
        if answer not in ("y", "yes"):
            print("SnapTune left unchanged.")
            return

    if platform.machine().lower() not in ("x86_64", "amd64"):
        print("This automatic SnapTune release installer currently targets x86_64 Linux.")
        print(f"Check other builds here: {GITHUB_PAGE}")
        return

    try:
        release = github_json(GITHUB_API)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"Could not contact GitHub: {exc}")
        print(f"Download SnapTune manually from: {GITHUB_PAGE}")
        return

    assets = release.get("assets", [])
    linux_asset = next(
        (
            asset for asset in assets
            if "linux" in asset.get("name", "").lower()
            and asset.get("name", "").lower().endswith((".tar.gz", ".tgz"))
        ),
        None,
    )
    if not linux_asset:
        print("No Linux .tar.gz release asset was found.")
        print(f"Check the release page: {GITHUB_PAGE}")
        return

    print(f"Latest release: {release.get('tag_name', 'unknown')}")
    print(f"Download: {linux_asset['name']}")
    answer = input("Download and run the official SnapTune user-level installer? [y/N]: ").strip().lower()
    if answer not in ("y", "yes"):
        print("SnapTune installation cancelled.")
        return

    with tempfile.TemporaryDirectory(prefix="snaptune-setup-") as temp_name:
        temp = Path(temp_name)
        archive_path = temp / linux_asset["name"]
        request = urllib.request.Request(
            linux_asset["browser_download_url"],
            headers={"User-Agent": "fedora-music-production-setup"},
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response, archive_path.open("wb") as output:
                shutil.copyfileobj(response, output)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            print(f"Download failed: {exc}")
            return

        extracted = temp / "extracted"
        extracted.mkdir()
        try:
            with tarfile.open(archive_path, "r:gz") as tar:
                safe_extract(tar, extracted)
        except (tarfile.TarError, RuntimeError, OSError) as exc:
            print(f"Could not safely extract the archive: {exc}")
            return

        installers = list(extracted.rglob("install.sh"))
        if not installers:
            print("The archive did not contain install.sh. Nothing was executed.")
            print(f"Review the official instructions: {GITHUB_PAGE}")
            return

        installer = installers[0]
        installer.chmod(installer.stat().st_mode | 0o100)
        print(f"Running official installer: {installer}")
        print("This installer should install to your home directory; this script does not use sudo.")
        result = run([str(installer)], check=False)
        if result is None or result.returncode != 0:
            print("SnapTune installer returned an error. Review its output above.")
        else:
            print("SnapTune installer completed. Restart your DAW and rescan plugins.")


def print_manual_notes() -> None:
    print("\n=== manual / optional applications ===")
    print("REAPER: download the Linux build from https://www.reaper.fm/download.php")
    print("         extract it, then run ./install-reaper.sh from the extracted folder.")
    print("         Launch with: reaper")
    print("SnapTune releases: https://github.com/NicoFerni/snaptune/releases")
    print("If an optional Fedora package is skipped, check it with:")
    print("         dnf search <package-name>")
    print("         dnf info <package-name>")


def main() -> int:
    parser = argparse.ArgumentParser(description="check and install a Fedora music production setup")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="only check installed apps and packages")
    group.add_argument("--packages", action="store_true", help="check and install Fedora repository packages")
    group.add_argument("--snaptune", action="store_true", help="download/install the official SnapTune Linux release")
    group.add_argument("--all", action="store_true", help="run checks, install packages, prepare folders, and install SnapTune")
    args = parser.parse_args()

    if not is_fedora():
        print("Note: this script is designed for Fedora Linux.")
    if args.check:
        check_report()
        return 0
    if args.packages:
        install_packages()
        return 0
    if args.snaptune:
        install_snaptune()
        return 0

    # Default action is a guided full setup.
    check_report()
    install_packages()
    create_lmms_folders()
    install_snaptune()
    print_manual_notes()
    print("\nSetup routine finished. Review any skipped packages or errors above.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
