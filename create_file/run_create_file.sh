python /home/smith/Script/create_file/create_file.py

cd /home/smith/myblog/_posts

filename=`ls -t |head -n1|awk '{print $0}'`

code $filename

exit
