"""
    Copyright 2013 KU Leuven Research and Development - iMinds - Distrinet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Administrative Contact: dnet-project-office@cs.kuleuven.be
    Technical Contact: bart.vanbrabant@cs.kuleuven.be
"""

import hashlib, subprocess, os, pwd, grp, shutil
  
class LocalIO(object):
    """
        This class provides handler IO methods
    """
    def hash_file(self, path):
        sha1sum = hashlib.sha1()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(32768), b''):
                sha1sum.update(chunk)
        
        return sha1sum.hexdigest()
    
    def run(self, command, arguments = []):
        """
            Execute a command with the given argument and return the result
        """
        cmds = [command] + arguments
        result = subprocess.Popen(cmds, stdout = subprocess.PIPE, 
                                  stderr = subprocess.PIPE)
        
        data = result.communicate()
        
        return (data[0].strip().decode("utf-8"), data[1].strip().decode("utf-8"), result.returncode)
    
    def file_exists(self, path):
        """
            Check if a given file exists
        """
        return os.path.exists(path)
    
    def readlink(self, path):
        """
            Return the target of the path
        """
        return os.readlink(path)
    
    def symlink(self, source, target):
        """
            Symlink source to target
        """
        return os.symlink(source, target)
    
    def is_symlink(self, path):
        """
            Is the given path a symlink
        """
        return os.path.islink(path)
    
    def file_stat(self, path):
        """
            Do a statcall on a file
        """
        stat_result = os.stat(path)
        status = {}
        status["owner"] = pwd.getpwuid(stat_result.st_uid).pw_name
        status["group"] = grp.getgrgid(stat_result.st_gid).gr_name
        status["permissions"] = int(oct(stat_result.st_mode)[-4:])
        
        return status
    
    def remove(self, path):
        """
            Remove a file
        """
        return os.remove(path)
    
    def put(self, path, content):
        """
            Put the given content at the given path
        """
        with open(path, "wb+") as fd:
            fd.write(content)
            
    def chown(self, path, user = None, group = None):
        """
            Change the ownership information
        """
        shutil.chown(path, user, group)
        
    def chmod(self, path, permissions):
        """
            Change the permissions
        """
        os.chmod(path, permissions)
        
    def mkdir(self, path):
        """
            Create a directory
        """
        os.mkdir(path)
        
    def rmdir(self, path):
        """
            Remove a directory
        """
        os.rmdir(path)
        
    def close(self):
        pass


if __name__ == '__channelexec__':
    local_io = LocalIO()
#    fd = open("/tmp/execnet.log", "a+")
    for item in channel:
        if hasattr(local_io, item[0]):
#            fd.write("Calling %s with args %s\n" % item)
            try:
                method = getattr(local_io, item[0])
                result = method(*item[1])
#                fd.write("Got result %s\n" % repr(result))
#
                channel.send(result)
            except Exception as e:
                import traceback
#                fd.write(str(e) + "\n")
#                fd.write(str(traceback.format_exc()))
                channel.send(str(traceback.format_exc()))
                pass
                
        else:
            raise AttributeError("Method %s is not supported" % item[0])
#    fd.close()
