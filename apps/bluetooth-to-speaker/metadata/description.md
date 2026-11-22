# Bluetooth to Speaker

Phones play to your server like to any Bluetooth speaker.

- **Bluetooth speaker:** phones stream over Bluetooth (A2DP). The phone's volume buttons
  and the speaker volume stay in sync.
- **Safe pairing:** the speaker stays hidden until you press **Pair new phone** in the web UI.
- **Several outputs:** 3.5 mm jack, HDMI and USB sound cards, alone or several at once.
- **Home Assistant and Music Assistant** play to it over DLNA; MQTT adds controls for
  pairing, outputs and volumes.

## Before you install

- BlueZ (`bluetoothd`) must run on the host.
- No other Bluetooth audio receiver on the host (PipeWire or PulseAudio with Bluetooth, bluez-alsa).
- The app uses the host network. With a host firewall, open TCP 8780 and UDP 1900.

More: [github.com/rosenkolev/bluetooth-to-speaker](https://github.com/rosenkolev/bluetooth-to-speaker)
