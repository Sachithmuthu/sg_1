#!/bin/sh -e

# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
#source /usr/local/bin/virtualenvwrapper.sh

PYTHONPATH="${PYTHONPATH}:[/usr/local/lib:/home/pi/.virtualenvs/cv/lib/python2.7/site-packages:/usr/bin:/usr/lib/python2.7:/usr/lib/python2.7/plat-linux2:/usr/lib/python2.7/lib-tk:/usr/lib/python2.7/lib-old:/usr/lib/python2.7/lib-dynload:/usr/local/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages:/usr/lib/pymodules/python2.7:/usr/lib/python2.7/dist-packages/IPython/extensions/:/home/pi/.virtualenvs/cv/lib/python2.7/site-packages/pip/_vendor/requests/packages/urllib3/util/"
export PYTHONPATH

#workon cv

#sleep 1

python /home/pi/Desktop/lights/sg_1/pro/rpcode.py &

