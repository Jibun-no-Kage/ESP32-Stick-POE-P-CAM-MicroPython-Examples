# ESP32-Stick-POE-P-CAM-MicroPython-Examples
MicroPython Examples for ESP32-Stick-POE-P-CAM and compatible SBCs

The example MicroPython code examples in this respository supports the following SBCs.  This list will be updated over time as more compatible SBCs are qualified.

Supported SBCs
- https://www.tindie.com/products/allexok/esp32-stick-poe-p-camn16r8/
- https://www.tindie.com/products/allexok/ai-on-the-edge-cam-esp32-s3-with-poe-sd-camera/

Code Examples
- Initialization of Ethernet Connectivity
- Initialization of Condurrent WiFi and Ethernet Connectivity
- Initialization of Concurrent WiFi, Ethernet Connectivty and Web Server Based Image Capture

These code examples are board feature and function illustratives, and incremental in design, such that each example adds features based on the preceding code example, as outlined above.  These code examples require integrated camera support via the https://github.com/cnadler86/micropython-camera-API project.

Known Issues
- The network.LAN (i.e. W5500 Ethernet support) module object in MicroPython does not completely reinitialize unless a hard reset is done
- The machine.SPI module object does not completely reinitialize as well, which the network.LAN module relies on
- The SPI baudrate should be set to 40 MHz to support maximum Ethernet port speed performance, a hardware reset ensures is achieved

The above issues do not affect core functionality, but do make interactive debugging problematic, especially if Thonny IDE is used.

About Thonny IDE
- Not the greatest IDE according to some MicroPython users, but a place to start if a beginner https://thonny.org/
- Download https://github.com/thonny/thonny/releases
- Other MicroPython Compatible IDEs https://randomnerdtutorials.com/micropython-ides-esp32-esp8266/

MicroPython Resources
- Overview https://micropython.org/
- Quick Start Guide https://docs.micropython.org/en/latest/esp32/tutorial/intro.html
- API Documentation https://docs.micropython.org/en/latest/
- Download Firmware Images https://micropython.org/download/
- Community Forum https://github.com/orgs/micropython/discussions
- Discord https://discord.com/invite/RB8HZSAExQ
