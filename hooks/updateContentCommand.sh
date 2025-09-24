#!/bin/bash

################################################################################
# https://containers.dev/implementors/json_reference/
# initializeCommand
# onCreateCommand
# >>> updateContentCommand
# postCreateCommand
# postStartCommand
# postAttachCommand

# This command is the second of three that finalizes container setup when a dev 
# container is created. It executes inside the container after onCreateCommand 
# whenever new content is available in the source tree during the creation process.

# It will execute at least once, but cloud services will also periodically execute
# the command to refresh cached or prebuilt containers. Like cloud services using 
# onCreateCommand, it can only take advantage of repository and org scoped secrets
# or permissions.

# Note that the array syntax will execute the command without a shell. You can 
# learn more about formatting string vs array vs object properties.
################################################################################