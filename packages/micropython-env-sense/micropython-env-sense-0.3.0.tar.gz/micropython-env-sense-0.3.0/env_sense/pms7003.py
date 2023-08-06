# The MIT License (MIT)
# https://mit-license.org/
# Thanks to:
# - https://github.com/kevinkk525/pms5003_micropython/blob/master/pms5003.py
# - https://github.com/pkucmus/micropython-pms7003/blob/master/pms7003.py

"""A micropython interface for the PMS7003 sensor"""

import machine
import time

"""Sources:
"""


class PmsSensorException(Exception):
    """
    Implies a problem with sensor communication that is unlikely to re-occur (e.g. serial connection glitch).
    Prevents from returning corrupt measurements.
    """
    pass


START_SEQ = bytes([0x42, 0x4d])
# should be 32 (30 + 2 bytes for start_seq) according to the manual, but is 28 for my sensor
# the first two bytes are the size of the frame, which also say 28, contrary to the manual
FRAME_BYTES = 30


# '.' are replaced with '_' for easier database compability
BYTES_MEANING = {
    1: 'pm1_0cf1',
    2: 'pm2_5cf1',
    3: 'pm10cf1',
    4: 'pm1_0',
    5: 'pm2_5',
    6: 'pm10',
    7: 'n0_3',
    8: 'n0_5',
    9: 'n1_0',
    10: 'n2_5',
    11: 'n5_0',
    12: 'n10',
    }

VALUES = list(BYTES_MEANING.values())

NO_VALUES = len(BYTES_MEANING) + 1


class Pms7003Sensor:
    def __init__(self, uart):
        self.uart = machine.UART(uart, baudrate=9600, bits=8, parity=None, stop=1)

    @staticmethod
    def _assert_byte(byte, expected):
        if byte is None or len(byte) < 1 or ord(byte) != expected:
            return False
        return True

    @staticmethod
    def _format_bytearray(buffer):
        return "".join("0x{:02x} ".format(i) for i in buffer)

    def find_start(self, f):
        START_SEQ = [0x42, 0x4d]
        for i in range(len(f)-1):
            if [f[i], f[i+1]] == START_SEQ:
                return i
        return 0

    # Reading is a matter of sync'ing with what the unit is sending us. Read more than we need and find the
    # frame we need within it
    def _get_frame(self, n=FRAME_BYTES*2):
        count = n
        frame = b''
        while count > 0:
            read_bytes = self.uart.read(count)
            if read_bytes:
                frame += read_bytes
                # print(len(read_bytes), read_bytes)
                count -= len(read_bytes)

        start_index = self.find_start(frame)
        return frame[start_index+2:start_index+FRAME_BYTES]

    def _parse_frame(self, f):
        """
        iterates every second index and glues the H and L bytes together
        :return: raw parsed integer values
        """
        vls = [f[i] << 8 | f[i+1] for i in range(0, len(f), 2)]
        return vls

    def _valid_frame(self, frame, vls):
        _checksum = vls[-1]
        return _checksum == sum(frame[:-2]) + sum(START_SEQ)

    def read(self, ordered=False):
        """
        :return: a dict with measurements or raises Pms7003Exception in case of a problem with connection
        """
        frame = self._get_frame()
        values = self._parse_frame(frame)

        if self._valid_frame(frame, values):
            return {BYTES_MEANING[i]: values[i] for i in range(1, NO_VALUES)}
        else:
            # TODO
            return {BYTES_MEANING[i]: values[i] for i in range(1, NO_VALUES)}
            raise PmsSensorException

    def _send_cmd(self, request, response):
        nr_of_written_bytes = self.uart.write(request)
        if nr_of_written_bytes != len(request):
            raise PmsSensorException('Failed to write to UART')

        if response:
            # time.sleep(1)  # TODO
            buf = self.uart.read(len(response))

            if buf != response:
                print('Warning: unexpected UART response, expecting: {}, getting: {}'.format(
                      Pms7003Sensor._format_bytearray(response), Pms7003Sensor._format_bytearray(buf)))
            # raise PmsSensorException('Wrong UART response, expecting: {}, getting: {}'.format(
            #             Pms7003Sensor._format_bytearray(response), Pms7003Sensor._format_bytearray(buf)))


# From: https://github.com/pkucmus/micropython-pms7003/blob/master/pms7003.py
class PassivePms7003Sensor(Pms7003Sensor):
    """
    More about passive mode here:
    http://github.com/teusH/MySense/blob/master/docs/pms7003.md
    https://patchwork.ozlabs.org/cover/1039261/
    https://joshefin.xyz/air-quality-with-raspberrypi-pms7003-and-java/
    """
    ENTER_PASSIVE_MODE_REQUEST = bytearray(
        [START_SEQ[0], START_SEQ[1], 0xe1, 0x00, 0x00, 0x01, 0x70]
    )
    ENTER_PASSIVE_MODE_RESPONSE = bytearray(
        [START_SEQ[0], START_SEQ[1], 0x00, 0x04, 0xe1, 0x00, 0x01, 0x74]
    )
    ENTER_ACTIVE_MODE_REQUEST = bytearray(
        [START_SEQ[0], START_SEQ[1], 0xe1, 0x00, 0x01, 0x01, 0x71]
    )
    # https://github.com/teusH/MySense/blob/master/docs/pms7003.md
    ENTER_ACTIVE_MODE_RESPONSE = bytearray(
        [START_SEQ[0], START_SEQ[1], 0x00, 0x04, 0xe1, 0x01, 0x01, 0x75]
    )
    SLEEP_REQUEST = bytearray(
        [START_SEQ[0], START_SEQ[1], 0xe4, 0x00, 0x00, 0x01, 0x73]
    )
    SLEEP_RESPONSE = bytearray(
        [START_SEQ[0], START_SEQ[1], 0x00, 0x04, 0xe4, 0x00, 0x01, 0x77]
    )
    # NO response
    WAKEUP_REQUEST = bytearray(
        [START_SEQ[0], START_SEQ[1], 0xe4, 0x00, 0x01, 0x01, 0x74]
    )
    # data as response
    READ_IN_PASSIVE_REQUEST = bytearray(
        [START_SEQ[0], START_SEQ[1], 0xe2, 0x00, 0x00, 0x01, 0x71]
    )

    def __init__(self, uart):
        super().__init__(uart=uart)
        # use passive mode pms7003
        self.wakeup()
        self.passive_mode()

    def active_mode(self):
        self._send_cmd(request=PassivePms7003Sensor.ENTER_ACTIVE_MODE_REQUEST,
                       response=PassivePms7003Sensor.ENTER_ACTIVE_MODE_RESPONSE)

    def passive_mode(self):
        self._send_cmd(request=PassivePms7003Sensor.ENTER_PASSIVE_MODE_REQUEST,
                       response=PassivePms7003Sensor.ENTER_PASSIVE_MODE_RESPONSE)

    def sleep(self):
        self._send_cmd(request=PassivePms7003Sensor.SLEEP_REQUEST,
                       response=PassivePms7003Sensor.SLEEP_RESPONSE)
        time.sleep(1)
        self._send_cmd(request=PassivePms7003Sensor.SLEEP_REQUEST,
                       response=PassivePms7003Sensor.SLEEP_RESPONSE)

    def wakeup(self):
        self._send_cmd(request=PassivePms7003Sensor.WAKEUP_REQUEST, response=None)

    def read(self):
        self._send_cmd(request=PassivePms7003Sensor.READ_IN_PASSIVE_REQUEST, response=None)
        return super().read()
