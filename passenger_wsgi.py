# passenger_wsgi.py
import os
import subprocess
import cgi
import traceback
import html

# Workshops (label -> Git URL)
WORKSHOPS = {
    "ml101": "https://github.com/nesi/ml101_workshop.git",
    "ml102": "https://github.com/nesi/ml102_workshop.git",
    "hpc-training": "https://github.com/nesi/hpc_training.git",
}

TARGET_BASE = os.path.join(os.path.expanduser("~"), "reannz_training")

def run_cmd(cmd, cwd=None):
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cwd,
        check=False,
    )
    return proc.returncode, proc.stdout.decode(errors="replace")

def clone_or_update(repo_url, target_dir, branch="main"):
    if os.path.isdir(os.path.join(target_dir, ".git")):
        cmds = [
            ["git", "fetch", "--depth", "1"],
            ["git", "checkout", branch],
            ["git", "reset", "--hard"],
        ]
    else:
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        cmds = [
            ["git", "clone", "--depth", "1", repo_url, target_dir]
        ]

    output = []
    for cmd in cmds:
        rc, out = run_cmd(cmd, cwd=target_dir if os.path.isdir(target_dir) else None)
        output.append(f"$ {' '.join(cmd)}\n{out}\n")
        if rc != 0:
            return rc, "".join(output)
    return 0, "".join(output)

def render_form(message=""):
    options = "\n".join(
        f'<option value="{name}">{name}</option>' for name in WORKSHOPS.keys()
    )
    return f"""<!DOCTYPE html>
<html>
<head><title>Workshop Downloader</title></head>
<body>
  <h1>Download a Workshop</h1>
  {f"<pre>{html.escape(message)}</pre>" if message else ""}
  <form method="POST">
    <label for="workshop">Select workshop:</label>
    <select name="workshop" id="workshop">
      {options}
    </select>
    <br><br>
    <input type="submit" value="Clone / Update">
  </form>
</body>
</html>"""

def application(environ, start_response):
    try:
        method = environ.get("REQUEST_METHOD", "GET")
        if method == "POST":
            # Read form data
            try:
                size = int(environ.get("CONTENT_LENGTH", 0))
            except ValueError:
                size = 0
            body = environ["wsgi.input"].read(size).decode()
            form = dict(item.split("=", 1) for item in body.split("&") if "=" in item)
            selected = form.get("workshop")
            if selected and selected in WORKSHOPS:
                repo_url = WORKSHOPS[selected]
                target_dir = os.path.join(TARGET_BASE, os.path.basename(repo_url).replace(".git", ""))
                rc, out = clone_or_update(repo_url, target_dir)
                message = f"Cloned/updated {selected} into {target_dir}\n\n{out}"
            else:
                message = "Invalid selection."
            response_body = render_form(message)
        else:
            response_body = render_form()

        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [response_body.encode("utf-8")]

    except Exception:
        tb = traceback.format_exc()
        start_response("500 Internal Server Error", [("Content-Type", "text/plain")])
        return [tb.encode("utf-8")]