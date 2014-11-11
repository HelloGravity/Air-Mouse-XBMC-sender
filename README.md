Air-Mouse-XBMC-sender
=====================

The problem:


I am using this cheap air mouse I got from eBay:


"Black 2.4GHz Wireless Fly Air Mouse Android Remote Control 3D Motion Stick" (also sold under the name "T2"). 


Anyone with this mouse and XBMC will agree that using it is very annoying, especially if you want to use it as a remote and disable the gyro mouse feature.


This is a script I wrote to fix the annoyances. 
It read key presses from this air mouse, and sends them to XBMC through EventServer.
It works on a raspberry pi with Xbian (chosen over OpenElec, for reasons that are explained later).
The script reads all the buttons that are pressed, and sends them to XBMC on the same machine, it does not care if the mouse is in 'mouse' mode, or in 'mouse disabled' mode.
It only respond to key presses, and ignores all mouse events, so that the device will only work as a remote and not as a mouse.

The script XBMCClient.py is taken from the XBMC repo:
https://github.com/xbmc/xbmc/blob/master/tools/EventClients/lib/python/xbmcclient.py

The script reads the following files:
 * /dev/input/by-id/usb-EXCEL_EXCELDIGI_Wireless_Device-event-if02
 * /dev/input/by-id/usb-EXCEL_EXCELDIGI_Wireless_Device-event-kbd
 * /dev/input/by-id/usb-EXCEL_EXCELDIGI_Wireless_Device-if01-event-mouse
 * /dev/input/by-id/usb-EXCEL_EXCELDIGI_Wireless_Device-if01-mouse

The reason I chose Xbian, is that on Xbian, xbmc does not run as root (as opposed to OpenElec), which made the following trick possible:


On Xbian, a config file located at /etc/init/xbmc.conf, loads XBMC. 
I changed it so that before XBMC's load, I change the permissions of /dev/input, so that XBMC won't be able to read the input by itself.
I also added a line after XBMC loads, to start the script read.py (as root).

If you want to use this,
1.	replace xbmc.conf in /etc/init/ with the one that is found here.
2.	move read.py and XBMCClient.py to /home/xbian (or another place, and change the line that calls read.py in xbmc.conf accordingly).
