import redis

class RedisConnection(object):

    def __init__(self, **kwargs) -> None:
        redis_conn = kwargs.get("redis")

    def redis_connection(self, host=None):
        return redis.Redis(
            host="localhost",
            port=6379,
            password="TeQLev6H0g1D",
            decode_responses=True,
            db=0,
            socket_connect_timeout=60,
            socket_timeout=60,
            retry_on_timeout=True,
        )

    def redis_connection_pipeline(self):
        return self.redis_connection().pipeline()
    



# "leaky_bucket:3.5-turbo" + str(i) + ":requests"
# if not request_bucket:
#                 request_bucket = {
#                     "request":              1,
#                     "last_refresh":         time.time(),
#                     "request_day":          1,
#                     "last_refresh_day":     time.time(),
#                     "request_second":       1,
#                     "last_refresh_second":  time.time()
#                 }
#             else:
#                 try:
#                     request_bucket = {k: float(v) for k, v in request_bucket.items()}
#                     request_bucket["request"] += 1
#                     request_bucket["request_day"] = 1 if request_bucket.get("request_day") is None else (request_bucket['request_day'] + 1)
#                     request_bucket["last_refresh_day"] = time.time() if request_bucket.get("last_refresh_day") is None else (time.time() - request_bucket['last_refresh_day'])
#                     request_bucket["request_second"] = 1 if request_bucket.get("request_second") is None else (request_bucket['request_second'] + 1)
#                     request_bucket["last_refresh_second"] = time.time() if request_bucket.get("last_refresh_second") is None else (time.time() - request_bucket['last_refresh_second'])
                    