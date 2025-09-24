#!/bin/bash

################################################################################
# https://containers.dev/implementors/json_reference/
# initializeCommand
# >>> onCreateCommand
# updateContentCommand
# postCreateCommand
# postStartCommand
# postAttachCommand
#
# This command is the first of three (along with updateContentCommand and 
# postCreateCommand) that finalizes container setup when a dev container is 
# created. It and subsequent commands execute inside the container immediately 
# after it has started for the first time.
#
# Cloud services can use this command when caching or prebuilding a container. 
# This means that it will not typically have access to user-scoped assets or 
# secrets.
#
# Note that the array syntax will execute the command without a shell. You can 
# learn more about formatting string vs array vs object properties.
#
################################################################################

# Install required packages
DEBIAN_FRONTEND=noninteractive apt-get update -qq \
  && apt-get install -y --no-install-recommends -qq \
    bash-completion \
    python3-virtualenv \
    python3-ipython

# Create Python virtual environment and activate it
virtualenv --system-site-packages --no-seed .venv
source .venv/bin/activate

# Install Odoo Python debugger extension
python -m pip install pydevd-odoo

# Configure Git to use LF endings and avoid EOL issues
# Prevents large PRs due to EOL changes
git config --global core.autocrlf input
git config --global core.eol lf

# Ensure .gitignore in /mnt/extra-addons contains required entries
GITIGNORE_PATH="/mnt/extra-addons/.gitignore"
if [ ! -e "$GITIGNORE_PATH" ]; then
  touch "$GITIGNORE_PATH"
fi

sed -i '$a\' "$GITIGNORE_PATH"

grep -qxF '/.venv/' "$GITIGNORE_PATH" || echo '/.venv/' >> "$GITIGNORE_PATH"
grep -qxF '/.vscode/' "$GITIGNORE_PATH" || echo '/.vscode/' >> "$GITIGNORE_PATH"
grep -qxF '/tsconfig.json' "$GITIGNORE_PATH" || echo '/tsconfig.json' >> "$GITIGNORE_PATH"

# Enable Odoo CLI auto-completion
# https://www.odoo.com/documentation/18.0/developer/reference/cli.html#help-version
echo "complete -W '` odoo --help | \
  sed -e 's/[^a-z_-]\(-\+[a-z0-9_-]\+\)/\\n\1\\n/' | \
  grep -- '^-' | sort | uniq | tr '\n' ' '`' odoo" >> ~/.bash_completion

# Enable bash completion in .bashrc
cat << 'EOF' >> ~/.bashrc
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi
EOF