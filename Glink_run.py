import datetime
import sys
import time
import tkinter as tk

import wx  # D2D use

import gui
from Instrument import D2D_Subprogram


class UCIe_2p5D:
    def __init__(self, phy, gui):
        self.vco_check = 0
        self.show = 1
        self.pi_total = 32
        self.phy = phy
        self.gui = gui
        self.non_slice = [0, 1, 2, 3]
        self.EHOST = [
            [0x01, 0x02, 0x03],  # Die0 tport/H/V
            [0x01, 0x02, 0x03],  # Die1 tport/H/V
            [0x01, 0x02, 0x03],
        ]  # Die3 tport/H/V
        self.visa = D2D_Subprogram(self.gui)
        self.Bist_thermal_en = 0

    def M4_D1H_D2V_mode(self):
        self.modes = ["M4_D1H_D2V_mode"]
        self.Multi_mode = 0
        self.NLB_s = 0
        self.tx_group = 1
        self.rx_group = 2
        self.tx_group_n = "H"
        self.rx_group_n = "V"
        self.tx_pcs_g = 2
        self.rx_pcs_g = 1
        self.tx_die = 1
        self.rx_die = 2
        self.die_arr = [1, 2]
        self.group_arr = [1, 2]
        self.tx_slice = [0, 1, 2, 3]
        self.rx_slice = [3, 2, 1, 0]
        self.tx_slice_sw = self.tx_slice
        self.rx_slice_sw = self.rx_slice

    def M4_D0V_D1V_mode(self):
        self.modes = ["M4_D0V_D1V_mode"]
        self.Multi_mode = 0
        self.NLB_s = 0
        self.tx_group = 2
        self.rx_group = 2
        self.tx_group_n = "V"
        self.rx_group_n = "V"
        self.tx_pcs_g = 1
        self.rx_pcs_g = 1
        self.tx_die = 0
        self.rx_die = 1
        self.die_arr = [0, 1]
        self.group_arr = [2, 2]
        self.tx_slice = [0, 1, 2, 3]
        self.rx_slice = [3, 2, 1, 0]
        self.tx_slice_sw = self.tx_slice
        self.rx_slice_sw = self.rx_slice

    def PLL_Checking(self, **kargs):
        mode = kargs.get("mode", "mode")
        pll_map = kargs.get("pll_map", [])
        pll_en_reg = kargs.get("pll_en_reg", [])

        self.phy.THM_Check(0x20)
        self.phy.THM_Check(0x40)
        self.phy.THM_Check(0x80)

        self.log_label("[Sequence] Check PLL Status")
        getattr(self, mode)()  # run Mx_mode()
        for idx in range(len(self.modes)):
            init_mode = self.modes[idx]
            getattr(self, init_mode)()  # run Mx_mode()

            self.phy.reg_user_set(
                die_arr=[0],
                group_arr=[1],
                tx_slice=self.tx_slice,
                rx_slice=self.rx_slice,
                reg_arr=pll_en_reg,
                mode=init_mode,
            )  # die0_H
            self.phy.check_vco(0, 1, "H")
            self.phy.reg_user_set(
                die_arr=[0],
                group_arr=[2],
                tx_slice=self.tx_slice,
                rx_slice=self.rx_slice,
                reg_arr=pll_en_reg,
                mode=init_mode,
            )  # die0_V
            self.phy.check_vco(0, 2, "V")
            self.phy.reg_user_set(
                die_arr=[1],
                group_arr=[1],
                tx_slice=self.tx_slice,
                rx_slice=self.rx_slice,
                reg_arr=pll_en_reg,
                mode=init_mode,
            )  # die1_H
            self.phy.check_vco(1, 1, "H")
            self.phy.reg_user_set(
                die_arr=[1],
                group_arr=[2],
                tx_slice=self.tx_slice,
                rx_slice=self.rx_slice,
                reg_arr=pll_en_reg,
                mode=init_mode,
            )  # die1_V
            self.phy.check_vco(1, 2, "V")
            self.phy.reg_user_set(
                die_arr=[2],
                group_arr=[1],
                tx_slice=self.tx_slice,
                rx_slice=self.rx_slice,
                reg_arr=pll_en_reg,
                mode=init_mode,
            )  # die2_H
            self.phy.check_vco(2, 1, "H")
            self.phy.reg_user_set(
                die_arr=[2],
                group_arr=[2],
                tx_slice=self.tx_slice,
                rx_slice=self.rx_slice,
                reg_arr=pll_en_reg,
                mode=init_mode,
            )  # die2_V
            self.phy.check_vco(2, 2, "V")

            # for v in range(2):
            #     d_sel = self.die_arr[v]
            #     g_sel = self.group_arr[v]
            #     if d_sel == 0 and g_sel == 1:
            #         self.phy.reg_user_set(die_arr=[0], group_arr=[1], tx_slice=self.tx_slice, rx_slice=self.rx_slice, reg_arr=pll_en_reg, mode=init_mode) # die0_H
            #         self.phy.check_vco(0, 1, 'H')
            #     elif d_sel == 0 and g_sel == 2:
            #         self.phy.reg_user_set(die_arr=[0], group_arr=[2], tx_slice=self.tx_slice, rx_slice=self.rx_slice, reg_arr=pll_en_reg, mode=init_mode) # die0_V
            #         self.phy.check_vco(0, 2, 'V')
            #     elif d_sel == 1 and g_sel == 1:
            #         self.phy.reg_user_set(die_arr=[1], group_arr=[1], tx_slice=self.tx_slice, rx_slice=self.rx_slice, reg_arr=pll_en_reg, mode=init_mode) # die1_H
            #         self.phy.check_vco(1, 1, 'H')
            #     elif d_sel == 1 and g_sel == 2:
            #         self.phy.reg_user_set(die_arr=[1], group_arr=[2], tx_slice=self.tx_slice, rx_slice=self.rx_slice, reg_arr=pll_en_reg, mode=init_mode) # die1_V
            #         self.phy.check_vco(1, 2, 'V')
            #     elif d_sel == 2 and g_sel == 1:
            #         self.phy.reg_user_set(die_arr=[2], group_arr=[1], tx_slice=self.tx_slice, rx_slice=self.rx_slice, reg_arr=pll_en_reg, mode=init_mode) # die2_H
            #         self.phy.check_vco(2, 1, 'H')
            #     elif d_sel == 2 and g_sel == 2:
            #         self.phy.reg_user_set(die_arr=[2], group_arr=[2], tx_slice=self.tx_slice, rx_slice=self.rx_slice, reg_arr=pll_en_reg, mode=init_mode) # die2_V
            #         self.phy.check_vco(2, 2, 'V')
            #     else:
            #         pass
            # self.log_label('[Sequence] PLL Checking Done')
        # self.phy.check_msd_lol()
        # self.log_label('[Sequence] MSD Checking Done')

    def Hardware_Training_Non(self, **kargs):
        # self.proteantecs()
        # return 1

        hw_non_1 = kargs.get("hw_non_1", [])
        data_training_en = kargs.get("data_training_en", 1)
        mode = kargs.get("mode", "mode")
        vref_start = kargs.get("vref_start", "0x00")
        eye_scan = kargs.get("eye_scan", "1d")
        lane_set_arr = kargs.get("lane_set_arr", [])
        setup_lane = kargs.get("setup_lane", [])
        self.lane_valid_en = kargs.get("lane_valid_en", 0)

        self.log_label("[Sequence] Run Hardware_Training_Normal_Path")
        getattr(self, mode)()  # run Mx_mode()

        self.center_tx_vref_arr = []
        self.center_rx_vref_arr = []
        if data_training_en != 0:
            for idx in range(len(self.modes)):
                init_mode = self.modes[idx]
                getattr(self, init_mode)()  # run Mx_mode()

                # self.phy.cfg_err_th(self.tx_die, self.tx_group, slice=self.tx_slice)
                # self.phy.cfg_err_th(self.rx_die, self.rx_group, slice=self.rx_slice)

                self.phy.cfg_en_clk_bias(self.tx_die, self.tx_group, slice=[0, 1, 2, 3])
                self.phy.cfg_en_clk_bias(self.rx_die, self.rx_group, slice=[0, 1, 2, 3])

                self.phy.TOP_CTRL_0000(self.tx_die, self.tx_group, setv="0x9", r_bk=0)
                self.phy.TOP_CTRL_0000(self.tx_die, self.tx_group, setv="0x9", r_bk=0)

                if eye_scan == "2d":
                    self.phy.rg_vref_range_start(
                        self.tx_die,
                        self.tx_group,
                        self.tx_group_n,
                        setv=vref_start,
                        slice=self.tx_slice,
                    )
                    self.phy.rg_vref_range_start(
                        self.rx_die,
                        self.rx_group,
                        self.rx_group_n,
                        setv=vref_start,
                        slice=self.rx_slice,
                    )
                    self.phy.rg_vref_range_num(
                        self.tx_die,
                        self.tx_group,
                        self.tx_group_n,
                        setv="0x0",
                        slice=self.tx_slice,
                    )
                    self.phy.rg_vref_range_num(
                        self.rx_die,
                        self.rx_group,
                        self.rx_group_n,
                        setv="0x0",
                        slice=self.rx_slice,
                    )
                else:
                    vref_start = "0x00 ~ 0x3F"

                print(
                    f"Init Slice : TX Slice=User Define / RX Slice=User Define (Test Die : Only Force Die0 and Die1)"
                )
                self.phy.reg_user_set(
                    die_arr=self.die_arr,
                    group_arr=self.group_arr,
                    tx_slice=self.tx_slice,
                    rx_slice=self.rx_slice,
                    reg_arr=hw_non_1,
                    mode=init_mode,
                )

                self.phy.rg_vref_range_start(
                    self.tx_die,
                    self.tx_group,
                    self.tx_group_n,
                    slice=self.tx_slice,
                    doset=0,
                    r_bk=0,
                )
                self.phy.rg_vref_range_start(
                    self.rx_die,
                    self.rx_group,
                    self.rx_group_n,
                    slice=self.rx_slice,
                    doset=0,
                    r_bk=0,
                )
                self.phy.rg_vref_range_num(
                    self.tx_die,
                    self.tx_group,
                    self.tx_group_n,
                    slice=self.tx_slice,
                    doset=0,
                    r_bk=0,
                )
                self.phy.rg_vref_range_num(
                    self.rx_die,
                    self.rx_group,
                    self.rx_group_n,
                    slice=self.rx_slice,
                    doset=0,
                    r_bk=0,
                )
                self.phy.rg_half_window(
                    self.tx_die,
                    self.tx_group,
                    self.tx_group_n,
                    slice=self.tx_slice,
                    doset=0,
                    r_bk=0,
                )
                self.phy.rg_half_window(
                    self.rx_die,
                    self.rx_group,
                    self.rx_group_n,
                    slice=self.rx_slice,
                    doset=0,
                    r_bk=0,
                )

                # self.log_label('[Sequence] Read_Data_Training_Result')
                print(f"{self.info}", flush=True)
                tx_train_result = self.phy.train_result(
                    self.tx_die, self.tx_group, self.tx_group_n, slice=self.tx_slice
                )
                rx_train_result = self.phy.train_result(
                    self.rx_die, self.rx_group, self.rx_group_n, slice=self.rx_slice
                )

                all_train_result = (
                    tx_train_result[0]
                    + tx_train_result[1]
                    + tx_train_result[2]
                    + tx_train_result[3]
                    + rx_train_result[0]
                    + rx_train_result[1]
                    + rx_train_result[2]
                    + rx_train_result[3]
                )

                # # run 1D or 2D HW Training
                # if init_mode == 'M4_D0V_D1V_mode':
                #     tx_txt_arr = ['D0_S0.txt', 'D0_S1.txt', 'D0_S2.txt', 'D0_S3.txt']
                #     rx_txt_arr = ['D1_S0.txt', 'D1_S1.txt', 'D1_S2.txt', 'D1_S3.txt']
                # else:
                #     tx_txt_arr = ['D1_S0.txt', 'D1_S1.txt', 'D1_S2.txt', 'D1_S3.txt']
                #     rx_txt_arr = ['D2_S0.txt', 'D2_S1.txt', 'D2_S2.txt', 'D2_S3.txt']
                # print(f'\nTest Result : 1D Eye Diagram')
                # self.phy.train_width(self.tx_die, self.tx_group, self.tx_group_n, txt_arr = tx_txt_arr, vref_start=vref_start)
                # self.phy.train_width(self.rx_die, self.rx_group, self.rx_group_n, txt_arr = rx_txt_arr, vref_start=vref_start)
                # if eye_scan != '2d' :
                #     print(f'\nTest Result : 2D Eye Diagram')
                #     self.phy.train_center_2D(self.tx_die, self.tx_group, self.tx_group_n, vref_start=vref_start)
                #     self.phy.train_center_2D(self.rx_die, self.rx_group, self.rx_group_n, vref_start=vref_start)

                # read center vref
                # Check Center Vref
                tx_center_vref = self.phy.cfg_vref_sel_rxgp(
                    self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
                )
                rx_center_vref = self.phy.cfg_vref_sel_rxgp(
                    self.rx_die, self.rx_group, slice=self.rx_slice, doset=0, r_bk=1
                )
                self.center_tx_vref_arr += [tx_center_vref]
                self.center_rx_vref_arr += [rx_center_vref]
        print("Center Vref Value")
        print(
            f"(HW) Die{self.tx_die}{self.tx_group_n}_Slice{self.tx_slice}_Center Vref Value = {self.center_tx_vref_arr}"
        )
        print(
            f"(HW) Die{self.rx_die}{self.rx_group_n}_Slice{self.rx_slice}_Center Vref Value = {self.center_rx_vref_arr}"
        )

        # if setup_lane != 'NA':
        #     print('\nEdit Test Pattern and RX Mask', flush=True)
        #     # [3] : 0=Normal , 1=inverted
        #     # [2:0] 0=p7 , 1/P31 , 2=Clock , 3=always 0 , 4=P5 , 5=P9 , 6=user pattern[15:0] , 7=reserved
        #     lane_arr = []
        #     for i in range(70):  # mask / type / pattern
        #         pattern = ((lane_set_arr[i]).split('/'))[2]
        #         if pattern == '5':  # PRBS5
        #             patn_bin = '100'
        #         elif pattern == '7':  # PRBS7
        #             patn_bin = '000'
        #         elif pattern == '9':  # PRBS9
        #             patn_bin = '101'
        #         elif pattern == '31':  # PRBS31
        #             patn_bin = '001'
        #         elif pattern == 'C':  # CLOCK
        #             patn_bin = '010'
        #         elif pattern == '0':  # always 0
        #             patn_bin = '011'
        #         elif pattern == 'U':  # User Pattern [15:0]
        #             patn_bin = '110'
        #         else:  # Reserved
        #             patn_bin = '111'
        #         type = ((lane_set_arr[i]).split('/'))[1]
        #         lane_bin = f'{type}{patn_bin}'
        #         lane_hex = (str(hex(int(lane_bin, 2))))[2:]
        #         lane_arr.append(lane_hex)
        #
        #     ptrn_07_00 = f'0x{lane_arr[7]}{lane_arr[6]}{lane_arr[5]}{lane_arr[4]}{lane_arr[3]}{lane_arr[2]}{lane_arr[1]}{lane_arr[0]}'
        #     ptrn_15_08 = f'0x{lane_arr[15]}{lane_arr[14]}{lane_arr[13]}{lane_arr[12]}{lane_arr[11]}{lane_arr[10]}{lane_arr[9]}{lane_arr[8]}'
        #     ptrn_23_16 = f'0x{lane_arr[23]}{lane_arr[22]}{lane_arr[21]}{lane_arr[20]}{lane_arr[19]}{lane_arr[18]}{lane_arr[17]}{lane_arr[16]}'
        #     ptrn_31_24 = f'0x{lane_arr[31]}{lane_arr[30]}{lane_arr[29]}{lane_arr[28]}{lane_arr[27]}{lane_arr[26]}{lane_arr[25]}{lane_arr[24]}'
        #     ptrn_39_31 = f'0x{lane_arr[39]}{lane_arr[38]}{lane_arr[37]}{lane_arr[36]}{lane_arr[35]}{lane_arr[34]}{lane_arr[33]}{lane_arr[32]}'
        #     ptrn_47_40 = f'0x{lane_arr[47]}{lane_arr[46]}{lane_arr[45]}{lane_arr[44]}{lane_arr[43]}{lane_arr[42]}{lane_arr[41]}{lane_arr[40]}'
        #     ptrn_55_48 = f'0x{lane_arr[55]}{lane_arr[54]}{lane_arr[53]}{lane_arr[52]}{lane_arr[51]}{lane_arr[50]}{lane_arr[49]}{lane_arr[48]}'
        #     ptrn_63_56 = f'0x{lane_arr[63]}{lane_arr[62]}{lane_arr[61]}{lane_arr[60]}{lane_arr[59]}{lane_arr[58]}{lane_arr[57]}{lane_arr[56]}'
        #     ptrn_rd3_rd0 = f'0x{lane_arr[67]}{lane_arr[66]}{lane_arr[65]}{lane_arr[64]}'
        #     ptrn_vldrd_vld = f'0x{lane_arr[69]}{lane_arr[68]}'
        #
        #     # dieA tx
        #     self.phy.SLICE_CTRL_00C0_07_00(self.tx_die, self.tx_group, setv=ptrn_07_00)
        #     self.phy.SLICE_CTRL_00C4_15_08(self.tx_die, self.tx_group, setv=ptrn_15_08)
        #     self.phy.SLICE_CTRL_00C8_23_16(self.tx_die, self.tx_group, setv=ptrn_23_16)
        #     self.phy.SLICE_CTRL_00CC_31_24(self.tx_die, self.tx_group, setv=ptrn_31_24)
        #     self.phy.SLICE_CTRL_00D0_39_32(self.tx_die, self.tx_group, setv=ptrn_39_31)
        #     self.phy.SLICE_CTRL_00D4_47_40(self.tx_die, self.tx_group, setv=ptrn_47_40)
        #     self.phy.SLICE_CTRL_00D8_55_48(self.tx_die, self.tx_group, setv=ptrn_55_48)
        #     self.phy.SLICE_CTRL_00DC_63_56(self.tx_die, self.tx_group, setv=ptrn_63_56)
        #     self.phy.SLICE_CTRL_00E0_rd3_rd0(self.tx_die, self.tx_group, setv=ptrn_rd3_rd0)
        #     self.phy.SLICE_CTRL_3350_vldrd_vld(self.tx_die, self.tx_group, setv=ptrn_vldrd_vld)
        #
        #     # dieA rx
        #     self.phy.SLICE_CTRL_0100_07_00(self.tx_die, self.tx_group, setv=ptrn_07_00)
        #     self.phy.SLICE_CTRL_0104_15_08(self.tx_die, self.tx_group, setv=ptrn_15_08)
        #     self.phy.SLICE_CTRL_0108_23_16(self.tx_die, self.tx_group, setv=ptrn_23_16)
        #     self.phy.SLICE_CTRL_010C_31_24(self.tx_die, self.tx_group, setv=ptrn_31_24)
        #     self.phy.SLICE_CTRL_0110_39_32(self.tx_die, self.tx_group, setv=ptrn_39_31)
        #     self.phy.SLICE_CTRL_0114_47_40(self.tx_die, self.tx_group, setv=ptrn_47_40)
        #     self.phy.SLICE_CTRL_0118_55_48(self.tx_die, self.tx_group, setv=ptrn_55_48)
        #     self.phy.SLICE_CTRL_011C_63_56(self.tx_die, self.tx_group, setv=ptrn_63_56)
        #     # self.phy.SLICE_CTRL_0120_rd3_rd0(self.tx_die, self.tx_group, setv=ptrn_rd3_rd0)
        #     # self.phy.SLICE_CTRL_0360_vldrd_vld(self.tx_die, self.tx_group, setv=ptrn_vldrd_vld)
        #
        #     # dieB tx
        #     self.phy.SLICE_CTRL_00C0_07_00(self.rx_die, self.rx_group, setv=ptrn_07_00)
        #     self.phy.SLICE_CTRL_00C4_15_08(self.rx_die, self.rx_group, setv=ptrn_15_08)
        #     self.phy.SLICE_CTRL_00C8_23_16(self.rx_die, self.rx_group, setv=ptrn_23_16)
        #     self.phy.SLICE_CTRL_00CC_31_24(self.rx_die, self.rx_group, setv=ptrn_31_24)
        #     self.phy.SLICE_CTRL_00D0_39_32(self.rx_die, self.rx_group, setv=ptrn_39_31)
        #     self.phy.SLICE_CTRL_00D4_47_40(self.rx_die, self.rx_group, setv=ptrn_47_40)
        #     self.phy.SLICE_CTRL_00D8_55_48(self.rx_die, self.rx_group, setv=ptrn_55_48)
        #     self.phy.SLICE_CTRL_00DC_63_56(self.rx_die, self.rx_group, setv=ptrn_63_56)
        #     self.phy.SLICE_CTRL_00E0_rd3_rd0(self.rx_die, self.rx_group, setv=ptrn_rd3_rd0)
        #     self.phy.SLICE_CTRL_3350_vldrd_vld(self.rx_die, self.rx_group, setv=ptrn_vldrd_vld)
        #
        #     # dieB rx
        #     self.phy.SLICE_CTRL_0100_07_00(self.rx_die, self.rx_group, setv=ptrn_07_00)
        #     self.phy.SLICE_CTRL_0104_15_08(self.rx_die, self.rx_group, setv=ptrn_15_08)
        #     self.phy.SLICE_CTRL_0108_23_16(self.rx_die, self.rx_group, setv=ptrn_23_16)
        #     self.phy.SLICE_CTRL_010C_31_24(self.rx_die, self.rx_group, setv=ptrn_31_24)
        #     self.phy.SLICE_CTRL_0110_39_32(self.rx_die, self.rx_group, setv=ptrn_39_31)
        #     self.phy.SLICE_CTRL_0114_47_40(self.rx_die, self.rx_group, setv=ptrn_47_40)
        #     self.phy.SLICE_CTRL_0118_55_48(self.rx_die, self.rx_group, setv=ptrn_55_48)
        #     self.phy.SLICE_CTRL_011C_63_56(self.rx_die, self.rx_group, setv=ptrn_63_56)
        #     # self.phy.SLICE_CTRL_0120_rd3_rd0(self.rx_die, self.rx_group, setv=ptrn_rd3_rd0)
        #     # self.phy.SLICE_CTRL_0360_vldrd_vld(self.rx_die, self.rx_group, setv=ptrn_vldrd_vld)
        #
        #     # 31 to 00
        #     mask_31_00_arr = []
        #     for i in range(32):  # mask / type / pattern
        #         buffer = ((lane_set_arr[31-i]).split('/'))[0]
        #         mask_31_00_arr.append(buffer)
        #     mask_31_00_val = ''.join(mask_31_00_arr)
        #     mask_31_00_hex = str(hex(int(mask_31_00_val, 2)))
        #
        #     # 63 to 31
        #     mask_63_32_arr = []
        #     for i in range(32):  # mask / type / pattern
        #         buffer = ((lane_set_arr[63-i]).split('/'))[0]
        #         mask_63_32_arr.append(buffer)
        #     mask_63_32_val = ''.join(mask_63_32_arr)
        #     mask_63_32_hex = str(hex(int(mask_63_32_val, 2)))
        #
        #     # 63 to 31
        #     mask_69_64_arr = []
        #     for i in range(6):  # mask / type / pattern
        #         buffer = ((lane_set_arr[69-i]).split('/'))[0]
        #         mask_69_64_arr.append(buffer)
        #     mask_69_64_val = ''.join(mask_69_64_arr)
        #     mask_69_64_hex = str(hex(int(mask_69_64_val, 2)))
        #
        #     # dieA rx mask
        #     self.phy.rg_rxpmad_BIST_MASK_31_00(self.tx_die, self.tx_group, setv=mask_31_00_hex)
        #     self.phy.rg_rxpmad_BIST_MASK_63_32(self.tx_die, self.tx_group, setv=mask_63_32_hex)
        #     self.phy.rg_rxpmad_BIST_MASK_69_64(self.tx_die, self.tx_group, setv=mask_69_64_hex)
        #
        #     # dieB rx mask
        #     self.phy.rg_rxpmad_BIST_MASK_31_00(self.rx_die, self.rx_group, setv=mask_31_00_hex)
        #     self.phy.rg_rxpmad_BIST_MASK_63_32(self.rx_die, self.rx_group, setv=mask_63_32_hex)
        #     self.phy.rg_rxpmad_BIST_MASK_69_64(self.rx_die, self.rx_group, setv=mask_69_64_hex)

        # # dieA OE Setup
        # self.phy.rg_pmaa_TX_OE_l(self.tx_die, self.tx_group, setv='0x00000001')
        # self.phy.rg_pmaa_TX_OE_h(self.tx_die, self.tx_group, setv='0x00000000')
        # self.phy.rg_pmaa_RDTX_OE(self.tx_die, self.tx_group, setv='0x0')
        # self.phy.rg_pmaa_TVLD_OE(self.tx_die, self.tx_group, setv='0x0')
        # self.phy.rg_pmaa_TRDVLD_OE(self.tx_die, self.tx_group, setv='0x0')
        #
        # # dieB OE Setup
        # self.phy.rg_pmaa_TX_OE_l(self.rx_die, self.rx_group, setv='0x00000001')
        # self.phy.rg_pmaa_TX_OE_h(self.rx_die, self.rx_group, setv='0x00000000')
        # self.phy.rg_pmaa_RDTX_OE(self.rx_die, self.rx_group, setv='0x0')
        # self.phy.rg_pmaa_TVLD_OE(self.rx_die, self.rx_group, setv='0x0')
        # self.phy.rg_pmaa_TRDVLD_OE(self.rx_die, self.rx_group, setv='0x0')
        #
        # # dieA IE/CLOCK Setup
        # self.phy.rg_pmaa_RX_IE_l(self.tx_die, self.tx_group, setv='0x00000001')
        # self.phy.rg_pmaa_RX_IE_h(self.tx_die, self.tx_group, setv='0x00000000')
        # self.phy.rg_pmaa_RDRX_IE(self.tx_die, self.tx_group, setv='0x0')
        # self.phy.rg_pmaa_RVLD_IE(self.tx_die, self.tx_group, setv='0x0')
        # self.phy.rg_pmaa_RRDVLD_IE(self.tx_die, self.tx_group, setv='0x0')
        # self.phy.cfg_en_clk_txd_l(self.tx_die, self.tx_group, setv='0x00000001')
        # self.phy.cfg_en_clk_txd_h(self.tx_die, self.tx_group, setv='0x00000000')
        # self.phy.cfg_en_clk_txdrd(self.tx_die, self.tx_group, setv='0x0')
        # self.phy.cfg_en_clk_txvld(self.tx_die, self.tx_group, setv='0x0')
        # self.phy.cfg_en_clk_txvldrd(self.tx_die, self.tx_group, setv='0x0')
        #
        # # dieB IE/CLOCK Setup
        # self.phy.rg_pmaa_RX_IE_l(self.rx_die, self.rx_group, setv='0x00000001')
        # self.phy.rg_pmaa_RX_IE_h(self.rx_die, self.rx_group, setv='0x00000000')
        # self.phy.rg_pmaa_RDRX_IE(self.rx_die, self.rx_group, setv='0x0')
        # self.phy.rg_pmaa_RVLD_IE(self.rx_die, self.rx_group, setv='0x0')
        # self.phy.rg_pmaa_RRDVLD_IE(self.rx_die, self.rx_group, setv='0x0')
        # self.phy.cfg_en_clk_txd_l(self.rx_die, self.rx_group, setv='0x00000001')
        # self.phy.cfg_en_clk_txd_h(self.rx_die, self.rx_group, setv='0x00000000')
        # self.phy.cfg_en_clk_txdrd(self.rx_die, self.rx_group, setv='0x0')
        # self.phy.cfg_en_clk_txvld(self.rx_die, self.rx_group, setv='0x0')
        # self.phy.cfg_en_clk_txvldrd(self.rx_die, self.rx_group, setv='0x0')
        # else:
        #     print('\nDefault Test Pattern and RX Mask', flush=True)

        # """ proteanTecs Test Start """
        # '''
        # register_name = 'cmu_rstn'
        # offset = 0x2000
        # bit = '7:4'
        # die = 0
        # group = 1
        # setv = '0x9'
        #
        # self.phy.die_sel(die=die) # select die
        # slave = self.EHOST[die][group] # setup i2c slave address
        # self.phy.indirect_write(slave, offset, bit, int(setv, 16), slice_num=-1)  # write register
        # read_register = self.phy.indirect_read(slave, offset, bit, slice_num=-1)  # read register
        # '''
        #
        # self.proteantecs()
        # """ proteanTecs Test Done """
        # return 1
        return all_train_result

    def PCS_BIST_Check_NON(self, **kargs):
        mode = kargs.get("mode", "mode")
        PCS_BIST_Check_NON = kargs.get("PCS_BIST_Check_NON", [])
        chk_time = kargs.get("chk_time", "5")
        chk_loop = kargs.get("chk_loop", "1")
        data_replay = kargs.get("data_replay", 1)
        voltage_sense_avdd = kargs.get("voltage_sense_avdd", 0.75)
        avdd_sense_en = kargs.get("avdd_sense_en", 1)

        # Rx_run need to enable then Tx_run enable
        self.log_label("[Sequence] Run PCS BIST Check Normal_Path")
        getattr(self, mode)()  # run Mx_mode()
        for idx in range(len(self.modes)):
            init_mode = self.modes[idx]
            getattr(self, init_mode)()  # run Mx_mode()
            print(f"Init Slice : TX Slice={self.tx_slice} / RX Slice={self.rx_slice}")

            self.phy.reg_user_set(
                die_arr=self.die_arr,
                group_arr=self.group_arr,
                tx_slice=self.tx_slice,
                rx_slice=self.rx_slice,
                reg_arr=PCS_BIST_Check_NON,
                mode=init_mode,
            )

            # inject error
            print("Function Check : RX_PCS_ERR_INJECT : Enable", flush=True)
            self.phy.MONITOR_CLR(
                self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1"
            )
            self.phy.MONITOR_CLR(
                self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1"
            )
            self.phy.RX_PCS_BIST_COMPARE(
                self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1"
            )
            self.phy.RX_PCS_BIST_COMPARE(
                self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1"
            )
            self.phy.TX_PCS_BIST_RUN(
                self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1"
            )
            self.phy.TX_PCS_BIST_RUN(
                self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1"
            )
            self.phy.RX_PCS_ERR_INJECT(
                self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1", r_bk=1
            )
            self.phy.RX_PCS_ERR_INJECT(
                self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1", r_bk=1
            )
            error_count_inject = self.PCS_BIST_Check_NON_result(
                mode=init_mode, skip_result=1
            )
            if avdd_sense_en == 1:
                time.sleep(0.1)
                self.avdd_sense(mode=init_mode, voltage_sense_avdd=voltage_sense_avdd)
                if self.gui.Thermal_die_en.Value == True:
                    self.thermal_voltage_read()
            if len(self.tx_slice) * 2 == error_count_inject:
                self.inject_chk = ""
                print(
                    f"\034Function Check : RX_PCS_ERR_INJECT Result : PASS", flush=True
                )
            elif error_count_inject == 0:
                self.inject_chk = "_Error (Valid_Failed)"
                print(
                    f"\033Function Check : RX_PCS_ERR_INJECT Result : Error_(Valid_Failed)",
                    flush=True,
                )
            else:
                self.inject_chk = "_Error (Inject_Failed)"
                print(
                    f"\033Function Check : RX_PCS_ERR_INJECT Result : Failed",
                    flush=True,
                )

            # Data Replay
            self.Replay_CHK = ""
            if data_replay == 1:
                print("Function Check : Data Replay : Enable", flush=True)
                self.Replay_CHK = ""
                self.phy.RX_PCS_RPLY_en(
                    self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1"
                )
                self.phy.TX_PCS_RPLY_en(
                    self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1"
                )
                self.phy.MONITOR_CLR(
                    self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1"
                )
                self.phy.MONITOR_CLR(
                    self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1"
                )
                self.phy.RX_PCS_BIST_COMPARE(
                    self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1"
                )
                self.phy.RX_PCS_BIST_COMPARE(
                    self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1"
                )
                self.phy.TX_PCS_BIST_RUN(
                    self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1"
                )
                self.phy.TX_PCS_BIST_RUN(
                    self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1"
                )
                print("Function Check : Replay_CHK : Enable", flush=True)
                self.phy.RX_PCS_ERR_INJECT(
                    self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1", r_bk=0
                )
                self.phy.RX_PCS_ERR_INJECT(
                    self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1", r_bk=0
                )
                self.PCS_BIST_Check_NON_result(mode=init_mode, skip_result=0)
                self.phy.RX_PCS_BIST_COMPARE(
                    self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x0"
                )
                self.phy.RX_PCS_BIST_COMPARE(
                    self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x0"
                )
                self.phy.TX_PCS_BIST_RUN(
                    self.tx_die, self.tx_group, slice=self.tx_slice_sw, setv="0x0"
                )
                self.phy.TX_PCS_BIST_RUN(
                    self.rx_die, self.rx_group, slice=self.rx_slice_sw, setv="0x0"
                )

            pcs_result = []
            for L in range(int(chk_loop)):
                # bist enable
                self.phy.MONITOR_CLR(
                    self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1"
                )
                self.phy.MONITOR_CLR(
                    self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1"
                )
                self.phy.RX_PCS_BIST_COMPARE(
                    self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1"
                )
                self.phy.RX_PCS_BIST_COMPARE(
                    self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1"
                )
                self.phy.TX_PCS_BIST_RUN(
                    self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1"
                )
                self.phy.TX_PCS_BIST_RUN(
                    self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1"
                )
                # bist check time
                if str(chk_time).find("pi") != -1:
                    num = int((chk_time.split("pi"))[0])
                    for n in range(num):
                        self.Read_pi_value()
                    print(f"PCS BIST Time : Read Pi Value Loop{L + 1}", flush=True)
                else:
                    print(
                        f"PCS BIST Time : Check Loop {L + 1}/{chk_loop} , Time {chk_time}s",
                        flush=True,
                    )
                    time.sleep(int(chk_time))

                error_count_inject = self.PCS_BIST_Check_NON_result(
                    mode=init_mode, skip_result=0
                )
                if self.Bist_thermal_en == 1:
                    self.thermal_voltage_read()
                # bist stop
                self.phy.RX_PCS_BIST_COMPARE(
                    self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x0"
                )
                self.phy.RX_PCS_BIST_COMPARE(
                    self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x0"
                )
                self.phy.TX_PCS_BIST_RUN(
                    self.tx_die, self.tx_group, slice=self.tx_slice_sw, setv="0x0"
                )
                self.phy.TX_PCS_BIST_RUN(
                    self.rx_die, self.rx_group, slice=self.rx_slice_sw, setv="0x0"
                )
                if error_count_inject == 0:
                    bist_val = 0
                else:
                    bist_val = 1
                pcs_result.append(bist_val)
            if sum(pcs_result) == 0:
                bist_val = "Pass"
            else:
                bist_val = "Failed"

            re_value = f"{bist_val}{self.inject_chk}{self.Replay_CHK}"
        return re_value

    def PCS_BIST_Check_NON_result(self, **kargs):
        mode = kargs.get("mode", "mode")
        skip_result = kargs.get("skip_result", 0)

        # self.log_label('[Sequence] Run PCS BIST Check Normal_Path Result')
        getattr(self, mode)()  # run Mx_mode()
        rbvs = []
        for idx in range(len(self.modes)):
            init_mode = self.modes[idx]
            getattr(self, init_mode)()  # run Mx_mode()
            print(f"Init Slice : TX Slice={self.tx_slice} / RX Slice={self.rx_slice}")

            print("PCS BIST Check Normal Path Test Result :")
            tx_pcs_val = self.phy.BIST_ERR_COUNT(
                self.tx_die, self.tx_group, slice=self.tx_slice
            )
            rx_pcs_val = self.phy.BIST_ERR_COUNT(
                self.rx_die, self.rx_group, slice=self.rx_slice
            )
            if skip_result == 0:
                for P in range(len(tx_pcs_val)):
                    if tx_pcs_val[P] != 0:
                        print(
                            f"\033Die{self.tx_die}{self.tx_group_n} Slice{self.tx_slice[P]}, Error Count={tx_pcs_val[P]}, Faiied",
                            flush=True,
                        )
                    else:
                        print(
                            f"\034Die{self.tx_die}{self.tx_group_n} Slice{self.tx_slice[P]}, Error Count={tx_pcs_val[P]}",
                            flush=True,
                        )
                    if rx_pcs_val[P] != 0:
                        print(
                            f"\033Die{self.rx_die}{self.rx_group_n} Slice{self.rx_slice[P]}, Error Count={rx_pcs_val[P]}, Failed",
                            flush=True,
                        )
                    else:
                        print(
                            f"\034Die{self.rx_die}{self.rx_group_n} Slice{self.rx_slice[P]}, Error Count={rx_pcs_val[P]}",
                            flush=True,
                        )
            else:
                for P in range(len(tx_pcs_val)):
                    if tx_pcs_val[P] != 0:
                        print(
                            f"\033Die{self.tx_die}{self.tx_group_n} Slice{self.tx_slice[P]}, Error Count={tx_pcs_val[P]}",
                            flush=True,
                        )
                    else:
                        print(
                            f"\034Die{self.tx_die}{self.tx_group_n} Slice{self.tx_slice[P]}, Error Count={tx_pcs_val[P]}",
                            flush=True,
                        )
                    if rx_pcs_val[P] != 0:
                        print(
                            f"\033Die{self.rx_die}{self.rx_group_n} Slice{self.rx_slice[P]}, Error Count={rx_pcs_val[P]}",
                            flush=True,
                        )
                    else:
                        print(
                            f"\034Die{self.rx_die}{self.rx_group_n} Slice{self.rx_slice[P]}, Error Count={rx_pcs_val[P]}",
                            flush=True,
                        )
            rbv = sum(tx_pcs_val) + sum(rx_pcs_val)  # rbv=0 pcs bist pass
            rbvs.append(rbv)
        pcs_error_count = sum(rbvs)
        return pcs_error_count

    """ Test Item and Function """

    def VCO(self, **kargs):
        CMU_S = kargs.get("CMU_S", 0)
        CMU_G = kargs.get("CMU_G", 0)
        CMU_E = kargs.get("CMU_E", 0)

        CMU_loop = int(((CMU_E - CMU_S) / CMU_G) + 1)

        # setup ctune value
        REX_arr = []
        tx_speed_arr = []
        self.visa.PG_81160A_2CH(
            CMU1_Amp=0.5, CMU1_S=100000000, CMU2_Amp=0.5, CMU2_S=100000000
        )
        for k in range(CMU_loop):
            CMU_Freq = CMU_S + (CMU_G * k)
            self.visa.PG_81160A_2CH(CMU_S=CMU_Freq)
            time.sleep(1)
            REXT = self.visa.M5_34411A_Voltage(
                visa="USB0::0x2A8D::0x1301::MY57223676::0::INSTR"
            )  # Die0 V1
            REX_arr += [REXT]
            print(f"RCLK Frequency={CMU_Freq}Hz , REXT_Did0_V1={REXT}V", flush=True)

            sel_div = self.phy.cfg_pre_div_sel(
                self.tx_die, self.tx_group, self.tx_slice, doset=0, slice_num=-1
            )  # vco Die0 V2 --> self.EHOST[0][2]
            tx_speed = CMU_Freq * 4 * int(sel_div, 16)
            tx_speed_arr += [tx_speed]

        r_data = REX_arr + tx_speed_arr
        return r_data

    def check_speed(self, **kargs):
        TestDataRate = kargs.get("TestDataRate", "0")
        mode = kargs.get("mode", "")

        getattr(self, mode)()  # run Mx_mode()

        # 32G   # 24    # 16
        # rg_pmaa_MODE_8_target   :       0           0         1
        # cfg_sel_div_target                 :     28        1E       28
        # cfg_vco_div_mode_target    :       0           0         1
        reg_chk = [
            "0x0/0x28/0x0/0x0/0x28/0x0",
            "0x0/0x1E/0x0/0x0/0x1E/0x0",
            "0x1/0x28/0x1/0x1/0x28/0x1",
        ]
        tx_check1 = self.phy.rg_pmaa_MODE_8_target(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )
        tx_check2 = self.phy.cfg_sel_div_target(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )
        tx_check3 = self.phy.cfg_vco_div_mode_target(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )
        rx_check1 = self.phy.rg_pmaa_MODE_8_target(
            self.rx_die, self.rx_group, slice=self.rx_slice, doset=0, r_bk=1
        )
        rx_check2 = self.phy.cfg_sel_div_target(
            self.rx_die, self.rx_group, slice=self.rx_slice, doset=0, r_bk=1
        )
        rx_check3 = self.phy.cfg_vco_div_mode_target(
            self.rx_die, self.rx_group, slice=self.rx_slice, doset=0, r_bk=1
        )
        reg_value = (
            f"{tx_check1}/{tx_check2}/{tx_check3}/{rx_check1}/{rx_check2}/{rx_check3}"
        )

        chk_value = ""
        if TestDataRate == 32:
            if reg_chk[0] == reg_value:
                chk_value = "PASS"
            else:
                chk_value = "Failed"
        elif TestDataRate == 24:
            if reg_chk[1] == reg_value:
                chk_value = "PASS"
            else:
                chk_value = "Failed"
        elif TestDataRate == 16:
            if reg_chk[2] == reg_value:
                chk_value = "PASS"
            else:
                chk_value = "Failed"

        print(f"\nCheck chip speed is {TestDataRate} is {chk_value}", flush=True)

    def Read_pi_value(self, **kargs):
        print(f"Read cck_rpt_code_i_reg value", flush=True)
        self.phy.cfg_rpt_cck_phase(
            self.tx_die, self.tx_group, slice=self.tx_slice_sw, setv="0x1"
        )
        self.phy.cck_rpt_code_i_reg(self.tx_die, self.tx_group, slice=self.tx_slice_sw)
        self.phy.cfg_rpt_cck_phase(
            self.tx_die, self.tx_group, slice=self.tx_slice_sw, setv="0x0"
        )
        self.phy.cfg_rpt_cck_phase(
            self.tx_die, self.tx_group, slice=self.tx_slice_sw, setv="0x1"
        )

        self.phy.cfg_rpt_cck_phase(
            self.rx_die, self.rx_group, slice=self.rx_slice_sw, setv="0x1"
        )
        self.phy.cck_rpt_code_i_reg(self.rx_die, self.rx_group, slice=self.rx_slice_sw)
        self.phy.cfg_rpt_cck_phase(
            self.rx_die, self.rx_group, slice=self.rx_slice_sw, setv="0x0"
        )
        self.phy.cfg_rpt_cck_phase(
            self.rx_die, self.rx_group, slice=self.rx_slice_sw, setv="0x1"
        )

    def Read_pi_status_die0_V(self, times):
        # Check pi point
        for g in range(times):
            self.phy.cfg_rpt_cck_phase(
                self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1"
            )
            self.phy.cfg_rpt_cck_phase(
                self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1"
            )
            self.phy.cck_rpt_code_i_reg(self.tx_die, self.tx_group, slice=self.tx_slice)
            # self.phy.cck_rpt_code_i_reg(self.rx_die, self.rx_group, slice= self.rx_slice)
            self.phy.cfg_rpt_cck_phase(
                self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x0"
            )
            self.phy.cfg_rpt_cck_phase(
                self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x0"
            )
            self.phy.cfg_rpt_cck_phase(
                self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1"
            )
            self.phy.cfg_rpt_cck_phase(
                self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1"
            )

    def Read_pi_status_die1_V(self, times):
        for g in range(times):
            self.phy.cfg_rpt_cck_phase(
                self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1"
            )
            self.phy.cfg_rpt_cck_phase(
                self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1"
            )
            # self.phy.cck_rpt_code_i_reg(self.tx_die, self.tx_group, slice= self.tx_slice)
            self.phy.cck_rpt_code_i_reg(self.rx_die, self.rx_group, slice=self.rx_slice)
            self.phy.cfg_rpt_cck_phase(
                self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x0"
            )
            self.phy.cfg_rpt_cck_phase(
                self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x0"
            )
            self.phy.cfg_rpt_cck_phase(
                self.tx_die, self.tx_group, slice=self.tx_slice, setv="0x1"
            )
            self.phy.cfg_rpt_cck_phase(
                self.rx_die, self.rx_group, slice=self.rx_slice, setv="0x1"
            )

    def read_center_vref(self, **kargs):
        mode = kargs.get("mode", "mode")

        getattr(self, mode)()  # run Mx_mode()
        tx_center_vref = self.phy.cfg_vref_sel_rxgp(
            self.tx_die, self.tx_group, doset=0, slice=self.tx_slice
        )
        rx_center_vref = self.phy.cfg_vref_sel_rxgp(
            self.rx_die, self.rx_group, doset=0, slice=self.rx_slice
        )
        # print(f'Die{self.tx_die}{self.tx_group_n}_Slice{self.tx_slice}_Center Vref Value = {self.center_tx_vref_arr}')
        # print(f'Die{self.rx_die}{self.rx_group_n}_Slice{self.rx_slice}_Center Vref Value = {self.center_rx_vref_arr}')

        all_center_vref = [tx_center_vref] + [rx_center_vref]
        return all_center_vref

    def pattern_set(self, **kargs):
        lane_set_arr = kargs.get("lane_set_arr", [])
        mode = kargs.get("mode", "")

        getattr(self, mode)()  # run Mx_mode()
        # [3] : 0=Normal , 1=inverted
        # [2:0] 0=p7 , 1/P31 , 2=Clock , 3=always 0 , 4=P5 , 5=P9 , 6=user pattern[15:0] , 7=reserved
        lane_arr = []
        for i in range(70):  # mask / type / pattern
            pattern = ((lane_set_arr[i]).split("/"))[2]
            if pattern == "5":  # PRBS5
                patn_bin = "100"
            elif pattern == "7":  # PRBS7
                patn_bin = "000"
            elif pattern == "9":  # PRBS9
                patn_bin = "101"
            elif pattern == "31":  # PRBS31
                patn_bin = "001"
            elif pattern == "C":  # CLOCK
                patn_bin = "010"
            elif pattern == "0":  # always 0
                patn_bin = "011"
            elif pattern == "U":  # User Pattern [15:0]
                patn_bin = "110"
            else:  # Reserved
                patn_bin = "111"
            type = ((lane_set_arr[i]).split("/"))[1]
            lane_bin = f"{type}{patn_bin}"
            lane_hex = (str(hex(int(lane_bin, 2))))[2:]
            lane_arr.append(lane_hex)

        ptrn_07_00 = f"0x{lane_arr[7]}{lane_arr[6]}{lane_arr[5]}{lane_arr[4]}{lane_arr[3]}{lane_arr[2]}{lane_arr[1]}{lane_arr[0]}"
        ptrn_15_08 = f"0x{lane_arr[15]}{lane_arr[14]}{lane_arr[13]}{lane_arr[12]}{lane_arr[11]}{lane_arr[10]}{lane_arr[9]}{lane_arr[8]}"
        ptrn_23_16 = f"0x{lane_arr[23]}{lane_arr[22]}{lane_arr[21]}{lane_arr[20]}{lane_arr[19]}{lane_arr[18]}{lane_arr[17]}{lane_arr[16]}"
        ptrn_31_24 = f"0x{lane_arr[31]}{lane_arr[30]}{lane_arr[29]}{lane_arr[28]}{lane_arr[27]}{lane_arr[26]}{lane_arr[25]}{lane_arr[24]}"
        ptrn_39_31 = f"0x{lane_arr[39]}{lane_arr[38]}{lane_arr[37]}{lane_arr[36]}{lane_arr[35]}{lane_arr[34]}{lane_arr[33]}{lane_arr[32]}"
        ptrn_47_40 = f"0x{lane_arr[47]}{lane_arr[46]}{lane_arr[45]}{lane_arr[44]}{lane_arr[43]}{lane_arr[42]}{lane_arr[41]}{lane_arr[40]}"
        ptrn_55_48 = f"0x{lane_arr[55]}{lane_arr[54]}{lane_arr[53]}{lane_arr[52]}{lane_arr[51]}{lane_arr[50]}{lane_arr[49]}{lane_arr[48]}"
        ptrn_63_56 = f"0x{lane_arr[63]}{lane_arr[62]}{lane_arr[61]}{lane_arr[60]}{lane_arr[59]}{lane_arr[58]}{lane_arr[57]}{lane_arr[56]}"
        ptrn_rd3_rd0 = f"0x{lane_arr[67]}{lane_arr[66]}{lane_arr[65]}{lane_arr[64]}"
        ptrn_vldrd_vld = f"0x{lane_arr[69]}{lane_arr[68]}"

        # dieA tx
        self.phy.SLICE_CTRL_00C0_07_00(self.tx_die, self.tx_group, setv=ptrn_07_00)
        self.phy.SLICE_CTRL_00C4_15_08(self.tx_die, self.tx_group, setv=ptrn_15_08)
        self.phy.SLICE_CTRL_00C8_23_16(self.tx_die, self.tx_group, setv=ptrn_23_16)
        self.phy.SLICE_CTRL_00CC_31_24(self.tx_die, self.tx_group, setv=ptrn_31_24)
        self.phy.SLICE_CTRL_00D0_39_32(self.tx_die, self.tx_group, setv=ptrn_39_31)
        self.phy.SLICE_CTRL_00D4_47_40(self.tx_die, self.tx_group, setv=ptrn_47_40)
        self.phy.SLICE_CTRL_00D8_55_48(self.tx_die, self.tx_group, setv=ptrn_55_48)
        self.phy.SLICE_CTRL_00DC_63_56(self.tx_die, self.tx_group, setv=ptrn_63_56)
        self.phy.SLICE_CTRL_00E0_rd3_rd0(self.tx_die, self.tx_group, setv=ptrn_rd3_rd0)
        self.phy.SLICE_CTRL_3350_vldrd_vld(
            self.tx_die, self.tx_group, setv=ptrn_vldrd_vld
        )

        # dieA rx
        self.phy.SLICE_CTRL_0100_07_00(self.tx_die, self.tx_group, setv=ptrn_07_00)
        self.phy.SLICE_CTRL_0104_15_08(self.tx_die, self.tx_group, setv=ptrn_15_08)
        self.phy.SLICE_CTRL_0108_23_16(self.tx_die, self.tx_group, setv=ptrn_23_16)
        self.phy.SLICE_CTRL_010C_31_24(self.tx_die, self.tx_group, setv=ptrn_31_24)
        self.phy.SLICE_CTRL_0110_39_32(self.tx_die, self.tx_group, setv=ptrn_39_31)
        self.phy.SLICE_CTRL_0114_47_40(self.tx_die, self.tx_group, setv=ptrn_47_40)
        self.phy.SLICE_CTRL_0118_55_48(self.tx_die, self.tx_group, setv=ptrn_55_48)
        self.phy.SLICE_CTRL_011C_63_56(self.tx_die, self.tx_group, setv=ptrn_63_56)
        # self.phy.SLICE_CTRL_0120_rd3_rd0(self.tx_die, self.tx_group, setv=ptrn_rd3_rd0)
        # self.phy.SLICE_CTRL_0360_vldrd_vld(self.tx_die, self.tx_group, setv=ptrn_vldrd_vld)

        # dieB tx
        self.phy.SLICE_CTRL_00C0_07_00(self.rx_die, self.rx_group, setv=ptrn_07_00)
        self.phy.SLICE_CTRL_00C4_15_08(self.rx_die, self.rx_group, setv=ptrn_15_08)
        self.phy.SLICE_CTRL_00C8_23_16(self.rx_die, self.rx_group, setv=ptrn_23_16)
        self.phy.SLICE_CTRL_00CC_31_24(self.rx_die, self.rx_group, setv=ptrn_31_24)
        self.phy.SLICE_CTRL_00D0_39_32(self.rx_die, self.rx_group, setv=ptrn_39_31)
        self.phy.SLICE_CTRL_00D4_47_40(self.rx_die, self.rx_group, setv=ptrn_47_40)
        self.phy.SLICE_CTRL_00D8_55_48(self.rx_die, self.rx_group, setv=ptrn_55_48)
        self.phy.SLICE_CTRL_00DC_63_56(self.rx_die, self.rx_group, setv=ptrn_63_56)
        self.phy.SLICE_CTRL_00E0_rd3_rd0(self.rx_die, self.rx_group, setv=ptrn_rd3_rd0)
        self.phy.SLICE_CTRL_3350_vldrd_vld(
            self.rx_die, self.rx_group, setv=ptrn_vldrd_vld
        )

        # dieB rx
        self.phy.SLICE_CTRL_0100_07_00(self.rx_die, self.rx_group, setv=ptrn_07_00)
        self.phy.SLICE_CTRL_0104_15_08(self.rx_die, self.rx_group, setv=ptrn_15_08)
        self.phy.SLICE_CTRL_0108_23_16(self.rx_die, self.rx_group, setv=ptrn_23_16)
        self.phy.SLICE_CTRL_010C_31_24(self.rx_die, self.rx_group, setv=ptrn_31_24)
        self.phy.SLICE_CTRL_0110_39_32(self.rx_die, self.rx_group, setv=ptrn_39_31)
        self.phy.SLICE_CTRL_0114_47_40(self.rx_die, self.rx_group, setv=ptrn_47_40)
        self.phy.SLICE_CTRL_0118_55_48(self.rx_die, self.rx_group, setv=ptrn_55_48)
        self.phy.SLICE_CTRL_011C_63_56(self.rx_die, self.rx_group, setv=ptrn_63_56)
        # self.phy.SLICE_CTRL_0120_rd3_rd0(self.rx_die, self.rx_group, setv=ptrn_rd3_rd0)
        # self.phy.SLICE_CTRL_0360_vldrd_vld(self.rx_die, self.rx_group, setv=ptrn_vldrd_vld)

        # 31 to 00
        mask_31_00_arr = []
        for i in range(32):  # mask / type / pattern
            buffer = ((lane_set_arr[31 - i]).split("/"))[0]
            mask_31_00_arr.append(buffer)
        mask_31_00_val = "".join(mask_31_00_arr)
        mask_31_00_hex = str(hex(int(mask_31_00_val, 2)))

        # 63 to 31
        mask_63_32_arr = []
        for i in range(32):  # mask / type / pattern
            buffer = ((lane_set_arr[63 - i]).split("/"))[0]
            mask_63_32_arr.append(buffer)
        mask_63_32_val = "".join(mask_63_32_arr)
        mask_63_32_hex = str(hex(int(mask_63_32_val, 2)))

        # 63 to 31
        mask_69_64_arr = []
        for i in range(6):  # mask / type / pattern
            buffer = ((lane_set_arr[69 - i]).split("/"))[0]
            mask_69_64_arr.append(buffer)
        mask_69_64_val = "".join(mask_69_64_arr)
        mask_69_64_hex = str(hex(int(mask_69_64_val, 2)))

        # dieA rx mask
        self.phy.rg_rxpmad_BIST_MASK_31_00(
            self.tx_die, self.tx_group, setv=mask_31_00_hex
        )
        self.phy.rg_rxpmad_BIST_MASK_63_32(
            self.tx_die, self.tx_group, setv=mask_63_32_hex
        )
        self.phy.rg_rxpmad_BIST_MASK_69_64(
            self.tx_die, self.tx_group, setv=mask_69_64_hex
        )

        # dieB rx mask
        self.phy.rg_rxpmad_BIST_MASK_31_00(
            self.rx_die, self.rx_group, setv=mask_31_00_hex
        )
        self.phy.rg_rxpmad_BIST_MASK_63_32(
            self.rx_die, self.rx_group, setv=mask_63_32_hex
        )
        self.phy.rg_rxpmad_BIST_MASK_69_64(
            self.rx_die, self.rx_group, setv=mask_69_64_hex
        )

    def avdd_sense(self, **kargs):
        mode = kargs.get("mode", "")
        voltage_sense_avdd = float(kargs.get("voltage_sense_avdd", 0.75))

        getattr(self, mode)()  # run Mx_mode()

        self.phy.cfg_rext_mode(self.tx_die, self.tx_group, setv="0x6")
        self.phy.cfg_rext_mode(self.rx_die, self.rx_group, setv="0x6")
        self.phy.cfg_tp_sel(self.tx_die, self.tx_group, setv="0x2")
        self.phy.cfg_tp_sel(self.rx_die, self.rx_group, setv="0x2")
        Data_log = self.visa.Keysight_DataLog_793_101_104(
            visa="USB0::0x2A8D::0x5101::MY58014090::0::INSTR"
        )
        avdd = Data_log[3]
        self.phy.cfg_tp_sel(self.tx_die, self.tx_group, setv="0x3")
        self.phy.cfg_tp_sel(self.rx_die, self.rx_group, setv="0x3")
        Data_log = self.visa.Keysight_DataLog_793_101_104(
            visa="USB0::0x2A8D::0x5101::MY58014090::0::INSTR"
        )
        avss = Data_log[3]
        meas_voltage = avdd - avss
        sense_voltage = voltage_sense_avdd + (voltage_sense_avdd - meas_voltage)
        if meas_voltage < 0.5:
            print("Chip Voltage Sense Function Failed(Sense Voltage < 0.5V)")
        else:
            print(
                f"Chip Internal Voltage Value={meas_voltage}V / Sense Voltage={sense_voltage}",
                flush=True,
            )
            # self.phy_0.TPSM831D31_VoltageSet(0x1, 'CHA', volt)  # VDD
            # self.phy_0.TPSM831D31_VoltageSet(0x1, 'CHB', volt)  # IOVDD
            self.phy.TPSM831D31_VoltageSet(0x2, "CHA", sense_voltage)  # D0_AVDD_V2
            # self.phy_0.TPSM831D31_VoltageSet(0x2, 'CHB', volt)  # D0_AVDD12_V2
            self.phy.TPSM831D31_VoltageSet(
                0x4, "CHA", sense_voltage
            )  # D0_AVDD_V1_D1_V1
            # self.phy_0.TPSM831D31_VoltageSet(0x4, 'CHB', volt)  # D0_AVDD12_V1_D1_V1
            self.phy.TPSM831D31_VoltageSet(
                0x8, "CHA", sense_voltage
            )  # D1_AVDD_V2_D2_V1
            # self.phy_0.TPSM831D31_VoltageSet(0x8, 'CHB', volt)  # D1_AVDD12_V2_D2_V1
            self.phy.TPSM831D31_VoltageSet(0x10, "CHA", sense_voltage)  # D2_AVDD_V2
            # self.phy_0.TPSM831D31_VoltageSet(0x10, 'CHB', volt)  # D2_AVDD12_V2
        BF = 0

    """' Subprogram """

    def log_label(self, label, **kargs):
        if self.show == 1:
            print(label, flush=True)
        self.Save_i2cLog(log_name=f"{label}\n")

    def avdd_voltage_sense(self, **kargs):
        mode = kargs.get("mode", "")
        D0_AVDD_V1_D2_V1 = kargs.get("D0_AVDD_V1_D2_V1", 0.75)
        D1_AVDD_V2_D2_V2 = kargs.get("D1_AVDD_V2_D2_V2", 0.75)

        if mode == "M2SN_mode":
            chan_array = ["112", "113"]
            voltage_def = D0_AVDD_V1_D2_V1
        elif mode == "M2EW_mode":
            chan_array = ["114", "117"]
            voltage_def = D1_AVDD_V2_D2_V2
        elif mode == "M2DIE0_2_FLB_mode":
            chan_array = ["112", "113"]
            voltage_def = D0_AVDD_V1_D2_V1
        elif mode == "M2DIE2_0_FLB_mode":
            chan_array = ["112", "113"]
            voltage_def = D0_AVDD_V1_D2_V1
        elif mode == "M2DIE2_1_FLB_mode":
            chan_array = ["114", "117"]
            voltage_def = D1_AVDD_V2_D2_V2
        elif mode == "M2DIE1_2_FLB_mode":
            chan_array = ["114", "117"]
            voltage_def = D1_AVDD_V2_D2_V2
        else:
            pass

        # Pll voltage sense(EVB to Chip ball)

        self.phy.rext_mode(self.tx_die, 0x2)  # cfg_rext_mode Vtune_i
        self.phy.rext_mode(self.rx_die, 0x2)  # cfg_rext_mode Vtune_i

        self.phy.pll_tp_sel_bit2_avdd(self.tx_die, 0x1)  # read avdd voltage
        self.phy.pll_tp_sel_bit2_avdd(self.rx_die, 0x1)  # read avdd voltage
        self.phy.pll_tp_sel_bit1_0_avdd(self.tx_die, 0x2)  # read avdd voltage
        self.phy.pll_tp_sel_bit1_0_avdd(self.rx_die, 0x2)  # read avdd voltage
        pll_avdd = self.visa.Keysight_DataLog_793(chan_array=chan_array)
        self.phy.pll_tp_sel_bit2_avdd(self.tx_die, 0x0)  # read avdd voltage
        self.phy.pll_tp_sel_bit2_avdd(self.rx_die, 0x0)  # read avdd voltage
        self.phy.pll_tp_sel_bit1_0_avdd(self.tx_die, 0x0)  # read avdd voltage
        self.phy.pll_tp_sel_bit1_0_avdd(self.rx_die, 0x0)  # read avdd voltage

        self.phy.pll_tp_sel_bit2_avss(self.tx_die, 0x0)  # read avss voltage
        self.phy.pll_tp_sel_bit2_avss(self.rx_die, 0x0)  # read avss voltage
        self.phy.pll_tp_sel_bit1_0_avss(self.tx_die, 0x1)  # read avss voltage
        self.phy.pll_tp_sel_bit1_0_avss(self.rx_die, 0x1)  # read avss voltage
        pll_avss = self.visa.Keysight_DataLog_793(chan_array=chan_array)
        self.phy.pll_tp_sel_bit2_avss(self.tx_die, 0x0)  # read avss voltage
        self.phy.pll_tp_sel_bit2_avss(self.rx_die, 0x0)  # read avss voltage
        self.phy.pll_tp_sel_bit1_0_avss(self.tx_die, 0x0)  # read avss voltage
        self.phy.pll_tp_sel_bit1_0_avss(self.rx_die, 0x0)  # read avss voltage

        pll_avdd_avg = ((pll_avdd[0] - pll_avss[0]) + (pll_avdd[1] - pll_avss[1])) / 2
        pll_volt = voltage_def + (voltage_def - pll_avdd_avg)

        # slice voltage sense(EVB to chip ic circuit)
        # self.phy.rext_mode(self.tx_die, 0x5)
        # self.phy.rext_mode(self.rx_die, 0x5)
        #
        # self.phy.rvdd_voltage_rext_en(self.tx_die, self.tx_group, [0] ,0x1)
        # self.phy.rvdd_voltage_rext_en(self.rx_die, self.rx_group, [0], 0x1)
        # rvdd_s0 = self.visa.Keysight_DataLog_793(chan_array=chan_array)
        # self.phy.rvdd_voltage_rext_en(self.tx_die, self.tx_group, [0] ,0x0)
        # self.phy.rvdd_voltage_rext_en(self.rx_die, self.rx_group, [0], 0x0)
        # self.phy.rvdd_voltage_rext_en(self.tx_die, self.tx_group, [2], 0x1)
        # self.phy.rvdd_voltage_rext_en(self.rx_die, self.rx_group, [2], 0x1)
        # rvdd_s2 = self.visa.Keysight_DataLog_793(chan_array=chan_array)
        # self.phy.rvdd_voltage_rext_en(self.tx_die, self.tx_group, [2], 0x0)
        # self.phy.rvdd_voltage_rext_en(self.rx_die, self.rx_group, [2], 0x0)
        #
        # self.phy.avdd_voltage_rext_en(self.tx_die, self.tx_group, [0] ,0x2)
        # self.phy.avdd_voltage_rext_en(self.rx_die, self.rx_group, [0], 0x2)
        # avdd_s0 = self.visa.Keysight_DataLog_793(chan_array=chan_array)
        # self.phy.avdd_voltage_rext_en(self.tx_die, self.tx_group, [0] ,0x0)
        # self.phy.avdd_voltage_rext_en(self.rx_die, self.rx_group, [0], 0x0)
        # self.phy.avdd_voltage_rext_en(self.tx_die, self.tx_group, [2], 0x2)
        # self.phy.avdd_voltage_rext_en(self.rx_die, self.rx_group, [2], 0x2)
        # avdd_s2 = self.visa.Keysight_DataLog_793(chan_array=chan_array)
        # self.phy.avdd_voltage_rext_en(self.tx_die, self.tx_group, [2], 0x0)
        # self.phy.avdd_voltage_rext_en(self.rx_die, self.rx_group, [2], 0x0)
        #
        # self.phy.avss_voltage_rext_en(self.tx_die, self.tx_group, [0], 0x3)
        # self.phy.avss_voltage_rext_en(self.tx_die, self.tx_group, [0], 0x3)
        # avss_s0 = self.visa.Keysight_DataLog_793(chan_array=chan_array)
        # self.phy.avss_voltage_rext_en(self.tx_die, self.tx_group, [0], 0x0)
        # self.phy.avss_voltage_rext_en(self.tx_die, self.tx_group, [0], 0x0)
        # self.phy.avss_voltage_rext_en(self.rx_die, self.rx_group, [2], 0x3)
        # self.phy.avss_voltage_rext_en(self.rx_die, self.rx_group, [2], 0x3)
        # avss_s2 = self.visa.Keysight_DataLog_793(chan_array=chan_array)
        # self.phy.avss_voltage_rext_en(self.rx_die, self.rx_group, [2], 0x0)
        # self.phy.avss_voltage_rext_en(self.rx_die, self.rx_group, [2], 0x0)
        #
        # avdd_avg = ((avdd_s0[0]-avss_s0[0])+(avdd_s0[1]-avss_s0[1])+(avdd_s2[0]-avss_s2[0])+(avdd_s2[1]-avss_s2[1]))/4
        # volt = voltage_def + (voltage_def - avdd_avg)

        print(
            f"Slice Voltage Sense : Die{self.tx_die} (PLL)AVDD Slice0 Voltage={pll_avdd[0]}V , (PLL)AVSS Slice0 Voltage={pll_avss[0]}V",
            flush=True,
        )
        print(
            f"Slice Voltage Sense : Die{self.rx_die} (PLL)AVDD Slice0 Voltage={pll_avdd[1]}V , (PLL)AVSS Slice0 Voltage={pll_avss[1]}V",
            flush=True,
        )
        # print(f'Slice Voltage Sense : Die{self.tx_die} RVDD Slice0 Voltage={rvdd_s0[0]} AVDD Slice0 Voltage={avdd_s0[0]}V , AVSS Slice0 Voltage={avss_s0[0]}V', flush=True)
        # print(f'Slice Voltage Sense : Die{self.rx_die} RVDD Slice0 Voltage={rvdd_s0[1]} AVDD Slice0 Voltage={avdd_s0[1]}V , AVSS Slice0 Voltage={avss_s0[1]}V', flush=True)
        # print(f'Slice Voltage Sense : Die{self.tx_die} RVDD Slice0 Voltage={rvdd_s2[0]} AVDD Slice2 Voltage={avdd_s2[0]}V , AVSS Slice2 Voltage={avss_s2[0]}V', flush=True)
        # print(f'Slice Voltage Sense : Die{self.rx_die} RVDD Slice0 Voltage={rvdd_s2[1]} AVDD Slice2 Voltage={avdd_s2[1]}V , AVSS Slice2 Voltage={avss_s2[1]}V', flush=True)

        if pll_volt > 1 or pll_volt < 0.5:
            print(f"\033Voltage Sense FAIL")
            pass
        else:
            if (
                mode == "M2SN_mode"
                or mode == "M2DIE2_0_FLB_mode"
                or mode == "M2DIE0_2_FLB_mode"
            ):
                self.phy.D0_AVDD_V1_D2_V1_set(pll_volt)
                print(
                    f"D0_AVDD_V1_D2_V1(PMIC) Sense Voltage(PLL) = {pll_volt}",
                    flush=True,
                )
            elif (
                mode == "M2EW_mode"
                or mode == "M2DIE2_1_FLB_mode"
                or mode == "M2DIE1_2_FLB_mode"
            ):
                self.phy.D1_AVDD_V2_D2_V2_set(pll_volt)
                print(
                    f"D1_AVDD_V2_D2_V2(PMIC) Sense Voltage(PLL) = {pll_volt}",
                    flush=True,
                )
            else:
                pass

    def zero_seach(self, zero_seach):
        if zero_seach[:1] == "1":
            for i in range(99):
                if zero_seach[i : i + 1] == "0":
                    break
                else:
                    pass
            for o in range(99):
                if zero_seach[o + i : o + i + 1] == "1":
                    break
                else:
                    pass
            zero_num = o
        else:
            for i in range(99):
                if zero_seach[i : i + 1] == "1":
                    break
                else:
                    pass
            for o in range(99):
                if zero_seach[o + i : o + i + 1] == "0":
                    break
                else:
                    pass
            for p in range(99):
                if zero_seach[o + p + i : o + p + i + 1] == "1":
                    break
                else:
                    pass
            zero_num = p
        return zero_num

    def sub_window(self):
        import tkinter as tk

        root = tk.Tk()
        root.title("my window")
        root.geometry("200x150")
        mybutton = tk.Button(root, text="EXIT")
        mybutton.pack()
        root.mainloop()
        print("\n")

    def even_message(self, **kargs):
        mode = "M4_D0V_D1V_mode"
        getattr(self, mode)()  # run Mx_mode()

        app = tk.Tk()
        radioValue = tk.IntVar()
        app.title("Even Message")
        app.geometry("+50+50")
        rdio_1 = tk.Radiobutton(
            app,
            variable=radioValue,
            value=0,
            text="Check M4_D0V_D1V_mode Die0 Pi Status 100 times",
        )
        rdio_2 = tk.Radiobutton(
            app,
            variable=radioValue,
            value=1,
            text="Check M4_D0V_D1V_mode Die1 Pi Status 100 times",
        )
        rdio_3 = tk.Radiobutton(
            app,
            variable=radioValue,
            value=2,
            text="Check M4_D0V_D1V_mode Die0 Pi Status 1000 times",
        )
        rdio_4 = tk.Radiobutton(
            app,
            variable=radioValue,
            value=3,
            text="Check M4_D0V_D1V_mode Die0 Pi Status 1000 times",
        )
        rdio_5 = tk.Radiobutton(
            app, variable=radioValue, value=4, text="Skip This Window"
        )
        button_1 = tk.Button(app, text="Run", command=app.destroy)

        rdio_1.grid(column=0, row=0, sticky="W")
        rdio_2.grid(column=0, row=1, sticky="W")
        rdio_3.grid(column=0, row=2, sticky="W")
        rdio_4.grid(column=0, row=3, sticky="W")
        rdio_5.grid(column=0, row=4, sticky="W")
        button_1.grid(column=0, row=5, sticky="W")
        app.mainloop()

        rdio_val = radioValue.get()
        # print(f'even1  {rdio_val}', flush=True)

        if rdio_val == 0:
            self.Read_pi_status_die0_V(100)
        elif rdio_val == 1:
            self.Read_pi_status_die1_V(100)
        elif rdio_val == 2:
            self.Read_pi_status_die0_V(1000)
        elif rdio_val == 3:
            self.Read_pi_status_die1_V(1000)
        else:
            rdio_val = -1
        return rdio_val

    def Save_i2cLog(self, **kargs):
        content = kargs.get("log_name", "NA")

        textfile = open("TestTools/i2c_log.txt", "a+")
        textfile.write(content)
        textfile.close()

    def log_info(self, info):
        self.info = info

    def THM_Value(self, THM_Voltage):
        temp_arr = [
            0.783926,
            0.782122,
            0.780318,
            0.778512,
            0.776705,
            0.774896,
            0.773085,
            0.771273,
            0.769460,
            0.767645,
            0.765828,
            0.764010,
            0.762190,
            0.760369,
            0.758546,
            0.756722,
            0.754896,
            0.753068,
            0.751239,
            0.749408,
            0.747576,
            0.745742,
            0.743907,
            0.742070,
            0.740232,
            0.738392,
            0.736550,
            0.734707,
            0.732863,
            0.731017,
            0.729169,
            0.727320,
            0.725469,
            0.723617,
            0.721763,
            0.719908,
            0.718051,
            0.716192,
            0.714333,
            0.712471,
            0.710608,
            0.708744,
            0.706878,
            0.705011,
            0.703142,
            0.701272,
            0.699400,
            0.697527,
            0.695652,
            0.693776,
            0.691899,
            0.690020,
            0.688139,
            0.686258,
            0.684374,
            0.682490,
            0.680604,
            0.678716,
            0.676827,
            0.674937,
            0.673046,
            0.671153,
            0.669258,
            0.667363,
            0.665466,
            0.663568,
            0.661668,
            0.659767,
            0.657865,
            0.655961,
            0.654056,
            0.652150,
            0.650243,
            0.648334,
            0.646424,
            0.644513,
            0.642601,
            0.640687,
            0.638772,
            0.636856,
            0.634939,
            0.633020,
            0.631100,
            0.629179,
            0.627257,
            0.625334,
            0.623410,
            0.621484,
            0.619558,
            0.617630,
            0.615701,
            0.613771,
            0.611839,
            0.609907,
            0.607974,
            0.606039,
            0.604104,
            0.602167,
            0.600230,
            0.598291,
            0.596351,
            0.594410,
            0.592468,
            0.590526,
            0.588582,
            0.586637,
            0.584691,
            0.582744,
            0.580796,
            0.578848,
            0.576898,
            0.574947,
            0.572995,
            0.571043,
            0.569089,
            0.567135,
            0.565179,
            0.563223,
            0.561265,
            0.559307,
            0.557348,
            0.555388,
            0.553427,
            0.551466,
            0.549503,
            0.547539,
            0.545575,
            0.543610,
            0.541644,
            0.539677,
            0.537709,
            0.535740,
            0.533771,
            0.531801,
            0.529829,
            0.527858,
            0.525885,
            0.523911,
            0.521937,
            0.519962,
            0.517986,
            0.516009,
            0.514032,
            0.512053,
            0.510074,
            0.508094,
            0.506114,
            0.504132,
            0.502150,
            0.500167,
            0.498183,
            0.496199,
            0.494214,
            0.492228,
            0.490241,
            0.488253,
            0.486265,
            0.484276,
            0.482287,
            0.480296,
            0.478305,
            0.476313,
            0.474320,
            0.472327,
            0.470333,
            0.468338,
            0.466342,
            0.464346,
            0.462349,
            0.460351,
            0.458353,
            0.456354,
            0.454354,
            0.452353,
            0.450352,
            0.448350,
            0.446347,
            0.444344,
            0.442339,
            0.440335,
            0.438329,
            0.436322,
            0.434315,
            0.432308,
            0.430299,
            0.428290,
            0.426280,
            0.424269,
            0.422258,
            0.420246,
            0.418233,
            0.416219,
            0.414205,
            0.412190,
            0.410174,
            0.408158,
            0.406141,
            0.404123,
            0.402104,
            0.400085,
            0.398065,
        ]

        for i in range(len(temp_arr)):
            if temp_arr[i] - THM_Voltage <= 0:
                break
            else:
                pass
        thermal_temp = -50 + i
        # print('Done')

        return thermal_temp

    def thermal_voltage_read(self):
        for g in range(1):
            Data_log = self.visa.Keysight_DataLog_793_101_104(
                visa="USB0::0x2A8D::0x5101::MY58014090::0::INSTR"
            )
            v1 = Data_log[0]
            v2 = Data_log[1]
            v3 = Data_log[2]
            self.die0_THM = self.THM_Value(v1)
            self.die1_THM = self.THM_Value(v2)
            self.die2_THM = self.THM_Value(v3)
            print(f"Die0_Thermal Temp Value={self.die0_THM} Degree C", flush=True)
            print(f"Die1_Thermal Temp Value={self.die1_THM} Degree C", flush=True)
            print(f"Die2_Thermal Temp Value={self.die2_THM} Degree C", flush=True)

    def thermal_die_CHK(self):
        self.phy.THM_Check(0x20)
        self.phy.THM_Check(0x40)
        self.phy.THM_Check(0x80)

        for g in range(1):
            Data_log = self.visa.Keysight_DataLog_793_101_104(
                visa="USB0::0x2A8D::0x5101::MY58014090::0::INSTR"
            )
            v1 = Data_log[0]
            v2 = Data_log[1]
            v3 = Data_log[2]
            self.die0_THM = self.THM_Value(v1)
            self.die1_THM = self.THM_Value(v2)
            self.die2_THM = self.THM_Value(v3)
            print(f"Die0_Thermal Temp Value={self.die0_THM} Degree C", flush=True)
            print(f"Die1_Thermal Temp Value={self.die1_THM} Degree C", flush=True)
            print(f"Die2_Thermal Temp Value={self.die2_THM} Degree C", flush=True)

    """' proteantecs """
    """
    if die == 0:
            setv = 0x01
        elif die == 1:
            setv = 0x02
        else:
            setv = 0x04

        self.i2c.write(0x70, setv, 0, 8, setv)

        self.EHOST = [[0x01, 0x02, 0x03],  # Die0 tport/H/V
                      [0x01, 0x02, 0x03],  # Die1 tport/H/V
                      [0x01, 0x02, 0x03]]  # Die3 tport/H/V

        die=0
        slave = self.EHOST[die][1]
        if die == 0:
            setv = 0x01
        elif die == 1:
            setv = 0x02
        else:
            setv = 0x04

        ftn_name = 'cmu_rstn'
        offset = 0x2000
        bit = '31:0'
        self.phy.non_i2c_write.write(0x70, setv, 0, 8, setv)
        self.phy.indirect_write(slave, offset, bit, int(setv, 16), slice_num=-1)
        rbv = self.phy.indirect_read(slave, offset, bit, slice_num=-1)
    """

    def prtn_tca_clk_en(self):
        addr = 0x01002160
        bit = "3:0"
        die = self.die
        slave = self.slave
        val = self.phy.indirect_read(slave, addr, "31:0", slice_num=-1)
        print("TCA enable reg before write to enable bits = ", val)
        self.phy.indirect_write(slave, addr, bit, 0xF, slice_num=-1)
        val = self.phy.indirect_read(slave, addr, "31:0", slice_num=-1)
        print("TCA enable reg after write to enable bits= ", val)
        """
        addr = 0x02002160
        val = self.phy.indirect_read(slave, addr, '31:0', slice_num=-1)
        print('TCA enable reg before write to enable bits = ', val)
        self.phy.indirect_write(slave, addr, bit, 0xf, slice_num=-1)
        val = self.phy.indirect_read(slave, addr, '31:0', slice_num=-1)
        print('TCA enable reg after write to enable bits= ', val)

        
        addr = 0x01042160
        val = self.phy.indirect_read(slave, addr, '31:0', slice_num=-1)
        print('TCA enable reg before write to enable bits = ', val)
        self.phy.indirect_write(slave, addr, bit, 0xf, slice_num=-1)
        val = self.phy.indirect_read(slave, addr, '31:0', slice_num=-1)
        print('TCA enable reg after write to enable bits= ', val)

        addr = 0x02042160
        val = self.phy.indirect_read(slave, addr, '31:0', slice_num=-1)
        print('TCA enable reg before write to enable bits = ', val)
        self.phy.indirect_write(slave, addr, bit, 0xf, slice_num=-1)
        val = self.phy.indirect_read(slave, addr, '31:0', slice_num=-1)
        print('TCA enable reg after write to enable bits= ', val)
        """

    def prtn_reg_read(self, addr, **kwargs):
        # slave = self.EHOST[self.die][self.group]
        # self.die_sel(die=self.die)
        # val = self.indirect_read(slave, self.prtn_offset + addr , 0, slice_num=-1)
        bit = "31:0"
        die = self.die
        slave = self.slave
        val = self.phy.indirect_read(slave, self.prtn_offset + addr, bit, slice_num=-1)
        return val

    def prtn_reg_write(self, addr, data, **kwargs):
        # slave = self.EHOST[self.die][self.group]
        # self.die_sel(die=self.die)
        # self.indirect_write(slave, self.prtn_offset + addr , 0 , int(data, 32), slice_num=-1)
        bit = "31:0"
        die = self.die
        slave = self.slave
        self.phy.indirect_write(slave, self.prtn_offset + addr, bit, data, slice_num=-1)

    def prtn_tca_unit_reg_cfg(self, block_idx, unit_reg_addr, data):
        config_data = 0x00000000
        config_data = (
            config_data
            | (block_idx << 22)
            | (unit_reg_addr & 0x1F) << 17
            | (data & 0xFFFF)
        )
        self.prtn_reg_write(0x48, config_data)  # command config
        self.prtn_info(
            f"Writing to TCA unit: {block_idx}, config_reg: {hex(unit_reg_addr)}, data: {hex(data)}, val: {hex(config_data)}"
        )
        #     + " val = "
        #     + hex(config_data)
        # )

    def prtn_tca_internal_reg_cfg(
        self, block_idx, tca_inter_reg_addr, tca_inter_reg_data
    ):
        self.prtn_tca_unit_reg_cfg(
            block_idx, 10, ((tca_inter_reg_addr & 0x1F) << 10) | 0x3FF
        )
        self.prtn_tca_unit_reg_cfg(block_idx, 17, tca_inter_reg_data)

    def prtn_tca_read_measure_en(self, block_idx):
        self.prtn_tca_unit_reg_cfg(block_idx, 29, (3 << 2))

    def prtn_qdca_osc_cfg(self, block_idx, include_dly_line, base_delay, fine_delay):
        tca_inter_reg_addr = 10
        tca_inter_reg_data = (
            0x1 << 15
            | (include_dly_line & 0x1) << 14
            | 0x3 << 9
            | (fine_delay & 0xF) << 5
            | (base_delay & 0x1F)
        )
        self.prtn_tca_internal_reg_cfg(
            block_idx, tca_inter_reg_addr, tca_inter_reg_data
        )

    def prtn_config_block(self, block_idx, base_delay, EW):
        tca_inter_reg_addr = 6
        tca_inter_reg_data = (base_delay & 0x1F) << 3
        self.prtn_tca_internal_reg_cfg(
            block_idx, tca_inter_reg_addr, tca_inter_reg_data
        )

        tca_inter_reg_addr = 3
        tca_inter_reg_data = 1 << 7 | (base_delay & 0x1F)
        self.prtn_tca_internal_reg_cfg(
            block_idx, tca_inter_reg_addr, tca_inter_reg_data
        )

        tca_inter_reg_addr = 5
        tca_inter_reg_data = 1 << 7 | 1 << 6 | 1 << 5 | (base_delay & 0x1F)
        self.prtn_tca_internal_reg_cfg(
            block_idx, tca_inter_reg_addr, tca_inter_reg_data
        )

        if EW == 1:
            M1_edge_0 = 0x0
            M1_edge_1 = 0x0
            M2_edge_0 = 0x0
            M2_edge_1 = 0x3

        elif EW == 2:
            M1_edge_0 = 0x1
            M1_edge_1 = 0x1
            M2_edge_0 = 0x1
            M2_edge_1 = 0x0

        elif EW == 3:
            M1_edge_0 = 0x2
            M1_edge_1 = 0x2
            M2_edge_0 = 0x2
            M2_edge_1 = 0x1

        elif EW == 4:
            M1_edge_0 = 0x3
            M1_edge_1 = 0x3
            M2_edge_0 = 0x3
            M2_edge_1 = 0x2

        else:
            print("ERROR")
            exit

        tca_inter_reg_addr = 2
        tca_inter_reg_data = (
            (0xF << 4) | (M1_edge_0 & 0x3) << 8 | (M1_edge_1 & 0x3) << 10
        )
        self.prtn_tca_internal_reg_cfg(
            block_idx, tca_inter_reg_addr, tca_inter_reg_data
        )

        tca_inter_reg_addr = 4
        tca_inter_reg_data = (
            (0xF << 4) | (M2_edge_0 & 0x3) << 8 | (M2_edge_1 & 0x3) << 10
        )
        self.prtn_tca_internal_reg_cfg(
            block_idx, tca_inter_reg_addr, tca_inter_reg_data
        )

    def prtn_read_data_cmd(self, unit_id):
        self.prtn_reg_write(0x44, unit_id)  # command read

    def prtn_global_config(self):
        self.prtn_info("In prtn_global_config")
        self.chip_id1 = 1
        self.chip_id2 = 2
        cfg = [
            [0, 0x00010032],  # fc_clocking
            [0xC, self.chip_id1],  # chipid0
            [0x10, self.chip_id2],  # chipid1
            [0x08, 0x00000001],  # control_word
            [0x3C, 0x00000001],  # cmd_ping
        ]
        for idx in range(len(cfg)):
            # Marked print(f'ryan2 {idx}')
            self.prtn_reg_write(cfg[idx][0], cfg[idx][1])
        # Marked print("0xc value = ",self.prtn_reg_read(0xc))
        # Marked print("0x10 value = ",self.prtn_reg_read(0x10))

    def prtn_read_data(self, expected_count, expected_wait, unit_id):
        self.prtn_read_data_cmd(unit_id)
        naknik = ""
        for idx in range(len(expected_count)):
            # self.prtn_info('Before sleep')
            # time.sleep(expected_wait[idx])
            time.sleep(0.1)
            # self.prtn_info('After sleep')
            read_data_b = int(self.prtn_reg_read(self.prtn_fifo_count_address), 16)
            # Marked print(f'read_data_b = {hex(read_data_b)}')
            fifo_cnt = (
                int(self.prtn_reg_read(self.prtn_fifo_count_address), 0) >> 6
            ) & 0x3F

            if fifo_cnt != expected_count[idx]:
                self.prtn_error(
                    "Expected "
                    + str(expected_count[idx])
                    + " entries in fifo , received "
                    + str(fifo_cnt)
                )
            else:
                self.prtn_info(
                    "Expected and got " + str(expected_count[idx]) + " entries in fifo"
                )
            for idx2 in range(fifo_cnt):
                val = self.prtn_reg_read(self.prtn_fifo_read_address)
                val = val[2:].zfill(8)
                # self.prtn_info("Received " + val +" from fifo")
                naknik += val

                # self.prtn_info('Before sleep 1 sec')
        time.sleep(0.1)
        # self.prtn_info('After sleep 1 sec')
        fifo_cnt = (
            int(self.prtn_reg_read(self.prtn_fifo_count_address), 0) >> 6
        ) & 0x3F
        if fifo_cnt != 0:
            self.prtn_error(str(fifo_cnt) + " still remain in FIFO")
            for idx2 in range(fifo_cnt):
                val = self.prtn_reg_read(self.prtn_fifo_read_address)
                val = val[2:].zfill(8)
                # self.prtn_info("Received " + val +" from fifo")
                naknik += val
        return naknik

    def prtn_start_measure(self):
        self.prtn_reg_write(0x30, 0x1)  # command measure

    def prtn_stop_measure(self, block_idx):
        self.prtn_info("Stop TCA measure")
        self.prtn_tca_unit_reg_cfg(block_idx, 23, 0xFFFF)
        # config_data = 0x00000000
        # config_data = (config_data | (0x3ff << 22) | 23 << 17 | 0xffff) #1<<5
        # self.prtn_reg_write(0x48, config_data)  # command config
        # self.prtn_info('Writing to TCA unit config_reg  , val = ' + hex(config_data))

    def prtn_info(self, msg):
        sys.stdout.write(
            "PRTN_INFO (" + str(datetime.datetime.now()) + "): " + msg + "\n"
        )
        sys.stdout.flush()

    def prtn_error(self, msg):
        sys.stdout.write(
            "PRTN_ERROR (" + str(datetime.datetime.now()) + "): " + msg + "\n"
        )
        sys.stdout.flush()

    def proteantecs_single_readout(self, mode):
        """
        Single readout version of proteantecs for CLI tool
        Runs 4 readouts per block (one for each EW configuration)
        Total: 4 blocks × 4 EW configs = 16 readouts per die
        """
        self.prtn_offset = 0x40000
        self.tca_inter_reg_addr = 0x0
        self.expected_count = [31, 31, 31, 31, 31, 31, 31, 31, 13]
        self.expected_wait = 0
        self.prtn_fifo_read_address = 0x24
        self.prtn_fifo_count_address = 0x28

        block_idx_range = range(4)  # 4 blocks: S0, S1, S2, S3

        # Single configuration for CLI tool
        cfg = 0x1E  # Use first configuration
        EW_range = [1, 2, 3, 4]  # 4 EW configurations
        qdca_osc_bypass_cfg = [0, 0]  # Single QDCA configuration
        num_of_iterations = 1  # Single iteration per configuration

        top_id = 0

        if mode == 0:
            dies_and_group_range = [{"die": 0, "group": 2}, {"die": 1, "group": 2}]
        elif mode == 1:
            dies_and_group_range = [{"die": 1, "group": 1}, {"die": 2, "group": 2}]

        for die_and_group in dies_and_group_range:
            # set die and group
            print("Working on: ", die_and_group)
            self.die = die_and_group["die"]
            self.slave = self.EHOST[die_and_group["die"]][die_and_group["group"]]
            self.phy.die_sel(die=self.die)
            print("Enable TCA clock to Block Controllers \n")
            self.prtn_tca_clk_en()
            print("After enabling TCA clock to Block Controllers \n")
            self.prtn_global_config()

            # Enable read/measure for all blocks
            for block_idx in block_idx_range:
                self.prtn_tca_read_measure_en(block_idx)

            # Run single readout for each EW configuration
            for EW in EW_range:
                print(f"Running EW configuration {EW}...")

                # Configure all blocks for this EW
                for block_idx in block_idx_range:
                    self.prtn_config_block(block_idx, cfg, EW)
                    self.prtn_qdca_osc_cfg(
                        block_idx=block_idx,
                        include_dly_line=qdca_osc_bypass_cfg[0],
                        base_delay=cfg,
                        fine_delay=qdca_osc_bypass_cfg[1],
                    )

                # Single iteration for this EW configuration
                for idx_iter in range(num_of_iterations):
                    self.prtn_reg_write(0x34, 0x1)  # broadcast_state
                    val = self.prtn_reg_read(0x6C)  # became_busy
                    print("Became_busy before Start : ", val)

                    # measure command
                    self.prtn_start_measure()
                    self.phy.TX_PCS_BIST_RUN(
                        self.tx_die,
                        self.tx_group,
                        slice=self.tx_slice,
                        setv="0x1",
                    )
                    self.phy.TX_PCS_BIST_RUN(
                        self.rx_die,
                        self.rx_group,
                        slice=self.rx_slice,
                        setv="0x1",
                    )
                    self.phy.die_sel(die=self.die)

                    time.sleep(0.1)

                    # Stop measurement for all blocks
                    for block_idx in block_idx_range:
                        self.prtn_stop_measure(block_idx)
                    self.prtn_reg_write(0x34, 0x1)  # broadcast_state

                    # Read all blocks one by one
                    for block_idx in block_idx_range:
                        naknik = self.prtn_read_data(
                            self.expected_count, self.expected_wait, block_idx
                        )

                        self.prtn_info(
                            "TCA_Naknik_params:die,slave,top_id,block_idx,cfg,EW,idx_iter,readout"
                        )
                        self.prtn_info(
                            "TCA_Naknik_output:"
                            + str(self.die)
                            + ","
                            + str(self.slave)
                            + ","
                            + str(top_id)
                            + ","
                            + str(block_idx)
                            + ","
                            + str(cfg)
                            + ","
                            + str(EW)
                            + ","
                            + str(idx_iter)
                            + ","
                            + naknik
                        )

                        val = int(self.prtn_reg_read(0x5C), 16)
                        if (val & 0x00000001) != 0x000000001:
                            self.prtn_error("Readout not ended")
                        self.prtn_reg_write(0x8, 5)
                        self.prtn_reg_write(0x8, 1)

                print(f"Completed EW configuration {EW}")

            print(f"Completed all EW configurations for die {self.die}")

    def proteantecs(self, mode):
        self.prtn_offset = 0x40000
        self.tca_inter_reg_addr = 0x0
        self.expected_count = [31, 31, 31, 31, 31, 31, 31, 31, 13]
        self.expected_wait = 0
        self.prtn_fifo_read_address = 0x24
        self.prtn_fifo_count_address = 0x28

        block_idx_range = range(
            4
        )  # 42*4=168, S0:42,S1:42,S2:42,S3:42,S4:42,S5:42,S6:42,S7:42
        # block_idx_range = [0]

        # vref_tx_phy_range = [0x20]
        # vref_rx_phy_range = [0x20]
        # ds_rx_phy_range = [0x3]
        # ds_tx_phy_range = [0x3]

        cfg_range = [
            0x1E,
            0xE,
            0x5,
            0x2,
            0x1,
            0x0,
        ]  # 1_1110, 01110, 00110, 00010, 00001, 00000
        # cfg_range = [0x1e, 0xe, 0x5]
        # cfg_range = [0x0]
        EW_range = [1, 2, 3, 4]
        # EW_range = [1]
        """
        vddio = self.io_v
        vdd_core = self.core_v
        process = self.process
        unit_id = self.id
        freq_val = self.rate
        top_id = self.top_id
        """

        top_id = 0

        # sys_clk = 50
        # mbist_type = "l_write_l_read"

        # temperature = 25
        # clock_pattern = 0  # When 1 - BIST will run clock define pattern. When 0 - LFSR

        # qdca_osc_cfg_range = range(16)
        # qdca_osc_bypass_cfg_range = [[1,item] for item in qdca_osc_cfg_range]
        # qdca_osc_bypass_cfg_range.insert(0,[0,0])
        qdca_osc_bypass_cfg_range = [[0, 0]]

        num_of_iterations = 10
        """
        dies_and_group_range = [
            #{'die': 0, 'group': 2},
            #{'die': 1, 'group': 2},
            #{'die': 1, 'group': 1},
            {'die': 2, 'group': 2}
        ]
        """
        if mode == 0:
            dies_and_group_range = [{"die": 0, "group": 2}, {"die": 1, "group": 2}]
        elif mode == 1:
            dies_and_group_range = [{"die": 1, "group": 1}, {"die": 2, "group": 2}]

        for die_and_group in dies_and_group_range:
            # set die and group
            print("Working on: ", die_and_group)
            self.die = die_and_group["die"]
            self.slave = self.EHOST[die_and_group["die"]][die_and_group["group"]]
            self.phy.die_sel(die=self.die)
            print("Enable TCA clock to Block Controllers \n")
            self.prtn_tca_clk_en()
            print("After enabling TCA clock to Block Controllers \n")
            self.prtn_global_config()
            for block_idx in block_idx_range:
                self.prtn_tca_read_measure_en(block_idx)

            for cfg in cfg_range:
                for EW in EW_range:
                    for qdca_osc in qdca_osc_bypass_cfg_range:
                        # all blocks configuration
                        for block_idx in block_idx_range:
                            self.prtn_config_block(block_idx, cfg, EW)
                            self.prtn_qdca_osc_cfg(
                                block_idx=block_idx,
                                include_dly_line=qdca_osc[0],
                                base_delay=cfg,
                                fine_delay=qdca_osc[1],
                            )
                        # for block_idx in block_idx_range:
                        for idx_iter in range(num_of_iterations):
                            self.prtn_reg_write(0x34, 0x1)  # broadcast_state
                            val = self.prtn_reg_read(0x6C)  # became_busy
                            print("Became_busy before Start : ", val)
                            # measure command
                            self.prtn_start_measure()
                            self.phy.TX_PCS_BIST_RUN(
                                self.tx_die,
                                self.tx_group,
                                slice=self.tx_slice,
                                setv="0x1",
                            )
                            self.phy.TX_PCS_BIST_RUN(
                                self.rx_die,
                                self.rx_group,
                                slice=self.rx_slice,
                                setv="0x1",
                            )
                            self.phy.die_sel(die=self.die)

                            for block_idx in block_idx_range:
                                self.prtn_stop_measure(block_idx)
                            self.prtn_reg_write(0x34, 0x1)  # broadcast_state
                            # val = self.prtn_reg_read(0x70)  # measure_ended
                            # print('Measure_ended after Stop : ', val)

                            # read all blocks one by one
                            for block_idx in block_idx_range:
                                naknik = self.prtn_read_data(
                                    self.expected_count, self.expected_wait, block_idx
                                )
                                # Marked print(f'naknik={naknik},type={type(naknik)}')
                                self.prtn_info(
                                    "TCA_Naknik_params:die,slave,top_id,block_idx,cfg,EW,idx_iter,readout"
                                )
                                self.prtn_info(
                                    "TCA_Naknik_output:"
                                    + str(self.die)
                                    + ","
                                    + str(self.slave)
                                    + ","
                                    + str(top_id)
                                    + ","
                                    + str(block_idx)
                                    + ","
                                    + str(cfg)
                                    + ","
                                    + str(EW)
                                    + ","
                                    + str(idx_iter)
                                    + ","
                                    + naknik
                                )

                                val = int(self.prtn_reg_read(0x5C), 16)
                                if (val & 0x00000001) != 0x000000001:
                                    self.prtn_error("Readout not ended")
                                # print(f'4')
                                self.prtn_reg_write(0x8, 5)
                                # print(f'5')
                                self.prtn_reg_write(0x8, 1)
