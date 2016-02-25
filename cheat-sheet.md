## Import a project

Based on an [answer to "Import existing source code to Github" by Peter](http://stackoverflow.com/a/8012698/2738262):

1. On GitHub, create the remote repository and get the HTTPS URL of the repository.
2. Unzip the zip distribution into a new folder.
3. Clean up the distribution.
4. Convert any documentation to Markdown.
5. Run these commands inside the project:

        git init
        git add .
        git commit -m 'Imported version X.Y.Z from ZIPURL'
        git remote add origin GITHUBURL
        git pull origin master
        git push origin master

An alternate method is to clone the GitHub repository first.

1. On GitHub, create the remote repository and get the HTTPS URL of the repository.
2. Download the repository:

        git clone GITHUBURL

3. Unzip the zip distribution into the resulting folder.
4. Clean up the distribution.
5. Convert any documentation to Markdown.
6. Add all new files:

        git add .
        git commit -m 'Imported version X.Y.Z from ZIPURL'
        git pull origin master
        git push origin master

## Create a feature branch locally and merge it locally

Say you've got the idea for a bug fix or new feature while riding the bus. For this, you create a branch of the tree, sometimes called a feature branch or topic branch.

**List** the existing branches.

    git branch

**Create** a new branch and switch to it.

    git checkout -b subseq-optimization

Make changes inside the branch.

    gedit src/pentlymusic.s &
    make

**Add new or changed files** to the cart. Git commits changed files only if they are in the "staging area", which is analogous to a shopping cart.

    git add src/somenewfile.s

Or remove a file:

    git rm src/obsoletefile.s

Or just add all additions and removals to the cart:

    git add -A .

**Show changes** since the last commit.

    git diff HEAD

Or only changes not added to cart.

    git diff

Or only changes that have been added to cart.

    git diff --cached

Or all changes since the commit before last.

    git diff HEAD^

**Commit changes** that have been added to the cart.

    git commit

Or add all changed files to the cart and commit them. Newly created files are skipped; they must be added manually.

    git commit -a

Do the same while adding to the commit message a signature that the changes are yours. Some projects require this signature to trace responsibility for copyright in changes.

    git commit -a -s

Or add more changes to the last commit.

    git commit -a --amend

Switch back to master and **merge** changes from the branch.

    git checkout master && git merge subseq-optimization

Scoot back and admire your work by viewing the **commit log**.

    git log -10
    git log --since='3 days ago'
    git log --until=2015-12-31

**Tag** the latest commit with a version number. Occasionally you may want to release your software, which creates a tarball or zipfile suitable for use by people who do not use Git.  A tag identifies a release.

        git tag v0.05wip4

## Working with remote repositories (e.g. GitHub)

The first time you contribute to a project, copy its repository to your computer.  This downloads its contents and sets up the `origin` link, which lets you keep up to date with changes to a remote repository.

    git clone GITHUBURL

Once it's cloned, you can branch and commit locally.  To publish the new branch to the remote, use the [`-u` switch](http://stackoverflow.com/a/6232535/2738262), added in Git 1.7, to set up the connection.

    git push -u origin subseq-optimization

Once you set up the connection, you'll usually want to pull before pushing to ensure that your local repository has not fallen behind. Otherwise, you'll get the [non-fast-forward](https://help.github.com/articles/dealing-with-non-fast-forward-errors/) error.

    git pull origin subseq-optimization
    git push origin subseq-optimization

If the remote has "pull request" functionality to associate merges with issues, you can do the merge that way. Or you can do the merge locally:

    git checkout master
    git merge subseq-optimization
    git push origin master
