python /home/smith/Projects/Gen_fixed_header_file/generate_file.py

cd /home/smith/Blog/_posts
filename=`ls -l | tail -n 1 | awk '{print $9}'`


typora $filename

