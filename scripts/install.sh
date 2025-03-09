#!/bin/bash
set -e

if [ -z "$VER" ]; then
  echo "Error: Specify the version to install."
  exit 1
fi

INSTALL_DIR=${INSTALL_DIR:-"/usr/local/bin"}
URL="https://github.com/LunaticFringers/shepherd/releases/download/v$VER/shpdctl-$VER.tar.gz"
TEMP_DIR=$(mktemp -d)

if [ "$(id -u)" -ne 0 ]; then
  echo "This script requires sudo privileges to install."
  exit 1
fi

echo "Installing shpdctl version $VER..."
echo "Downloading from URL $URL"
curl -fsSL "$URL" -o "$TEMP_DIR/shpdctl.tar.gz"

echo "Extracting the package..."
tar -xzvf "$TEMP_DIR/shpdctl.tar.gz" -C "$TEMP_DIR"

echo "Installing shpdctl binary to $INSTALL_DIR..."
mv "$TEMP_DIR/shpdctl" "$INSTALL_DIR/shpdctl"

chmod +x "$INSTALL_DIR/shpdctl"
rm -rf "$TEMP_DIR"

if command -v shpdctl > /dev/null; then
  echo "shpdctl installed successfully! You can run it using the 'shpdctl' command."
else
  echo "Installation failed."
  exit 1
fi
