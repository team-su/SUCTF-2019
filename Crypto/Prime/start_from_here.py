import os
port = 22222
command = 'socat -d -d tcp-l:' + str(port) + ',reuseaddr,fork EXEC:"python -u server.py" '
os.system(command)