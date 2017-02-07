# Saunatime
As our beloved student housing foundation didn't offer recurring sauna turns I decided to take matters into my own hands.

## Background
Sauna reservations are divided into time slots of one hour and treated as first come first served basis. Reservations can be made **exactly** two weeks into the future meaning on Monday at 8 PM a reservation for time slot 8-9PM two weeks ahead can be made. Needless to say, popular time slots will be taken fast and it all comes down to timing. Only if we could automate it...

Enter saunatime. Quick & dirty script for doing just that, sauna reservations when needed.
This script should be in under no circumstances referenced as an example that follows good coding practises, however, it does one thing and does it well, making sauna reservations. With proven track record of over one year of consecutive reservations made on prime time Friday (sorry neighbours).

## Disclaimer
This comes with absolutely no warranty or future support as I've moved to private housing. However, it served me well and I thought some fellow students might find it useful as well so decided to release it anyway.

## Preparations
You'll be needing following thigs:
 - Python 2.7
 - requests (```pip install requests```)
 - OmaPSOAS credentials (https://ssl.omapsoas.fi)
 - *cid* of the sauna (more on that below)
 - (Linux) machine (that's always on) where you can run this script

**What's cid and where do I get it?**
Easiest way to obtain the *cid* is opening booking calendar of your desired sauna, right clicking on any time slot item and then choosing *inspect* from the dropdown menu. We're interested in the href attribute of the anchor item which should be something along the lines: `/reservation/new/tabId/1/resId/304/year/2017/month/01/day/09/cid/6088/date/2017-01-12/mins/1020`.
The magic value we're after is the number combination following /cid/ which in this case is **6088**.

## Running
Running the script using
```python sauna.py -u myuser -p mypass -c 6088```
will try to reserve a time slot to sauna (with cid of 6088) in **two weeks time starting at the closest hour**.

E.g., running it at 20:08 tries to reserve a time slot **starting at 20:00** (and ending at 21:00) in **two weeks**. So closer you run the script to the full hour the better, in this this case 20:00:00 would be optimal.

**But that doesn't make any sense, I just want to define when I feel like going to sauna!?**
Most desired time slots (evenings, weekends) tend to get reserved pretty fast, meaning you have strike right after they come available. We're assuming that everything is booked for the next two weeks, but if not you can try to score those cancellations manually. So, essentially we are interested in and only in time slots two weeks ahead.

**Okay, but I don't want to run the script manually everytime I'm about to go to sauna so that I can secure the time slot in two weeks also**
Neither do I. Easiest way is to run this script in crontab on machine that's preferable on(line) all the time (put tose Uni computing servers in use).

For example, to reserve sauna on Fridays from 20 to 21 and output log to file:
```0 20 * * 5 python /home/<user>/saunatime/sauna.py >> /home/<user>/saunatime/sauna.log```

And that's about it, happy bathing!

## Licence
WTFPL, do as you please.
