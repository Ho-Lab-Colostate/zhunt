import shlex, subprocess
command_line = "zhunt pBR322.txt"
args = shlex.split(command_line)
p = subprocess.Popen(args)
tmp=subprocess.call("./a.out")
