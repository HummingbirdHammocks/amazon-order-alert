# Amazon Order Alert
Add a task to Todoist if an Amazon order shipment in Shipstation will soon be late.

## How To Use

1. Ensure you have python3 installed and working correctly

2. Install requirements using the following command:

`pip3 install -r requirements.txt`

3. Copy config-sample.py to a new file called config.py. Populate with your Todoist API token and which projects you want to associate with each button action.

4. Test by running the following from the project directory.

`python3 main.py`

5. Add as a service so the script will run on startup

```
cd /lib/systemd/system/
sudo nano listprinter.service
```

_Copy in from example file_

```
sudo chmod 644 /lib/systemd/system/listprinter.service
chmod +x /home/pi/list-printer-pi/main.py
sudo systemctl daemon-reload
sudo systemctl enable listprinter.service
sudo systemctl start listprinter.service
```

6. Reboot and test
