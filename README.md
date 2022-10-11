# vanderbilt-entro-client

Library for managing bookings in Vanderbilt Entro Reservation system (earlier called Bewator Entro).

## Features

* Login with username and password
* Get current active booking
* Make a new booking

## Not (yet?) implemented

* Delete a booking
* List all bookings in system
* Switching language

## Example usage

```
from entro.client import EntroClient

# Login
client = EntroClient("[URL]")
client.login("[USERNAME]", "[PASSWORD]")

# Get active booking
booking = client.get_active_booking()
print(booking)

# Make new booking next week
client.make_booking(start, stop) # Pass datetimes for start and stop
```

## Notes
I only have user level access to one (live) instance of this system, so there is probably quite a few configurations this library doesn't support.
