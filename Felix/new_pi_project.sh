#!/bin/bash -e

# Set target for raspberry pi architecture
TARGET=aarch64-unknown-linux-gnu

# Make sure rust is installed locally
if ! type "cargo" > /dev/null; then
  echo "Like you don't have rust installed"
  echo "Please follow instructions at https://www.rust-lang.org/tools/install"
  exit 1
else
  echo "Found cargo, proceeding with creation of project"
fi

# Check if cross is installed
if ! type "cross" > /dev/null; then
  echo "Could not find rust cross compilation tool 'cross'"
  read -p "Install cross? (Y/n)" CROSS
  case $CROSS in
    "Y")
      cargo install cross;;
    "y")
      cargo install cross;;
    "yes")
      cargo install cross;;
    *)
      exit 1;;
    esac
else
  echo "Found cross to be installed"
fi

# Get the necessary details for the creation of a new project
read -p "Enter name of the new project: " NAME
read -p "Enter ip for raspberry pi device: " PI_IP
read -p "Enter username for raspberry pi: " USER

# Create new rust project
cargo new $NAME

cd $NAME || exit 1;
# Create execution file
touch deploy.sh
chmod +x deploy.sh

# prep execution file
echo "#!/bin/bash -e
cross build --release --target $TARGET

scp -r ./target/$TARGET/release/$NAME $USER@$PI_IP:/tmp/

ssh $USER@$PI_IP /tmp/$NAME" >> deploy.sh


