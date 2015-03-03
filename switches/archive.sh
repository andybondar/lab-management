#!/bin/bash

directory=`date +%s`

mkdir -p ../../$directory/switches
cp requirements.txt blink.py ../../$directory/switches/
cd ../../$directory/switches/
virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt
deactivate

wd=`pwd`
arr=($(grep $wd/.env $wd/.env/bin/* | awk -F":" '{print $1}'))
for i in ${arr[@]};
do sed -i s,$wd,/home/virtualenv/switches,g $i
done

echo '#!/bin/bash' > venv.sh
echo 'wd=`pwd`' >> venv.sh
echo 'arr=($(grep /home/virtualenv/switches/.env $wd/.env/bin/* | awk -F":" '\''{print $1}'\''))' >> venv.sh
echo 'for i in ${arr[@]};' >> venv.sh
echo ' do sed -i s,/home/virtualenv/switches,$wd,g $i' >> venv.sh
echo 'done' >> venv.sh
chmod 755 venv.sh

cd ..
tar cvfz switches.tar.gz switches/
mv switches.tar.gz ../switches.tar.gz
cd ..
rm -rf $directory/