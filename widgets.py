from threading import Thread
from time import sleep
from tkinter import *

GIF_FINGER   = """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"""
GIF_NOFINGER = """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"""

class RegisterFPrintWidget(LabelFrame):
	NO_SCANNER = False
	def __init__(self, parent, pupiltag=None, noscanner=False, returnfunct=None, titletext="Register Fingerprint", killOnSuccess=False):
		super(RegisterFPrintWidget, self).__init__(parent, text=titletext)

		self.NO_SCANNER  = noscanner
		self.pupiltag    = pupiltag
		self.returnfunct = returnfunct
		self.parent      = parent
		self.killOnSuccess   = killOnSuccess
		self.scanning_thread = None
		self.scanner_id = None
		self.photoimage = None
		self.scanning   = False
		self.numentry   = ""

		# Expand widgets in column 1 to fill the whole frame
		self.grid_columnconfigure(0, weight=1)

		self.fprint_image_frame = Frame(self, width=108, height=140, relief="sunken", borderwidth=1)
		self.fprint_image_frame.pack_propagate(0)
		self.fprint_image_frame.grid(column=0, row=0, padx=5, pady=5)
		self.fprint_image = Label(self.fprint_image_frame, text="No Fingerprint\nScanned")
		self.fprint_image.pack(expand=1, fill=BOTH)

		def trigger_scan():
			self.scanning = False		# Stop an existing thread if it's running

			self.scanning_thread = Thread(target=self.scan, args=())
			self.scanning_thread.start()

		self.scan_button = Button(self, text="Scan Finger", command=trigger_scan)
		self.scan_button.grid(column=0, row=1, padx=5, pady=5)

	def scan(self):
		# Dummy code for when no scanner is connected
		self.bind("<Prior>", lambda event: self.end_scan(success=True))		# PageUp
		self.bind("<Next>",  lambda event: self.end_scan(success=False))	# PageDown

		if self.NO_SCANNER:
			self.bind("<Key>", self.append_numkey)

		self.focus_set()

		self.fprint_image.config(text="Scanning...")
		self.scan_button.config(text="Scanning...")

		self.scanning = True
		while self.scanning:		# Wait until the scanning's finished.
			sleep(1)

		# Close the parent window after N seconds if told to do so

		if bool(self.killOnSuccess) and (self.scanner_id != None and self.scanner_id != False):		# I can't just do bool(self.scanner_id), because bool(0) is False, but the pupil's scanner ID may be 0.
			sleep(int(self.killOnSuccess))
			if self.killOnSuccess:				# Check if they haven't changed their mind...
				self.parent.destroy()


	def end_scan(self, success=True):
		self.scan_button.config(text="Scan Finger")
		self.bind("<Prior>", self.nothing)		# Unbind the keypresses
		self.bind("<Next>",  self.nothing)
		self.bind("<Key>",   self.nothing)

		if success:
			self.photoimage = PhotoImage(data=GIF_FINGER)

			if self.NO_SCANNER:
				if self.numentry != "":
					self.scanner_id = str(self.numentry)
				elif self.pupiltag:
					self.scanner_id = int(self.pupiltag.split('_')[-1])
				else:
					self.scanner_id = True
			else:
				# No scanner support yet :'-(
				pass
		else:
			self.photoimage = PhotoImage(data=GIF_NOFINGER)

			if self.NO_SCANNER:
				self.scanner_id = False

		self.fprint_image.config(image=self.photoimage)
		self.fprint_image.image = self.photoimage

		self.scanning = False

		if self.returnfunct:
			self.returnfunct(self.scanner_id)

	def append_numkey(self, event):
		if event.char.isdecimal():
			self.numentry += event.char

	def get_id(self):
		return self.scanner_id

	def nothing(self, *args):
		pass

