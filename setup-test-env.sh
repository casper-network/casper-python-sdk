#!/bin/bash
LOGPROMPT=">>> "
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ROOT_DIR=$SCRIPTPATH/tn
CASPER_NODE=$ROOT_DIR/casper-node
CASPER_NODE_LAUNCHER=$ROOT_DIR/casper-node-launcher
CASPER_COMPILE=true

if [ ! -d "$ROOT_DIR" ]; then
	mkdir $ROOT_DIR
fi
if [ ! -d "$CASPER_NODE" ] && [ ! -L "$CASPER_NODE" ]; then
	echo $LOGPROMPT"clone casper-node..."
	git clone https://github.com/casper-network/casper-node $CASPER_NODE
else
	CASPER_COMPILE=false
	echo $LOGPROMPT"casper-node found!"
fi
if [ ! -d "$CASPER_NODE_LAUNCHER" ] && [ ! -L "$CASPER_NODE" ]; then
	echo $LOGPROMPT"clone casper-node-launcher..."
	git clone https://github.com/casper-network/casper-node-launcher $CASPER_NODE_LAUNCHER
else
	echo $LOGPROMPT"casper-node-launcher found!"
fi
if [ ! -d "$SCRIPTPATH/.venv" ]; then 
	echo $LOGPROMPT"create virual environment (.venv)..."
	virtualenv $SCRIPTPATH/.venv
	source $SCRIPTPATH/.venv/bin/activate
	pip install -r requirements-test-node.txt
else
	echo $LOGPROMPT"virtual environment (.venv) found!"
	echo $LOGPROMPT"set up virtual environment (.venv)..."
	source $SCRIPTPATH/.venv/bin/activate
fi

echo $LOGPROMPT"set up casper-node environment..."
source $ROOT_DIR/casper-node/utils/nctl/activate
export NCTL=$ROOT_DIR/casper-node/utils/nctl
# compile if freshly cloned
if [ "$CASPER_COMPILE" = true ]; then
	echo $LOGPROMPT"start compiling casper-node..."
	nctl-compile
fi
