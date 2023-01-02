#!/bin/sh -l

# install curl
apk add --no-cache curl

# install flyctl
curl -L https://fly.io/install.sh | sh

# set flyctl environmental variables
export FLYCTL_INSTALL="/root/.fly"

export PATH="$FLYCTL_INSTALL/bin:$PATH"

echo "Successfully Installed Flyctl"

# deploy app
sh -c "flyctl deploy"

# get app Information
sh -c "flyctl info"

exit 0