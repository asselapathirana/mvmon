#!/bin/bash
git checkout main
git status
read -p "Check if everything is committed. Press [Enter] to continue..."
git checkout privatmain
git merge main
git push origin privatmain
read -p "Press [Enter] to push to private server..."
git push secsrv privatmain
read -p "Press [Enter] to push to public server..."
git checkout publicmain
git merge main
git push origin publicmain
git push pubsrv publicmain
git checkout main



