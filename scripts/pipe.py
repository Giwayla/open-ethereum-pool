from redis import Redis
redis_client = Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

key_input = 'eth:shares2'
key_output = 'gobin:eth:shares'

while True:
    try:
        share = redis_client.brpop('eth:shares2')[1]
        print(share)
        ms, login, diff = share.split(':')
        user, rig = login.split('.')
        share2 = {'user': user, 'rig': rig, 'diff':diff}
        redis_client.xadd(key_output, share2, id=ms)
    except Exception as e:
        print('pipe error:', e)
