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

# DefaultDelegate: to receive Bluetooth message asynchronously

# Scanner: to scan for BLE devices which are broadcasting data
class ScanDelegate(DefaultDelegate):
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

	def handleNotification(self, cHandle, data):
		print(cHandle)
		print(data)

# withDelegate: to stores a reference to a delegate object, which receives callbacks when broadcasts from devices are received
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

mode = input('Choose the mode: (1: default; else: custom)')
try:
	if mode=="1":
		print ("Services...")
		for service in dev.services:
			print (str(service))
		print (str(dev.getServiceByUUID(UUID(SERVICE_UUID))))
		ch = dev.getCharacteristics(uuid=UUID(CHAR_UUID))[0] 	# writeHandle = ch.valHandle or ch.getHandle()
	else:
		print ("Services...")
		n = 0
		services = dev.services
		for service in services:
			print (str(n)+": "+str(service))
			n+=1
		number = input('Enter your service number: ')
		print('Service', number)
		service_uuid = list(services)[int(number)].uuid
		print(service_uuid)
		service = dev.getServiceByUUID(UUID(service_uuid))
		print (str(service))

		print ("Characteristics...")
		n = 0
		characteristics = service.getCharacteristics()
		for ch in characteristics:
			print (str(n)+": "+str(ch))
			n+=1
		number = input('Enter your characteristic number: ')
		print('Characteristic', number)
		ch = list(characteristics)[int(number)]
		# print(ch_uuid)
		# ch = service.getCharacteristics(UUID(ch_uuid))
		print (str(ch))
		
	dev.writeCharacteristic(ch.valHandle, b"\x65\x66") 		# Test writeCharacteristic

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