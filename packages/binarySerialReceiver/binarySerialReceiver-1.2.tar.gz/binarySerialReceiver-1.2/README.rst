Binary Serial Receiver
======================

Simple module for receiving binary data from a serial port in an asynchronous form. Useful for receiving data from an Arduino or a microcontroller without the need to use strings.

Description
-------------

This modules lets you specify the format of the binary data and the header to be received from a serial port. The module creates a dedicated thread to read de serial port and feed the numpy arrays passed as buffers in a circular forma, always keeping the same length.

Example
-------------

In the example folder there is a script that creates a virtual serial port (works only on linux) allowing you to run test-receiver.py which will print the received data buffer.

An exemple code for an arduino to send data to be read using this module would be the fallowing:


.. code-block:: c

  void loop() {
    uint16_t adc_signal = analogRead(sensorPin);
    long unsigned t_now = micros();

    uint16_t buffer_size = sizeof(uint16_t) + sizeof(long unsigned) + 2;
    byte buf[buffer_size];
    buf[0] = 0xFD;
    memcpy(buf + 1, (byte *)&t_now, sizeof(unsigned long));
    memcpy(buf + 1 + sizeof(unsigned long), (byte *)&adc_vdd, sizeof(uint16_t));
    buf[buffer_size - 1] = '\n';
    Serial.write(buf, buffer_size);
  }

In this case the format for receiving would be 'Lh'. All the possible formats are defined in the `struct package page`_ .

.. _struct package page: https://docs.python.org/3/library/struct.html#format-characters