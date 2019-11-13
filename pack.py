'''
	Mstar bin firmware packer
'''

'''
	Header structure
	-------
	Multi-line script which contains MBOOT commands
	The header script ends with line: '% <- this is end of file symbol'
	Line separator is '\n'
	The header is filled by 0xFF to 16KB
	The header size is always 16KB
'''

'''
	Bin structure
	-------
	Basically it's merged parts:

	[part 1]
	[part 2]
	....
	[part n]

	Each part is 4 byte aligned (filled by 0xFF)
'''

'''
	Footer structure
	|MAGIC|CRC1: SWAPPED HEADER CRC32|CRC2: SWAPPED BIN CRC32|FIRST 16 BYTES OF HEADER|

	# NB XGIMI uses HEADER+BIN+MAGIC+HEADER_CRC to calculate crc2
	# Use USE_XGIMI_CRC2=True option to enable "XGIMI" mode
'''

import configparser
import sys
import time
import os
import struct
import utils
import shutil

DEBUG = False

def DB(m):
	if(DEBUG):
		print(m)

print("[i] Packing...")

tmpDir = 'tmp'
headerPart = os.path.join(tmpDir, '~header')
binPart = os.path.join(tmpDir, '~bin') 
footerPart = os.path.join(tmpDir, '~footer') 

# Command line args
if len(sys.argv) == 1: 
	DB("Usage: pack.py <config file>")
	DB("Example: pack.py configs/letv-x355pro.ini")
	quit()

configFile = sys.argv[1]

# Parse config file
config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
#config = configparser.ConfigParser()
config.read(configFile)

# Main
main = config['Main'];
firmwareFileName = main['FirmwareFileName']
projectFolder = main['ProjectFolder']
useHexValuesPrefix = utils.str2bool(main['useHexValuesPrefix'])

SCRIPT_FIRMWARE_FILE_NAME = main['SCRIPT_FIRMWARE_FILE_NAME']
DRAM_BUF_ADDR = main['DRAM_BUF_ADDR']
MAGIC_FOOTER = main['MAGIC_FOOTER']
HEADER_SIZE = utils.sizeInt(main['HEADER_SIZE'])

# XGIMI uses HEADER+BIN+MAGIC+HEADER_CRC to calculate crc2
if 'USE_XGIMI_CRC2' in main:
	USE_XGIMI_CRC2 = utils.str2bool(main['USE_XGIMI_CRC2'])
else:
	USE_XGIMI_CRC2 = False

# Header
header = config['HeaderScript'];
headerScriptPrefix = config.get('HeaderScript', 'Prefix', raw = True)
headerScriptSuffix = config.get('HeaderScript', 'Suffix', raw = True)


# Parts
parts = list(filter(lambda s: s.startswith('part/'), config.sections()))

DB("\n")
DB("[i] Date: {}".format(time.strftime("%d/%m/%Y %H:%M:%S")))
DB("[i] Firmware file name: {}".format(firmwareFileName))
DB("[i] Project folder: {}".format(projectFolder))
DB("[i] Use hex values: {}".format(useHexValuesPrefix))
DB("[i] Script firmware filename: {}".format(SCRIPT_FIRMWARE_FILE_NAME))
DB("[i] DRAM_BUF_ADDR: {}".format(DRAM_BUF_ADDR))
DB("[i] MAGIC_FOOTER: {}".format(MAGIC_FOOTER))
DB("[i] HEADER_SIZE: {}".format(HEADER_SIZE))

# Create working directory
DB('[i] Create working directory ...')
utils.createDirectory(tmpDir)

DB('[i] Generating header and bin ...')
# Initial empty bin to store merged parts
open(binPart, 'w').close()

