import datetime
import pytz
import jdatetime

unaware = datetime.datetime(2011, 8, 15, 8, 15, 12, 0)
aware = datetime.datetime(2011, 8, 15, 8, 15, 12, 0, tzinfo=pytz.timezone('Asia/Tehran'))

now_aware = pytz.utc.localize(unaware)

print(unaware)
print(aware)
x = jdatetime.datetime.now(tz=pytz.timezone('Asia/Tehran'))
print(x.tzname())

