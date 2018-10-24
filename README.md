# Index Checker

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
docker run -v $(pwd)/checker.yaml:/app/checker.yaml -i boranx/index-checker:latest python3.6 main.py -< checker.yaml
```

### Slack Notifier

- Pass your Slack Hook URI to ```src/checker.py```

- Uncomment the ```slack.notify``` line