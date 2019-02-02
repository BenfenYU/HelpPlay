import logging,time

from client import api
from client import names
import config

import influxdb

log = logging.getLogger(__name__)

# 
def make_datas():
    datapoints = []
    for a in api.attractions():
        
        if a.zhName and a.wait_minutes:
            datapoint = {
                "measurement": "wait_minutes",
                "tags": {
                    "name": a.name,
                },
                "fields": {
                    "value": a.wait_minutes,
                },
            }
            datapoints.append(datapoint)
            log.info("%s wait: %sm;" % (a.zhName, a.wait_minutes)+" singleRider: {}; FP: {};".format(a.single_rider,a.fastPass))

    return datapoints


def get_influxdb():
    db = influxdb.InfluxDBClient(config.INFLUXDB_HOST, config.INFLUXDB_PORT,
                                 config.INFLUXDB_USER, config.INFLUXDB_PASS,
                                 config.INFLUXDB_DB)
    db.create_database(config.INFLUXDB_DB)
    return db


def main():
    db = get_influxdb()
    while True:
        datapoints = make_datas()
        #print(datapoints)
        assert db.write_points(datapoints, database='disney', batch_size=50)
        time.sleep(300)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        log.exception("exception")
