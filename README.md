# Sendhub Coding Challenge - Message Routing Service

## Run unit and integration tests

To run unit and integrations tests, here you create a virtualenv first

```bash
virtualenv --no-site-packages .env
```

activate the environment

```bash
source .env/bin/activate
```

and install the project.

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

To test against an URL other than `127.0.0.1:5678`, you can expose the environment variable `TEST_URL`, like this.

```bash
TEST_URL=http://msg-router-prod.elasticbeanstalk.com/ TEST_ACCEPTANCE=1 py.test -s -vv tests/acceptance
```

If you prefer to run cURL commands manually, you can use `tests.acceptance.make_curl_cmds` script to generate some commands for you, here you type

```bash
python -m tests.acceptance.make_curl_cmds
```

Likewise, to change target URL, you can expose `TEST_URL` in environment.

## Test against the demo server

The demo server is running at `http://msg-router-prod.elasticbeanstalk.com/`, to test against it, you can run following cURL commands:

```
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "SendHub Rocks", "recipients": ["+15555555556", "+15555555555", "+15555555554", "+15555555553", "+15555555552", "+15555555551"]}' http://msg-router-prod.elasticbeanstalk.com/route-msg
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "Whatsup", "recipients": ["+15555555551", "+15555555552", "+15555555553", "+15555555554", "+15555555555", "+15555555556", "+15555555557", "+15555555558"]}' http://msg-router-prod.elasticbeanstalk.com/route-msg
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "YOLO!", "recipients": ["+15555555551", "+15555555552", "+15555555553", "+15555555554"]}' http://msg-router-prod.elasticbeanstalk.com/route-msg
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "YOLO!", "recipients": ["+15555555551", "+155555555", "abcd", "123456789", ""]}' http://msg-router-prod.elasticbeanstalk.com/route-msg
curl -X POST -v -H 'Content-Type: application/json' -d '{}' http://msg-router-prod.elasticbeanstalk.com/route-msg
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": ""}' http://msg-router-prod.elasticbeanstalk.com/route-msg
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "", "recipients": []}' http://msg-router-prod.elasticbeanstalk.com/route-msg
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "", "recipients": ["a", "a"]}' http://msg-router-prod.elasticbeanstalk.com/route-msg
curl -X POST -v -H 'Content-Type: application/json' -d '{"message": "", "recipients": ["a", "a", 123]}' http://msg-router-prod.elasticbeanstalk.com/route-msg
```

## Deployment

I use Docker + AWS Elastic Beanstalk for deployment, for more details, you can read my article - [Running Docker with AWS Elastic Beanstalk](http://victorlin.me/posts/2014/11/26/running-docker-with-aws-elastic-beanstalk).

You need to install Docker in your host first, then you need to run `eb init` to create an application and the environment. It's dead simple to deploy, modify `Dockerrun.aws.json` to the new version number, commit and tag current version number. And here you run

```
make && make push && eb deploy
```

`make` command builds the Docker image here, and `make push` push it to the Docker registry. Finally, `eb deploy` deploy current version defined in `Dockerrun.aws.json` to the environment associated with current branch.

## Algorithm

### Analysis

As the given problem is a [Change-making problem](http://en.wikipedia.org/wiki/Change-making_problem), in usual cases, we need to use Dynamic programming to solve the problem, however, given denominations is a special case, so we can solve it with greedy algorithm. The idea is simple, try to make change from the largest denomination as much as possible.

There are 4 denominations in this case, given value N to make change, so we will need to check at most 4 times for each denomination.

### Complexity

For the core cashier algorithm, since it's a constant number 4 we need to check, and the given value doesn't affect how many times we need to calculate, so the complexity

```
O(4) = O(1)
```

It's a constant time `O(1)` algorithm.

### Algorithm category

Greedy.

### Other throughput values

For this given case, any given value has no better solution than the biggest one we found, that's why we can use greedy. But for other cases, like 1, 3, 4. Given value 6, if we use greedy, 4 will be found first, the result will be 4, 1, 1. But for 3, 3 is actually a better solution. In this case, we need to use Dynamic Programming to solve the problem. 
