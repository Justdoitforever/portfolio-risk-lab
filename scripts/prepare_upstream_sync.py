"""Stage upstream main on a separate branch for a manual pull request.
Never checks out, merges, resets, or force-pushes the user's branches.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "https://github.com/ElijahRange/portfolio-risk-lab.git"
ORIGIN = "https://github.com/Justdoitforever/portfolio-risk-lab.git"

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

def main():
    origin = git("remote", "get-url", "--push", "origin")
    if origin not in (ORIGIN, "git@github.com:Justdoitforever/portfolio-risk-lab.git"):
        raise SystemExit("Stopped: origin must point to Justdoitforever/portfolio-risk-lab.")
    # Explicit source and destination avoid changing local branches or FETCH_HEAD.
    git("fetch", "--no-tags", "--no-write-fetch-head", UPSTREAM,
        "refs/heads/main:refs/remotes/upstream-review/main")
    sha = git("rev-parse", "refs/remotes/upstream-review/main")
    if not re.fullmatch(r"[0-9a-f]{40,64}", sha):
        raise SystemExit("Unexpected commit ID.")
    branch = "upstream-sync-" + sha
    # No force: an existing divergent branch is rejected by Git.
    git("push", "origin", sha + ":refs/heads/" + branch)
    print("Open this link, review the diff, then click Create pull request:")
    print("https://github.com/Justdoitforever/portfolio-risk-lab/compare/main..." + branch)
    print("Merge only after review/testing. Conflicts require manual resolution.")
    print("If there is nothing to compare, main already contains this upstream commit.")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        raise SystemExit("Git stopped safely (exit %s). Check repository access and the error above." % exc.returncode)
