casper-client-py
======================================================

Python 3.9+ library for interacting with a CSPR node.


What is casper-client-py ?
------------------------------------------------------

The python client is published as pycspr: **PY**thon **C**a**SP**e**R**.  It's goal is to streamline client side experience of interacting with a casper node.


How To: Install ?
------------------------------------------------------

```
pip install pycspr
```

## Usage

* **Query a node** See [here](how_tos/how_to_query_a_node.py).
* **Transfer funds between 2 accounts** See [here](how_tos/how_to_transfer.py).
* **Delegate funds to a validator** See [here](how_tos/how_to_delegate.py).
* **Undelegate funds from a validator**  See [here](how_tos/how_to_undelegate.py).
* **Stake funds as a validator** See [here](how_tos/how_to_stake.py).
* **Unstake funds as a validator** See [here](how_tos/how_to_unstake.py).
* **Install a smart contract** See [here](how_tos/how_to_install_a_contract.py).
* **Invoke a smart contract** See [here](how_tos/how_to_invoke_a_contract.py).

## Development

### Set up local test NCTL network

#### Installing Rust

Follow the Casper Documentation: [Getting
Started](https://docs.casperlabs.io/en/latest/dapp-dev-guide/setup-of-rust-contract-sdk.html)

#### Installing a local test NCTL network
Use `setup-test-env.sh` to setup a local test environment. 
It will:
* clone and compile `casper-node` and `casper-launcher` to
  `YOUR_WORKING_DIRECTORY/tn`
* create an virtuale python environment(`YOUR_WORKING_DIRECTORY/.venv`)
* install all requirements
* set all necessary environment variables 
* launch `.venv`

```bash
> cd YOUR_WORKING_DIRECTORY
> bash #change to bash !!! important
$ source setup-test-env.sh  
```

If you already have a installation of `casper-node` and `casper-node-launcher`
create a link bevor running `setup-test-env.sh`:

```bash
> cd YOUR_WORKING_DIRECTORY
> mkdir tn && cd tn
> ln -s /path/to/your/casper-node casper-node
> ln -s /path/to/your/casper-node-launcher casper-node-launcher
> cd .. # back to YOUR_WORKING_DIRECTORY
> bash # change to bash !!! important
$ source setup-test-env.sh  
```

See also the Casper Documentation for manual installation:
[Local Network Testing](https://docs.casperlabs.io/en/latest/dapp-dev-guide/setup-nctl.html)

#### Running the local test network
```bash
$ nctl-assets-setup && nctl-start 
```

You can stop the server and delete created assets with `nctl-assets-teardown`.

### Testing (against an NCTL network)
Now we have a running local NCTL network. Let's run the unit tests. I use a
freshly opend terminal. Since  `casper-node` and `casper-node-launcher` are already
installed, `setup-test-env.sh` will only launch the virtual environment and set the environment variables: 

```bash
> cd YOUR_WORKING_DIRECTORY
> source setup-test-env.sh
(.venv) > pytest ./tests
```
or

```bash
> cd YOUR_WORKING_DIRECTORY
> pipenv shell # or source .venv/bin/activate
> export NCTL=/path/to/your/casper-node/utils/nctl
> pytest ./tests
````

#### Important Environment Variables
* NTCL *default* **not set** (ie: ~/casper-node/utils/nctl). It will be set automatically if you use `setup-test-env.sh`
* PYCSPR_TEST_NODE_HOST" *default set to* "localhost")
* PYCSPR_TEST_NODE_PORT_REST *default set to* 14101)
* PYCSPR_TEST_NODE_PORT_RPC *default set to* 11101)
* PYCSPR_TEST_NODE_PORT_SSE *default set to* 18101)

