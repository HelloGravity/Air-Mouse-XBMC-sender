import sys, select,os, XBMCClient, time, threading, fcntl

done = False;
input_files = [ "/dev/input/by-id/" + f for f in os.listdir("/dev/input/by-id/") if f.startswith("usb-EXCEL_EXCELDIGI_Wireless_Device-") ]

class CommunicationThread(threading.Thread):
	def __init__(self):
		super(CommunicationThread, self).__init__()
		self.connected = False;
	def run(self):
		global done;
		try:
			self.client = XBMCClient.XBMCClient(name='AirMouse');
			while not self.client.connect() and not done:
				time.sleep(1);
			self.connected = not done;
			while not done and self.client.ping:
				time.sleep(30);
			done = True;
		except:
			done = True;
	def sendKey(self, keyCode, down):
		if self.connected and not done:
			self.client.send_button_state("KB", keyCode, 0, down);

class MainThread(threading.Thread):
	def __init__(self):
		super(MainThread, self).__init__()

	def analyze_and_send (self, data):
		if len(data) != 16:
			return;
		if ord(data[8]) != 1 or ord(data[9]) != 0 or ord(data[13]) != 0 or ord(data[14]) != 0 or ord(data[15]) != 0:
			return;
		down = ord(data[12]);
		if down > 1:
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
		communicationThread.sendKey(keyCode, down);		

	def read(self):
		global done;
		poll = select.poll();
		for file in input_files:
			fd = os.open(file, os.O_RDWR| os.O_NONBLOCK);
			try:
				fcntl.ioctl(fd, 1074021776, 1);
				poll.register(fd,select.POLLIN);
			except:
				pass;
		while not done:
			for (fd, mask) in poll.poll():
				if mask == select.POLLNVAL :
					poll.unregister(fd);
					continue;
				if mask != select.POLLIN :
					continue;
				self.analyze_and_send(os.read(fd, 16));
		done = True;
		
	def run(self):
		global done;
		try:
			self.read();
		except Exception as e:
			print "Unexpected error:", sys.exc_info()[0]
			print e
			done = True;

communicationThread = CommunicationThread();
communicationThread.start()
mainThread = MainThread();
mainThread.start();
