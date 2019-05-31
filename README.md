gsltctrl is a small script to generate GSLT Tokens for game servers.
https://steamcommunity.com/dev/managegameservers

# How to use it

Place your API key in a file called `APIKEY` next to the gsltctrl.py script.

Then run `python3 gsltctrl.py <appid> <memo>`.
The script will print a valid token to stdout.

If no token with the memo `<memo>` exists it will be created.
If it has expired it will be regenerated and the new token will be printed.
If it exists and is not expired it will be printed.

If you want to have spaces in `<memo>` use
`python3 gsltctrl.py <appid> '<memo>'` instead.

e.g. `python3 gsltctrl.py 730 'cool csgo server'`

