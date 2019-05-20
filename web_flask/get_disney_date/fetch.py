import logging,time
#import get_disney_date
import config,api

#log_format = "%(asctime)s %(levelname)s [%(name)s] - %(message)s"
#logging.basicConfig(format=log_format,filename='disney.log',level=logging.DEBUG)
#logging.info('So should this')

# 

view_waitTime = {}

def make_datas(return_now = False):
    datapoints = []
    global view_waitTime
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

            view_waitTime[a.name] = float(a.wait_minutes)
            #logging.info("%s wait: %sm;" % (a.zhName, a.wait_minutes)\
            #    +" singleRider: {}; FP: {};".format(a.single_rider,a.fastPass))
    
    if return_now:
        return view_waitTime

    return datapoints


def get_influxdb():
    db = influxdb.InfluxDBClient(config.INFLUXDB_HOST, config.INFLUXDB_PORT,
                                 config.INFLUXDB_USER, config.INFLUXDB_PASS,
                                 config.INFLUXDB_DB)
    db.create_database(config.INFLUXDB_DB)
    return db


def main(lock):
    import influxdb
    db = get_influxdb()
    while True:
        lock.acquire()
        datapoints = make_datas()
        assert db.write_points(datapoints, database='disney', batch_size=50)
        lock.release()
        print('Getting wait time of views.')

        time.sleep(180)

def get_now_data():
    view_waitTime = make_datas(return_now=True)

    return view_waitTime

if __name__ == "__main__":
    api.save_to_json()