with open(headerPart, 'wb') as header:

	header.write('#-------------USB Upgrade Bin Info----------------\n'.encode())
	header.write('# Device : cv6a358_international\n'.encode())
	header.write('# Build PATH : /home/luoshupeng/project_358/358\n'.encode())
	header.write('# Build TIME : {}\n'.format(time.strftime("%Y-%m-%d %H:%M:%S")).encode())
	header.write('\n'.encode())

	# Directive tool
	directive = utils.directive(header, DRAM_BUF_ADDR, useHexValuesPrefix)

	header.write('# Header prefix'.encode())
	header.write(headerScriptPrefix.encode())
	header.write('\n\n'.encode())

	header.write('# Partitions'.encode())
	for sectionName in parts:

		part = config[sectionName]
		name = sectionName.replace('part/', '')
		create = utils.str2bool(utils.getConfigValue(part, 'create', ''))
		size = utils.getConfigValue(part, 'size', 'NOT_SET')
		erase = utils.str2bool(utils.getConfigValue(part, 'erase', ''))
		type = utils.getConfigValue(part, 'type', 'NOT_SET')
		imageFile = utils.getConfigValue(part, 'imageFile', 'NOT_SET')
		chunkSize = utils.sizeInt(utils.getConfigValue(part, 'chunkSize', '0'))
		lzo = utils.str2bool(utils.getConfigValue(part, 'lzo', ''))
		simg = utils.str2bool(utils.getConfigValue(part, 'simg', ''))
		memoryOffset = utils.getConfigValue(part, 'memoryOffset', 'NOT_SET')
		emptySkip = utils.str2bool(utils.getConfigValue(part, 'emptySkip', 'True'))

		DB("\n")
		DB("[i] Processing partition")
		DB("[i]      Name: {}".format(name))
		DB("[i]      Create: {}".format(create))
		DB("[i]      Size: {}".format(size))
		DB("[i]      Chunk Size: {}".format(chunkSize))
		DB("[i]      Erase: {}".format(erase))
		DB("[i]      Type: {}".format(type))
		DB("[i]      Image: {}".format(imageFile))
		DB("[i]      LZO: {}".format(lzo))
		DB("[i]      Simg: {}".format(simg))
		DB("[i]      Memory Offset: {}".format(memoryOffset))
		DB("[i]      Empty Skip: {}".format(emptySkip))

		emptySkip = utils.bool2int(emptySkip) # 0 - False, 1 - True

		header.write('\n'.encode())
		header.write('# {}\n'.format(name).encode())

		if (create):
			directive.create(name, size)

		if (erase and imageFile == 'NOT_SET'):
			directive.erase_p(name)

		if (type == 'partitionImage'):
			
			if (chunkSize > 0):
				if(simg == False):
					DB('[i] Splitting ...')
					chunks = utils.splitFile(imageFile, tmpDir, chunksize = chunkSize)
				else:
					#create chunk files
					#simg2simg system.simg systemchunk 157286400
					DB('[i] Splitting ...')
					chunks = utils.createChunkFile(imageFile, tmpDir, chunksize = chunkSize)
					
			else:
				# It will contain whole image as a single chunk
				chunks = utils.splitFile(imageFile, tmpDir, chunksize = 0)

			for index, inputChunk in enumerate(chunks):
				DB('[i] Processing chunk: {}'.format(inputChunk))
				(name1, ext1) = os.path.splitext(inputChunk)
				if lzo:
					outputChunk = name1 + '.lzo'
					DB('[i]     LZO: {} -> {}'.format(inputChunk, outputChunk))
					utils.lzo(inputChunk, outputChunk)
				else:
					outputChunk = inputChunk

				# Size, offset (hex)
				size = "{:02X}".format(os.path.getsize(outputChunk))
				offset = "{:02X}".format(os.path.getsize(binPart) + HEADER_SIZE)

				directive.filepartload(SCRIPT_FIRMWARE_FILE_NAME, offset, size)
				if (index == 0 and erase): 
					directive.erase_p(name) 

				DB('[i]     Align chunk')
				utils.alignFile(outputChunk)

				DB('[i]     Append: {} -> {}'.format(outputChunk, binPart))
				utils.appendFile(outputChunk, binPart)

				if lzo:
					if index == 0:
						directive.unlzo(name, size, DRAM_BUF_ADDR, emptySkip)
					else:
						directive.unlzo_cont(name, size, DRAM_BUF_ADDR, emptySkip)
				elif simg:
					#if len(chunks) == 1:
					directive.sparse_write_mmc(name, size, DRAM_BUF_ADDR, emptySkip)
					#else:
					#	DB('[!] UNSUPPORTED: sparse_write mmc more than 1 time')
					#	quit()
				else:
					if len(chunks) == 1:
						directive.write_p(name, size, DRAM_BUF_ADDR, emptySkip)
					else:
						# filepartload 50000000 MstarUpgrade.bin e04000 c800000
						# mmc write.p.continue 50000000 system 0 c800000 1

						# filepartload 50000000 MstarUpgrade.bin d604000 c800000
						# mmc write.p.continue 50000000 system 64000 c800000 1
						# Why offset is 64000 but not c800000 ???
						DB('[!] UNSUPPORTED: mmc write.p.continue')
						quit()

		if (type == 'secureInfo'):

			chunks = utils.splitFile(imageFile, tmpDir, chunksize = 0)
			outputChunk = chunks[0]

			size = "{:02X}".format(os.path.getsize(outputChunk))
			offset = "{:02X}".format(os.path.getsize(binPart) + HEADER_SIZE)
			directive.filepartload(SCRIPT_FIRMWARE_FILE_NAME, offset, size)

			DB('[i]     Align')
			utils.alignFile(outputChunk)

			DB('[i]     Append: {} -> {}'.format(outputChunk, binPart))
			utils.appendFile(outputChunk, binPart)
			directive.store_secure_info(name)

		if (type == 'nuttxConfig'):

			chunks = utils.splitFile(imageFile, tmpDir, chunksize = 0)
			outputChunk = chunks[0]

			size = "{:02X}".format(os.path.getsize(outputChunk))
			offset = "{:02X}".format(os.path.getsize(binPart) + HEADER_SIZE)
			directive.filepartload(SCRIPT_FIRMWARE_FILE_NAME, offset, size)

			DB('[i]     Align')
			utils.alignFile(outputChunk)

			DB('[i]     Append: {} -> {}'.format(outputChunk, binPart))
			utils.appendFile(outputChunk, binPart)
			directive.store_nuttx_config(name)

		if (type == 'sboot'):

			chunks = utils.splitFile(imageFile, tmpDir, chunksize = 0)
			outputChunk = chunks[0]

			size = "{:02X}".format(os.path.getsize(outputChunk))
			offset = "{:02X}".format(os.path.getsize(binPart) + HEADER_SIZE)
			directive.filepartload(SCRIPT_FIRMWARE_FILE_NAME, offset, size)

			DB('[i]     Align')
			utils.alignFile(outputChunk)

			DB('[i]     Append: {} -> {}'.format(outputChunk, binPart))
			utils.appendFile(outputChunk, binPart)
			directive.write_boot(size, DRAM_BUF_ADDR, emptySkip)
			
		if (type == 'inMemory'):
		
			chunks = utils.splitFile(imageFile, tmpDir, chunksize = 0)
			outputChunk = chunks[0]
			
			size = "{:02X}".format(os.path.getsize(outputChunk))
			offset = "{:02X}".format(os.path.getsize(binPart) + HEADER_SIZE)
			directive.filepartload(SCRIPT_FIRMWARE_FILE_NAME, offset, size, memoryOffset=memoryOffset)
			
			DB('[i]     Align')
			utils.alignFile(outputChunk)
			
			DB('[i]     Append: {} -> {}'.format(outputChunk, binPart))
			utils.appendFile(outputChunk, binPart)
		
		
			
	header.write('\n'.encode())
	header.write('# Header suffix'.encode())
	header.write(headerScriptSuffix.encode())
	header.write('\n'.encode())

	header.write('% <- this is end of script symbol\n'.encode())
	header.flush()

	DB('[i] Fill header script to 16KB')
	header.write( ('\xff' * (HEADER_SIZE - os.path.getsize(headerPart))).encode(encoding='iso-8859-1') ) 

