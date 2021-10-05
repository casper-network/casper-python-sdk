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

How To: Query a node  ?
------------------------------------------------------
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

### Design

```
_____________  _______________
|           |  |             |
| Deploys   |  |             |
|           |  |             |
-------------  ---------------
      |
     call
      |
      V
_______________________________________
|                    |                |   Manipulating in and output. 
|        Client      |  pycspr.types  |   More complex but common tasks using the CasperApi calls.
|    (pycspr.client) |                |   Converts raw responses into pycspr.types.
---------------------------------------
            |
           call
            |
            V
___________________________
|                         |    
|      CasperApi          |   "Low Level" communication, REST and RPC Api calls. 
|     (pycspr.api)        |   No manipulation of in and output. All endpoints are 
---------------------------   defined here. They are returning the raw rpc/rest response.
            |
           call
            |
            V
___________________________
|                         |    
|      request,           |   
|    jsonrpcclient, ...   |   
---------------------------
```

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

See [here](how_tos/how_to_query_a_node.py).


How To: Transfer funds between 2 accounts  ?
------------------------------------------------------

See [here](how_tos/how_to_transfer.py).

How To: Delegate funds to a validator  ?
------------------------------------------------------

See [here](how_tos/how_to_delegate.py).

How To: Undelegate funds from a validator  ?
------------------------------------------------------

See [here](how_tos/how_to_undelegate.py).

How To: Stake funds as a validator  ?
------------------------------------------------------

See [here](how_tos/how_to_stake.py).

How To: Unstake funds as a validator ?
------------------------------------------------------

See [here](how_tos/how_to_unstake.py).

How To: Install a smart contract  ?
------------------------------------------------------

See [here](how_tos/how_to_install_a_contract.py).

How To: Invoke a smart contract  ?
------------------------------------------------------

See [here](how_tos/how_to_invoke_a_contract.py).

How To: Run unit tests against an NCTL network ?
------------------------------------------------------

```
cd YOUR_WORKING_DIRECTORY
pipenv shell
pytest ./tests
````
