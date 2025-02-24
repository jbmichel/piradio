# Physical web radio

## Installing as a daemon
```
sudo cp piradio/piradio.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart piradio.service
```

Check that it works
```systemctl | grep piradio```

See output
```journalctl -u piradio```

## Inspiration
- Adafruit rotary encoder: https://www.adafruit.com/product/5880
- Adafruit code: https://learn.adafruit.com/adafruit-i2c-qt-rotary-encoder/python-circuitpython
- Sparkfun switches: https://www.sparkfun.com/rotary-switch-10-position.html
- Core Electronics guide: https://core-electronics.com.au/guides/getting-started-with-rotary-encoders-examples-with-raspberry-pi-pico/#choosing

## Development notes
- This is how I installed CircuitPi: https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
- This is what ended up working: https://www.instructables.com/Keeping-It-Stoopid-Simple-Internet-Radio-KISSIR/
Could not get streaming mp3s to play from python directly; this instructs the OS to play it through mpg123.

## Future extensions
### Pico
- Interesting work: https://forums.raspberrypi.com/viewtopic.php?t=381266
- Pico: https://www.raspberrypi.com/products/raspberry-pi-pico/
### Audio cards, power bank...
Potential audio card: 
- https://www.slashgear.com/1403850/how-to-make-smart-speaker-with-raspberry-pi/
- https://www.pishop.us/product/iqaudio-dac-pro/?src=raspberrypi
