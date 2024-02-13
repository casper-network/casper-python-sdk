# Casper Python SDK

Python library for interacting with a CSPR node.

##  Installation

```
pip3 install pycspr
```

##  Usage

* [How To: Query a node ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_query_nodes.py)

* [How To: Transfer funds between 2 accounts ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_transfer.py)

* [How To: Delegate funds to a validator ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_delegate.py)

* [How To: Undelegate funds from a validator ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_undelegate.py)

* [How To: Stake funds as a validator ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_stake.py)

* [How To: Unstake funds as a validator ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_unstake.py)

* [How To: Install a smart contract ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_install_a_contract.py)

* [How To: Invoke a smart contract ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_invoke_a_contract.py)

* [How To: Query a smart contract ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_query_contracts.py)

* [How To: Speculatively execute a deploy ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_speculatively_execute_a_deploy.py)

* [How To: Hash data ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_hash_data.py)

* [How To: Create Key Pairs ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_create_key_pairs.py)

* [How To: Apply a checksum ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_apply_a_checksum.py)

* [How To: Await Events  ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_await_events.py)

* [How To: Consume Events  ?](https://github.com/casper-network/casper-python-sdk/blob/main/how_tos/how_to_consume_events.py)

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

    * PYCSPR_TEST_NODE_PORT_SPEC_EXEC

        * port of speculative execution server exposed by test node
        * default =  25101

#### Running Tests

```
cd YOUR_WORKING_DIRECTORY/casper-python-sdk
poetry shell
pytest ./tests [TEST-FILTER]
```
