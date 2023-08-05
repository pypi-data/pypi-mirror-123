import time
import struct
import copy
import logging
from threading import Thread

import serial
import numpy as np

class binaryReceiver():
  def __init__(
      self, data: list[np.ndarray], dataFormat: str, 
      serialPort: str, serialBaud: int, packetHeader=b'\xFD'
    ):
    self.outData = data
    self.dataFormat = dataFormat
    self.port = serialPort
    self.baud = serialBaud
    self.bufferLength = data[0].size
    self.header = packetHeader
    print()

    self.nData = data.__len__()
    
    """ Thread Variables """
    self.serialThread = None
    self.isReceiving = False
    self.isRun = False
    self.isPaused = False

    """ Serial Connection """
    self.serialConnection = None

  def start(self):
    logging.info(f'Connecting to {self.port} at {self.baud} BAUD.')
    try:
      self.serialConnection = serial.Serial(self.port, self.baud, timeout=4)
      logging.info('Connected')
    except Exception as e:
      logging.error(f'Failed to connect: {e}')
      raise e
    self.isRun = True
    if self.serialThread == None:
      self.serialThread = Thread(target=self.readingThread)
      self.serialThread.start()
      logging.info('Reading thread started')
      # Block till we start receiving values
      while self.isReceiving != True:
        time.sleep(0.1)

  def pause(self):
    self.isPaused = True

  def resume(self):
    self.isPaused = False

  def stop(self):
    self.isRun = False
    self.serialThread.join()


  def readingThread(self):
    packetHeaderLen = self.header.__len__()
    packetSize = struct.calcsize(self.dataFormat) + packetHeaderLen
    packets = 10

    invalid = 0
    time.sleep(1.0)  # give some buffer time for retrieving data
    while (self.isRun):
      dataValid = False
      while (dataValid == False):
        self.rawData = self.serialConnection.read(size=packets * packetSize)
        if (bytes(self.rawData[:packetHeaderLen]) != self.header):
          self.serialConnection.reset_input_buffer()
          invalid += 1
          if (invalid > 10):
            logging.warn('Receiving invalid data')
        else:
          invalid = 0
          privateData = copy.deepcopy(self.rawData[1:9])
          dataValid = True
      self.isReceiving = True

      if (self.isPaused == False):
        for i in range(packets):
          privData = copy.deepcopy(self.rawData[i * (packetSize) + packetHeaderLen:(i + 1) * packetSize])
          unpacked = list(struct.unpack(self.dataFormat, privData))
          
          for i in range(self.nData):
            self.outData[i][:-1] = self.outData[i][1:]
            self.outData[i][-1] = unpacked[i]


