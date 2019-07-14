import os
import subprocess

PROJECT_PATH = os.path.abspath(os.curdir) + '/'
PROJECT_FOLDER = PROJECT_PATH.split('/')[-2]
CONF_PATH = PROJECT_PATH + PROJECT_FOLDER + '.conf'

f = open(CONF_PATH, "w")
text = ''
programs = ['websockets/wsBibox', 'websockets/wsBinance', 'websockets/wsBitmart',
            'websockets/wsBittrex', 'websockets/wsHitbtc', 'websockets/wsHuobi',
            'websockets/wsOkex', 'monitor']
for program_path in programs:
    block = f'''
[program:{'e' + program_path.split('/')[-1]}]
command={PROJECT_PATH}venv/bin/python {PROJECT_PATH}{program_path}.py
stdout_logfile=/var/log/{PROJECT_FOLDER}/{program_path.replace('calculator/rel/', '')}.log
stderr_logfile=/var/log/{PROJECT_FOLDER}/{program_path.replace('calculator/rel/', '')}_ERR.log
stdout_logfile_maxbytes = 5MB
stderr_logfile_maxbytes = 5MB
stdout_logfile_backups = 0
stderr_logfile_backups = 0
autorestart = false
autostart = false
startsecs = 0
user=root
stopsignal=KILL
numprocs=1
\n\n\n\n'''
    text += block
f.write(text)
f.close()

files = ['websockets/wsBibox.py', 'websockets/wsBinance.py', 'websockets/wsBitmart.py',
         'websockets/wsBittrex.py', 'websockets/wsHitbtc.py', 'websockets/wsHuobi.py',
         'websockets/wsOkex.py', ]

for f in files:
    subprocess.call([f'''sed -i "s%# import sys%import sys%g" "{PROJECT_PATH}{f}"'''], shell=True)
    subprocess.call([f'''sed -i "s%# sys.path.append(PROJECT_PATH)%sys.path.append('{PROJECT_PATH}')%g" "{f}"'''],
                    shell=True)
subprocess.call([f'''sed -i "s%/home/kusko/PyProjects/CryptoEye/%{PROJECT_PATH}%g" "config.py"'''], shell=True)
print('Done')
