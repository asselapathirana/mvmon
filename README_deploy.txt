Deploy with dokku

Need storage
# 
dokku dokku storage:mount mvmon /home/ubuntu/get_data_python:/app/data
dokku dokku storage:mount mvmonsecure /home/ubuntu/get_data_python:/app/data

# it is possible to commit only some of the modified files. 
#Strongly recommended to do that
git add <file>
git commit -m "message" 
# Note no -am , but -m 

# there are two branches. 
git push pubsrv publicmain:main
git push secsrv privatmain:main

# use deploy.bash to automatically update both the branches and deploy to the servers

# developing 

Do all the development in main branch 
git checkout main
<develop>
commit

But when editing loginornot.py go to either 

privatmain or publicmain 

git checkout publicmain
git merge main

# Do not run in main
# Do NOT add loginornot.py to main branch!!!
