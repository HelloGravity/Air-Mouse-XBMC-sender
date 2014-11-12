Air-Mouse-XBMC-sender
=====================

The problem:


I am using this cheap air mouse I got from eBay:


"Black 2.4GHz Wireless Fly Air Mouse Android Remote Control 3D Motion Stick" (also sold under the name "T2"). 

Anyone with this mouse and XBMC will agree that using it is very annoying, especially if you want to use it as a remote and disable the gyro mouse feature.

This is a script I wrote to fix the annoyances. 
It reads key presses from this air mouse, and sends them to XBMC through EventServer.
It works on a Raspberry Pi with OpenElec (will probably also work on Xbian and Raspbmc).
The script reads all the button presses, and sends them to XBMC on the same machine, and it does not care if the mouse is in 'mouse' mode, or in 'mouse disabled' mode.
It only respond to key presses, and ignores all mouse events, so that the device will only work as a remote and not as a mouse.

The script XBMCClient.py is taken from the XBMC repo:
https://github.com/xbmc/xbmc/blob/master/tools/EventClients/lib/python/xbmcclient.py

The script reads the input from "/dev/input/" and searches the files that start with
"usb-EXCEL_EXCELDIGI_Wireless_Device-".

Since XBMC uses the EVIOCGRAB operation, it is impossible to read the files after XBMC has launched, so in order to fix that, the script is called from autostart.sh, and it also uses EVIOCGRAB, to prevent XBMC from accessing the device files.

If you want to use this (instructions are for OpenElec on the Raspberry Pi):

1.	Create an autostart.sh file as shown here: http://wiki.openelec.tv/index.php?title=Autostart.sh

2.	Take script.py and XBMCClient.py and put them in a directory (I used /storage/AirMouseScript/)

3.	Change autostart.sh to run script.py (like in the provided autostart.sh), and don't forget the '&' in the end of the command.

4.	Put airmouse.xml in /storage/.kodi/userdata/keymaps or /storage/.xbmc/userdata/keymaps, depending on your OpenElec Version.
