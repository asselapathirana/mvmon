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


