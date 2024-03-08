Deploy with dokku

Need storage
# 
dokku dokku storage:mount mvmon /home/ubuntu/get_data_python:/app/data
dokku dokku storage:mount mvmonsecure /home/ubuntu/get_data_python:/app/data

# there are two branches. 
git push srv public:main 
git push secsrv secure:main

# developing 

Do all the development in main branch 
git checkout main
<develop>
commit

But when running or editing loginornot.py go to either 

privatmain or publicmain 

git checkout publicmain
git merge main

# Do not run in main
# Do NOT add loginornot.py to main branch!!!