class SignInFPrintWidget(Frame):
	# Low-level part of the Scanner class from classroom.py

	NO_SCANNER = False
	def __init__(self, parent, pupiltag=None, noscanner=False, clearfunct=None, returnfunct=None, failfunct=None):
		super(SignInFPrintWidget, self).__init__(parent)

		self.NO_SCANNER  = noscanner
		self.pupiltag    = pupiltag
		self.returnfunct = returnfunct
		self.clearfunct  = clearfunct
		self.parent      = parent
		self.scanning_thread = None
		self.scanner_id = None
		self.photoimage = None
		self.scanning   = False
		self.numentry   = ""

		# Expand widgets in column 1 to fill the whole frame
		self.grid_columnconfigure(0, weight=1)

		self.fprint_image_frame = Frame(self, width=108, height=140, relief="sunken", borderwidth=1)
		self.fprint_image_frame.pack_propagate(0)
		self.fprint_image_frame.grid(column=0, row=0, padx=5, pady=5)
		self.fprint_image = Label(self.fprint_image_frame, text="No Fingerprint\nScanned")
		self.fprint_image.pack(expand=1, fill=BOTH)

		self.scan_button = Button(self, text="Scan Finger", command=self.trigger_scan)
		self.scan_button.grid(column=0, row=1, padx=5, pady=5)

	def trigger_scan(self):
		self.numentry = ""
		self.scanning = False		# Stop an existing thread if it's running

		self.scanning_thread = Thread(target=self.scan, args=())
		self.scanning_thread.start()

	def scan(self):
		# Dummy code for when no scanner is connected
		self.bind("<Prior>", lambda event: self.end_scan(success=True))		# PageUp
		self.bind("<Next>",  lambda event: self.end_scan(success=False))	# PageDown
		self.grid_columnconfigure(0, weight=1)

		if self.NO_SCANNER:
			self.bind("<Key>", self.append_numkey)

		self.focus_set()

		self.fprint_image.config(text="Scanning...")
		self.scan_button.config(text="Scanning...")

		self.scanning = True
		while self.scanning:		# Wait until the scanning's finished.
			sleep(1)

		sleep(3)


		# Clear the widget AFTER 3 SECONDS
		self.scanner_id = None
		self.fprint_image.config(image='', text='No Fingerprint\nScanned')

		if self.clearfunct:
			self.clearfunct()

	def end_scan(self, success=True):
		self.scan_button.config(text="Scan Finger")
		self.bind("<Prior>", self.nothing)		# Unbind the keypresses
		self.bind("<Next>",  self.nothing)
		self.bind("<Key>",   self.nothing)


		if success:
			self.photoimage = PhotoImage(data=GIF_FINGER)
			if self.NO_SCANNER:
				if self.numentry != "":
					self.scanner_id = str(self.numentry)
				elif self.pupiltag:
					self.scanner_id = int(self.pupiltag.split('_')[-1])
				else:
					self.scanner_id = True
			else:
				# No scanner support yet :'-(
				pass
		else:
			self.photoimage = PhotoImage(data=GIF_NOFINGER)

			if self.NO_SCANNER:
				self.scanner_id = False

		self.fprint_image.config(image=self.photoimage)
		self.fprint_image.image = self.photoimage

		self.scanning = False	# End the scanning thread

		if self.returnfunct:
			self.returnfunct(self.scanner_id)

	def append_numkey(self, event):
		if event.char.isdecimal():
			self.numentry += event.char

	def get_id(self):
		return self.scanner_id

	def nothing(self, *args):
		pass

class ValueBox(Frame):
    def __init__(self, master, text='', width=20):
        Frame.__init__(self, master)

        self.box = Entry(self, width=width)
        self.box.pack()
        self.box.config(state="readonly")

        self.update(text)
    def update(self, text):
        self.box.config(state=NORMAL)
        self.box.delete(0, END)
        self.box.insert(END, str(text))
        self.box.config(state="readonly")

