# Casper Python SDK

Python library for interacting with a CSPR node.

##  Installation


pip3 install pycspr


##  Usage

### Cryptography

* [How To: Apply a checksum ?](how_tos/crypto/how_to_apply_a_checksum.py)

* [How To: Create Key Pairs ?](how_tos/crypto/how_to_create_key_pairs.py)

* [How To: Hash data ?](how_tos/crypto/how_to_hash_data.py)

* [How To: Sign data ?](how_tos/crypto/how_to_sign_data.py)

### Deploys

* [How To: Transfer funds between 2 accounts ?](how_tos/deploys/how_to_transfer.py)

* [How To: Delegate funds to a validator ?](how_tos/deploys/how_to_delegate.py)

* [How To: Undelegate funds from a validator ?](how_tos/deploys/how_to_undelegate.py)

* [How To: Stake funds as a validator ?](how_tos/deploys/how_to_stake.py)

* [How To: Unstake funds as a validator ?](how_tos/deploys/how_to_unstake.py)

### Smart Contracts

* [How To: Install a smart contract ?](how_tos/smart_contracts/how_to_install.py)

* [How To: Invoke a smart contract ?](how_tos/smart_contracts/how_to_invoke.py)

* [How To: Query a smart contract ?](how_tos/smart_contracts/how_to_query.py)

### Node APIs

* [How To: Use REST API ?](how_tos/node_apis/how_to_use_rest_client.py)

* [How To: Use RPC API ?](how_tos/node_apis/how_to_use_rpc_client.py)

* [How To: Use Speculative RPC API ?](how_tos/node_apis/how_to_use_speculative_rpc_client.py)

* [How To: Use SSE API ?](how_tos/node_apis/how_to_use_sse_client.py)

##  Development

### Pre-Requisites

[1. Setup Local CCTL Network](https://github.com/casper-network/cctl).

[2. Install poetry](https://python-poetry.org).

### Install SDK

```
cd YOUR_WORKING_DIRECTORY
git clone https://github.com/casper-network/casper-python-sdk.git
cd casper-python-sdk
poetry install
````

### Testing 

#### Important Environment Variables

* Mandatory

    * CCTL

        * path to local clone of CCTL repo

* Optional

    * PYCSPR_TEST_NODE_HOST

        * host of a test node
        * default =  localhost

    * PYCSPR_TEST_NODE_PORT_REST

        * port of rest server exposed by test node
        * default =  14101

    * PYCSPR_TEST_NODE_PORT_RPC

        * port of json-rpc server exposed by test node
        * default =  11101

    * PYCSPR_TEST_NODE_PORT_SSE

        * port of sse server exposed by test node
        * default =  18101

    * PYCSPR_TEST_NODE_PORT_RPC_SPECULATIVE

        * port of speculative execution server exposed by test node
        * default =  25101

#### Running Tests

```
cd YOUR_WORKING_DIRECTORY/casper-python-sdk
poetry shell
pytest ./tests [TEST-FILTER]
```
