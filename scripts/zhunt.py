import shlex, subprocess
command_line = "zhunt 12 6 12 pBR322.fasta"
args = shlex.split(command_line)
p = subprocess.Popen(args)
tmp=subprocess.call("./a.out")
