#!/bin/sh
set -e

(cat <<EOF
  {
    "ip": "127.0.0.1",
    "requestpath": "/api/v1.0/elog",
    "httpmethod": "POST",
    "useragent": "Mozilla/5.0 (Windows NT 5.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0 `date +%s`",
    "userplatform": "Linux",
    "userbrowser": "Mozilla Firefox",
    "userbrowserversion": "`date +%s`",
    "referrer": "referrer-`date +%s`",
    "requestargs": "requestargs-`date +%s`",
    "postvalues": "postvalues-`date +%s`",
    "errortype": "errortype-`date +%s`",
    "errormsg": "errormsg-`date +%s`",
    "when": "`date -u +"%Y-%m-%dT%H:%M:%S"`",
    "errortraceback": "errortraceback-`date +%s`",
    "code": 400,
    "date": "`date -u +"%Y-%m-%dT%H:%M:%S"`"
}
EOF
) | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin)))"


#curl -X POST -H 'Content-Type: application/json' -H 'EXTERNAL-APP-ID: 3501569308' http://127.0.0.1:9040/api/v1.0/elog --data '{"ip": "127.0.0.1", "requestpath": "/api/v1.0/elog", "httpmethod": "POST", "useragent": "Mozilla/5.0 (Windows NT 5.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0 1625051082", "userplatform": "Linux", "userbrowser": "Mozilla Firefox", "userbrowserversion": "1625051082", "referrer": "referrer-1625051082", "requestargs": "requestargs-1625051082", "postvalues": "postvalues-1625051082", "errortype": "errortype-1625051082", "errormsg": "errormsg-1625051082", "when": "2021-06-30T11:04:42.00000", "errortraceback": "errortraceback-1625051082", "code": 400, "date": "2021-06-30T11:04:42"}'