python /home/smith/Projects/create_file/create_file.py

cd /home/smith/Blog/_posts
filename=`ls -l | tail -n 1 | awk '{print $9}'`


typora $filename

