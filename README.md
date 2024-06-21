# rakwrap
A simple Python wrapper for [Rakuten Advertising](https://developers.rakutenadvertising.com/documentation/en-CA/affiliate_apis)'s APIs.
Work in progress, will become a pip package soon!

# Quickstart
```
from rakwrap.core import Rakwrap
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
ACCOUNT_ID = ACCOUNT_ID

rak = Rakwrap(CLIENT_ID, CLIENT_SECRET, ACCOUNT_ID)
rak.auth()

# Fetching all transaction events in the past 30 days
import datetime
process_date_end = datetime.datetime.now()
process_date_start = process_date_end - datetime.timedelta(days=29)
transaction_date_start = process_date_start
transaction_date_end = process_date_end

res = rak.get_events(process_date_start, process_date_end, transaction_date_start, transaction_date_end)
for event in res:
    print(event)
```

## Implemented endpoints
- `​/advertisersearch​/1.0`
- `​/events​/1.0​/transactions`
- `/productsearch/1.0`
- `​/v2​/advertisers`