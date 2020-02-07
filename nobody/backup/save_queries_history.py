#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,urllib,subprocess,json
from datetime import datetime, timedelta

f = datetime(2018, 6, 19, 0, 0, 0)
to = datetime(2018, 7, 15, 0, 0, 0)
delta = timedelta(minutes=30)
f1=""
f2=""

with open('/data/queries/impala_queries_from_PROD_%s-%s.json' % (f,to), mode='aw') as ff:
 print>>ff,"["
 while f < to:
    f1=urllib.quote_plus(f.isoformat())
    f += delta
    f2=urllib.quote_plus(f.isoformat())
    json_data=subprocess.check_output("curl -u cron:****************** \"http://master3.domain.ru:7180/api/v7/clusters/cluster/services/impala/impalaQueries?from=%s&to=%s&limit=1000&filter=\"" % (f1,f2),shell=True)
    j = json.loads(str(json_data))
    for jj in j['queries']:
     print>>ff, json.dumps(jj)
     print>>ff, ","
 print>>ff, "{} ]"

# Cloudera Manager API:
# http://cloudera.github.io/cm_api/apidocs/v19/path__clusters_-clusterName-_services_-serviceName-_impalaQueries.html

