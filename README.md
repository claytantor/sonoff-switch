# sonoff-switch
provides a scheduler for muiple sonoff switches

## installing stuff
```
python3 -m venv ./venv
source venv/bin/activate
$(pwd)/venv/bin/python3 -m pip install --upgrade pip
$(pwd)/venv/bin/python3 -m pip install -r requirements.txt
```

# creating the systemd service
```
$(pwd)/venv/bin/python3 makeservice.py -d $(pwd) -t sonoff.service.mustache > sonoff.service
```

Instructions for setting up your service can be found at https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/

```
sudo cp sonoff.service /lib/systemd/system/sonoff.service
sudo chmod 644 /lib/systemd/system/sonoff.service
sudo systemctl daemon-reload
sudo systemctl enable sonoff.service
```
