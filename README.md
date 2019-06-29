# Accept requests of new members (for a Facebook group)
*Automatically accept new requests of people willing to join your FB group.*


## Setup

Install python dependencies:

```
pip install -r requirements.txt
```

Install Chromedriver:

- https://sites.google.com/a/chromium.org/chromedriver/

## CLI

```
python auto-accept.py --fb_user <FB_EMAIL> --fb_pass <FB_PASS> --group_id <FB_GROUP_ID> --headless
```

If it does not work, set the chromedriver path with `--chromedriver <CHROME_DRIVER_PATH>`.

## What does the script do?

- Log in to Facebook.
- Fetch the list of the new member requests for the Facebook group.
- Accept all of them.
- Log out of Facebook.
