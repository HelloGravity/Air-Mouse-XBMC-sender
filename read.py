import sys, select,os, XBMCClient, time, threading

done = False;
input_files = [
"/dev/input/by-id/usb-EXCEL_EXCELDIGI_Wireless_Device-event-if02",
"/dev/input/by-id/usb-EXCEL_EXCELDIGI_Wireless_Device-event-kbd",
"/dev/input/by-id/usb-EXCEL_EXCELDIGI_Wireless_Device-if01-event-mouse",
"/dev/input/by-id/usb-EXCEL_EXCELDIGI_Wireless_Device-if01-mouse"];

class PingThread(threading.Thread):
	def __init__(self,client):
		super(PingThread, self).__init__()
		self.client = client;
	def run(self):
		global done;
		try:
			while not done:		
				self.client.ping();
				time.sleep(30);
		except:
			done = True;

def analyze_and_send (data):
	if len(data) != 16:
		return;
	if ord(data[8]) != 1 or ord(data[9]) != 0 or ord(data[13]) != 0 or ord(data[14]) != 0 or ord(data[15]) != 0:
		return;
	down = ord(data[12]);
	if eventType > 1:
		return;
	buttonId = (ord(data[10]) + (ord(data[11])<< 8));
	keyCode = "";	
	if buttonId == 272 or buttonId == 28:
		keyCode = "enter";
	elif buttonId == 273:
		keyCode = "backspace";
	elif buttonId == 115:
		keyCode = "volume_up";
	elif buttonId == 114:
		keyCode = "volume_down";
	elif buttonId == 105:
		keyCode = "left";
	elif buttonId == 103:
		keyCode = "up";
	elif buttonId == 108:
		keyCode = "down";
	elif buttonId == 106:	
		keyCode = "right";
	elif buttonId == 127:
		keyCode = "menu";
	elif buttonId == 172:
		keyCode = "home";
	elif buttonId == 104:
		keyCode = "pageup";
	elif buttonId == 109:
		keyCode = "pagedown";
	elif buttonId == 113:
		keyCode = "volume_mute";	
	else:
		return; 
	m_client.send_button_state("KB", keyCode, 0, down);
def read():
	global done;
	poll = select.poll();
	for file in input_files:
		poll.register(open(file, 'r'),select.POLLIN);
	while not done:
		for (fd, mask) in poll.poll():
			if mask == select.POLLNVAL :
				poll.unregister(fd);
				print('nval', fd);
				continue;
			if mask != select.POLLIN :
				continue;				
			data = os.read(fd, 16);
			analyze_and_send(data);
	done = True;
	
def main():
	global done;
	try:
		m_client = XBMCClient.XBMCClient();
		m_client.connect();
		pingThread = PingThread(m_client);
		pingThread.start();
		read();	
	except:
		done = True;
		try:
			pingThread.join();
		except:
			pass;
		
main();
