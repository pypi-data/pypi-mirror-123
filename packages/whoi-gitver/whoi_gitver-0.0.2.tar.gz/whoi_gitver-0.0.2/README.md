# gitver

gitver is a simple script that generates a string to describe the version status of a git repository.

## Format

gitver presumes that the git repository is using tags to track version releases and that those tags adhere to the semantic versioning format of vMAJOR.MINOR.PATCH.

It will generate a string that includes the git project name, branch name, tagged version number, and status of the working copy.

### Clean working copy example
gitver\_master\_v0.0.1

### Some number n commits beyond a tagged version
gitver\_master\_v0.0.1-2-98a7gb37
Where the number of commits and the latest commit hash are appended

### Local
If the working copy is out of sync with the origin remote, then -local will be appended to the end of the string

### Dirty
If the working copy has changes that have not been committed or files that have not been added to version control, then -dirty will be appended to the end of the string.
