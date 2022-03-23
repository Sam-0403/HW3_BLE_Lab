from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate, AssignedNumbers
import struct
INDIC_ON = struct.pack('BB', 0x02, 0x00)
NOTIF_ON = struct.pack('BB', 0x01, 0x00)
NOTIF_OFF = struct.pack('BB', 0x00, 0x00)

# user config
DEVICE_NAME = "Heart Rate"
SERVICE_UUID = 0xfff0
CHAR_UUID = 0xfff4

class ScanDelegate(DefaultDelegate):
	"""
	DefaultDelegate receive Bluetooth message asynchronously, 
	Scanner is to scan for LE devices which are broadcasting data
	withDelegate stores a reference to a delegate object, which receives callbacks when broadcasts from devices are received
	"""
	def __init__(self):
		DefaultDelegate.__init__(self)
	def handleDiscovery(self, dev, isNewDev, isNewData):
		if isNewDev:
			print("Discovered device", dev.addr)
		elif isNewData:
			print("Received new data from", dev.addr)

class PeripheralDelegate(DefaultDelegate):
	def __init__(self, handle):
		DefaultDelegate.__init__(self)
		print("handleNotification init")
		self.hndl = handle
		# ... initialise here

	def handleNotification(self, cHandle, data):
	# ... perhaps check cHandle
		print(cHandle)
		print(data)
	# ... process 'data'

scanner = Scanner().withDelegate(ScanDelegate()) 
devices = scanner.scan(3.0)
n = 0
for dev in devices:
	print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi))
	n += 1
	for (adtype, desc, value) in dev.getScanData():
		if (value == DEVICE_NAME):
			print('===============================')
			print ("%s, %s" % (desc, value))
			print('===============================')
		else:
			print ("%s, %s" % (desc, value))
number = input('Enter your device number: ')
print('Device', number)
print(list(devices)[int(number)].addr)

print ("Connecting...")
dev = Peripheral(list(devices)[int(number)].addr, 'random')

print ("Services...")
for svc in dev.services:
	print (str(svc))
try:
	print (str(dev.getServiceByUUID(UUID(SERVICE_UUID))))
	ch = dev.getCharacteristics(uuid=UUID(CHAR_UUID))[0] # writeHandle = ch.valHandle
	dev.writeCharacteristic(ch.valHandle, b"\x65\x66") # Test writeCharacteristic

	# custom_service_handle_cccd = ch.valHandle + 1
	# dev.writeCharacteristic(custom_service_handle_cccd, INDIC_ON)	# Can't work
	desc = ch.getDescriptors(AssignedNumbers.client_characteristic_configuration)
	print(str(desc))
	dev.writeCharacteristic(desc[0].handle, INDIC_ON) # test writeCharacteristic

	custom_service_handle_cccd = ch.valHandle + 1
	dev = dev.withDelegate(PeripheralDelegate(custom_service_handle_cccd))

	while True:
		if dev.waitForNotifications(3.0):
			print("Test Notification")
			continue
		print ("Waiting...")
finally:
	dev.disconnect()