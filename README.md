# Index Checker

[![Build Status](https://api.travis-ci.org/boranx/index-checker.svg?branch=master)](https://travis-ci.org/boranx/index-checker)
[![Coverage](https://codecov.io/gh/boranx/index-checker/branch/master/graph/badge.svg)](https://codecov.io/gh/boranx/index-checker)

Index Checker is an Elasticsearch index validator that validates the index within the given time range and document count.  
All you need is docker (or python 3.6).  
CI Compatible. If the tests fail, the exit code will be different than 0.  

<img src="img/index_checker.png?raw=true" width="720px">

### Usage

- Clone the repository

- Just modify and pass valid ```checker.yaml```.

### Run

```shell
make run
```

### Test

```shell
make test
```

### Docker

```shell
docker run -v /etc/localtime:/etc/localtime:ro -v $(pwd)/checker.yaml:/app/checker.yaml -i boranx/index-checker:latest python3.6 main.py
```

### Slack Notifier

- Pass your Slack Hook URI as flag like this :

```shell
cd index-checker && export PYTHONPATH=./ && python3.6 src/main.py -s https://hooks.slack.com/services/SLACKHOOKUID
```

- You can pass to docker with the same way.

- Slack channel will be notified when all tests are passed.
- Slack channel will be notified when some tests fail.