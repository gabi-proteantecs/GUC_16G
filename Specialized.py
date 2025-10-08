from Instrument import D2D_Subprogram
from Glink_run import UCIe_2p5D
import pyvisa
import datetime
from tabulate import tabulate


class UCIe_2p5D:
    def __init__(self, phy, gui):
        self.phy = phy
        self.gui = gui
        self.run = UCIe_2p5D
        self.visa = D2D_Subprogram(self.gui)
    def Specialized_0(self):
        # gui_value = self.gui.Corner_Version_wx.Value
        # self.run.ALL_mode()
        self.SRAM()
        # self.IT6300_Output_en()
        # pass
    def PMIC_OTP_REV(self):
        self.phy.non_i2c_write(0x71, 0x1, 0, 8, 0x1)
        buffer = self.phy.non_i2c_read(0x60, 0x1, 0, 8)
        print(f'PMIC OTP EPROM Version {buffer}', flush=True)
        self.phy.non_i2c_write(0x71, 0x00, 0, 8, 0x00)
    def IT6300_Output_en(self):
        visa = 'USB0::0xFFFF::0x6300::600068011717630047::0::INSTR'
        rm = pyvisa.ResourceManager()
        IT6300 = rm.open_resource(visa)
        buffer = IT6300.query('*IDN?')
        print(f'Test Instrument ID {buffer}')
    def SRAM(self):
        print('Run SRAM Function')
        # self.phy.non_i2c_write(0x70, 0x4, 0, 8, 0x4)
        # buffer = self.phy.non_i2c_read(0x70, 0x4, 0, 8)
        # print(f'PMIC OTP EPROM Version {buffer}', flush=True)
        # buffer = self.phy.non_i2c_read(0x50,  0x0, 0, 8)
        # print(f'RG1 {buffer}', flush=True)
        #
        # buffer = self.phy.non_i2c_read(0x50,  0x3, 0, 8)
        # print(f'RG2 {buffer}', flush=True)
        # self.phy.non_i2c_write(0x50, 0x3, 0, 8, 0xff)
        # buffer = self.phy.non_i2c_read(0x50,  0x3, 0, 8)
        # print(f'RG3 {buffer}', flush=True)

        #print(f'BUF {buf}', flush=True)
        #print(f'REG {buffer}', flush=True)

        #self.phy.non_i2c_write(0xA0, 0x1, 0, 8, 0xf)
        #buffer = self.phy.non_i2c_read(0xA0, 0x1, 0, 8)
        #print(f'REG {buffer}', flush=True)


        #self.phy.non_i2c_write(0x71, 0x00, 0, 8, 0x00)