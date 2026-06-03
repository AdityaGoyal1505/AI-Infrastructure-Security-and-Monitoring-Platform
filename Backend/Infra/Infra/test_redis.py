import redis

r = redis.from_url("rediss://default:gQAAAAAAAU9-AAIgcDI2ODEzMzM1MDJhMGQ0M2YwYjNlZDkwNzgxYTE4M2U1OQ@humane-adder-85886.upstash.io:6379?ssl_cert_reqs=none")
print(r.ping())