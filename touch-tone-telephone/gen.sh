#!/bin/sh

# Generate the touch-tone telephone program

read -p "Do you want to enter a custom flag? " yn
case $yn in
    [Yy]* ) read -p "Enter the flag: " flag;;
    [Nn]* ) flag="";;
    * ) echo "Please answer yes or no.";;
esac

read -p "Do you want to enter a custom seed? " yn
case $yn in
    [Yy]* ) read -p "Enter the seed (integer): " seed;;
    [Nn]* ) seed="";;
    * ) echo "Please answer yes or no.";;
esac

if [ -z "$flag" ]; then
    sleep 0
else
    export TEAM_FLAG="$flag"
fi

if [ -z "$seed" ]; then
    sleep 0
else
    export TEAM_SEED="$seed"
fi

cargo run --release --bin gen
