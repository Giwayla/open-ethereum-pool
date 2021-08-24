from local_config import *
import redis, datetime, requests, json, time
stream = 'gobin:eth:shares'
client = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

def get_minute_range(dt, mins=1):
    dt_start = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    dt_end = dt_start + datetime.timedelta(minutes=1)
    dt_start = dt_end - datetime.timedelta(minutes=mins)
    start = int(dt_start.timestamp() * 1000)
    end = int(dt_end.timestamp() * 1000 - 1)
    return [start, end]

def get_mins(dt):
    return dt.hour * 60 + dt.minute

now = datetime.datetime.now() - datetime.timedelta(minutes=1)
t2 = time.time() - 60

start, end = get_minute_range(now)
print('start:', start)
print('end:', end)
data = client.xrange(stream, start, end)
print(data)

stats = {}
for i in data:
    d = i[1]
    user = d['user']
    rig = d['rig']
    if not stats.get(user):
        stats[user] = {}
        stats[user]['total'] = 0
    stats[user][rig] = 0
#print(stats)

for i in data:
    d = i[1]
    user = d['user']
    rig = d['rig']
    diff = int(d['diff'])
    stats[user]['total'] = stats[user]['total'] + diff
    stats[user][rig] = stats[user][rig] + diff
#print(now)    
#print(stats)

stats2 = {}
print('%s:%s'%(now.hour, now.minute))
t = str(get_mins(now))
print(t)
for u, v in stats.items():
    for r, c in v.items():
        print('%s_%s: %s'%(u, r, c))
        key2 = '%s_%s'%(u, r) 
        stats2[key2] = c
print(stats2)
if stats2:
    data = {
        't': t,
        't2': t2,
        'stats': stats2
    }
    payload = {
        'token': TOKEN,
        'data': data
    }
    print()
    print('payload:', payload)
    resp = requests.post(STATS_URL, data={'data': json.dumps(payload)}, timeout=10)
    print(resp.status_code)
