## Identify yourself

Before you do anything else, install Git and associate your commits
with your name.  Some lines are commented out to discourage copying
and pasting without the address changed.  If your favorite text
editor is graphical, you may have to configure it to wait for you
to close the file using a command-line option
(per [digitaldreamer's answer]).

    sudo apt update
    sudo apt install git build-essential
    #git config --global user.email "jdoe@example.com"
    #git config --global user.name "John Doe"
    #git config --global core.editor "nano"

As of 2021-08-13, GitHub's Git remote [no longer accepts passwords].
Thus you must do one of two things: create a [personal access token]
and paste it as your password every time you "push" (upload) your
work to GitHub, or create an SSH key pair and [add its public key]
to your GitHub account.  If you are not behind an especially tight
corporate firewall, SSH may prove more convenient.  This is because
existing HTTPS [credential helpers] as of mid-2021 are made for
proprietary desktop operating systems, not GNU/Linux, though
[libsecret] looks promising.

    ssh-keygen -t rsa
    cat ~/.ssh/id_rsa.pub

[digitaldreamer's answer]: https://stackoverflow.com/a/2596835/2738262
[no longer accepts passwords]: https://github.blog/2020-12-15-token-authentication-requirements-for-git-operations/
[personal access token]: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token
[add its public key]: https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh
[credential helpers]: https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage
[libsecret]: https://www.softwaredeveloper.blog/git-credential-storage-libsecret

## Import a project

A Git repository consists of **commits**, which represent states of the source code as a whole.
Each commit has usually 1 or 2 parent commits representing an earlier state.
The first commit to a repository is an **initial commit** which has no parent.

Based on [Peter's answer] to "Import existing source code to Github":

1. Create the remote repository and get its SSH URL.
2. Unzip the zip distribution into a new folder.
3. Clean up the distribution.
4. Convert documentation to Markdown.
5. Run these commands inside the project:

        git init
        git add .
        git commit -m "Import version X.Y.Z from ZIPURL"

This creates the initial *commit*, or state of the source code.

Or if your working copy has files that shouldn't be tracked quite
yet, but you have a newline-separated list of files that should,
pass this manifest file to Git (per [David King's answer]).
Make sure to do this *before* you set up a `.gitignore` that
includes the manifest file.  Otherwise, Git will complain that
you're adding an ignored file and refuse to do anything.

    git init
    xargs -d \\012 git add < zip.in
    git rm --cached zip.in
    cp ~/path/to/some/gitignore .gitignore
    git add .gitignore
    git commit -m "Import version X.Y.Z from ZIPURL"

Then you can send this new project to the remote.  (A shortcut for
`--set-upstream` is `-u`.

    git remote add origin GITHUBURL
    git push --set-upstream origin master

An alternate method is to clone the repository on the remote first.

1. Create the remote repository and get its SSH or HTTPS URL.
2. Download the repository:

        git clone GITHUBURL

3. Unzip the zip distribution into the resulting folder.
4. Clean up the distribution.
5. Convert documentation to Markdown.
6. Add all new files:

        git add .
        git commit -m 'Import version X.Y.Z from ZIPURL'
        git pull origin master
        git push origin master

## Create a feature branch locally and merge it locally

A commit can have any number of children that represent different directions of change, such as by different developers.
A **branch** represents one of these directions.
When a new repository is created, only one branch exists, with a name like `master`, `main`, or `trunk`.

Say you've got the idea for a bug fix or new feature while riding the bus.
To build this, you create a "feature branch" or "topic branch", a sequence of commits representing the development of this feature.

**List** the existing branches and show which is checked out.

    git branch

**Create** a new branch and switch to it.
Switching to a branch, also called **checking out** the branch, points the special `HEAD` branch at that branch and (if the branch already exists) unpacks that state of the source code into the working copy.

    git checkout -b subseq-optimization

Make changes inside the branch.  This can be done before or after
creating the branch (per [knittl's answer]).

    mousepad src/pentlymusic.s &
    make

**Add new or changed files** to the cart. Git commits changed files
only if they are in the "staging area", which is analogous to a
shopping cart.

    git add src/somenewfile.s

Or remove a file.

    git rm src/obsoletefile.s

Add all changes to tracked files (not newly added files) to the cart.

    git add -u

Add all changes, including added *and removed* files, to the cart.

    git add -A .

Interactively cherry-pick changes in the work tree into the cart.
Calculate `git diff`, show each hunk of diff in each changed text
file, and ask for thumbs up (`y`) or thumbs down (`n`) on adding it.

    git add -p

**Remove a file** from the cart as if it had not been changed
(per [genehack's answer]).

    git reset src/notready.s

Empty the cart.

    git reset

**Revert a file** to the copy in the repository.

    git checkout -- src/messedthisup.s

**Rename a file** in the repository while preserving its history.

    git mv mispeld.s spellcheck.s

**Rename all files in a directory** so that syntax highlighting can
recognize them (per [thkala's answer]).

    find -type f -name '*.s' | while read f; do git mv "$f" "${f%.s}.z80"; done
    # Or the following if a filename contains newlines, which
    # shouldn't happen in a well-behaved repository
    find -type f -name '*.s' -print0 | while read -d $'\0' f; do git mv "$f" "${f%.s}.z80"; done

**Show a summary of what has been changed** since the last commit.

    git status

Or a line-by-line difference of changes since the last commit.

    git diff HEAD

Or only changes not added to cart.

    git diff

Or only changes that have been added to cart.  This shows what will
be committed.  (Both commands mean the same.)

    git diff --cached
    git diff --staged

Or all changes since the commit before last.

    git diff HEAD^

Or all changes made in the last commit.  Either of these works:

    git diff HEAD^ HEAD
    git show HEAD

View a file from two commits ago (per [mipadi's answer]).

    git show HEAD~2:src/floorvram.s

**Exclude files or directories** from inclusion in the repository, such as intermediate object code files, converted graphics or audio, or binary releases. (See [gitignore docs] for how to specify paths and wildcards.)

    nano .gitignore
    git add .gitignore

Or exclude files or directories only from your copy of the
repository, without disclosing their paths to collaborators.

    nano .git/info/exclude

**Commit changes** that have been added to the cart, with a message describing the change. Some remotes watch for specially formatted messages and use them to trigger actions such as closing issue reports.

    git commit -m "Fix #13: blah blah check if null"

Or add a commit with a longer message spanning multiple lines.  This opens a text file in your chosen text editor to compose the message.  Once you save the file and close the editor, Git uses the first 50 characters of the first line as the summary.

    git commit

Or add all changed files to the cart and commit them, skipping newly created files.  These are equivalent:

    git add -u && git commit -m "Update chat server list"
    git commit -am "Update chat server list"

Do the same while adding to the commit message a signature that the changes are yours. Some projects require this signature to trace responsibility for copyright in changes.

    git commit -a -s

Add changes in the cart to the last commit or correct its commit
message before you push it.

    git commit --amend

(See also "[How to Write a Git Commit Message]" by Chris Beams.)

Commits are added to `HEAD`, which should be on a feature branch at this point.
After a commit is added, the branch is moved to point at the child commit.
Once you have made progress on the branch, switch back to `master` and **merge** changes from the branch.

    git checkout master && git merge subseq-optimization

**Delete a branch** that has been merged and is no longer needed.

    git branch -d subseq-optimization

Scoot back and admire your work by viewing the **commit log**.

    git log -10
    git log --since='3 days ago'
    git log --until=2015-12-31

View the commit messages of commits that changed a file
(per [Richard and VolkA]).

    git log -- kitten.txt

See all diffs to a file.

    git log -p kitten.txt

**Tag** the latest commit with a version number.
Occasionally you may want to release your software, which creates a tarball or zipfile suitable for use by people who do not use Git or even a compiler.
A tag acts as a long-term nickname for a particular commit.
Some remotes use a tag to associate a binary release with the corresponding commit.
A common naming convention for tags uses the letter `v` followed by a group of numbers separated by periods.
These numbers often follow the [SemVer] spec for production software or the [0ver] spec for early experimental software.

    git tag v0.05wip4

Remove outdated files and **estimate the total size** of the
repository (per [VonC's answer]).

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

[Peter's answer]: https://stackoverflow.com/a/8012698/2738262
[David King's answer]: https://unix.stackexchange.com/a/244172/119806
[knittl's answer]: https://stackoverflow.com/a/1394804/2738262
[genehack's answer]: https://stackoverflow.com/a/348234/2738262
[thkala's answer]: https://stackoverflow.com/a/4509530/2738262
[gitignore docs]: https://git-scm.com/docs/gitignore
[mipadi's answer]: https://stackoverflow.com/a/338470/2738262
[How to Write a Git Commit Message]: https://chris.beams.io/posts/git-commit/
[Richard and VolkA]: https://stackoverflow.com/q/278192/2738262
[SemVer]: https://semver.org/
[0ver]: https://0ver.org/
[VonC's answer]: https://stackoverflow.com/a/16163608/2738262

## Fixing serious mistakes

Say things go horribly wrong in your repo, and you've already
committed.  If you haven't done `git gc` recently, you can probably
recover your data.  Visit [Oh Shit, Git!?!] to see how.  Eevee's
2015 article "[Just enough Git to be (less) dangerous]" may help
build your mental model enough to understand the documentation.

[Oh Shit, Git!?!]: https://ohshitgit.com/
[Just enough Git to be (less) dangerous]: https://eev.ee/blog/2015/04/24/just-enough-git-to-be-less-dangerous/

## Working with out-of-band change submissions

Review a folder containing individual files that you modified while
on break on someone else's computer where you do not have the full
repository cloned.  This folder in your Dropbox or extracted using
`unzip` contains only those files that were modified.  (The `-D` flag
allows `git diff` to produce "irreversible deletes".  Without `-D`,
the diff includes the full text of each unmodified file.)

    git diff -D src ~/Dropbox/myproject/changes

Then merge the changes into your working copy.

    cp ~/Dropbox/myproject/changes/* src

TODO: `git request-pull` and how it differs from GitHub pull request

## Working with remote repositories (such as GitHub)

The first time you contribute to a project, copy its repository to your computer.  This downloads its contents and sets up the `origin` link, which lets you keep up to date with changes to a remote repository.

    git clone GITHUBURL

Once it's cloned, you can branch and commit locally.
To publish the new branch to the remote, use the `-u` switch (per
[Daniel Ruoso's answer]), added in Git 1.7, to set up the connection.

    git push -u origin subseq-optimization

Once you set up the connection, you'll usually want to pull before pushing to ensure that your local repository has not fallen behind. Otherwise, you'll get the [non-fast-forward](https://help.github.com/articles/dealing-with-non-fast-forward-errors/) error.

    git pull origin subseq-optimization
    git push origin subseq-optimization

If the remote has "pull request" functionality to associate merges with issues and perform them, you can do the merge that way. Or you can do the merge locally and then push the changes:

    git checkout master
    git merge subseq-optimization
    git push origin master

GitHub uses "fork" to refer to a downstream copy of someone else's
repository used for making changes and submitting them upstream
through pull requests.  Once you've made a fork and cloned it, add
the upstream as an additional remote.

    git remote -v
    git remote add upstream https://github.com/gbdev/database.git

Synchronize changes from the parent project.

    git pull upstream master
    git push origin master

If it's been a while, there might be a lot of changes in the parent
that you have not incorporated.  Another way to merge is to replay
your changes on top of the parent's HEAD.

    git fetch upstream master
    git rebase upstream/master
    git push origin master

Then reapply work done in a feature branch on top of synced changes.

    git checkout subseq-optimization
    git rebase master

If you're starting a new project from a template repository,
[clone it as a new project].  First create `my-game` as an empty
repository on GitHub and treat it as the upstream repository.
Then clone the template into a new folder.

    git clone https://github.com/pinobatch/nrom-template.git PROJECT
    cd PROJECT
    git remote rename origin upstream
    git remote add origin https://github.com/USERNAME/PROJECT.git
    git push -u origin master

[Daniel Ruoso's answer]: https://stackoverflow.com/a/6232535/2738262
[clone it as a new project]: https://web.archive.org/web/20170114224227/http://bitdrift.com/post/4534738938/fork-your-own-project-on-github

## Working with non-text file types

Git is designed for file types that can be represented as a sequence
of lines of text.  This includes program source code, HTML, CSS,
and Scalable Vector Graphics (SVG).  These formats are "diffable,"
meaning that a program can calculate differences and apply those
differences when merging changes.

Many video games and other applications include images that the
program displays while it is running, and not all are in a diffable
format such as SVG.  In the [gbdev Discord server], [Eevee] (of "PHP:
a fractal of bad design" fame) provided a formula to have `git diff`
run common image types through ImageMagick.  Her formula, similar
to the one in the article "[Image diffs with git]" by Aki Koskinen,
won't help much with a merge, but it should still help you spot-check
changes that you're about to commit.

`~/.local/bin/git-imgdiff`:

    #!/bin/sh
    compare -metric PHASH "$2" "$1" png:- \
      | montage -tile 1x -geometry +4+4 "$2" - "$1" png:- \
      | display -title "$1" -
    # don't forget to chmod +x ~/.local/bin/git-imgdiff

`~/.gitattributes-global`:

    *.gif diff=image
    *.jpeg diff=image
    *.jpg diff=image
    *.png diff=image

`~/.gitconfig`:

    [core]
        attributesfile = ~/.gitattributes-global
    [diff "image"]
        command = ~/.local/bin/git-imgdiff

[gbdev Discord server]: https://gbdev.io/chat.html
[Eevee]: https://eev.ee/
[Image diffs with git]: https://akikoskinen.info/image-diffs-with-git/

## Working with managers

Record a time-lapse video of your day to prove to yourself and others how much time you spend on various types of task.  Based on [FFmpeg desktop capture].  Using FFmpeg on X Window System (on FreeBSD or Linux):

    ffmpeg -y -f x11grab -video_size 1024x768 -framerate 1/2 -i :0.0 \
      -filter:v "setpts=PTS/60,fps=30" \
      ~/Desktop/rec.mp4

The first line takes a screenshot of the primary screen every 2 seconds, and the second speeds up playback to 60 times real time so that each minute of the video represents one hour of real time.

[FFmpeg desktop capture]: https://trac.ffmpeg.org/wiki/Capture/Desktop
