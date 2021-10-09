# Casper Python SDK

Python 3.9+ library for interacting with a CSPR node.


## What is Casper Python SDK `pycspr`

The python client is published as `pycspr`: **PY**thon **C**a**SP**e**R**.  It's goal is to streamline client side experience of interacting with a casper node.


## How To: Install ?

It's recommend to create a virtual environment for your application:
```bash
$ cd path/to/your/project
$ virtualenv .venv  # if you just starting and need a venv anyway
$ source ./.venv/bin/activate  # launch your environment
$ pip install pycspr
```
If you want to take part in develeopment, follow the [intallation instructions
for development](#installing-the-sdk-for-development).

## Usage

* **Query a node** See [here](how_tos/how_to_query_a_node.py).
* **Transfer funds between 2 accounts** See [here](how_tos/how_to_transfer.py).
* **Delegate funds to a validator** See [here](how_tos/how_to_delegate.py).
* **Undelegate funds from a validator**  See [here](how_tos/how_to_undelegate.py).
* **Stake funds as a validator** See [here](how_tos/how_to_stake.py).
* **Unstake funds as a validator** See [here](how_tos/how_to_unstake.py).
* **Install a smart contract** See [here](how_tos/how_to_install_a_contract.py).
* **Invoke a smart contract** See [here](how_tos/how_to_invoke_a_contract.py).

### Set up local test NCTL network
#### Installing Rust

Follow the Casper Documentation: [Getting
Started](https://docs.casperlabs.io/en/latest/dapp-dev-guide/setup-of-rust-contract-sdk.html)

#### Installing a local test NCTL network
See the Casper Documentation for installation:
[Local Network Testing](https://docs.casperlabs.io/en/latest/dapp-dev-guide/setup-nctl.html)

### Installing the SDK for Development 

after cloning:
```bash
$ cd casper-python-sdk/
$ virtualenv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt
```

### Testing 
#### Important Environment Variables
* NTCL *default* **not set** (ie: ~/casper-node/utils/nctl).
* PYCSPR_TEST_NODE_HOST" *default set to* "localhost")
* PYCSPR_TEST_NODE_PORT_REST *default set to* 14101)
* PYCSPR_TEST_NODE_PORT_RPC *default set to* 11101)
* PYCSPR_TEST_NODE_PORT_SSE *default set to* 18101)

#### Run Unit Tests
```bash
$ cd casper-python-sdk/
$ source .venv/bin/activate  # or pipenv shell
(.venv) $ export NCTL=/path/to/your/casper-node/utils/nctl
(.venv) $ pytest ./tests
````

## Additional Resources
* Json RPC Schema in [resources/rpc_schema.json](resources/rpc_schema.json)
* Casper Specifcation:
  [https://caspernetwork.readthedocs.io/en/latest/implementation/](https://caspernetwork.readthedocs.io/en/latest/implementation/)
* Casper Documentation: [https://docs.casperlabs.io/](https://docs.casperlabs.io/)
* How to stake your CSPR:
  [https://casper.network/network/blog/how-to-stake-your-cspr](https://casper.network/network/blog/how-to-stake-your-cspr)
* Python Enhancement Proposals(PEP): [https://www.python.org/dev/peps/](https://www.python.org/dev/peps/)
