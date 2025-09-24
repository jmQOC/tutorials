#!/bin/bash

################################################################################
# https://containers.dev/implementors/json_reference/
# initializeCommand
# onCreateCommand
# updateContentCommand
# >>> postCreateCommand
# postStartCommand
# postAttachCommand

# This command is the last of three that finalizes container setup when a dev 
# container is created. It happens after updateContentCommand and once the dev 
# container has been assigned to a user for the first time.

# Cloud services can use this command to take advantage of user specific secrets 
# and permissions.

# Note that the array syntax will execute the command without a shell. You can 
# learn more about formatting string vs array vs object properties.
################################################################################