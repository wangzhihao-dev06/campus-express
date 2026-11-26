import datetime
import json
import os
from pathlib import Path
import subprocess
import tempfile

out = Path(os.environ["YOUTH_STATS_OUTPUT"])
sql = '''SELECT (SELECT COUNT(*) FROM `user`),
COUNT(DISTINCT parcel_id),
COUNT(DISTINCT CASE WHEN order_no LIKE 'DEMO%' THEN parcel_id END),
(SELECT COUNT(*) FROM rider), (SELECT COUNT(*) FROM station)
FROM pickup_order WHERE status IN (3,4)'''
result = subprocess.run([
    '/usr/bin/mysql', '--defaults-extra-file=' + os.environ['YOUTH_MYSQL_DEFAULTS'],
    '--protocol=SOCKET', '--batch', '--skip-column-names', '--connect-timeout=5',
    '--database=' + os.environ['YOUTH_STATS_DATABASE'], '--execute', sql
], check=True, capture_output=True, text=True, timeout=15)
keys = ('students', 'delivered', 'demo', 'riders', 'stations')
values = [int(x) for x in result.stdout.split()]
if len(values) != len(keys) or min(values) < 0 or values[2] > values[1]:
    raise ValueError('Invalid statistics result')
payload = dict(zip(keys, values))
payload['asOf'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
fd, path = tempfile.mkstemp(prefix='.stats-', dir=out.parent)
with os.fdopen(fd, 'w', encoding='utf-8') as stream:
    json.dump(payload, stream, separators=(',', ':'))
    stream.write('\n')
    stream.flush()
    os.fchmod(stream.fileno(), 0o644)
os.replace(path, out)
