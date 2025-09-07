# ESP32-Stick-POE-P-CAM-MicroPython-Examples
MicroPython Examples for ESP32-Stick-POE-P-CAM and compatible SBCs

The MicroPython code examples in this respository support the following SBCs.  This list will be updated over time as more compatible SBCs are qualified.

Supported SBCs
- https://www.tindie.com/products/allexok/esp32-stick-poe-p-camn16r8/
- https://www.tindie.com/products/allexok/ai-on-the-edge-cam-esp32-s3-with-poe-sd-camera/

Code Examples
- Ethernet Connectivity
- WiFi and Ethernet Concurrent Connectivity
- WiFi and Ethernet Concurrent Connectivty and Web Server Based Camera Image Capture (i.e. Stream)

These code examples are board feature and function illustrative, and incremental in design, such that each example adds features based on the preceding code example, as outlined above.  These code examples require integrated camera support via the https://github.com/cnadler86/micropython-camera-API project.

Known Issues
- 'OSError: [Errno 95] EOPNOTSUPP: ESP_ERR_NOT_SUPPORTED' Change 'frame_size' in the Camera() object creation method to a frame size appropriate for your camera
    >>> from camera import FrameSize
    >>> dir(camera)
    ['__class__', '__name__', 'CIF', 'FHD', 'HD', 'HQVGA', 'HVGA', 'P_3MP', 'P_FHD', 'P_HD', 'QCIF', 'QHD', 'QQVGA', 'QSXGA', 'QVGA', 'QXGA',
    'R128x128', 'R240X240', 'R320X320', 'R96X96', 'SVGA', 'SXGA', 'UXGA', 'VGA', 'WQXGA', 'XGA', '__bases__', '__dict__']
- The network.LAN (i.e. W5500 Ethernet support) module object in MicroPython does not completely (re)initialize unless a hard reset is done
- 'OSError: SPI host already in use' The machine.SPI module object does not completely (re)initialize as well, which the network.LAN module relies on, press SBC 'reset' button after code download
- The SPI baudrate should be set to 40 MHz to support maximum Ethernet port speed performance, a button (hardware) reset ensures is achieved
- 'No peripheral is connected to the channel' Camera (de)initialization can report a warning https://github.com/espressif/esp32-camera/issues/750
- 'spi_master_deinit_driver(*): not all CSses freed' SPI (de)initialization can report a warning

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

The code examples are completely free to use, without any restriction or limitation.  Professional, polite feedback welcome.  If you find this code of educational value, and wish support, motivate, future development, please consider a donation to the Dachshund Rescue of your choice.
