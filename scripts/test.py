import redis

redis_host = 'redis'  # Use the service name as the hostname since both containers are in the same Docker network
redis_port = 6379  # Default Redis port

redis_client = redis.Redis(host=redis_host, port=redis_port)


def test_redis():
    # Set a key-value pair in Redis
    redis_client.set('test_key', 'test_value')

    # Get the value of the key from Redis
    value = redis_client.get('test_key')

    # Decode the value if it's in bytes
    if value is not None:
        value = value.decode()

    # Print the value
    print(f'The value of the key  is: {value}')


# Run the test
test_redis()
