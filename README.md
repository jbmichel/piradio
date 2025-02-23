# Physical web radio

## Installing as a daemon
sudo cp piradio/piradio.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart piradio.service

Check that it works
systemctl | grep piradio

See output
journalctl -u piradio