DB('[i] Generating footer ...')

if (USE_XGIMI_CRC2):
	# NB XGIMI uses HEADER+BIN+MAGIC+HEADER_CRC to calculate crc2
	headerCRC = utils.crc32(headerPart)
	header16bytes = utils.loadPart(headerPart, 0, 16)

	# Step #1. Merge HEADER+BIN+MAGIC+HEADER_CRC to one file
	mergedPart = os.path.join(tmpDir, '~merged')
	open(mergedPart, 'w').close()
	utils.appendFile(headerPart, mergedPart)
	utils.appendFile(binPart, mergedPart)
	with open(mergedPart, 'ab') as part:
		DB('[i]     Magic: {}'.format(MAGIC_FOOTER))
		part.write(MAGIC_FOOTER.encode())
		DB('[i]     Header CRC: 0x{:02X}'.format(headerCRC))
		part.write(struct.pack('L', headerCRC))
	
	# Step #2 Calculate CRC2
	mergedCRC = utils.crc32(mergedPart)
	with open(footerPart, 'wb') as footer:
		DB('[i]     Merged CRC: 0x{:02X}'.format(mergedCRC))
		footer.write(struct.pack('L', mergedCRC))
		DB('[i]     First 16 bytes of header: {}'.format(header16bytes))
		footer.write(header16bytes)

	DB('[i] Merging parts ...')
	open(firmwareFileName, 'w').close()
	utils.appendFile(mergedPart, firmwareFileName)
	utils.appendFile(footerPart, firmwareFileName)
else:
	headerCRC = utils.crc32(headerPart)
	binCRC = utils.crc32(binPart)
	header16bytes = utils.loadPart(headerPart, 0, 16)
	with open(footerPart, 'wb') as footer:
		DB('[i]     Magic: {}'.format(MAGIC_FOOTER))
		footer.write(MAGIC_FOOTER.encode())
		DB('[i]     Header CRC: 0x{:02X}'.format(headerCRC))
		footer.write(struct.pack('I', headerCRC)) # struct.pack('L', data) <- returns byte swapped data
		DB('[i]     Bin CRC: 0x{:02X}'.format(binCRC))
		footer.write(struct.pack('I', binCRC))
		DB('[i]     First 16 bytes of header: {}'.format(header16bytes))
		footer.write(header16bytes)

	DB('[i] Merging header, bin, footer ...')
	open(firmwareFileName, 'w').close()
	utils.appendFile(headerPart, firmwareFileName)
	utils.appendFile(binPart, firmwareFileName)
	utils.appendFile(footerPart, firmwareFileName)

shutil.rmtree(tmpDir)
DB('[i] Done')
