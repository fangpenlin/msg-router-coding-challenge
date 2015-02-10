# Sendhub Coding Challenge - Message Routing Service

## Run unit and integration tests

To run uni and integrations tests, here you create a virtualenv first

```bash
virtualenv --no-site-packages .env
```

then install the project.

```bash
pip install -e .[tests]
```

And here you go, run the tests.

```bash
py.test -sv
```

## Run acceptance tests

To run acceptance tests, you need to run the server first.

```bash
pserve development.ini
```

Then, run the acceptance tests

```bash
TEST_ACCEPTANCE=1 py.test -s -vv tests/acceptance
```

If you prefer to run cURL commands manually, you can use `tests.acceptance.make_curl_cmds` script to generate some commands for you, here you type

```bash
python -m tests.acceptance.make_curl_cmds
```
