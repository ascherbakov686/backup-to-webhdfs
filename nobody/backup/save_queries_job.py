#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,urllib,subprocess,json
from datetime import datetime, timedelta

yesterday = datetime.today() - timedelta(1)
f = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 1)
to = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)
delta = timedelta(minutes=30)
f1=""
f2=""

with open('/data/queries/impala_queries_from_PROD_%s.json' % yesterday.strftime('%Y-%d-%B'), mode='aw') as ff:
 print>>ff,"["
 while f < to:
    f1=urllib.quote_plus(f.isoformat())
    f += delta
    f2=urllib.quote_plus(f.isoformat())
    json_data=subprocess.check_output("curl -k -u cron:******************** \"https://master3.domain.ru:7183/api/v7/clusters/cluster/services/impala/impalaQueries?from=%s&to=%s&limit=1000&filter=\"" % (f1,f2),shell=True)
    #print "curl -k -u cron:************************ \"http://master3.domain.ru:7180/api/v7/clusters/cluster/services/impala/impalaQueries?from=%s&to=%s&limit=1000&filter=\"" % (f1,f2)
    j = json.loads(str(json_data))
    for jj in j['queries']:
     print>>ff, json.dumps(jj)
     print>>ff, ","
 print>>ff, "{} ]"

# Cloudera Manager API:
# http://cloudera.github.io/cm_api/apidocs/v19/path__clusters_-clusterName-_services_-serviceName-_impalaQueries.html

