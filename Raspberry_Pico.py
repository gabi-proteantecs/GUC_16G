import json
import logging
import sys
import time

import serial.tools.list_ports

from TestTools.pico_python_library.mpremote import pyboard


class Pico:
    # def __init__(self, scl=19, sda=18, bit_sel=1) -> None:  # 7-bit slave address
    def __init__(self, i2c_address) -> None:  # 7-bit slave address
        self.offset_len = 8
        if i2c_address != "7-bit":
            print("Error : Please change i2c_address_bits to 7-bit !!!")
            return ()

        # self.bit_sel = bit_sel  #  0 :(msb, lsb)  ;  1 : (start_bit, field_size)
        self.pyb = None
        scl = 19
        sda = 18
        # self.pyb = pyboardextended.PyboardExtended('/dev/ttyAMA0') # by GPIO interface
        # self.pyb = pyboardextended.PyboardExtended('/dev/ttyACM0') # by USB  interface

        # Auto-detect and auto-connect to the first available device.
        for p in sorted(serial.tools.list_ports.comports()):
            if str(p).find("USB") != -1:
                try:
                    print(p, flush=True)
                    self.pyb = pyboard.Pyboard(p.device)
                    # self.pyb = pyboardextended.PyboardExtended(p.device)
                    # print(p.device, flush=True)
                    # ports=serial.tools.list_ports.comports()
                    # for port in ports:
                    #     print(f'{port.description}')
                    break
                except pyboard.PyboardError:
                    # except pyboardextended.PyboardError:
                    print("failed to access", flush=True)
                    return
            else:
                pass

        if self.pyb == None:
            print("no device found", flush=True)
            return

        self.pyb.enter_raw_repl()  # soft_reset=True
        self.pyb.exec("from machine import Pin, I2C, freq")
        self.GP25_low()
        self.default_high_pin10()
        self.default_high_pin11()
        self.default_high_pin12()
        self.pyb.exec(
            "i2c = I2C(1, sda=Pin("
            + str(sda)
            + "), scl=Pin("
            # +str(scl)+'), freq=1000_000)') # EY0008A okay
            + str(scl)
            + "), freq=1000_000)"
        )
        self.scan()

    def close(self) -> None:
        self.pyb.close()

    def shutdown(self) -> None:
        if self.pyb:
            self.pyb.exit_raw_repl()
            self.pyb.close()
        sys.exit(1)

    def scan(self) -> list:
        result = self.to_list(self.pyb.eval("i2c.scan()"))
        slave = list(map(hex, result))
        print(f"I2C address 7-bit , i2c slave address scan : {slave}", flush=True)
        self.GP25_high()

    def default_high(self, pin=2) -> None:
        logging.debug("  GPIO default_high")
        self.pyb.exec("Pin(" + str(pin) + ", Pin.IN)")

    def default_high_pin6(self, pin=6) -> None:
        logging.debug("  GPIO default_high")
        self.pyb.exec("Pin(" + str(pin) + ", Pin.IN)")

    def default_high_pin10(self, pin=10) -> None:
        logging.debug("  GPIO default_high")
        self.pyb.exec("Pin(" + str(pin) + ", Pin.IN)")

    def default_high_pin11(self, pin=11) -> None:
        logging.debug("  GPIO default_high")
        self.pyb.exec("Pin(" + str(pin) + ", Pin.IN)")

    def default_high_pin12(self, pin=12) -> None:
        logging.debug("  GPIO default_high")
        self.pyb.exec("Pin(" + str(pin) + ", Pin.IN)")

    def pull_low(self, pin=2) -> None:
        logging.debug("  GPIO pull_low")
        self.pyb.exec("rst = Pin(" + str(pin) + ", Pin.OUT)")
        self.pyb.exec("rst.value(0)")

    def GP25_led(self, pin=25) -> None:
        logging.debug("  GPIO pull_low")
        self.pyb.exec("rst = Pin(" + str(pin) + ", Pin.OUT)")
        self.pyb.exec("rst.value(0)")
        time.sleep(0.1)
        self.pyb.exec("rst = Pin(" + str(pin) + ", Pin.OUT)")
        self.pyb.exec("rst.value(1)")

    def GP25_low(self, pin=25) -> None:
        self.pyb.exec("rst = Pin(" + str(pin) + ", Pin.OUT)")
        self.pyb.exec("rst.value(0)")

    def GP25_high(self, pin=25) -> None:
        self.pyb.exec("rst = Pin(" + str(pin) + ", Pin.OUT)")
        self.pyb.exec("rst.value(1)")

    def GPIO_Set(self, pin, H_L) -> None:
        self.pyb.exec("rst = Pin(" + str(pin) + ", Pin.OUT)")
        self.pyb.exec(f"rst.value({H_L})")  # 0:pull_low , 1:pull_high

    def to_list(self, string) -> list:
        return json.loads(string)

    def apply_bits(self, rd_data, start_bit, field_size, val, bit_size=32) -> int:
        mask = 2**bit_size - 1 - (2**field_size - 1) * (2**start_bit)
        val = min(val, 2 ** (field_size) - 1)
        w = val * 2**start_bit
        return (rd_data & mask) | w

    def get_bits(self, rd_data, start_bit, field_size, bit_size=32) -> int:
        mask = 0
        for i in range(start_bit, start_bit + field_size):
            mask += 1 << i

        mask &= 2**bit_size - 1  # 0xffffffff
        return (rd_data & mask) >> start_bit

    def write_bytes(self, slave, offset, val, bytes=4) -> None:
        self.pyb.exec(
            "i2c.writeto_mem("
            + str(slave)
            + ","
            + str(offset)
            + ","
            + str(val.to_bytes(bytes, "little"))
            + ")"
        )

    def read_bytes(self, slave, offset, bytes=4) -> int:
        result = int(
            self.pyb.eval(
                "int.from_bytes(i2c.readfrom_mem("
                + str(slave)
                + ","
                + str(offset)
                + ","
                + str(bytes)
                + "),'little')"
            )
        )
        return result

    def write(self, slave, offset, start_bit, field_size, val) -> None:
        # print(f'Pico Write' , flush=True)
        # self.GP25_high()
        if (start_bit + field_size > 32) or (field_size < 1):
            raise Exception("Wrong bit length or start bit ...")
        if (start_bit == 0) and (field_size == 32):
            self.write_bytes(slave, offset, val)
        elif (start_bit == 0) and (field_size == 8):
            self.write_bytes(slave, offset, val, 1)
        elif (start_bit == 0) and (field_size == 16):
            self.write_bytes(slave, offset, val, 2)
        elif (start_bit == 0) and (field_size == 24):
            self.write_bytes(slave, offset, val, 3)
        else:
            self.write_bytes(
                slave,
                offset,
                self.apply_bits(
                    self.read_bytes(slave, offset), start_bit, field_size, val
                ),
            )
        # self.GP25_low()

    def read(self, slave, offset, start_bit, field_size) -> hex:
        # print(f'Pico Read' , flush=True)
        # self.GP25_high()
        if (start_bit + field_size > 32) or (field_size < 1):
            raise Exception("Wrong bit length or start bit ...")
        if (start_bit == 0) and (field_size == 32):
            return hex(self.read_bytes(slave, offset))
        elif (start_bit == 0) and (field_size == 8):
            return hex(self.read_bytes(slave, offset, 1))
        elif (start_bit == 0) and (field_size == 16):
            return hex(self.read_bytes(slave, offset, 2))
        elif (start_bit == 0) and (field_size == 24):
            return hex(self.read_bytes(slave, offset, 3))
        else:
            rd_data = self.get_bits(
                self.read_bytes(slave, offset), start_bit, field_size
            )
            return hex(rd_data)
        # self.GP25_low()

    def _rol(self, val, r_bits, max_bits):
        return (val << r_bits % max_bits) & (2**max_bits - 1) | (
            (val & (2**max_bits - 1)) >> (max_bits - (r_bits % max_bits))
        )

    def _ror(self, val, r_bits, max_bits):
        return ((val & (2**max_bits - 1)) >> r_bits % max_bits) | (
            val << (max_bits - (r_bits % max_bits)) & (2**max_bits - 1)
        )

    def _truncate(self, val, num_bits):
        return val & (2**num_bits - 1)

    def pmic(self):
        self.scan()
        mux = 0x20
        self.write(0x71, mux, 0, 8, mux)
        ID = self.read(0x60, 0x20, 0, 8)
        print(ID)
        self.write(0x60, 0x03, 0, 3, 0x07)
        self.write(0x60, 0x0A, 0, 8, 0x00)
        self.write(0x60, 0x02, 6, 2, 0x02)
