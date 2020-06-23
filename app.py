import time
import math
import redis

from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/isPrime/<number>')
def is_prime(number):
    number = int(number)
    result = False
    if number > 1:
        for i in range(2, int(math.sqrt(number))):
                if (number % i) == 0:
                    return "%d is not a prime number" % number
        primes = [int(x) for x in cache.lrange('primes', 0, -1)]
        if not number in primes:
            cache.lpush('primes', number)
        return "%d is a prime number" % number
        
    return "%d is not a prime number" % number

@app.route('/primesStored')
def primes_stored():
    return str([int(x) for x in cache.lrange('primes', 0, -1)])

