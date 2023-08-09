from zipfile import ZipFile
import os, shutil
from subprocess import run
from tempfile import gettempdir
from platform import system
cwd = os.getcwd()

def get_all_file_paths(directory):
  file_paths = []
  for root, directories, files in os.walk(directory):
    for filename in files:
      filepath = os.path.join(root, filename)
      file_paths.append(filepath)
  return file_paths


def write_zipfile():
  with ZipFile('pack.enres', 'w') as pack:
    for f in get_all_file_paths('assets'):
      pack.write(f)
    f=open("objects", "w")
    f.write("Will be needed for the Engine GUI")
    f.close()
    pack.write('objects')
  print("Done packin'")


def read_zipfile():
    if not os.path.exists(tmpdir): os.mkdir(tmpdir)
    if os.path.exists(tmpdir):
      shutil.rmtree(tmpdir)
      os.mkdir(tmpdir)
    with ZipFile('pack.enres', 'r') as pack:
        pack.extractall(path=tmpdir)
    if system == "Linux": os.chdir(tmpdir+"/assets")
    if system == "Windows": os.chdir(tmpdir+"\\assets")

def build(gamepath):
    os.chdir(cwd)
    write_zipfile()
    if not os.path.exists("Build"): os.mkdir("Build")
    run(['pyinstaller', '--onefile', '--name', 'build', '-w', gamepath])
    os.rename('pack.enres', 'Build/pack.enres')
    os.rename('dist/build', 'Build/build')
    shutil.rmtree('dist')
    shutil.rmtree('build')
    os.remove('build.spec')
    os.chdir(tmpdir)
        

if system() == 'Windows': tmpdir = gettempdir() + '\\.getemp'
elif system() == 'Linux': tmpdir = gettempdir() + '/.getemp'
else: tmpdir = gettempdir() + '/.getemp'
if __name__ == "__main__": write_zipfile()
