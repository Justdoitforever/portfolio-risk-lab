# Fork setup and safe upstream updates

Verified on October 18, 2026:
- Account: Justdoitforever; fork permissions: admin, maintain, push, pull, triage.
- Existing private fork: https://github.com/Justdoitforever/portfolio-risk-lab
- GitHub parent/source: ElijahRange/portfolio-risk-lab (private), default branch main.
- Parent metadata reports license: null. The fork snapshot has no license file.
- No .github/workflows files exist in the fork snapshot. Upstream contents could not be inspected: the connected GitHub app receives 404 for upstream and cross-repository comparison. Current upstream license text and workflows remain unverified.
- scripts/sync.sh is a server origin/main fast-forward deployment pull, not upstream-to-fork synchronization. It does not configure this fork's upstream tracking.

## Local setup

Install Git and Python 3.12. Authenticate Git with your GitHub account when prompted.
Your account needs access to the private upstream to fetch updates. Access through this app and local Git credentials are separate.

Windows PowerShell (no activation or execution-policy changes required):

```powershell
git clone https://github.com/Justdoitforever/portfolio-risk-lab.git
cd portfolio-risk-lab
git remote add upstream https://github.com/ElijahRange/portfolio-risk-lab.git
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt numpy pandas requests
$env:DASH_AUTH_DISABLED = "1"
.\.venv\Scripts\python.exe app.py
```

Unix shell (macOS/Linux):

```bash
git clone https://github.com/Justdoitforever/portfolio-risk-lab.git
cd portfolio-risk-lab
git remote add upstream https://github.com/ElijahRange/portfolio-risk-lab.git
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt numpy pandas requests
DASH_AUTH_DISABLED=1 .venv/bin/python app.py
```

Open http://127.0.0.1:8050 . Disable authentication only for local use. The inspected app binds to 127.0.0.1.
On an existing clone, inspect `git remote -v` before adding upstream; do not replace an existing remote blindly.
Gunicorn in requirements.txt is for the Linux deployment; Windows local development runs app.py.
The requirements file assumes numpy, pandas, and requests are already installed on LinuxONE, hence the extra packages above.
Local installation and runtime have not been tested during this setup.

## Manual upstream sync through pull requests

Run from the clone, using either OS:

```
python scripts/prepare_upstream_sync.py
```

On Windows use `.\.venv\Scripts\python.exe` instead of `python`; on Unix use `.venv/bin/python`.
The script fetches upstream main into a dedicated tracking ref, pushes its commit to a separate SHA-named branch in your fork, and prints a compare link.
It never changes your working tree or main, never resets, never force-pushes, and never merges automatically.
A rewritten upstream tracking history or a conflicting existing sync branch causes Git to reject the operation.
It creates no PR until you click the link and choose **Create pull request**.

In the compare page confirm **base repository: Justdoitforever/portfolio-risk-lab**, **base: main**, and **compare: upstream-sync-...**.
Review and test, then use **Create a merge commit** to retain upstream ancestry. Avoid squash/rebase for recurring upstream syncs.
If GitHub reports conflicts, resolve them on the sync branch before merging; never discard your changes to make a sync succeed.
If there is nothing to compare, no update is needed.
Future upstream default-branch renames require updating the script's explicit main ref after verifying the new default.

No scheduled Actions job is installed: upstream is private and the app cannot read it; a fork's automatic token should not be assumed to grant upstream access.
This manual workflow uses your local Git credentials without storing a token in the repository.

## Access troubleshooting

Open https://github.com/ElijahRange/portfolio-risk-lab while signed in as Justdoitforever.
If unavailable, ask Elijah to invite this account and accept the invitation.
To grant the connected app access, open GitHub **Settings > Applications > Installed GitHub Apps > the app used by Codex > Configure**, and include the repository if you are allowed to manage its installation. Elijah may need to configure access on his account.
Then upstream workflows/license and current commit differences can be inspected.

A fork already exists, so do not click Create repository or create another copy.
If working under a different account without a fork, open the upstream repository, click **Fork > Create a new fork**, select that account as **Owner**, keep the name, select **Copy the main branch only**, then click **Create fork**. A disabled Fork button requires upstream-owner permission/settings changes.
