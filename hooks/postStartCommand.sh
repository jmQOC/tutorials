#!/bin/bash

################################################################################
# https://containers.dev/implementors/json_reference/
# initializeCommand
# onCreateCommand
# updateContentCommand
# postCreateCommand
# >>> postStartCommand
# postAttachCommand

# A command to run each time the container is successfully started.

# Note that the array syntax will execute the command without a shell. 
# You can learn more about formatting string vs array vs object properties.
################################################################################_

# Set Enterprise Addons Directory variable
ENTERPRISE_ADDONS_DIR="/var/lib/odoo/addons/${ODOO_VERSION}"

# Check if the Enterprise addons directory is empty
if [ ! -d "$ENTERPRISE_ADDONS_DIR" ] || [ -z "$(ls -A $ENTERPRISE_ADDONS_DIR)" ]; then
    # Clone Enterprise to the appropriate folder
    git clone --single-branch --branch ${ODOO_VERSION} \
        https://github.com/odoo/enterprise.git "$ENTERPRISE_ADDONS_DIR"
else
    # Enterprise already exists, pull the most recent updates
    git -C "$ENTERPRISE_ADDONS_DIR" pull --ff-only
fi

odoo --stop-after-init -i website_enterprise

# Initialize Odoo for development
ODOO_MAJOR_VERSION=${ODOO_VERSION%%.*} # Bash can't do floating point math
if [ "$ODOO_MAJOR_VERSION" -ge 15 ]; then
    # CLI Features Added in Odoo 15
    # Generate tsconfig for better JS editing (native VSCode tooling)
    odoo tsconfig \
    --addons-path /mnt/extra-addons,$ENTERPRISE_ADDONS_DIR,/usr/lib/python3/dist-packages/odoo/addons \
    > /mnt/extra-addons/tsconfig.json
fi

if [ "$ODOO_MAJOR_VERSION" -ge 16 ]; then
    # CLI Features Added in Odoo 16
    odoo neutralize
fi


