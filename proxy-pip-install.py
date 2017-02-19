import sys
import os
import commands


libpath=os.path.join('lib','site-packages')
if os.path.exists(libpath):
    sys.path.append(libpath)
else:
    libpath=os.path.join('lib','python2.6','site-packages')
    if os.path.exists(libpath):
        sys.path.append(libpath)
    else:
        libpath='.'

bin=os.path.join('bin','pip')
if not os.path.exists(bin):
    bin=os.path.join('scripts','pip.exe')
test_command = ''.join(('PYTHONPATH=',libpath, ' ', bin,' install -r requirements.txt --prefix -I'))
stdout = commands.getoutput(test_command)
print stdout