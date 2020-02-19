python3 /home/smith/Projects/touch_post/touch.py
cd /home/smith/Blog/_posts
filename=`ls -l | tail -n 1 | awk '{print $9}'`
typora $filename

