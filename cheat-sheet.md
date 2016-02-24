## How to import a project

Based on an [answer to "Import existing source code to Github" by Peter][1]

1. On GitHub, create the remote repository and get the HTTPS URL of the repository.
2. Unzip the zip distribution into a new folder.
3. Clean up the distribution.
4. Convert any documentation to Markdown.
5. Run these commands:

        git init
        git add .
        git commit -m 'Imported version X.Y.Z from ZIPURL'
        git remote add origin GITHUBURL
        git pull origin master
        git push origin master

## How to create a feature branch locally and push it to GitHub

Say you've got the idea for a bug fix or new feature while riding the bus.

## How to 

[1]: http://stackoverflow.com/a/8012698/2738262
