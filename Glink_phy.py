from tabulate import tabulate
from Raspberry_Pico import *
import time
import numpy as np
import datetime
import logging


class UCIe_2p5D:
    def __init__(self, gui, i2c, jtag):
        self.jtag = jtag
        self.gui = gui
        self.i2c = Pico('7-bit')
        self.pmic_120 = 0x69
        self.DIE = 4
        self.GROUP = 4
        self.SLICE = 8
        self.pi_range = 17
        self.pi_total = 32
        self.pi_range_4UI = 125
        self.vef_num = 64
        self.eye_W_spec = 16
        self.eye_H_spec = 15 # RD shawn and Wayne define
        self.slice_offset = 0x10000
        self.pll_offset_min = int(0x1999)
        self.pll_offset_max =  int(0x2FFF)
        self.slice_offset_min = int(0x3000)
        self.slice_offset_max = int(0x7FFF)
        self.EHOST = [   [0x01, 0x02, 0x03],  # Die0 tport/H/V
                                    [0x01, 0x02, 0x03],  # Die1 tport/H/V
                                    [0x01, 0x02, 0x03]]  # Die3 tport/H/V
        self.GROUP_NUM = {0: 'TPORT', 1: 'H', 2: 'V'}
        self.save_log = 1
    def log_info(self,info,reg_save):
        self.info = info
        if reg_save == True:
            self.save_log=1
        else:
            self.save_log=0
    def resetn(self, **kwargs):
        abp_en = kwargs.get('abp_en', 1)
        if abp_en == 1:
            print(f'all EHOST APB from I2C enable')
            f = open('TestTools/i2c_log.txt', mode='w')
            f.write('\n\n\n< Register Information and sequence >\n')
            f.close()

            # Reset select


            # self.Save_i2cLog(log_name='[Sequence] I2C Indirect Write through EHOST\n')
            for die in [0, 1, 2]:
                # print(f'Die{die}')
                for group in [1, 2]:
                    self.indirect_enable(die, group)
    def die_sel(self, **kwargs):
        die = kwargs.get('die', 0)

        if die == 0:
            setv = 0x01
        elif die == 1:
            setv = 0x02
        else:
            setv = 0x04

        # self.D0_THM_CLK()

        # print('start')
        # w_s = time.perf_counter()
        # for g in range(1000):
        #     self.i2c.write(0x70, setv, 0, 8, setv)
        # w_d =  time.perf_counter()
        # now_w = w_d-w_s
        #
        # r_s = time.perf_counter()
        # for g in range(1000):
        #     self.i2c.read(0x70, setv, 0, 8)
        # r_d =  time.perf_counter()
        # now_r = r_d-r_s


        self.i2c.write(0x70, setv, 0, 8, setv)
        # print(f'Die Select Die{die}')
        if self.save_log == 1:
            self.Save_i2cLog(log_name='[Die_Select] : Die' + str(die) + '\n')
    def non_i2c_write(self, slave, offset, s_bit, b_len, setv, **kwargs):
        self.i2c.write(slave, offset, s_bit, b_len, setv)
    def non_i2c_read(self, slave, offset, s_bit, b_len, **kwargs):
        buffer = self.i2c.read(slave, offset, s_bit, b_len)
        return buffer
    def normal_i2c(self, die, group, offset, s_bit, b_len, w_r, **kwargs):
        setv = kwargs.get('setv', 0)

        self.die_sel(die=die)
        if w_r == 'read':
            buffer = self.i2c.read(self.EHOST[die][group], offset, s_bit, b_len)
            return buffer
        elif w_r == 'write':
            setv = int(setv, 16)
            self.i2c.write(self.EHOST[die][group], offset, s_bit, b_len, setv)
        else:
            print('i2c read/write failed')
    def indirect_enable(self, die, group):
        self.die_sel(die=die)
        self.i2c.write(self.EHOST[die][group], 0x2, 7, 1, 1)  # EHOST_ADDR0: [0x02] Indirect Address 0
        self.i2c.write(self.EHOST[die][group], 0x1, 7, 1, 1)  # EHOST_DISABLE: [0x01] External APB Enable

        content = (f'< Code > I2C write : slave={hex(self.EHOST[die][group])} , offset=0x02 , s_bit=7, b_len=1, (W) value=0x01\n')
        textfile = open("TestTools/i2c_log.txt", "a+")
        textfile.write(content)
        textfile.close()
    def indirect_write(self, slave, address, bit, data, **kwargs):
        top = kwargs.get('top', 0)
        dbg = kwargs.get('dbg', 0)
        slice_num = kwargs.get('slice_num', -1)
        reg_source = kwargs.get('reg_source', '< Code >')

        if self.save_log == 1:
            if slice_num == -1:
                content = (f'{reg_source} Indirect_Write : Slave={hex(slave)} , Offset={hex(address)} , Bit={bit} , (W) Value={hex(data)}\n')
            else:
                offset_skip_slice = address - ((int(self.slice_offset)) * slice_num)
                content = (f'{reg_source} Indirect_Write : Slave={hex(slave)} , Slice{slice_num}_Offset={hex(address)}(Offset={hex(offset_skip_slice)}) , Bit={bit} , (W) Value={hex(data)}\n')
            textfile = open("TestTools/i2c_log.txt", "a+")
            textfile.write(content)
            textfile.close()

        # Start Bit / Bit Leng
        if (bit.strip()).find(':') != -1:
            buffer = bit.split(':')
            s_bit = int(buffer[1])
            b_len =(abs(int(buffer[0]) - int(buffer[1]))+1)
        else:
            s_bit = int(bit)
            b_len = 1

        do_write = 1
        if (top == 1):
            addr_len = 32
            apb_addr = 0x3
            data_len = 32
            apb_wdat = 0x7
            apb_rdat = 0xb
            apb_rwcl = 0xf
            apb_wcmv = 0x1
            apb_rcmv = 0x80
        else:
            addr_len = 32
            # apb_addr = 0x2 # EZ0003A
            apb_addr = 0x1 # EZ0005A
            data_len = 32
            apb_wdat = 0x4
            apb_rdat = 0x8
            apb_rwcl = 0xc
            apb_wcmv = 0x1
            apb_rcmv = 0x2

        if dbg == 1:
            print(f'Write_APB address, I2C write {hex(slave)}, ' f'{hex(apb_addr)}  {addr_len} bit  {hex(apb_addr)}', flush=True)
        self.i2c.write(slave, apb_addr, 0, addr_len, address)  # abp address eHost or Slice function

        if s_bit > 32:
            print(F'no support !! start bit {s_bit} bigger than 32')
            fail_status = 'out range'
            do_write = 0
        else:
            if (s_bit + b_len) > 32:
                print(F'Out boundary write, may ignore {s_bit + b_len - 32} MSB')
                fail_status = 'out boundary'
                b_len_2 = 32 - s_bit
                s_bit_map = s_bit + (address % 4) * 8
                b_len_map = b_len_2
                address_map = address - (address % 4)
            else:
                s_bit_map = s_bit + (address % 4) * 8
                b_len_map = b_len
                address_map = address - (address % 4)

        if s_bit_map + b_len_map > 32:
            write_next = 1
            b_len_map_2 = s_bit_map + b_len_map - 32
            b_len_map = 32 - s_bit_map
            data_2 = int(data / (2 ** b_len_map))
        else:
            write_next = 0
            b_len_map_2 = 0

        if do_write == 1:
            if dbg == 1:
                print(f'Write_APB address, I2C write {hex(slave)}, ' f'{hex(apb_addr)}  {addr_len} bit  {hex(address_map)}', flush=True)
            self.i2c.write(slave, apb_addr, 0, addr_len, address_map)  # abp address EHOST/Slice
            val_ok = 1
            if data >= 2 ** b_len or data < 0:
                aa = 2 ** b_len
                fail_status = 'wrong input value'
                print(fail_status)
                val_ok = 0

            if (val_ok):
                if (s_bit_map == 0) & (b_len_map == 32):
                    if dbg == 1:
                        print(f'Write_APB address, I2C write {hex(slave)}, ' f'{hex(apb_addr)}  {addr_len} bit  {hex(address_map)}', flush=True)
                    self.i2c.write(slave, apb_addr, 0, addr_len, address_map)  # abp address
                    if dbg == 1:
                        print(f'Write_APB data, I2C write {hex(slave)}, ' f'{hex(apb_wdat)}  {data_len} bit  {hex(data)}', flush=True)
                    self.i2c.write(slave, apb_wdat, 0, data_len, data)  # 32bit write
                    if dbg == 1:
                        print(f'Write_APB wcmd, I2C write {hex(slave)}, ' f'{hex(apb_rwcl)}  8 bit  {hex(apb_wcmv)}', flush=True)
                    self.i2c.write(slave, apb_rwcl, 0, 8, apb_wcmv)  # write command
                else:
                    if dbg == 1:
                        print(f'Write_APB rcmd, I2C write {hex(slave)}, ' f'{hex(apb_rwcl)}  8 bit  {hex(apb_rcmv)}', flush=True)
                    self.i2c.write(slave, apb_rwcl, 0, 8, apb_rcmv)  # read command
                    if dbg == 1:
                        print(f'Write_APB read checking', flush=True)
                    # self.indirect_read_chk(slave, top=top)
                    rd_data = int(self.i2c.read(slave, apb_rdat, 0, data_len), 16)
                    if dbg == 1:
                        print(f'Read_APB data , I2C read {hex(slave)}, ' f'{hex(apb_rdat)}  {data_len} bit  {hex(rd_data)}', flush=True)
                    mask = self.i2c._rol((0xffffffff << b_len_map), s_bit_map, 32)  # 32-bit mask
                    rd_data = rd_data & mask  # clear bit-field
                    wr_data = rd_data | (self.i2c._truncate(data, b_len_map) << s_bit_map)  # or bit-field with (data << s_bit)
                    if dbg == 1:
                        print(f'Write_APB data, I2C write {hex(slave)}, ' f'{hex(apb_wdat)}  {data_len} bit  {hex(wr_data)}', flush=True)
                    self.i2c.write(slave, apb_wdat, 0, data_len, wr_data)  # 32bit write
                    if dbg == 1:
                        print(f'Write_APB wcmd, I2C write {hex(slave)}, ' f'{hex(apb_rwcl)}  8 bit  {hex(apb_wcmv)}', flush=True)
                    self.i2c.write(slave, apb_rwcl, 0, 8, apb_wcmv)  # write command
                if dbg == 1:
                    print(f'Write_APB Check ', flush=True)
                # self.indirect_write_chk(slave, top=top)

                if (write_next == 1):
                    self.i2c.write(slave, apb_addr, 0, addr_len, address_map + 4)  # abp address
                    self.i2c.write(slave, apb_rwcl, 0, 8, apb_rcmv)  # read command
                    if dbg == 1:
                        print(f'Read_APB Check ', flush=True)
                    # self.indirect_read_chk(slave, top=top)

                    rd_data = int(self.i2c.read(slave, apb_rdat, 0, data_len), 16)
                    if dbg == 1:
                        print(f'Read_APB data , I2C read {hex(slave)}, ' f'{hex(apb_rdat)}  {data_len} bit  {hex(rd_data)}', flush=True)
                    mask = self.i2c._rol((0xffffffff << b_len_map_2), 0, 32)  # 32-bit mask
                    rd_data = rd_data & mask  # clear bit-field
                    wr_data = rd_data | (self.i2c._truncate(data_2, b_len_map_2) << 0)  # or bit-field with (data << s_bit)
                    if dbg == 1:
                        print(f'Write_APB data2, I2C write {hex(slave)}, ' f'{hex(apb_wdat)}  {data_len} bit  {hex(wr_data)}', flush=True)
                    self.i2c.write(slave, apb_wdat, 0, data_len, wr_data)  # 32bit write
                    if dbg == 1:
                        print(f'Write_APB wcmd2, I2C write {hex(slave)}, ' f'{hex(apb_rwcl)}  8 bit  {hex(apb_wcmv)}', flush=True)
                    self.i2c.write(slave, apb_rwcl, 0, 8, apb_wcmv)  # write command
                    if dbg == 1:
                        print(f'Write_APB Check, ', flush=True)
                    # self.indirect_write_chk(slave, top=top)
    def indirect_read(self, slave, address, bit, **kwargs):  # bit need use string
        top = kwargs.get('top', 0)
        save_i2c_log = kwargs.get('save_i2c_log', 1)
        slice_num = kwargs.get('slice_num', -1)
        reg_source = kwargs.get('reg_source', '< Code >')

        do_read = 1
        if top == 1:
            addr_len = 32
            apb_addr = 0x3
            data_len = 32
            apb_rdat = 0xb
            apb_rwcl = 0xf
            apb_rcmv = 0x80
        else:
            addr_len = 32
            apb_addr = 0x2 # EZ0003A
            apb_addr = 0x1 # EZ0005A
            data_len = 32
            apb_rdat = 0x8
            apb_rwcl = 0xc
            apb_rcmv = 0x2

        # Start Bit / Bit Leng
        if (bit.strip()).find(':') != -1:
            buffer = bit.split(':')
            s_bit = int(buffer[1])
            b_len =(abs(int(buffer[0]) - int(buffer[1]))+1)
        else:
            s_bit = int(bit)
            b_len = 1

        # print('Read_APB,  ', slave_hex, ',', address_hex, ',', s_bit, ',', b_len, flush=True)
        if s_bit > 32:
            print(F'no support !! start bit {s_bit} bigger than 32')
            fail_status = 'out range'
            do_read = 0
        else:
            if (s_bit + b_len) > 32:
                print(F'Out boundary read, may ignore {s_bit + b_len - 32} MSB')
                fail_status = 'out boundary'
                b_len_2 = 32 - s_bit
                s_bit_map = s_bit + (address % 4) * 8
                b_len_map = b_len_2
                address_map = address - (address % 4)
            else:
                s_bit_map = s_bit + (address % 4) * 8
                b_len_map = b_len
                address_map = address - (address % 4)

        if s_bit_map + b_len_map > 32:
            read_next = 1
            b_len_map_2 = s_bit_map + b_len_map - 32
            b_len_map = 32 - s_bit_map
        else:
            read_next = 0
            b_len_map_2 = 0

        if do_read == 1:

            # ccc = self.i2c.read(slave, 0x1, 0, 8)
            self.i2c.write(slave, 0x0, 0, 8, 0x80)
            # gg = self.i2c.read(slave, 0x1, 0, 8)
            self.i2c.write(slave, apb_addr, 0, addr_len, address_map)  # abp address
            # self.i2c.write(slave, 0x1, 0, 8, 0x28)
            # self.i2c.write(slave, 0x2, 0, 8, 0x21)
            # self.i2c.write(slave, 0x3, 0, 8, 0x00)
            self.i2c.write(slave, apb_rwcl, 0, 8, apb_rcmv)  # read command
            # self.indirect_read_chk(slave, top=top)

            rd_data = int(self.i2c.read(slave, apb_rdat, 0, data_len), 16)
            if b_len_map == 0:
                rd_data = 0
            else:
                rd_data = self.i2c._rol(rd_data >> (s_bit_map), 0, b_len_map)

            val = rd_data
            if read_next == 1:
                self.i2c.write(slave, apb_addr, 0, addr_len, address_map + 4)  # abp address
                self.i2c.write(slave, apb_rwcl, 0, 8, apb_rcmv)  # read command
                # self.indirect_read_chk(slave, top=top)

                rd_data_2 = int(self.i2c.read(slave, apb_rdat, 0, data_len), 16)
                if b_len_map_2 == 0:
                    rd_data_2 = 0
                else:
                    rd_data_2 = self.i2c._rol(rd_data_2, 0, b_len_map_2)
                # mask = self.i2c._rol((0xffffffff << b_len_map_2), 0, 32)  # 32-bit mask
                # rd_data_2 = rd_data_2 & mask  # clear bit-field
                val = rd_data_2 * 2 ** b_len_map + rd_data

        if self.save_log == 1:
            if slice_num == -1:
                content = (f'{reg_source} indirect_read : slave={hex(slave)} , offset={hex(address)} , s_bit={bit} , (R) value=0x{val:0{int((b_len - 1) / 4) + 1}x}\n')
            else:
                offset_skip_slice = address - ((int(self.slice_offset)) * slice_num)
                content = (f'{reg_source} indirect_read : slave={hex(slave)} , slice{slice_num}_offset={hex(address)}(offset={hex(offset_skip_slice)}), s_bit={bit} , (R) value=0x{val:0{int((b_len - 1) / 4) + 1}x}\n')
            if save_i2c_log:
                textfile = open("TestTools/i2c_log.txt", "a+")
                textfile.write(content)
                textfile.close()

        # self.i2c.write(0x01, 0xF, 0, 8, 0x80)  # read command
        # self.i2c.write(0x01, 0x3, 0, 32, 0x13004)  # abp address
        # rd_data_2 = int(self.i2c.read(0x01, 0xB, 0, 32), 16)
        # print(rd_data_2)


        return f'0x{val:0{int((b_len - 1) / 4) + 1}x}'
    def indirect_write_chk(self, slave, **kwargs):
        top = kwargs.get('top', 0)
        ck_times = kwargs.get('ck_times', 10)

        if top == 1:
            apb_rwcl = 0x10
            apb_stsb = 0
            apb_stsl = 2
        else:
            apb_rwcl = 0xc
            apb_stsb = 6
            apb_stsl = 1
        for i in range(ck_times):
            result = int(self.i2c.read(slave, apb_rwcl, apb_stsb, apb_stsl), 16)
            if result == 1:
                break
            # time.sleep(0.05)
        if (result != 1):  # ready and no error
            fail_status = "Write APB failed"
            # print(f'\033{self.Prog_module} write to APB failed! -------------------------------------------------------------------------------------------', flush=True)
            # sys.stdout.flush()
    def indirect_read_chk(self, slave, **kwargs):
        top = kwargs.get('top', 0)
        ck_times = kwargs.get('ck_times', 10)

        if top == 1:
            apb_rwcl = 0x10  #
            apb_stsb = 0
            apb_stsl = 2
        else:
            apb_rwcl = 0xc
            apb_stsb = 7
            apb_stsl = 1
        for i in range(ck_times):
            result = int(self.i2c.read(slave, apb_rwcl, apb_stsb, apb_stsl), 16)
            if result == 1:
                break
            # time.sleep(0.05)
        if (result != 1):  # ready and no error, [0] ready [1] error
            fail_status = "Read APB failed"
            # print(f'\033{self.Prog_module} read from APB failed! -------------------------------------------------------------------------------------------', flush=True)
            # sys.stdout.flush()
    def reg_map_set(self, die, group, slices, **kwargs):
        reg_arr = kwargs.get('reg_arr', [])
        r_bk = kwargs.get('r_bk',0)
        show = kwargs.get('show', 0)
        mode = kwargs.get('mode', 'mode')

        self.die_sel(die=die)
        for i in range(len(reg_arr)):
            reg_list = (reg_arr[i]).split(',')
            # print(f'{i}  {reg_list}')
            # if i == 80 :
            #     print('stop')
            slave = (self.EHOST[die][group])
            offset = int(reg_list[0], 16)
            bit = (reg_list[1])
            setv_string = reg_list[2]

            if setv_string.find('Die') != -1:
                my_list = setv_string.split('\n')
                Die_list = ('Die0', 'Die1', 'Die2')
                for d in range(3):
                    if setv_string.find(Die_list[d]) != -1:
                        reg = ([s for s in my_list if Die_list[d] in s])[0]
                        reg = '0x' + ((reg.split('h'))[1])
                        setv = int(reg, 16)
                        self.die_sel(die=d)

                        if offset < int(0x0FFF):
                            self.indirect_write(slave, offset, bit, setv, slice_num=-1, reg_source='< User_Define >')
                        # slice register write
                        else:
                            for s in range(len(slices)):
                                rx_base = slices[s] * self.slice_offset
                                self.indirect_write(slave, offset + rx_base, bit, setv, slice_num=slices[s],  reg_source='< User_Define >')
                                if r_bk == 1:
                                    rbv = self.indirect_read(slave, offset + rx_base, bit, slice_num=slices[s])
                                if show == 1:
                                    print(f'Write offset={offset} set to {setv} for die{die} / group{group} S#{s} ')
                                if r_bk == 1:
                                    print(f'Read offset={offset} register value {rbv} for die{die} / group{group} S#{s} ')
                    else:
                        pass
                    if d ==2:
                        self.die_sel(die=die)


            else:
                if setv_string.find('nan') != -1:
                    pass
                elif setv_string.find('-') != -1:
                    pass
                else:
                    if setv_string.find('M4_D0V_D1V') != -1 or setv_string.find('EW') != -1 :
                        buffer = setv_string.split('\n')
                        if buffer[0].find('M4_D0V_D1V') != -1  or mode == 'M2DIE0_2_FLB_mode' or mode == 'M2DIE2_0_FLB_mode':
                            M4_D0V_D1V = buffer[0]
                            M4_D0V_D1V = buffer[1]
                        else:
                            M4_D0V_D1V = buffer[1]
                            M4_D0V_D1V = buffer[0]
                        if mode == 'M4_D0V_D1V_mode' or mode == 'M2DIE0_2_FLB_mode' or mode == 'M2DIE2_0_FLB_mode':
                            reg = (M4_D0V_D1V.split('='))[1]
                        elif mode == 'M4_D0V_D1V_mode' or mode == 'M2DIE1_2_FLB_mode' or mode == 'M2DIE2_1_FLB_mode':
                            reg = (M4_D0V_D1V.split('='))[1]
                        reg = (reg.split('h'))[1]
                        setv = int(reg, 16)
                    else :
                        setv = int(setv_string, 16)

                    # Top / PLL register write
                    if offset < int(0x0FFF):
                        self.indirect_write(slave, offset, bit, setv, slice_num=-1, reg_source='< User_Define >')
                    # slice register write
                    else:
                        for s in range(len(slices)):
                            rx_base = slices[s] * self.slice_offset
                            self.indirect_write(slave, offset + rx_base, bit, setv, slice_num=slices[s],  reg_source='< User_Define >')
                            if r_bk == 1:
                                rbv = self.indirect_read(slave, offset + rx_base, bit, slice_num=slices[s])
                            if show == 1:
                                print(f'Write offset={offset} set to {setv} for die{die} / group{group} S#{s} ')
                            if r_bk == 1:
                                print(f'Read offset={offset} register value {rbv} for die{die} / group{group} S#{s} ')
    def reg_user_set(self, **kwargs):
        reg_arr = kwargs.get('reg_arr', [])
        mode = kwargs.get('mode', 'mode')
        show = kwargs.get('show', 1)
        gui_die_sel = kwargs.get('gui_die_sel', 1)
        gui_group_num = kwargs.get('gui_group_num', 1)
        gui_slice_num = kwargs.get('gui_slice_num', 1)
        die_arr = kwargs.get('die_arr', [0,1,2,3])
        group_arr = kwargs.get('group_arr', [0,1,2,3])
        tx_slice = kwargs.get('tx_slice', [0,1,2,3])
        rx_slice = kwargs.get('rx_slice', [0,1,2,3])


        for i in range(len(reg_arr)):
            reg_list = (reg_arr[i]).split(',')
            offset = int(reg_list[0], 16)
            bit = (reg_list[1]).strip()
            if (reg_list[2]).strip() =='nan':
                pass
            else:
                setv = int((reg_list[2]).strip(), 16)
            edit_log = reg_list[3]
            TPORT = (reg_list[4]).strip()
            write_en = (reg_list[5]).strip()
            read_en = (reg_list[6]).strip()
            die_list = (reg_list[7]).split('/')
            V_list = (reg_list[8]).split('/')
            slice_list = (reg_list[9]).split('/')


            rd_value = 'na'
            if write_en.find('nan') ==-1 or read_en.find('nan') ==-1 :
                if mode == 'gui_tree':
                    die_list= [gui_die_sel]
                    if gui_group_num == 'TPORT':
                        V_list = [0]
                    elif gui_group_num == 'H':
                        V_list = [1]
                    elif gui_group_num == 'V':
                        V_list = [2]
                    else:
                        pass
                    slice_list=[gui_slice_num]
                else:
                    die_list = list(map(int, die_list))
                    V_list = list(map(int, V_list))
                    slice_list = list(map(int, slice_list))
                    if mode == 'USER_mode' or offset == 16: # reg=0x10 only init Die1 V and H
                        die_list = list(map(int, die_list))
                        V_list = list(map(int, V_list))
                        slice_list = list(map(int, slice_list))
                    else:
                        die_list = die_arr
                        V_list = group_arr
                        slice_list = slice

            for s in range(len(die_list)) :
                # print(s,flush=True)
                die = die_list[s]
                self.die_sel(die=die)
                if mode == 'USER_mode' or offset == 16 or mode == 'gui_tree' :  # reg=0x10 only init Die1 V and H
                    pass
                else:
                    slice_list = tx_slice if s == 0 else rx_slice
                if len(V_list) == 1:
                    group = V_list[0]
                else:
                    group = V_list[0] if s== 0 else V_list[1]

                # TPORT reigster set
                if TPORT.find('nan') == -1:
                    slave = (self.EHOST[die][0])
                    info = f'Die{die}'
                    if write_en.find('nan') == -1:
                        self.indirect_write(slave, offset, bit, setv, slice_num=-1, top=1, reg_source='< User_Define >')
                        if show  == 1 and edit_log.find('nan') == -1:
                            print(f'({edit_log} {info} ) Indirect Write , offset={hex(offset)} [{bit}] , Register Value={hex(setv)}')
                    else:
                        pass
                    if read_en.find('nan') == -1:
                        rd_value = self.indirect_read(slave, offset, bit, slice_num=-1, top=1, reg_source='< User_Define >')
                        if show  == 1 and edit_log.find('nan') == -1:
                            print(f'({edit_log} {info} ) Indirect Read , offset={hex(offset)} [{bit}] , Register Value={(rd_value)}')
                    else:
                        pass
                # pll/slice register write
                else:
                    # pll register write
                    if self.pll_offset_min <= int(offset) < self.pll_offset_max:
                        if group == 0:
                            v_name = 'TPORT'
                        elif group ==1:
                            v_name = 'H'
                        elif group ==2:
                            v_name = 'V'
                        else:
                            v_name = 'failed'
                        slave = (self.EHOST[die][group])
                        info = f'Die{die} {v_name}'
                        if write_en.find('nan') == -1:
                            self.indirect_write(slave, offset, bit, setv, slice_num=-1, reg_source='< User_Define >')
                            rd_value = self.indirect_read(slave, offset, bit, slice_num=-1, reg_source='< User_Define >')
                            if show  == 1 and edit_log.find('nan') == -1:
                                print(f'({edit_log} {info} ) Indirect Write , offset={hex(offset)} [{bit}] , Register Value={hex(setv)}')
                        elif read_en.find('nan') == -1:
                            rd_value = self.indirect_read(slave, offset, bit, slice_num=-1, reg_source='< User_Define >')
                            if show  == 1 and edit_log.find('nan') == -1:
                                print(f'({edit_log} {info} ) Indirect Read , offset={hex(offset)} [{bit}] , Register Value={(rd_value)}')
                        else:
                            pass
                    # slice register write
                    else:
                        if group == 0:
                            v_name = 'TPORT'
                        elif group ==1:
                            v_name = 'H'
                        elif group ==2:
                            v_name = 'V'
                        else:
                            v_name = 'failed'
                        for s in range(len(slice_list)):
                            slice_num = int(slice_list[s])
                            base = slice_num * self.slice_offset
                            slave = (self.EHOST[die][group])
                            info = f'Die{die} {v_name}'
                            if write_en.find('nan') == -1:
                                if offset == 16 and bit == '10': # rg0010_start_link_training
                                    self.die_sel(die=1)
                                    self.indirect_write(0x2, offset + base, bit, setv, slice_num=slice_num, reg_source='< User_Define >')
                                    self.indirect_write(0x3, offset + base, bit, setv, slice_num=slice_num, reg_source='< User_Define >')
                                else:
                                    self.indirect_write(slave, offset + base, bit, setv, slice_num=slice_num,  reg_source='< User_Define >')
                                if show  == 1 and edit_log.find('nan') == -1:
                                    print(f'({edit_log} {info} ) Indirect Write = offset={hex(offset)} [{bit}] , Register Value={hex(setv)}')
                            else:
                                pass
                            if read_en.find('nan') == -1:
                                rd_value = self.indirect_read(slave, offset + base, bit, slice_num=slice_num,  reg_source='< User_Define >')
                                if show  == 1 and edit_log.find('nan') == -1:
                                    print(f'({edit_log} {info} ) Indirect Read , offset={hex(offset + base)} [{bit}] , Register Value={(rd_value)} Slice Number={slice_num}')
                            else:
                                pass
                        else:
                            pass
            else:
                pass
        return rd_value
    def check_vco(self, die, group, group_name, **kwargs):
        check_vco = kwargs.get('check_vco', 1)

        self.die_sel(die=die)
        if check_vco == 1:
            vco = self.indirect_read(self.EHOST[die][group], 0x2158, '9:4', slice_num=-1)  # vco
            lol_0x2154 = self.indirect_read(self.EHOST[die][group], 0x2154, '0', slice_num=-1)  # lol
            lol_0x2150 = self.indirect_read(self.EHOST[die][group], 0x2150, '0', slice_num=-1)  # lol

            if int(lol_0x2154, 16) == 1 or int(vco, 16) ==  63 or int(vco, 16) == 0:
                print(F'\033die{die} group{group_name} : vco = {vco} , lol(0x2154) = {lol_0x2154} , lol(0x2150) = {lol_0x2150} , PLL UnLock Failed', flush=True) # PLL Unlock
                LOL=1
            else:
                print(F'\034die{die} group{group_name} : vco = {vco} , lol(0x2154) = {lol_0x2154} , lol(0x2150) = {lol_0x2150} , PLL Lock Pass', flush=True) # PLL Lock
            LOL=0
        return LOL
    def check_msd_lol(self):
        for i in range(3):
            mux_arr = [0x20, 0x40, 0x80]
            self.i2c.write(0x71, mux_arr[i], 0, 8, mux_arr[i]) # U142 i2c mux switch

            lol = self.i2c.read(0x50, 0xC, 0, 8)

            if int(lol, 16) != 1:
                print(f'\033die{i} MSD_lol={lol}, PLL UnLock Failed', flush=True)  # PLL Unlock
            else:
                print(f'\034die{i} MSD_lol={lol}, PLL Lock PASS', flush=True)  # PLL Lock
    def cfg_pre_div_sel(self, die, group, slices, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', 1)
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 1)

        ftn_name = 'cfg_pre_div_sel'
        if 'int' in str(type(slices)):
            slices = [slices]
        slave = self.EHOST[die][group]
        address = 0x114
        bit = '1:0'

        self.die_sel(die=die)
        rbvs = []
        for slice_n in slices:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, address + base, bit, 0x00, slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, address + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{slices} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{slices} = {rbvs}')

        return rbvs[0]
    def Save_i2cLog(self, **kargs):
        content = kargs.get('log_name', 'NA')

        textfile = open("TestTools/i2c_log.txt", "a+")
        textfile.write(content)
        textfile.close()
    def pico_gpio_low(self, pin, H_L): # gpio number , 0:pull low 1:pull high
        self.i2c.GPIO_Set(pin, H_L)
    def set_input_pin6(self):
        self.i2c.default_high_pin6()
    def msd_function_en(self):
        for i in range(3):
            mux_arr = [0x20, 0x40, 0x80]

            self.i2c.write(0x71, mux_arr[i], 0, 8, mux_arr[i]) # U142 i2c mux switch
            self.i2c.write(0x50, 0xA, 0, 8, 0x0)
            self.i2c.write(0x50, 0xB, 0, 8, 0x0)
            self.i2c.write(0x50, 0xE, 0, 8, 0xA)
            self.i2c.write(0x50, 0x10, 0, 16, 0x3F)
            self.i2c.write(0x50, 0xA, 0, 8, 0x1)
            self.i2c.write(0x50, 0xB, 0, 8, 0x2)
    def train_result(self, die, group, group_name, **kwargs):
        self.die_sel(die=die)
        slave = self.EHOST[die][group]
        slice = kwargs.get('slice', [0,1,2,3])

        rbvs_eye = []
        rbvs_val1 = []
        rbvs_val2 = []
        rbvs_val3 = []
        rbvs_val4 = []
        for slice_n in slice:
            base_addr = slice_n * self.slice_offset
            die_info = f'Die{die}{group_name}'

            self.read_train_value(slave, base_addr)
            if int(self.mbt_pass,16) == 255 or int(self.mbt_pass,16) == 223:
                self.mbt_pass_fail=''
            else:
                print(f'\033MBT Register = {self.mbt_pass}, MBT Failed', flush=True)
                self.mbt_pass_fail = 'MBT Failed'


            buffer_w = buffer_h = slice_note = ''
            if  self.mbt_pass_fail != 'MBT Failed':
                pass_fail = 'Pass'
                if (self.eye_W_spec - self.win_size) > 0 :
                    buffer_w = 'Eye Width Worst'
                if (self.eye_H_spec - self.vref_size) > 0 :
                    buffer_h = 'Eye Height Worst'
                slice_note = f'/{buffer_w}/{buffer_h}/'
            else:
                pass_fail = 'Failed'
                if (self.eye_W_spec - self.win_size) > 0 :
                    buffer_w = 'Eye Width Worst'
                if (self.eye_H_spec - self.vref_size) > 0 :
                    buffer_h = 'Eye Height Worst'
                slice_note = f'/{self.mbt_pass_fail}/{buffer_w}/{buffer_h}/'

            rbv = [die_info,str(slice_n),'NA',self.win_left,self.win_right,self.center_phase,str(self.win_size),self.win_p,self.vref_left,self.vref_right,self.vref_center,str(self.vref_size),self.vref_p,self.mbt_pass, slice_note]
            rbvs_eye.append(rbv)
            headers0 = ['Die','Slice', 'T_F', 'w_l', 'w_r', 'w_c', 'w_s', 'W(%)','v_l', 'v_h', 'v_c', 'v_s', 'H(%)','MBT_Pass(HEX)','Note']
            headers0 = headers0 + []

            self.read_deskew_tx(slave, base_addr)
            rbv1 = [die_info,str(slice_n),'NA',
                        self.cfg_deskew_sel_txd00_03, self.cfg_deskew_sel_txd04_07, self.cfg_deskew_sel_txd08_11, self.cfg_deskew_sel_txd12_15,
                        self.cfg_deskew_sel_txd16_19, self.cfg_deskew_sel_txd20_23, self.cfg_deskew_sel_txd24_27, self.cfg_deskew_sel_txd28_31
                        ]
            u,indices = np.unique(np.array(rbv1), return_index=True)
            if len(u) != len(rbv1):
                deskew_res = 'Failed'
            else:
                deskew_res = 'Pass'
            rbv1 = [die_info,str(slice_n),deskew_res,
                        self.cfg_deskew_sel_txd00_03, self.cfg_deskew_sel_txd04_07, self.cfg_deskew_sel_txd08_11, self.cfg_deskew_sel_txd12_15,
                        self.cfg_deskew_sel_txd16_19, self.cfg_deskew_sel_txd20_23, self.cfg_deskew_sel_txd24_27, self.cfg_deskew_sel_txd28_31
                        ]
            rbvs_val1.append(rbv1)
            headers1 = ['Die','Slice', 'T_F',
                                'D00 TO D03 ', 'D04 TO D07 ', 'D08 TO D11 ', 'D12 TO D15 ',
                                'D16 TO D19 ', 'D20 TO D23 ', 'D24 TO D27 ', 'D28 TO D31 '
                                ]

            headers1 = headers1 + []
            rbv2 = [die_info,str(slice_n),'NA',
                        self.cfg_deskew_sel_txd32_35, self.cfg_deskew_sel_txd36_39, self.cfg_deskew_sel_txd40_43, self.cfg_deskew_sel_txd44_47,
                        self.cfg_deskew_sel_txd48_51, self.cfg_deskew_sel_txd52_55, self.cfg_deskew_sel_txd56_59, self.cfg_deskew_sel_txd60_63
                        ]
            u,indices = np.unique(np.array(rbv2), return_index=True)
            if len(u) != len(rbv2):
                deskew_res = 'Failed'
            else:
                deskew_res = 'Pass'
            rbv2 = [die_info,str(slice_n),deskew_res,
                        self.cfg_deskew_sel_txd32_35, self.cfg_deskew_sel_txd36_39, self.cfg_deskew_sel_txd40_43, self.cfg_deskew_sel_txd44_47,
                        self.cfg_deskew_sel_txd48_51, self.cfg_deskew_sel_txd52_55, self.cfg_deskew_sel_txd56_59, self.cfg_deskew_sel_txd60_63
                        ]
            rbvs_val2.append(rbv2)
            headers2 = ['Die','Slice', 'T_F',
                                'D32 TO D35 ', 'D36 TO D39 ', 'D40 TO D43 ', 'D44 TO D47 ',
                                'D48 TO D51 ', 'D52 TO D55 ', 'D56 TO D59 ', 'D60 TO D63 '
                                ]
            headers2 = headers2 + []

            self.read_offset_rx(slave, base_addr)
            rbv3 = [die_info,str(slice_n),'NA',
                        self.cfg_rx_ofs_rxd00_07, self.cfg_rx_ofs_rxd08_15, self.cfg_rx_ofs_rxd16_23, self.cfg_rx_ofs_rxd24_31,
                        self.cfg_rx_ofs_rxd32_39, self.cfg_rx_ofs_rxd40_47, self.cfg_rx_ofs_rxd48_55, self.cfg_rx_ofs_rxd56_63
                        ]
            rbvs_val3.append(rbv3)
            headers3 = ['Die','Slice', 'T_F',
                                'D00 TO D07 ', 'D08 TO D15 ', 'D16 TO D23 ', 'D24 TO D31 ',
                                'D32 TO D39 ', 'D40 TO D47 ', 'D48 TO D55 ', 'D56 TO D63 '
                                ]
            headers3 = headers3 + []

            # dvs / dck / cck / rx_pi
            self.read_dvs_dck_cck_rx_pi(slave, base_addr)
            rbv4 =  [die_info,str(slice_n),'NA',
                        self.rpt_dvs_pi_vld, self.rpt_dvs_pi_code, self.dck_rpt_phase_vld, self.dck_rpt_code_i,
                        self.cck_rpt_phase_vld, self.cck_rpt_code_i, self.rpt_rx_pi_vld, self.rpt_rx_pi_code
                        ]
            rbvs_val4.append(rbv4)
            headers4 = ['Die','Slice', 'T_F',
                                '  dvs_pi   ', 'dvs_pi_code', ' dck_phase ', ' dck_code_i',
                                ' cck_phase ', ' cck_code_i', '   rx_pi   ', ' rx_pi_code'
                                ]
            headers4 = headers4 + []

        # creat txt table
        print(f'Eye Width Specification : {self.eye_W_spec} < Test Value < {self.pi_total} , PI Range={self.pi_total}')
        print(f'Eye Height Specification : {self.eye_H_spec} < Test Value < {self.vef_num} , PI Range={self.vef_num}')
        from prettytable import PrettyTable
        print('Test Result : Eye Size Value')
        myTable = PrettyTable(headers0)
        for r in range(len(rbvs_eye)):
            myTable.add_row(rbvs_eye[r])
        print(myTable)

        print('Read Register : Chip dvs / dck / cck / rx_pi')
        myTable = PrettyTable(headers4)
        for r in range(len(rbvs_val4)):
            myTable.add_row(rbvs_val4[r])
        print(myTable)

        log_type = 'User'
        if log_type == 'RD':
            print('Read Register : Chip Cfg_Deskew_Sel_TX D00 TO D31')
            myTable = PrettyTable(headers1)
            for r in range(len(rbvs_val1)):
                myTable.add_row(rbvs_val1[r])
            print(myTable)

            print('Read Register : Chip Cfg_Deskew_Sel_TX D32 TO D63')
            myTable = PrettyTable(headers2)
            for r in range(len(rbvs_val2)):
                myTable.add_row(rbvs_val2[r])
            print(myTable)

            print('Read Register : Chip Cfg_RX_Ofsset_Rx =D00 TO D63')
            myTable = PrettyTable(headers3)
            for r in range(len(rbvs_val3)):
                myTable.add_row(rbvs_val3[r])
            print(myTable)

        return rbvs_eye
    def train_width(self, die, group, group_name, **kwargs):
        txt_arr = kwargs.get('txt_arr', [])
        vref_start = kwargs.get('vref_start', 'Default Value')
        slice = kwargs.get('slice', [0,1,2,3])

        self.die_sel(die=die)
        slave = self.EHOST[die][group]

        print(f'( Note : 1:Bit Error / 0:Bit Pass / C:Center Point Pass / X : Not Test)')
        for slice_n in slice:
            base_addr = slice_n * self.slice_offset
            self.read_train_sweep0_1(slave, base_addr)
            print(f'Die{die}{group_name}_Group{group_name}_Slice{slice_n} RX Diagram Vref_Start={vref_start} : (HEX : rx_sweep0/1={self.eye_rx_sweep0_hex}H/{self.eye_rx_sweep1_hex}H) Bin={self.sweep_result_bin}(MBT Value={self.mbt_pass})')

            # self.rg_half_window(die, group, setv='0x3f')
            # self.read_train_sweep0_1_2_3(slave, base_addr)
            # print('\n\nCheck Sweep 0 To 3 ')
            # print(f'Die{die}{group_name}_Group{group_name}_Slice{slice_n} RX Diagram Vref_Start={vref_start} : (HEX : rx_sweep0/1={self.eye_rx_sweep0_hex}H/{self.eye_rx_sweep1_hex}H/{self.eye_rx_sweep2_hex}H/{self.eye_rx_sweep3_hex}H) Bin={self.sweep_result_bin}(MBT Value={self.mbt_pass})')

            buffer = (f'{self.sweep_result_bin}')
            path = f'TestTools/{txt_arr[slice_n]}'
            textfile = open(path, "a+")
            textfile.write(buffer)
            textfile.close()
            path = f'TestTools/{txt_arr[slice_n]}'
            textfile = open(path, "a+")
            textfile.write('\n')
            textfile.close()
    def train_center_2D(self, die, group, group_name, **kwargs):
        vref_start = kwargs.get('vref_start', 'Default Value')
        slice = kwargs.get('slice', [0,1,2,3])

        self.die_sel(die=die)
        slave = self.EHOST[die][group]

        # 2D center vref eye daigram
        print(f'( Note : 1:Bit Error / 0:Bit Pass / C:Center Point Pass / X : Not Test)')
        for slice_n in slice:
            base_addr = slice_n * self.slice_offset

            self.read_train_sweep0_1(slave, base_addr)
            self.read_train_value(slave, base_addr)

            print(f'\nDie{die}{group_name}_Group{group_name}_Slice{slice_n} RX Diagram Vref_Start={vref_start}')

            center_log=[]
            for d in range(self.pi_total):
                if d == int(self.center_phase):
                    buffer = '0'
                else:
                    buffer = 'x'
                center_log += [buffer]
            center_log_str = ''.join(map(str,center_log))
            for v in range(self.vef_num):
                if int(self.vref_left) < v < int(self.vref_right):
                    if v == int(self.vref_center):
                        print(f'{self.sweep_result_bin}')
                    else:
                        print(center_log_str)
                else:
                    print(self.sweep_result_bin_vref_fail)
    def read_train_sweep0_1(self, slave,base_addr):
        self.mbt_pass = str(self.indirect_read(slave, 0x332c + base_addr, '7:0', slice_num=-1))

        self.eye_rx_sweep0_hex = self.indirect_read(slave, 0x3304 + base_addr, '31:0', slice_num=-1)  # eye_rx_sweep0
        eye_rx_sweep0 = bin(int(self.eye_rx_sweep0_hex, 16))  # eye_rx_sweep0
        # eye_rx_sweep0 = str(eye_rx_sweep0).zfill(self.pi_range)
        eye_rx_sweep0 = eye_rx_sweep0.replace('0b', '')[::-1]
        self.eye_rx_sweep0 = ((eye_rx_sweep0.replace('1', '9')).replace('0', '1')).replace('9', '0')

        self.eye_rx_sweep1_hex = self.indirect_read(slave, 0x3308 + base_addr, '31:0', slice_num=-1)  # eye_rx_sweep1
        eye_rx_sweep1 = bin(int(self.eye_rx_sweep1_hex, 16))  # eye_rx_sweep1
        # eye_rx_sweep1 = str(eye_rx_sweep1).zfill(self.pi_range)
        eye_rx_sweep1 = eye_rx_sweep1.replace('0b', '')[::-1]
        self.eye_rx_sweep1 = ((eye_rx_sweep1.replace('1', '9')).replace('0', '1')).replace('9', '0')

        if int(self.mbt_pass, 16) != 255:
            self.eye_rx_sweep0_hex = self.eye_rx_sweep1_hex = '0xFFFF'
            self.eye_rx_sweep0 = '?????????????????????????????????'
            self.eye_rx_sweep1 = '????????????????????????????????'

        sweep_len = len(self.eye_rx_sweep0 + self.eye_rx_sweep1)
        add_1 = ['', '1', '11', '111', '1111', '11111','111111','11111']
        add_1 = self.pi_total - sweep_len
        rbvs = []
        for a in range(add_1):
            rbv = '1'
            rbvs.append(rbv)
        rbvs_str = ''.join(rbvs)
        self.sweep_result_bin = f'{self.eye_rx_sweep0 + self.eye_rx_sweep1}{rbvs_str}'

        # set center point
        self.center_phase = int(self.indirect_read(slave, 0x3314 + base_addr, '6:0', slice_num=-1), 16)
        self.sweep_result_bin = self.sweep_result_bin[:self.center_phase] + 'C' + self.sweep_result_bin[self.center_phase + 1:]
        self.sweep_result_bin_vref_fail = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.sweep_result_bin_vref_fail = self.sweep_result_bin_vref_fail[:self.center_phase] + '1' + self.sweep_result_bin_vref_fail[self.center_phase + 1:]
    def read_train_sweep0_1_2_3(self, slave,base_addr):
        self.mbt_pass = str(self.indirect_read(slave, 0x332c + base_addr, '7:0', slice_num=-1))

        self.eye_rx_sweep0_hex = self.indirect_read(slave, 0x3304 + base_addr, '31:0', slice_num=-1)  # eye_rx_sweep0
        eye_rx_sweep0 = int(self.eye_rx_sweep0_hex, 16)  # eye_rx_sweep0
        eye_rx_sweep0 = (((str((bin(eye_rx_sweep0)).zfill(self.pi_range))).replace('0b', ''))[::-1])
        self.eye_rx_sweep0 = ((eye_rx_sweep0.replace('1', '9')).replace('0', '1')).replace('9', '0')

        self.eye_rx_sweep1_hex = self.indirect_read(slave, 0x3308 + base_addr, '31:0', slice_num=-1)  # eye_rx_sweep1
        eye_rx_sweep1 = int(self.eye_rx_sweep1_hex, 16)  # eye_rx_sweep1
        eye_rx_sweep1 = (((str((bin(eye_rx_sweep1)).zfill(self.pi_range))).replace('0b', ''))[::-1])
        self.eye_rx_sweep1 = ((eye_rx_sweep1.replace('1', '9')).replace('0', '1')).replace('9', '0')

        self.eye_rx_sweep2_hex = self.indirect_read(slave, 0x330C + base_addr, '31:0', slice_num=-1)  # eye_rx_sweep2
        eye_rx_sweep2 = int(self.eye_rx_sweep2_hex, 16)  # eye_rx_sweep1
        eye_rx_sweep2 = (((str((bin(eye_rx_sweep2)).zfill(self.pi_range))).replace('0b', ''))[::-1])
        self.eye_rx_sweep2 = ((eye_rx_sweep2.replace('1', '9')).replace('0', '1')).replace('9', '0')

        self.eye_rx_sweep3_hex = self.indirect_read(slave, 0x3310 + base_addr, '31:0', slice_num=-1)  # eye_rx_sweep3
        eye_rx_sweep3 = int(self.eye_rx_sweep3_hex, 16)  # eye_rx_sweep1
        eye_rx_sweep3 = (((str((bin(eye_rx_sweep3)).zfill(self.pi_range))).replace('0b', ''))[::-1])
        self.eye_rx_sweep3 = ((eye_rx_sweep3.replace('1', '9')).replace('0', '1')).replace('9', '0')

        if int(self.mbt_pass, 16) != 255:
            self.eye_rx_sweep0_hex = self.eye_rx_sweep1_hex = self.eye_rx_sweep2_hex = self.eye_rx_sweep3_hex = '0xFFFFFFFF'
            self.eye_rx_sweep0 = '????????????????????????????????'
            self.eye_rx_sweep1 = '???????????????????????????????'
            self.eye_rx_sweep2 = '???????????????????????????????'
            self.eye_rx_sweep3 = '???????????????????????????????'

        sweep_len = len(self.eye_rx_sweep0 + self.eye_rx_sweep1+self.eye_rx_sweep2+self.eye_rx_sweep3)
        if self.pi_range_4UI - sweep_len == 0:
            self.sweep_result_bin = f'{self.eye_rx_sweep0 + self.eye_rx_sweep1 + self.eye_rx_sweep2 + self.eye_rx_sweep3}'
        elif self.pi_range_4UI - sweep_len == 1:
            self.sweep_result_bin = f'{self.eye_rx_sweep0 + self.eye_rx_sweep1 + self.eye_rx_sweep2 + self.eye_rx_sweep3}1'
        elif self.pi_range_4UI - sweep_len == 2:
            self.sweep_result_bin = f'{self.eye_rx_sweep0 + self.eye_rx_sweep1 + self.eye_rx_sweep2 + self.eye_rx_sweep3}11'
        elif self.pi_range_4UI - sweep_len == 3:
            self.sweep_result_bin = f'{self.eye_rx_sweep0 + self.eye_rx_sweep1 + self.eye_rx_sweep2 + self.eye_rx_sweep3}111'
        elif self.pi_range_4UI - sweep_len == 4:
            self.sweep_result_bin = f'{self.eye_rx_sweep0 + self.eye_rx_sweep1 + self.eye_rx_sweep2 + self.eye_rx_sweep3}1111'
        else:
            print('Eye width result failed')

        # set center point
        self.center_phase = int(self.indirect_read(slave, 0x3314 + base_addr, '6:0', slice_num=-1), 16)
        self.sweep_result_bin = self.sweep_result_bin[:self.center_phase] + 'C' + self.sweep_result_bin[self.center_phase + 1:]
        self.sweep_result_bin_vref_fail = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.sweep_result_bin_vref_fail = self.sweep_result_bin_vref_fail[:self.center_phase] + '1' + self.sweep_result_bin_vref_fail[self.center_phase + 1:]
    def read_train_value(self, slave,base_addr):
        self.mbt_pass = str(self.indirect_read(slave, 0x332c + base_addr, '7:0', slice_num=-1))
        self.center_phase = str(int(self.indirect_read(slave, 0x3314 + base_addr, '6:0', slice_num=-1), 16))
        self.win_left = str(int(self.indirect_read(slave, 0x3314 + base_addr, '14:8', slice_num=-1), 16))
        self.win_right = str(int(self.indirect_read(slave, 0x3314 + base_addr, '22:16', slice_num=-1), 16))
        self.win_size = (int(self.indirect_read(slave, 0x3314 + base_addr, '30:24', slice_num=-1), 16))
        self.vref_center = str(int(self.indirect_read(slave, 0x32e4 + base_addr, '7:2', slice_num=-1), 16))
        self.vref_left = str(int(self.indirect_read(slave, 0x32e4 + base_addr, '13:8', slice_num=-1), 16))
        self.vref_right = str(int(self.indirect_read(slave, 0x32e4 + base_addr, '21:16', slice_num=-1), 16))
        self.vref_size = (int(self.indirect_read(slave, 0x32e4 + base_addr, '29:24', slice_num=-1), 16))
        self.deskew_tx = str(self.indirect_read(slave, 0x3464 + base_addr, '31:0', slice_num=-1))
        self.offset_rx = str(self.indirect_read(slave, 0x34B4 + base_addr, '31:0', slice_num=-1))
        self.win_p = (str((self.win_size / self.pi_total) * 100))[0:4]
        self.vref_p = (str((self.vref_size / self.vef_num) * 100))[0:4]
    def read_deskew_tx(self, slave,base_addr):
        self.cfg_deskew_sel_txd00_03 = str(self.indirect_read(slave, 0x3464 + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd04_07 = str(self.indirect_read(slave, 0x3468 + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd08_11 = str(self.indirect_read(slave, 0x346C + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd12_15 = str(self.indirect_read(slave, 0x3470 + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd16_19 = str(self.indirect_read(slave, 0x3474 + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd20_23 = str(self.indirect_read(slave, 0x3478 + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd24_27 = str(self.indirect_read(slave, 0x347C + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd28_31 = str(self.indirect_read(slave, 0x3480 + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd32_35 = str(self.indirect_read(slave, 0x3484 + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd36_39 = str(self.indirect_read(slave, 0x3488 + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd40_43 = str(self.indirect_read(slave, 0x348C + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd44_47 = str(self.indirect_read(slave, 0x3490 + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd48_51 = str(self.indirect_read(slave, 0x3494 + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd52_55 = str(self.indirect_read(slave, 0x3498 + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd56_59 = str(self.indirect_read(slave, 0x349C + base_addr, '31:0', slice_num=-1))
        self.cfg_deskew_sel_txd60_63 = str(self.indirect_read(slave, 0x34A0 + base_addr, '31:0', slice_num=-1))
    def read_offset_rx(self, slave,base_addr):
        self.cfg_rx_ofs_rxd00_07 = str(self.indirect_read(slave, 0x34B4 + base_addr, '31:0', slice_num=-1))
        self.cfg_rx_ofs_rxd08_15 = str(self.indirect_read(slave, 0x34B8+ base_addr, '31:0', slice_num=-1))
        self.cfg_rx_ofs_rxd16_23 = str(self.indirect_read(slave, 0x34BC+ base_addr, '31:0', slice_num=-1))
        self.cfg_rx_ofs_rxd24_31 = str(self.indirect_read(slave, 0x34C0+ base_addr, '31:0', slice_num=-1))
        self.cfg_rx_ofs_rxd32_39 = str(self.indirect_read(slave, 0x34C4+ base_addr, '31:0', slice_num=-1))
        self.cfg_rx_ofs_rxd40_47 = str(self.indirect_read(slave, 0x34C8+ base_addr, '31:0', slice_num=-1))
        self.cfg_rx_ofs_rxd48_55 = str(self.indirect_read(slave, 0x34CC+ base_addr, '31:0', slice_num=-1))
        self.cfg_rx_ofs_rxd56_63 = str(self.indirect_read(slave, 0x34D0+ base_addr, '31:0', slice_num=-1))
    def read_dvs_dck_cck_rx_pi(self, slave,base_addr):
        self.rpt_dvs_pi_vld = str(self.indirect_read(slave, 0x3644 + base_addr, '11', slice_num=-1))
        self.rpt_dvs_pi_code = str(self.indirect_read(slave, 0x3644 + base_addr, '10:4', slice_num=-1))
        self.dck_rpt_phase_vld = str(self.indirect_read(slave, 0x362C + base_addr, '1', slice_num=-1))
        self.dck_rpt_code_i = str(self.indirect_read(slave, 0x362C + base_addr, '10:4', slice_num=-1))
        self.cck_rpt_phase_vld = str(self.indirect_read(slave, 0x3630 + base_addr, '0', slice_num=-1))
        self.cck_rpt_code_i = str(self.indirect_read(slave, 0x3630 + base_addr, '10:4', slice_num=-1))
        self.rpt_rx_pi_vld = str(self.indirect_read(slave, 0x3638 + base_addr, '1', slice_num=-1))
        self.rpt_rx_pi_code = str(self.indirect_read(slave, 0x3638 + base_addr, '9:4', slice_num=-1))
    def rg_vref_range_start(self, die, group, group_name, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', 0)
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_vref_range_start'
        offset = 0x32e0
        bit = '13:8'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} GROUP_NUM{group_name} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} GROUP_NUM{group_name} S#{self.slice_offset} = {rbvs}')
    def rg_vref_range_num(self, die, group, group_name, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', 0)
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_vref_range_num'
        offset = 0x32e0
        bit = '21:16'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} GROUP_NUM{group_name} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} GROUP_NUM{group_name} S#{self.slice_offset} = {rbvs}')
    def rg_half_window(self, die, group, group_name, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', 0)
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_half_window'
        offset = 0x3300
        bit = '5:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} GROUP_NUM{group_name} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} GROUP_NUM{group_name} S#{self.slice_offset} = {rbvs}')
    def eye_setup_info(self, die, group, group_n, **kwargs):
        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rg_vref_range_start = hex(int(self.indirect_read(slave, 0x32e0, '13:8', slice_num=-1), 16))
        rg_vref_range_num = hex(int(self.indirect_read(slave, 0x32e0, '21:16', slice_num=-1), 16))
        rg_half_window = hex(int(self.indirect_read(slave, 0x3300, '5:0', slice_num=-1), 16))
        print(f'Die{die}{group_n} Eye_Register_Setup_Info : rg_vref_range_start={rg_vref_range_start} , rg_vref_range_num={rg_vref_range_num} , rg_half_window={rg_half_window}')
    def scu_cti(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', 0)
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)

        ftn_name = 'rg_vref_range_num'
        offset = 0x1300C
        bit = '9:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        if doset == 1:
            self.indirect_write(slave, offset, bit, int(setv, 16), top=1)
        if r_bk == 1:
            rbv = self.indirect_read(slave, offset, bit, top=1)
            rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]}')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} = {rbvs}')
    def start_link_training(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', 0)
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)

        ftn_name = 'start_link_training'
        offset = 0x0010
        bit = '10'

        slave = self.EHOST[1][group]
        self.die_sel(die=1)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{1} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{1} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def BIST_ERR_COUNT(self, die, group, **kwargs):
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'Read_Bist_Result'
        offset = 0x7134
        bit = '15:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbv = int(rbv,16)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} :  offset={offset} , S#{self.slice_offset} = {rbvs}')
        return rbvs
    def CRC(self, die, group, **kwargs):
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 1)
        slice = kwargs.get('slice', [0,1,2,3])
    def RX_PCS_ERR_INJECT(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'RX_PCS_ERR_INJECT'
        offset = 0x7184
        bit = '0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def RX_PCS_RPLY_en(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'RX_PCS_RPLY_en'
        offset = 0x7140
        bit = '0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def TX_PCS_RPLY_en(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'TX_PCS_RPLY_en'
        offset = 0x7040
        bit = '0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def cfg_vref_sel_rxgp(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_vref_sel_rxgp'
        offset = 0x3450
        bit = '21:16'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        # if r_bk == 1:
        #     print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}',flush=True)

        return rbvs
    def rs_vref_center(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rs_vref_center'
        offset = 0x32E4
        bit = '7:2'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        # if r_bk == 1:
        #     print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}',flush=True)

        return rbvs
    def cfg_cck_offset_dn(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_cck_offset_dn'
        offset = 0x3628
        bit = '18'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def cfg_cck_offset(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_cck_offset'
        offset = 0x3628
        bit = '14:8'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def cfg_cck_offset_set(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'RX_PCS_ERR_INJECT'
        offset = 0x3628
        bit = '19'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def cfg_rpt_cck_phase(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_rpt_cck_phase'
        offset = 0x3624
        bit = '0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def cck_rpt_code_i_reg(self, die, group, **kwargs):
        doset = kwargs.get('doset', 0)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cck_rpt_code_i'
        offset = 0x3630
        bit = '10:4'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        rbvs_Dec = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            # if doset == 1:
            #     self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbv2 = int(rbv, 16)
                rbvs.append(rbv)
                rbvs_Dec.append(rbv2)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}(Hex){rbvs_Dec}(Dec)',flush=True)
    def cck_up_dn_flag(self, die, group, **kwargs):
        doset = kwargs.get('doset', 0)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cck_up_dn_flag'
        offset = 0x362C
        bit = '20'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        rbvs_Dec = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            # if doset == 1:
            #     self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbv2 = int(rbv, 16)
                rbvs.append(rbv)
                rbvs_Dec.append(rbv2)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}(Hex){rbvs_Dec}(Dec)',flush=True)
    def RX_PCS_BIST_MODE(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'RX_PCS_BIST_MODE'
        offset = 0x7100
        bit = '0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def RX_PCS_BIST_COMPARE(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'RX_PCS_BIST_COMPARE'
        offset = 0x7104
        bit = '0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def TX_PCS_BIST_MODE(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'TX_PCS_BIST_MODE'
        offset = 0x7000
        bit = '0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def TX_PCS_BIST_RUN(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'TX_PCS_BIST_RUN'
        offset = 0x7004
        bit = '0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def MONITOR_CLR(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'MONITOR_CLR'
        offset = 0x7120
        bit = '0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rs_rxpmad_BIST_FAIL_OR_sync(self, die, group, **kwargs):
        doset = kwargs.get('doset', 0)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rs_rxpmad_BIST_FAIL_OR_sync'
        offset = 0x3360
        bit = '10'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = int(self.indirect_read(slave, offset + base, bit, slice_num=slice_n),16)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
        buffer = str(sum(rbvs))
        return buffer
    def rg_rxpmad_BIST_FAIL_31_00(self, die, group, **kwargs):
        doset = kwargs.get('doset', 0)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_rxpmad_BIST_FAIL_31_00'
        offset = 0x3370
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        # if r_bk == 1:
        #     print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
        return rbvs
    def rg_rxpmad_BIST_FAIL_63_32(self, die, group, **kwargs):
        doset = kwargs.get('doset', 0)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_rxpmad_BIST_FAIL_63_32'
        offset = 0x3374
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        # if r_bk == 1:
        #     print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
        return rbvs
    def rg_rxpmad_BIST_FAIL_69_64(self, die, group, **kwargs):
        doset = kwargs.get('doset', 0)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_rxpmad_BIST_FAIL_69_64'
        offset = 0x3378
        bit = '5:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        # if r_bk == 1:
        #     print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
        return rbvs
    def rg_rxpmad_BIST_FAIL_31_00_1bit(self, die, group, **kwargs):
        doset = kwargs.get('doset', 0)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])
        bit = kwargs.get('bit', '0')

        ftn_name = 'rg_rxpmad_BIST_FAIL_31_00'
        offset = 0x3370
        bit = bit

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = int(self.indirect_read(slave, offset + base, bit, slice_num=slice_n),16)
                rbv_str = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        # if r_bk == 1:
        #     print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbv_str}')
        buffer = str(sum(rbvs))
        return buffer
    def rg_rxpmad_BIST_FAIL_63_32_1bit(self, die, group, **kwargs):
        doset = kwargs.get('doset', 0)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])
        bit = kwargs.get('bit', '0')

        ftn_name = 'rg_rxpmad_BIST_FAIL_63_32'
        offset = 0x3374
        bit = bit

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = int(self.indirect_read(slave, offset + base, bit, slice_num=slice_n),16)
                rbv_str = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        # if r_bk == 1:
        #     print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbv_str}')
        buffer = str(sum(rbvs))
        return buffer
    def rg_rxpmad_BIST_FAIL_69_64_1bit(self, die, group, **kwargs):
        doset = kwargs.get('doset', 0)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])
        bit = kwargs.get('bit', '0')

        ftn_name = 'rg_rxpmad_BIST_FAIL_69_64'
        offset = 0x3378
        bit = bit

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = int(self.indirect_read(slave, offset + base, bit, slice_num=slice_n),16)
                rbv_str = (self.indirect_read(slave, offset + base, bit, slice_num=slice_n),16)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        # if r_bk == 1:
        #     print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbv_str}')
        buffer = str(sum(rbvs))
        return buffer
    def RX_PMAD_BIST_COMPARE(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'RX_PMAD_BIST_COMPARE'
        offset = 0x3360
        bit = '8'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg0010_start_link_training(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg0010_start_link_training'
        offset = 0x10
        bit = '10'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def cfg_cck_ini_offset(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_cck_ini_offset'
        offset = 0x3628
        bit = '4:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg_load_pll_target(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_load_pll_target'
        offset = 0x215C
        bit = '0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}',flush=True)
    def rg_pmaa_MODE_8_target(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_pmaa_MODE_8_target'
        offset = 0x215C
        bit = '1'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset}')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}',flush=True)

        return rbvs
    def cfg_sel_div_target(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_sel_div_target'
        offset = 0x215C
        bit = '11:2'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}',flush=True)

        return rbvs
    def cfg_vco_div_mode_target(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_vco_div_mode_target'
        offset = 0x215C
        bit = '14:12'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}',flush=True)

        return rbvs
    def cmu_rstn(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)

        ftn_name = 'cmu_rstn'
        offset = 0x2100
        bit = '0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        if doset == 1:
            self.indirect_write(slave, offset, bit, int(setv, 16), slice_num=-1)
        if r_bk == 1:
            rbv = self.indirect_read(slave, offset, bit, slice_num=-1)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} = {rbv}',flush=True)
    def rg_rxpmad_BIST_MASK_31_00(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_rxpmad_BIST_MASK_31_00'
        offset = 0x3364
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg_rxpmad_BIST_MASK_63_32(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_rxpmad_BIST_MASK_63_32'
        offset = 0x3368
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg_rxpmad_BIST_MASK_69_64(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_rxpmad_BIST_MASK_69_64'
        offset = 0x336C
        bit = '5:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def cfg_en_clk_bias(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_en_clk_bias'
        offset = 0x3504
        bit = '2'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def TOP_CTRL_0000(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)

        ftn_name = 'cmu_rstn'
        offset = 0x2000
        bit = '7:4'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        if doset == 1:
            self.indirect_write(slave, offset, bit, int(setv, 16), slice_num=-1)
        if r_bk == 1:
            rbv = self.indirect_read(slave, offset, bit, slice_num=-1)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} = {rbv}',flush=True)
    def cfg_err_th(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_err_th'
        offset = 0x3628
        bit = '27:24'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_00C0_07_00(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'SLICE_CTRL_00C0_07_00'
        offset = 0x30C0
        bit = '31:0'
        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_00C4_15_08(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'SLICE_CTRL_00C4_15_08'
        offset = 0x30C4
        bit = '31:0'
        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_00C8_23_16(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'SLICE_CTRL_00C8_23_16'
        offset = 0x30C8
        bit = '31:0'
        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_00CC_31_24(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0, 1, 2, 3])

        ftn_name = 'SLICE_CTRL_00CC_31_24'
        offset = 0x30CC
        bit = '31:0'
        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_00D0_39_32(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0, 1, 2, 3])

        ftn_name = 'SLICE_CTRL_00D0_39_32'
        offset = 0x30D0
        bit = '31:0'
        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_00D4_47_40(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0, 1, 2, 3])

        ftn_name = 'SLICE_CTRL_00D4_47_40'
        offset = 0x30D4
        bit = '31:0'
        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_00D8_55_48(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0, 1, 2, 3])

        ftn_name = 'SLICE_CTRL_00D8_55_48'
        offset = 0x30D8
        bit = '31:0'
        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_00DC_63_56(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0, 1, 2, 3])

        ftn_name = 'SLICE_CTRL_00DC_63_56'
        offset = 0x30DC
        bit = '31:0'
        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_00E0_rd3_rd0(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0, 1, 2, 3])

        ftn_name = 'SLICE_CTRL_00E0_rd3_rd0'
        offset = 0x30E0
        bit = '15:0'
        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_3350_vldrd_vld(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0, 1, 2, 3])

        ftn_name = 'SLICE_CTRL_3350_vldrd_vld'
        offset = 0x3350
        bit = '7:0'
        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_0100_07_00(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'SLICE_CTRL_0100_07_00'
        offset = 0x3100
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_0104_15_08(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'SLICE_CTRL_0104_15_08'
        offset = 0x3104
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_0108_23_16(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'slice'
        offset = 0x3108
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_010C_31_24(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'SLICE_CTRL_010C_31_24'
        offset = 0x310C
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_0110_39_32(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'SLICE_CTRL_0110_39_32'
        offset = 0x3110
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_0114_47_40(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'SLICE_CTRL_0114_47_40'
        offset = 0x3114
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_0118_55_48(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'SLICE_CTRL_0118_55_48'
        offset = 0x3118
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_011C_63_56(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'SLICE_CTRL_011C_63_56'
        offset = 0x311C
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_0120_rd3_rd0(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'SLICE_CTRL_0120_rd3_rd0'
        offset = 0x3120
        bit = '15:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def SLICE_CTRL_0360_vldrd_vld(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'SLICE_CTRL_0120_rd3_rd0'
        offset = 0x3360
        bit = '7:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg_pmaa_TX_OE_l(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_pmaa_TX_OE_l'
        offset = 0x3408
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg_pmaa_TX_OE_h(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_pmaa_TX_OE_h'
        offset = 0x340C
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg_pmaa_RDTX_OE(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_pmaa_RDTX_OE'
        offset = 0x340C
        bit = '3:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg_pmaa_TVLD_OE(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_pmaa_TVLD_OE'
        offset = 0x3400
        bit = '4'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg_pmaa_TRDVLD_OE(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_pmaa_TRDVLD_OE'
        offset = 0x3400
        bit = '5'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg_pmaa_RX_IE_l(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_pmaa_RX_IE_l'
        offset = 0x3414
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg_pmaa_RX_IE_h(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_pmaa_RX_IE_h'
        offset = 0x3418
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg_pmaa_RDRX_IE(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_pmaa_RDRX_IE'
        offset = 0x341C
        bit = '3:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg_pmaa_RVLD_IE(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_pmaa_RVLD_IE'
        offset = 0x3404
        bit = '4'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg_pmaa_RRDVLD_IE(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_pmaa_RRDVLD_IE'
        offset = 0x3404
        bit = '5'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def cfg_en_clk_txd_l(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_en_clk_txd_l'
        offset = 0x3438
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def cfg_en_clk_txd_h(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_en_clk_txd_h'
        offset = 0x343C
        bit = '31:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def cfg_en_clk_txdrd(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_en_clk_txdrd'
        offset = 0x3440
        bit = '3:0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def cfg_en_clk_txvld(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_en_clk_txvld'
        offset = 0x3444
        bit = '0'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def cfg_en_clk_txvldrd(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_en_clk_txvld'
        offset = 0x3444
        bit = '1'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
    def rg_rxpmad_BIST_FAIL_69_64_valid(self, die, group, **kwargs):
        doset = kwargs.get('doset', 0)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 1)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'rg_rxpmad_BIST_FAIL_69_64'
        offset = 0x3378
        bit = '4'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        # if r_bk == 1:
        #     print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')
        return rbvs
    def cfg_rext_mode(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)

        ftn_name = 'cfg_rext_mode'
        offset = 0x2124
        bit = '16:14'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        if doset == 1:
            self.indirect_write(slave, offset, bit, int(setv, 16))
        if r_bk == 1:
            rbv = self.indirect_read(slave, offset, bit)
            rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]}')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} = {rbvs}',flush=True)
    def cfg_tp_sel(self, die, group, **kwargs):
        doset = kwargs.get('doset', 1)
        setv = kwargs.get('setv', '0x1')
        r_bk = kwargs.get('r_bk', 0)
        show = kwargs.get('show', 0)
        slice = kwargs.get('slice', [0,1,2,3])

        ftn_name = 'cfg_tp_sel'
        offset = 0x3450
        bit = '6:4'

        slave = self.EHOST[die][group]
        self.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.indirect_write(slave, offset + base, bit, int(setv, 16), slice_num=slice_n)
            if r_bk == 1:
                rbv = self.indirect_read(slave, offset + base, bit, slice_num=slice_n)
                rbvs.append(rbv)
        if show == 1:
            print(f'{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} ')
        if r_bk == 1:
            print(f'{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}')


    ''''Module CTL'''
    def slave_scan(self):
        self.i2c.scan()
    def pico_gpio(self):
        self.i2c.default_high()
        self.i2c.pull_low()
        self.i2c.default_high()
        self.i2c.pull_low()
    def mux_scan(self):
        mux_offset = 0x01
        self.i2c.write(0x71, mux_offset, 0, 8, mux_offset) # U142 i2c mux switch
        self.i2c.scan()
        mux_offset = 0x02
        self.i2c.write(0x71, mux_offset, 0, 8, mux_offset) # U142 i2c mux switch
        self.i2c.scan()
        mux_offset = 0x04
        self.i2c.write(0x71, mux_offset, 0, 8, mux_offset) # U142 i2c mux switch
        self.i2c.scan()
        mux_offset = 0x08
        self.i2c.write(0x71, mux_offset, 0, 8, mux_offset) # U142 i2c mux switch
        self.i2c.scan()
        mux_offset = 0x10
        self.i2c.write(0x71, mux_offset, 0, 8, mux_offset) # U142 i2c mux switch
        self.i2c.scan()
        mux_offset = 0x20
        self.i2c.write(0x71, mux_offset, 0, 8, mux_offset) # U142 i2c mux switch
        self.i2c.scan()
        mux_offset = 0x40
        self.i2c.write(0x71, mux_offset, 0, 8, mux_offset) # U142 i2c mux switch
        self.i2c.scan()
        mux_offset = 0x80
        self.i2c.write(0x71, mux_offset, 0, 8, mux_offset) # U142 i2c mux switch
        self.i2c.scan()
    def VDD(self, mux, ch_select, volt):
        self.i2c.write(0x71, mux, 0, 8, mux) # U142 i2c mux switch
        self.TPSM831D31_VoltageSet_eprom(ch_select, volt)
        self.i2c.write(0x71, 0x00, 0, 8, 0x00) # channel open
    def IOVDD(self, mux, ch_select, volt):
        self.i2c.write(0x71, mux, 0, 8, mux) # U142 i2c mux switch
        self.TPSM831D31_VoltageSet_eprom(ch_select, volt)
        self.i2c.write(0x71, 0x00, 0, 8, 0x00) # channel open
    def D0_AVDD_V2_D0_AVDD12_V2(self, CHA_Volt, CHB_Volt):
        mux_offset = 0x02
        self.i2c.write(0x71, mux_offset, 0, 8, mux_offset) # U142 i2c mux switch
        # self.i2c.scan()
        self.TPSM831D31_VoltageSet(CHA_Volt, CHB_Volt)
        # self.i2c.write(0x71, 0x00, 0, 8, 0x00) # channel open
    def D0_AVDD_V1_D1_V1_D0_AVDD12_V1_D1_V1(self, CHA_Volt, CHB_Volt):
        mux_offset = 0x04
        self.i2c.write(0x71, mux_offset, 0, 8, mux_offset) # U142 i2c mux switch
        # self.i2c.scan()
        self.TPSM831D31_VoltageSet(CHA_Volt, CHB_Volt)
        # self.i2c.write(0x71, 0x00, 0, 8, 0x00) # channel open
    def D1_AVDD_V2_D2_V1_D1_AVDD12_V2_D2_V1(self, CHA_Volt, CHB_Volt):
        mux_offset = 0x08
        self.i2c.write(0x71, mux_offset, 0, 8, mux_offset) # U142 i2c mux switch
        # self.i2c.scan()
        self.TPSM831D31_VoltageSet(CHA_Volt, CHB_Volt)
        # self.i2c.write(0x71, 0x00, 0, 8, 0x00) # channel open
    def D2_AVDD_V2_D2_AVDD12_V2(self, CHA_Volt, CHB_Volt):
        mux_offset = 0x10
        self.i2c.write(0x71, mux_offset, 0, 8, mux_offset) # U142 i2c mux switch
        # self.i2c.scan()
        self.TPSM831D31_VoltageSet(CHA_Volt, CHB_Volt)
        # self.i2c.write(0x71, 0x00, 0, 8, 0x00) # channel open
    def TPSM831D31_VoltageSet(self,  mux, ch_select, volt):
        self.i2c.write(0x71, mux, 0, 8, mux) # U142 i2c mux switch

        if volt == 0:
            Vout_command = 0
        else:
            Vout_command = int(((volt - 0.25) / 0.005) + 1)

        if ch_select == 'CHA':
            self.i2c.write(self.pmic_120, 0x00, 0, 8, 0x0)  # 切 CH_A
            self.i2c.write(self.pmic_120, 0x02, 0, 8, 0x1b)
            self.i2c.write(self.pmic_120, 0x01, 0, 8, 0x80)
            self.i2c.write(self.pmic_120, 0x21, 0, 16, Vout_command)
            self.i2c.write(self.pmic_120, 0xDB, 0, 8, Vout_command)
            self.i2c.write(self.pmic_120, 0xDB, 0, 8, Vout_command)
            # self.i2c.write(self.pmic_120, 0x11, 0, 16, 0x0)
            # self.i2c.write(self.pmic_120, 0x12, 0, 16, 0x0)
        elif ch_select == 'CHB':
            self.i2c.write(self.pmic_120, 0x00, 0, 8, 0x1)  # 切  CH_B
            self.i2c.write(self.pmic_120, 0x02, 0, 8, 0x1b)
            self.i2c.write(self.pmic_120, 0x01, 0, 8, 0x80)
            self.i2c.write(self.pmic_120, 0x21, 0, 16, Vout_command)
            self.i2c.write(self.pmic_120, 0xDB, 0, 8, Vout_command)
            self.i2c.write(self.pmic_120, 0xDB, 0, 8, Vout_command)
            # self.i2c.write(self.pmic_120, 0x11, 0, 16, 0x0)
            # self.i2c.write(self.pmic_120, 0x12, 0, 16, 0x0)
        else:
            pass
        # self.i2c.write(self.pmic_120, 0x11, 0, 16, 0x00)
    def TPSM831D31_Output_Disable(self,  mux, ch_select):
        self.i2c.write(0x71, 0x0, 0, 8, 0x0) # U142 i2c mux switch
        self.i2c.write(0x71, mux, 0, 8, mux) # U142 i2c mux switch
        if ch_select == 'CHA':
            self.i2c.write(self.pmic_120, 0x00, 0, 8, 0x0)  # 切 CH_A
            self.i2c.write(self.pmic_120, 0x01, 0, 8, 0x00)
        elif ch_select == 'CHB':
            self.i2c.write(self.pmic_120, 0x00, 0, 8, 0x1)  # 切  CH_B
            self.i2c.write(self.pmic_120, 0x01, 0, 8, 0x00)
        else:
            pass
        # self.i2c.write(self.pmic_120, 0x11, 0, 16, 0x00)
    def TPSM831D31_Output_Enable(self,  mux, ch_select):
        self.i2c.write(0x71, 0x0, 0, 8, 0x0) # U142 i2c mux switch
        self.i2c.write(0x71, mux, 0, 8, mux) # U142 i2c mux switch
        if ch_select == 'CHA':
            self.i2c.write(self.pmic_120, 0x00, 0, 8, 0x0)  # 切 CH_A
            self.i2c.write(self.pmic_120, 0x01, 0, 8, 0x80)
        elif ch_select == 'CHB':
            self.i2c.write(self.pmic_120, 0x00, 0, 8, 0x1)  # 切  CH_B
            self.i2c.write(self.pmic_120, 0x01, 0, 8, 0x80)
        else:
            pass
        # self.i2c.write(self.pmic_120, 0x11, 0, 16, 0x00)
    def TPSM831D31_VoltageSet_eprom(self,  mux, ch_select):
        self.i2c.write(0x71, mux, 0, 8, mux) # U142 i2c mux switch
        if ch_select == 'CHA':
            self.i2c.write(self.pmic_120, 0x00, 0, 8, 0x0)  # 切 CH_A
            self.i2c.write(self.pmic_120, 0x11, 0, 8, 0x01)
        elif ch_select == 'CHB':
            self.i2c.write(self.pmic_120, 0x00, 0, 8, 0x1)  # 切  CH_B
            self.i2c.write(self.pmic_120, 0x11, 0, 8, 0x01)
        else:
            pass
    def TPSM831D31_CurrentRead(self,  mux, ch_select):
        self.i2c.write(0x71, mux, 0, 8, mux) # U142 i2c mux switch

        if ch_select == 'CHA':
            self.i2c.write(self.pmic_120, 0x00, 0, 8, 0x0)  # 切 CH_A
            self.i2c.write(self.pmic_120, 0x02, 0, 8, 0x1b)
            self.i2c.write(self.pmic_120, 0x01, 0, 8, 0x80)
            buffer0 = self.i2c.read(self.pmic_120, 0x8B, 0, 16)
            buffer1 = self.i2c.read(self.pmic_120, 0x79, 0, 16)
            buffer2 = self.i2c.read(self.pmic_120, 0x8B, 0, 16)
            buffer3 = self.i2c.read(self.pmic_120, 0x9A, 0, 16)
            print(buffer3)

        elif ch_select == 'CHB':
            self.i2c.write(self.pmic_120, 0x00, 0, 8, 0x1)  # 切  CH_B
            self.i2c.write(self.pmic_120, 0x02, 0, 8, 0x1b)
            self.i2c.write(self.pmic_120, 0x01, 0, 8, 0x80)
            buffer00 = self.i2c.read(self.pmic_120, 0x8B, 0, 16)
            buffer10 = self.i2c.read(self.pmic_120, 0x79, 0, 16)
            buffer20 = self.i2c.read(self.pmic_120, 0x8B, 0, 16)
            buffer30 = self.i2c.read(self.pmic_120, 0x9A, 0, 16)
            print(buffer30)

        else:
            pass
    def PMIC_all_disable(self):
        for offset in [0x01, 0x02, 0x04, 0x08, 0x10, 0x20]:
            self.i2c.write(0xE2, offset, 0, 8, offset)  # i2c mux switch
            time.sleep(0.1)
            self.PMIC_DisableOut()
    def PMIC_EnableOut(self, **kargs):
        self.i2c.write(0x60, 0x02, 6, 2, 0x02)
    def PMIC_DisableOut(self, **kargs):
        self.i2c.write(0x60, 0x16, 0, 1, 0x01)
    def THM_Check(self, mux):
        self.i2c.write(0x71, mux, 0, 8, mux) # U142 i2c mux switch
        self.i2c.write(0x50, 0x1, 1, 1, 0x1)
        self.i2c.write(0x50, 0x1, 2, 1, 0x1)
        self.i2c.write(0x50, 0x3, 4, 3, 0x5)
        self.i2c.write(0x50, 0x7, 0, 3, 0x3)
        self.i2c.write(0x50, 0x1, 0, 1, 0x1)
    def PG1_SI5396C_Register_Library(self, **kargs):
        Reg_path = kargs.get('Reg_path', 0)
        MUX_slave = kargs.get('MUX_slave', 0xE0)
        MUX_offset = kargs.get('MUX_offset', 0x20)

        self.esp32.read(MUX_slave, MUX_offset, 0, 8)  # Do not skip(YQ)
        self.esp32.write(MUX_slave, MUX_offset, 0, 8, MUX_offset)
        # print(self.esp32.read(MUX_slave, MUX_offset, 0, 8))

        slave = int("0xD8", 16)
        with open(Reg_path, "r") as f:
            PG_Register_list = f.readlines()
            for i in range(len(PG_Register_list)):
                if '#' in PG_Register_list[i]:
                    pass
                elif 'Address' in PG_Register_list[i]:
                    pass
                else:
                    register_list = list(PG_Register_list[i].strip().split(','))
                    # print(register_list)
                    register_address = register_list[0].split('x')
                    register_address = register_address[1]
                    page = int(register_address[0:2],16)
                    offset = int(register_address[2:4],16)
                    register_value = register_list[1].split('x')
                    register_value = register_value[1]
                    new_register_value = int(register_value,16)

                    self.esp32.write(slave, 0x01, 0, 8, page) # set page
                    old_register_value = (self.esp32.read(slave, offset, 0, 8)) # read old register value  Check Register flow use
                    self.esp32.write(slave, offset, 0, 8, new_register_value) # write new register value
                    Now_Value = (self.esp32.read(slave, offset, 0, 8)) # read old register value  Check Register flow use


                    if int(old_register_value,16) == int(hex(new_register_value),16) and int(old_register_value,16) == int(Now_Value,16) : # Check Register flow use
                        pass # Check Register flow use
                    else: # Check Register flow use
                        print(register_list) # Check Register flow use
                        # print(page, old_register_value, hex(new_register_value), Now_Value)
                        pass