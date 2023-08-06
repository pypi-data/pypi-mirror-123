
# Getting Started with CoinGecko API V3

## Install the Package

The package is compatible with Python versions `2 >=2.7.9` and `3 >=3.4`.
Install the package from PyPi using the following pip command:

```python
pip install automation-test==1.16
```

You can also view the package at:
https://pypi.python.org/pypi/automation-test

## Test the SDK

You can test the generated SDK and the server with test cases. `unittest` is used as the testing framework and `nose` is used as the test runner. You can run the tests as follows:

Navigate to the root directory of the SDK and run the following commands

```
pip install -r test-requirements.txt
nosetests
```

## Initialize the API Client

**_Note:_** Documentation for the client can be found [here.](/doc/client.md)

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| `timeout` | `float` | The value to use for connection timeout. <br> **Default: 60** |
| `max_retries` | `int` | The number of times to retry an endpoint call if it fails. <br> **Default: 0** |
| `backoff_factor` | `float` | A backoff factor to apply between attempts after the second try. <br> **Default: 2** |
| `retry_statuses` | `Array of int` | The http statuses on which retry is to be done. <br> **Default: [408, 413, 429, 500, 502, 503, 504, 521, 522, 524]** |
| `retry_methods` | `Array of string` | The http methods on which retry is to be done. <br> **Default: ['GET', 'PUT']** |

The API client can be initialized as follows:

```python
from coingeckoapiv3.coingeckoapiv_3_client import Coingeckoapiv3Client
from coingeckoapiv3.configuration import Environment

client = Coingeckoapiv3Client(
    environment=Environment.PRODUCTION,)
```

## List of APIs

* [Ping](/doc/controllers/ping.md)
* [Simple](/doc/controllers/simple.md)
* [Coins](/doc/controllers/coins.md)
* [Contract](/doc/controllers/contract.md)
* [Asset Platforms](/doc/controllers/asset-platforms.md)
* [Categories](/doc/controllers/categories.md)
* [Exchanges](/doc/controllers/exchanges.md)
* [Finance](/doc/controllers/finance.md)
* [Indexes](/doc/controllers/indexes.md)
* [Derivatives](/doc/controllers/derivatives.md)
* [Status Updates](/doc/controllers/status-updates.md)
* [Events](/doc/controllers/events.md)
* [Exchange Rates](/doc/controllers/exchange-rates.md)
* [Trending](/doc/controllers/trending.md)
* [Global](/doc/controllers/global.md)
* [Companies Beta](/doc/controllers/companies-beta.md)

## Classes Documentation

* [Utility Classes](/doc/utility-classes.md)
* [HttpResponse](/doc/http-response.md)
* [HttpRequest](/doc/http-request.md)

