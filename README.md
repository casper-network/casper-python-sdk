![PEP conform](https://github.com/MrKrautee/casper-python-sdk/actions/workflows/cl.yml/badge.svg)
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

### NodeClient
#### Queries
#### Deploys
#### Events
### Important modules
#### crypto
#### factory
#### serialisation 
#### types
#### utils

## Development
### Architecture

```
                     ______________ Your APP needs to call the NodeClient to
                     | Your App   | make API calls. In addition you may need
                     |____________| some tools which can be found in factory,
                            X       crypto and utils.
                            |
=========================== | ================================================
                            V 
_____________        _______________      ______________ More complex
|           |        |             |      |            | operations and
| Deploys   |<------X|  NodeClient |X---->|EventsClient| simplification of
|           |   ----X|             |      |            | composed API/Client
-------------   |    ---------------      -------------- calls.
      X         |
===== | ======= | ============================================================
      V         V                       
_______________________________________ Supposes all API calls and additional   
|                    |                | methods, composed of basic API calls.
|        Client      |  pycspr.types  | Converts API response into pycspr.types.
|(client.QueryClient)|                | Extracts result from API response.
--------------------------------------- Checking and converting input params. 
            X
=========== | ==================================================================
            V               
___________________________ "Low Level" communication, REST and RPC Api calls.
|                         | Does all REST and RPC calls. All endpoints defined
|      CasperApi          | here. No converting or manipulation of output or
|     (pycspr.api)        | input params at all. All in all its a simple        
--------------------------- interface to the REST/RPC API.                      
            X                 
=========== | ==================================================================
            V
  ___________________________          ___________________________
  |                         |          |                         | 
  |   NodeConnectionInfo    |X-------> |      requests,          | 
  |      (pycspr.api)       |          |    jsonrpcclient, ...   | 
  ---------------------------          ---------------------------
```

### Set up local test NCTL network

#### Installing Rust

Follow the Casper Documentation: [Getting
Started](https://docs.casperlabs.io/en/latest/dapp-dev-guide/setup-of-rust-contract-sdk.html)

#### Installing a local test NCTL network
See the Casper Documentation for installation:
[Local Network Testing](https://docs.casperlabs.io/en/latest/dapp-dev-guide/setup-nctl.html)

#### Running the local test network
```bash
$ nctl-assets-setup && nctl-start 
```

You can stop the server and delete created assets with `nctl-assets-teardown`.

### Installing the SDK for Development 

after cloning:
```bash
$ cd casper-python-sdk/
$ virtualenv .venv
$ source ./.venv/bin/activate
(.venv) $ pip install -r requirements-dev.txt
```
### Pre Commit/PullRequest Actions
Always asure that the tests are running and that you follow the PEP.

#### Testing 
##### Important Environment Variables
* NTCL *default* **not set** (ie: ~/casper-node/utils/nctl).
* PYCSPR_TEST_NODE_HOST" *default set to* "localhost")
* PYCSPR_TEST_NODE_PORT_REST *default set to* 14101)
* PYCSPR_TEST_NODE_PORT_RPC *default set to* 11101)
* PYCSPR_TEST_NODE_PORT_SSE *default set to* 18101)

##### Run Unit Tests
```bash
$ cd casper-python-sdk/
$ source .venv/bin/activate  # or pipenv shell
(.venv) $ export NCTL=/path/to/your/casper-node/utils/nctl
(.venv) $ pytest ./tests
````
TODO: Git pre-commit-hook needed.

#### Codestyle Guidelines
run flake8 (Style Guide Enforcement):
```bash
(.venv) $ cd casper-python-sdk/
(.venv) $ flake8 .
```
TODO: Git pre-commit-hook needed.

## Additional Resources
* Json RPC Schema in [resources/rpc_schema.json](resources/rpc_schema.json)
* Casper Documentation: [https://docs.casperlabs.io/](https://docs.casperlabs.io/)
* Python Enhancement Proposals(PEP): [https://www.python.org/dev/peps/](https://www.python.org/dev/peps/)
