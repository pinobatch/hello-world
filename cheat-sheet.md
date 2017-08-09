## Identify yourself

Before you do anything else, install Git and associate your commits
with your name.  (Some lines are commented out to discourage copying
and pasting without the address changed.)

    sudo apt-get update
    sudo apt-get install git build-essential
    #git config --global user.email "jdoe@example.com"
    #git config --global user.name "John Doe"

## Import a project

Based on an [answer to "Import existing source code to Github" by Peter](https://stackoverflow.com/a/8012698/2738262):

1. On GitHub, create the remote repository and get the HTTPS URL of the repository.
2. Unzip the zip distribution into a new folder.
3. Clean up the distribution.
4. Convert any documentation to Markdown.
5. Run these commands inside the project:

        git init
        git add .
        git commit -m "Imported version X.Y.Z from ZIPURL"

Or if your working copy has files that shouldn't be tracked
quite yet, but you have a newline-separated list of files that
should, you can pass this manifest file to Git
[using `xargs`](http://unix.stackexchange.com/a/244172/119806).
But make sure to do this *before* you set up a `.gitignore` that
includes the manifest file.  Otherwise, Git will complain that you're
adding an ignored file and refuse to do anything.

    git init
    xargs -d \\012 git add < zip.in
    git rm --cached zip.in
    cp ~/path/to/some/gitignore .gitignore
    git add .gitignore
    git commit -m "Imported version X.Y.Z from ZIPURL"

Then you can send this new project to GitHub.

    git remote add origin GITHUBURL
    git push --set-upstream origin master

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

**List** the existing branches and show which is checked out.

    git branch

**Create** a new branch and switch to it.

    git checkout -b subseq-optimization

Make changes inside the branch. This can actually be done before or after creating the branch ([thanks knittl](https://stackoverflow.com/a/1394804/2738262)).

    mousepad src/pentlymusic.s &
    make

**Add new or changed files** to the cart. Git commits changed files only if they are in the "staging area", which is analogous to a shopping cart.

    git add src/somenewfile.s

Or remove a file.

    git rm src/obsoletefile.s

Add all changes to tracked files (not newly added files) to the cart.

    git add -u

Or just add all additions and removals to the cart.

    git add -A .

**Remove a file** from the cart as if it had not been changed ([thanks genehack](https://stackoverflow.com/a/348234/2738262)).

    git reset src/notready.s

Empty the cart.

    git reset

**Revert a file** to the copy in the repository.

    git checkout -- src/messedthisup.s

**Show a summary of what has been changed** since the last commit.

    git status

Or a line-by-line difference of changes since the last commit.

    git diff HEAD

Or only changes not added to cart.

    git diff

Or only changes that have been added to cart. This shows what will be committed.

    git diff --cached

Or all changes since the commit before last.

    git diff HEAD^

Or all changes made in the last commit.  Either of these works:

    git diff HEAD^ HEAD
    git show HEAD

**Commit changes** that have been added to the cart, with a message describing the change. Some remotes watch for specially formatted messages and use them to trigger actions such as closing issue reports.

    git commit -m "fixes #13"

Or add all changed files to the cart and commit them, skipping newly created files.  These are equivalent:

    git add -u && git commit -m "update chat server list"
    git commit -am "update chat server list"

Do the same while adding to the commit message a signature that the changes are yours. Some projects require this signature to trace responsibility for copyright in changes.

    git commit -a -s

Or add more changes to the last commit before you push them.

    git commit -a --amend

Switch back to master and **merge** changes from the branch.

    git checkout master && git merge subseq-optimization

Scoot back and admire your work by viewing the **commit log**.

    git log -10
    git log --since='3 days ago'
    git log --until=2015-12-31

**Tag** the latest commit with a version number. Occasionally you may want to release your software, which creates a tarball or zipfile suitable for use by people who do not use Git or even a compiler.  A tag identifies a release, and some remotes use it to associate a binary release with the corresponding source release.

    git tag v0.05wip4

Remove outdated files and **estimate the total size** of the repository ([thanks VonC](https://stackoverflow.com/a/16163608/2738262)).

    git gc
    git count-objects -vH | grep size-pack

List all tracked files whose name does not begin with a dot.  This helps determine what files to include in a release archive.

    git ls-files | grep -e "^[^.]"

This can be incorporated into a makefile:

    .PHONY: dist
    dist: mygame-git.zip
    mygame-git.zip: \
      zip.in mygame.nes README.md CHANGES.txt $(objdir)/index.txt
    	zip -9 -u $@ -@ < $<
    zip.in:
    	git ls-files | grep -e "^[^.]" > $@
    	echo zip.in >> $@

## Working with remote repositories (such as GitHub)

The first time you contribute to a project, copy its repository to your computer.  This downloads its contents and sets up the `origin` link, which lets you keep up to date with changes to a remote repository.

    git clone GITHUBURL

Once it's cloned, you can branch and commit locally.  To publish the new branch to the remote, use the [`-u` switch](https://stackoverflow.com/a/6232535/2738262), added in Git 1.7, to set up the connection.

    git push -u origin subseq-optimization

Once you set up the connection, you'll usually want to pull before pushing to ensure that your local repository has not fallen behind. Otherwise, you'll get the [non-fast-forward](https://help.github.com/articles/dealing-with-non-fast-forward-errors/) error.

    git pull origin subseq-optimization
    git push origin subseq-optimization

If the remote has "pull request" functionality to associate merges with issues and perform them, you can do the merge that way. Or you can do the merge locally and then push the changes:

    git checkout master
    git merge subseq-optimization
    git push origin master

If you're starting a new project from a template released on GitHub, you can fork it *unless* the repository is your own. If it's yours, you have to manually [check it out and check it in as a different project](http://bitdrift.com/post/4534738938/fork-your-own-project-on-github). First create `my-game` as an empty repository on GitHub. Then clone your existing project into a new folder:

    git clone https://github.com/pinobatch/nrom-template.git PROJECT
    cd PROJECT
    git remote rename origin upstream
    git remote add origin https://github.com/USERNAME/PROJECT.git
    git push -u origin master

To sync changes from the parent project:

    git pull upstream master
    git push origin master
