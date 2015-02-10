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

To change target URL, you can expose `TEST_URL` in environment.

## Test against the demo server

The demo server is running at `http://msg-router-prod.elasticbeanstalk.com/`, to test against it, you can run following cURL commands:

```
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "SendHub Rocks", "recipients": ["+15555555556", "+15555555555", "+15555555554", "+15555555553", "+15555555552", "+15555555551"]}' http://127.0.0.1:5678/route-msg
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "Whatsup", "recipients": ["+15555555551", "+15555555552", "+15555555553", "+15555555554", "+15555555555", "+15555555556", "+15555555557", "+15555555558"]}' http://127.0.0.1:5678/route-msg
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "YOLO!", "recipients": ["+15555555551", "+15555555552", "+15555555553", "+15555555554"]}' http://127.0.0.1:5678/route-msg
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "YOLO!", "recipients": ["+15555555551", "+155555555", "abcd", "123456789", ""]}' http://127.0.0.1:5678/route-msg
(.env)[VictorLin@MacBook-Air sendhub-coding-challenge] (master)$ TEST_URL=http://msg-router-prod.elasticbeanstalk.com/ python -m tests.acceptance.make_curl_cmds
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "SendHub Rocks", "recipients": ["+15555555556", "+15555555555", "+15555555554", "+15555555553", "+15555555552", "+15555555551"]}' http://msg-router-prod.elasticbeanstalk.com/route-msg
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "Whatsup", "recipients": ["+15555555551", "+15555555552", "+15555555553", "+15555555554", "+15555555555", "+15555555556", "+15555555557", "+15555555558"]}' http://msg-router-prod.elasticbeanstalk.com/route-msg
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "YOLO!", "recipients": ["+15555555551", "+15555555552", "+15555555553", "+15555555554"]}' http://msg-router-prod.elasticbeanstalk.com/route-msg
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "YOLO!", "recipients": ["+15555555551", "+155555555", "abcd", "123456789", ""]}' http://msg-router-prod.elasticbeanstalk.com/route-msg
```