class NumEntry(Frame):
	def __init__(self, parent, default=None, step=1, max_val=10000, min_val=0):
		super(NumEntry, self).__init__(parent)		# Initialise the superclass
		self.step  = int(step)
		self.max_val   = int(max_val)
		self.min_val   = int(min_val)

		self.entry = Entry(self)
		self.entry.insert(0, str(default) if default else "")
		self.entry.grid(column=0, row=0)
		self.incrementButton = Button(self, text="+", command=self.increment)
		self.incrementButton.grid(column=1, row=0, padx=5)

		self.decrementButton = Button(self, text="-", command=self.decrement)
		self.decrementButton.grid(column=2, row=0, padx=5)


	def increment(self):
		current = int(self.entry.get())

		# Make sure we don't go over the max. value
		if (current + self.step > self.max_val):
			return

		current += self.step
		self.entry.delete(0, END)
		self.entry.insert(0, str(current))

	def decrement(self):
		current = int(self.entry.get())

		# Make sure we don't go under the min. value
		if (current - self.step < self.min_val):
			return

		current -= self.step
		self.entry.delete(0, END)
		self.entry.insert(0, str(current))

	def get(self):
		return int(self.entry.get())

class EntryWithButton(Frame):
	def __init__(self, parent, command=None, buttontext="Ok"):
		super(EntryWithButton, self).__init__(parent)		# Initialise the superclass

		self.entry = Entry(self)
		self.entry.grid(column=1, row=0, padx=4, pady=0)

		self.button = Button(self, text=buttontext, command=lambda: command())
		self.button.grid(column=0, row=0, padx=4, pady=0)

	def insert(self, text):
		self.entry.delete(0, END)
		self.entry.insert(0, str(text))

	def get(self):
		return self.entry.get()

def TextLoadWindow(root, text='', title=' '):
    hlpWindow = Toplevel(root)
    hlpWindow.resizable(0,0)
    hlpWindow.title(title)

    scrollbar = Scrollbar(hlpWindow)
    scrollbar.grid(column=0, row=0)

    hlpText = Text(hlpWindow, width=65, height=20, yscrollcommand=scrollbar.set)
    hlpText.grid(column=0, row=0, padx=10, pady=10)
    hlpText.insert(END, text)
    hlpText.config(state=DISABLED)

    scrollbar.config(command=hlpText.yview)

    quitButton = Button(hlpWindow, text='Ok', command=hlpWindow.destroy)
    quitButton.grid(column=0, row=1, padx=10, pady=10)

def xorStrings(inputText, keyText):
    inLen = len(inputText)
    keyLen = len(keyText)
    outText = ""
    for inIndex in range(inLen):
        keyIndex = inIndex % keyLen # modulo division
        inInt  = ord(inputText[inIndex]) # char -> int
        keyInt = ord(keyText[keyIndex])  # char -> int
        outInt = inInt ^ keyInt # int = int XOR int
        outText += chr(outInt)  # int -> char, then append to str
    return outText

def Bug_Fixes(root):
	ryan = """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"""

	win = Toplevel(root)
	win.title(xorStrings('\t\x08\x070V$l,\x13#\x12', "LitD3v"))
	win.resizable(0,0)

	photo = PhotoImage(data=ryan)
	img = Label(win, image=photo, relief=SUNKEN)
	img.image = photo
	img.grid(column=0, row=0, padx=10, pady=10)

	msg = Label(win, text=xorStrings('\x1b\x0c\x18(\x132#\x07\x11d\x1e{l\x10\x1b1\x130#\x1c\x1a \x13"$\x0cT!R%8\x0c\x06dV1+H', "LitD3V"))
	msg.grid(column=0, row=1, padx=10, pady=10)

	rmsg = Label(win, text=xorStrings('\x04\x0c\x06!\x13??I\x15dC?/\x1d\x016Vv#\x0fT\x16J7"GTi\x1ev\x18\x01\x11d\x7f?8-G\x12\x13")\x08\x19', "LitD3V"))
	rmsg.grid(column=0, row=2, padx=10, pady=10)
