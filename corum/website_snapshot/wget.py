import tempfile
import subprocess
import shutil
import os
import zipfile

class Wget(object):

    url = None
    args = None
    change_links = False
    user_agent = None
    tmp_dir = None
    cmds = None

    def __init__(self, url, change_links=False, args=None, user_agent=None):
        self.url = url
        if change_links:
            self.change_links = True
        self.args = args
        if user_agent:
            self.user_agent = user_agent
        self.pass_cmds()

    def pass_cmds(self):
        cmds = ['/usr/local/bin/wget', '-E', '-H', '-p']
        if self.change_links:
            cmds.append('-k')
            cmds.append('-K')
        if self.user_agent:
            cmds.append('-U')
            cmds.append("'%s'" % (self.user_agent))
        cmds.append('-e')
        cmds.append('robots=off')
        cmds.append(self.url)
        self.cmds = cmds

    def start(self):
        self.tmp_dir = tempfile.mkdtemp()
        output = subprocess.check_output(self.cmds, cwd=self.tmp_dir)

    def _zip(self):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        zp = zipfile.ZipFile(tmp, 'w')
        for root, dirs, files in os.walk(self.tmp_dir):
            for file in files:
                arc_name = os.path.join(root, file).split(self.tmp_dir + '/')[-1]
                zp.write(os.path.join(root, file), arc_name)
        zp.close()
        tmp.close
        return tmp.name

    def __del__(self):
        if self.tmp_dir:
            shutil.rmtree(self.tmp_dir)


class UserAgent:
    CHROME = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.27 "
              "(KHTML, like Gecko) Chrome/26.0.1389.0 Safari/537.27")

