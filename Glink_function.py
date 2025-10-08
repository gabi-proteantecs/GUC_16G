import datetime

import pyvisa
from tabulate import tabulate

from Glink_run import UCIe_2p5D
from Instrument import D2D_Subprogram


class UCIe_2p5D:
    def __init__(self, phy, gui):
        self.phy = phy
        self.gui = gui
        self.run = UCIe_2p5D
        self.visa = D2D_Subprogram(self.gui)
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
        self.slice_offset = 0x10000
        self.GROUP_NUM = {0: "TPORT", 1: "H", 2: "V"}

    def Specialized_0(self):
        # gui_value = self.gui.Corner_Version_wx.Value
        # self.run.ALL_mode()
        self.SRAM()
        # self.IT6300_Output_en()
        # pass

    def PMIC_OTP_REV(self):
        self.phy.non_i2c_write(0x71, 0x1, 0, 8, 0x1)
        buffer = self.phy.non_i2c_read(0x60, 0x1, 0, 8)
        print(f"PMIC OTP EPROM Version {buffer}", flush=True)
        self.phy.non_i2c_write(0x71, 0x00, 0, 8, 0x00)

    def IT6300_Output_en(self):
        visa = "USB0::0xFFFF::0x6300::600068011717630047::0::INSTR"
        rm = pyvisa.ResourceManager()
        IT6300 = rm.open_resource(visa)
        buffer = IT6300.query("*IDN?")
        print(f"Test Instrument ID {buffer}")

    def LR_EN(self, **kargs):
        LR = kargs.get("LR", [])
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
                # self.phy.reg_user_set(die_arr=self.die_arr, group_arr=self.group_arr, tx_slice=[0,1,2,3], rx_slice=[0,1,2,3], reg_arr=hw_non_1, mode=init_mode)
                self.phy.reg_user_set(
                    die_arr=self.die_arr,
                    group_arr=self.group_arr,
                    tx_slice=self.tx_slice,
                    rx_slice=self.rx_slice,
                    reg_arr=LR,
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

        if setup_lane != "NA":
            print("\nEdit Test Pattern and RX Mask", flush=True)
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
            self.phy.SLICE_CTRL_00E0_rd3_rd0(
                self.tx_die, self.tx_group, setv=ptrn_rd3_rd0
            )
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
            self.phy.SLICE_CTRL_0120_rd3_rd0(
                self.tx_die, self.tx_group, setv=ptrn_rd3_rd0
            )
            self.phy.SLICE_CTRL_0360_vldrd_vld(
                self.tx_die, self.tx_group, setv=ptrn_vldrd_vld
            )

            # dieB tx
            self.phy.SLICE_CTRL_00C0_07_00(self.rx_die, self.rx_group, setv=ptrn_07_00)
            self.phy.SLICE_CTRL_00C4_15_08(self.rx_die, self.rx_group, setv=ptrn_15_08)
            self.phy.SLICE_CTRL_00C8_23_16(self.rx_die, self.rx_group, setv=ptrn_23_16)
            self.phy.SLICE_CTRL_00CC_31_24(self.rx_die, self.rx_group, setv=ptrn_31_24)
            self.phy.SLICE_CTRL_00D0_39_32(self.rx_die, self.rx_group, setv=ptrn_39_31)
            self.phy.SLICE_CTRL_00D4_47_40(self.rx_die, self.rx_group, setv=ptrn_47_40)
            self.phy.SLICE_CTRL_00D8_55_48(self.rx_die, self.rx_group, setv=ptrn_55_48)
            self.phy.SLICE_CTRL_00DC_63_56(self.rx_die, self.rx_group, setv=ptrn_63_56)
            self.phy.SLICE_CTRL_00E0_rd3_rd0(
                self.rx_die, self.rx_group, setv=ptrn_rd3_rd0
            )
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
            self.phy.SLICE_CTRL_0120_rd3_rd0(
                self.rx_die, self.rx_group, setv=ptrn_rd3_rd0
            )
            self.phy.SLICE_CTRL_0360_vldrd_vld(
                self.rx_die, self.rx_group, setv=ptrn_vldrd_vld
            )

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
        else:
            print("\nDefault Test Pattern and RX Mask", flush=True)

        return all_train_result

    def FLY_LR_EN(self, **kargs):
        FLY_LR = kargs.get("FLY_LR", [])
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
                # self.phy.reg_user_set(die_arr=self.die_arr, group_arr=self.group_arr, tx_slice=[0,1,2,3], rx_slice=[0,1,2,3], reg_arr=hw_non_1, mode=init_mode)
                self.phy.reg_user_set(
                    die_arr=self.die_arr,
                    group_arr=self.group_arr,
                    tx_slice=self.tx_slice,
                    rx_slice=self.rx_slice,
                    reg_arr=FLY_LR,
                    mode=init_mode,
                )

        #         self.phy.rg_vref_range_start(self.tx_die, self.tx_group, self.tx_group_n, slice=self.tx_slice, doset=0, r_bk=0)
        #         self.phy.rg_vref_range_start(self.rx_die, self.rx_group, self.rx_group_n, slice=self.rx_slice, doset=0, r_bk=0)
        #         self.phy.rg_vref_range_num(self.tx_die, self.tx_group, self.tx_group_n, slice=self.tx_slice, doset=0, r_bk=0)
        #         self.phy.rg_vref_range_num(self.rx_die, self.rx_group, self.rx_group_n, slice=self.rx_slice, doset=0, r_bk=0)
        #         self.phy.rg_half_window(self.tx_die, self.tx_group, self.tx_group_n, slice=self.tx_slice, doset=0, r_bk=0)
        #         self.phy.rg_half_window(self.rx_die, self.rx_group, self.rx_group_n, slice=self.rx_slice, doset=0, r_bk=0)
        #
        #         # self.log_label('[Sequence] Read_Data_Training_Result')
        #         print(f'{self.info}', flush=True)
        #         tx_train_result = self.phy.train_result(self.tx_die, self.tx_group, self.tx_group_n, slice=self.tx_slice)
        #         rx_train_result = self.phy.train_result(self.rx_die, self.rx_group, self.rx_group_n, slice=self.rx_slice)
        #
        #         all_train_result = tx_train_result[0]+tx_train_result[1]+tx_train_result[2]+tx_train_result[3]+rx_train_result[0]+rx_train_result[1]+rx_train_result[2]+rx_train_result[3]
        #
        #         # # run 1D or 2D HW Training
        #         # if init_mode == 'M4_D0V_D1V_mode':
        #         #     tx_txt_arr = ['D0_S0.txt', 'D0_S1.txt', 'D0_S2.txt', 'D0_S3.txt']
        #         #     rx_txt_arr = ['D1_S0.txt', 'D1_S1.txt', 'D1_S2.txt', 'D1_S3.txt']
        #         # else:
        #         #     tx_txt_arr = ['D1_S0.txt', 'D1_S1.txt', 'D1_S2.txt', 'D1_S3.txt']
        #         #     rx_txt_arr = ['D2_S0.txt', 'D2_S1.txt', 'D2_S2.txt', 'D2_S3.txt']
        #         # print(f'\nTest Result : 1D Eye Diagram')
        #         # self.phy.train_width(self.tx_die, self.tx_group, self.tx_group_n, txt_arr = tx_txt_arr, vref_start=vref_start)
        #         # self.phy.train_width(self.rx_die, self.rx_group, self.rx_group_n, txt_arr = rx_txt_arr, vref_start=vref_start)
        #         # if eye_scan != '2d' :
        #         #     print(f'\nTest Result : 2D Eye Diagram')
        #         #     self.phy.train_center_2D(self.tx_die, self.tx_group, self.tx_group_n, vref_start=vref_start)
        #         #     self.phy.train_center_2D(self.rx_die, self.rx_group, self.rx_group_n, vref_start=vref_start)
        #
        #         # read center vref
        #         # Check Center Vref
        #         tx_center_vref = self.phy.cfg_vref_sel_rxgp(self.tx_die, self.tx_group, slice= self.tx_slice, doset=0, r_bk=1)
        #         rx_center_vref = self.phy.cfg_vref_sel_rxgp(self.rx_die, self.rx_group, slice= self.rx_slice, doset=0, r_bk=1)
        #         self.center_tx_vref_arr += [tx_center_vref]
        #         self.center_rx_vref_arr +=[rx_center_vref]
        # print('Center Vref Value')
        # print(f'(HW) Die{self.tx_die}{self.tx_group_n}_Slice{self.tx_slice}_Center Vref Value = {self.center_tx_vref_arr}')
        # print(f'(HW) Die{self.rx_die}{self.rx_group_n}_Slice{self.rx_slice}_Center Vref Value = {self.center_rx_vref_arr}')
        #
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
        #     self.phy.SLICE_CTRL_0120_rd3_rd0(self.tx_die, self.tx_group, setv=ptrn_rd3_rd0)
        #     self.phy.SLICE_CTRL_0360_vldrd_vld(self.tx_die, self.tx_group, setv=ptrn_vldrd_vld)
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
        #     self.phy.SLICE_CTRL_0120_rd3_rd0(self.rx_die, self.rx_group, setv=ptrn_rd3_rd0)
        #     self.phy.SLICE_CTRL_0360_vldrd_vld(self.rx_die, self.rx_group, setv=ptrn_vldrd_vld)
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
        #
        #     # # dieA OE Setup
        #     # self.phy.rg_pmaa_TX_OE_l(self.tx_die, self.tx_group, setv='0x00000001')
        #     # self.phy.rg_pmaa_TX_OE_h(self.tx_die, self.tx_group, setv='0x00000000')
        #     # self.phy.rg_pmaa_RDTX_OE(self.tx_die, self.tx_group, setv='0x0')
        #     # self.phy.rg_pmaa_TVLD_OE(self.tx_die, self.tx_group, setv='0x0')
        #     # self.phy.rg_pmaa_TRDVLD_OE(self.tx_die, self.tx_group, setv='0x0')
        #     #
        #     # # dieB OE Setup
        #     # self.phy.rg_pmaa_TX_OE_l(self.rx_die, self.rx_group, setv='0x00000001')
        #     # self.phy.rg_pmaa_TX_OE_h(self.rx_die, self.rx_group, setv='0x00000000')
        #     # self.phy.rg_pmaa_RDTX_OE(self.rx_die, self.rx_group, setv='0x0')
        #     # self.phy.rg_pmaa_TVLD_OE(self.rx_die, self.rx_group, setv='0x0')
        #     # self.phy.rg_pmaa_TRDVLD_OE(self.rx_die, self.rx_group, setv='0x0')
        #     #
        #     # # dieA IE/CLOCK Setup
        #     # self.phy.rg_pmaa_RX_IE_l(self.tx_die, self.tx_group, setv='0x00000001')
        #     # self.phy.rg_pmaa_RX_IE_h(self.tx_die, self.tx_group, setv='0x00000000')
        #     # self.phy.rg_pmaa_RDRX_IE(self.tx_die, self.tx_group, setv='0x0')
        #     # self.phy.rg_pmaa_RVLD_IE(self.tx_die, self.tx_group, setv='0x0')
        #     # self.phy.rg_pmaa_RRDVLD_IE(self.tx_die, self.tx_group, setv='0x0')
        #     # self.phy.cfg_en_clk_txd_l(self.tx_die, self.tx_group, setv='0x00000001')
        #     # self.phy.cfg_en_clk_txd_h(self.tx_die, self.tx_group, setv='0x00000000')
        #     # self.phy.cfg_en_clk_txdrd(self.tx_die, self.tx_group, setv='0x0')
        #     # self.phy.cfg_en_clk_txvld(self.tx_die, self.tx_group, setv='0x0')
        #     # self.phy.cfg_en_clk_txvldrd(self.tx_die, self.tx_group, setv='0x0')
        #     #
        #     # # dieB IE/CLOCK Setup
        #     # self.phy.rg_pmaa_RX_IE_l(self.rx_die, self.rx_group, setv='0x00000001')
        #     # self.phy.rg_pmaa_RX_IE_h(self.rx_die, self.rx_group, setv='0x00000000')
        #     # self.phy.rg_pmaa_RDRX_IE(self.rx_die, self.rx_group, setv='0x0')
        #     # self.phy.rg_pmaa_RVLD_IE(self.rx_die, self.rx_group, setv='0x0')
        #     # self.phy.rg_pmaa_RRDVLD_IE(self.rx_die, self.rx_group, setv='0x0')
        #     # self.phy.cfg_en_clk_txd_l(self.rx_die, self.rx_group, setv='0x00000001')
        #     # self.phy.cfg_en_clk_txd_h(self.rx_die, self.rx_group, setv='0x00000000')
        #     # self.phy.cfg_en_clk_txdrd(self.rx_die, self.rx_group, setv='0x0')
        #     # self.phy.cfg_en_clk_txvld(self.rx_die, self.rx_group, setv='0x0')
        #     # self.phy.cfg_en_clk_txvldrd(self.rx_die, self.rx_group, setv='0x0')
        # else:
        #     print('\nDefault Test Pattern and RX Mask', flush=True)
        #
        # return all_train_result

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

    def CPM(self):
        slave = 0x34
        # slave = 0x04
        slave_die = 0xE0
        # die_select_set = [0x01, 0x02, 0x04, 0x08]
        die_select_set = [0x01, 0x02, 0x04]
        # die_select_set = [0x01]
        # die_number_set = [0, 1, 2, 3]
        die_number_set = [0, 1, 2]
        # die_number_set = [0]
        PM_en_counter_H = 0x00  # PM Start time = n*20ns
        PM_en_counter_L = 0x80  # PM Start time = n*20ns
        DL_select_set = [0, 16]  # delay line type = 0~23
        # DL_select_set = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        PM_select = 0x1FF
        PM_select_L = PM_select % 0x100
        PM_select_H = int(PM_select / 0x100)
        PM_number_set = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        PM_address_L_set = [0x00, 0x04, 0x08, 0x0C, 0x10, 0x14, 0x18, 0x1C, 0x20]
        PM_address_H_set = [0x01, 0x05, 0x09, 0x0D, 0x11, 0x15, 0x19, 0x1D, 0x21]

        TestTemp = 25
        chip_num = "LD01"
        TestDataRate = 17.2
        Chip_Mode = ""
        Log_File_Name = "test report"

        start_time = datetime.datetime.now()
        print(start_time, flush=True)
        print("PM function run ")
        # w_time = 40

        for die_number, die_select in zip(die_number_set, die_select_set):
            # for die_number in [0,1,2,3]:
            self.phy.die_sel(die=die_number)
            self.phy.non_i2c_write(slave, 0xFE, 0, 8, 0x00)  # set PM_Value
            self.phy.non_i2c_write(
                slave, 0x04, 0, 8, PM_en_counter_H
            )  # PM_en_counter[15:8]
            self.phy.non_i2c_write(
                slave, 0x05, 0, 8, PM_en_counter_L
            )  # PM_en_counter[7:0]
            self.phy.non_i2c_write(slave, 0x08, 0, 8, PM_select_L)  # PM_select_L
            self.phy.non_i2c_write(slave, 0x09, 0, 8, PM_select_H)  # PM_select_H
            # self.phy.non_i2c_write(slave, 0x07, 0, 8, 0x01)  # PM_Start
            # self.phy.non_i2c_write(slave, 0xfe, 0, 8, 0x01)  # read PM_Value
        # print('PM function run2 ')
        for DL_select in DL_select_set:
            die_PM_all = []
            for die_number, die_select in zip(die_number_set, die_select_set):
                # self.non_i2c_write(slave_die, die_select, 0, 8, die_select)  # die_select
                self.phy.die_sel(die=die_number)
                self.phy.non_i2c_write(slave, 0xFE, 0, 8, 0x00)  # set PM_Value
                self.phy.non_i2c_write(slave, 0x06, 0, 8, DL_select)  # DL_select[7:0]
                self.phy.non_i2c_write(slave, 0x07, 0, 8, 0x01)  # PM_Start
                self.phy.non_i2c_write(slave, 0xFE, 0, 8, 0x01)  # read PM_Value
                PM_counter_all = []
                for PM_number, PM_address_L, PM_address_H in zip(
                    PM_number_set, PM_address_L_set, PM_address_H_set
                ):
                    PM_counter_L = int(
                        self.phy.non_i2c_read(slave, PM_address_L, 0, 8), 16
                    )  # PM_counter[7:0]
                    PM_counter_H = int(
                        self.phy.non_i2c_read(slave, PM_address_H, 0, 8), 16
                    )  # PM_counter[15:8]
                    PM_counter = PM_counter_L + 256 * PM_counter_H
                    PM_counter_all.append(PM_counter)
                    # print(f'die_#{die_number},PM_#{PM_number}, counter[15:0]={PM_counter_H*256+PM_counter_L}', flush=True)
                    # print(f'PM_#{PM_number}, counter[15:0]={PM_counter_H:02x}{PM_counter_L:02x}', flush=True)
                # print(f'die_#{die_number}, PM1~PM9 = {PM_counter_all}', flush=True)
                die_PM_all.append(PM_counter_all)

            print(f"Delay Line : DL {DL_select}", flush=True)
            write_tb = tabulate(
                die_PM_all,
                headers=[
                    "Die",
                    "PM_1",
                    "PM_2",
                    "PM_3",
                    "PM_4",
                    "PM_5",
                    "PM_6",
                    "PM_7",
                    "PM_8",
                    "PM_9",
                ],
                showindex="always",
                tablefmt="psql",
            )
            print(write_tb, flush=True)

            Report_time = datetime.datetime.now()
            Report_time = ((str(Report_time)).replace(":", "-"))[0:19]
            Log_Folder_path = (
                "Test Report\\Test Report Log\\CPM_"
                + chip_num
                + "_"
                + str(TestTemp)
                + "Degree_"
                + str(TestDataRate)
                + "Gbps_"
                + "DL"
                + str(DL_select)
                + "_"
                + str(Log_File_Name)
                + "_"
                + str(Report_time)
                + ".txt"
            )
            # print(Log_Folder_path)

            f = open(Log_Folder_path, "w")
            # f.write('Die\tPM_1\tPM_2\tPM_3\tPM_4\tPM_5\tPM_6\tPM_7\tPM_8\tPM_9')
            f.write(write_tb)
            f.close()

        self.phy.non_i2c_write(slave, 0xFE, 0, 8, 0x00)  # set PM_Value
        # self.phy.PM_read(lintype, count_set, die pm_enable)
        print("End Test Elapsed: ", datetime.datetime.now() - start_time)
        #

    def Flyover(self, **kargs):
        mode = kargs.get("mode", "mode")
        getattr(self, mode)()  # run Mx_mode()

        start_time = datetime.datetime.now()
        print(start_time, flush=True)
        print(" ==================================== ")
        print("    Flyover function start ")
        print(" ====================================\n ")

        # self.TX_FLOV_input(self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1) # read
        # self.TX_FLOV_input(self.rx_die, self.rx_group, slice=self.rx_slice, doset=0, r_bk=1) # read
        # self.reg1(self.tx_die, self.tx_group, slice=self.tx_slice, setv='0x9', r_bk=0) # write
        # self.reg1(self.rx_die, self.rx_group, slice=self.rx_slice, setv='0x9', r_bk=0) # write

        TX_FLOV_CLK = self.TX_CLK(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )  # read
        self.TX_CLK(
            self.rx_die, self.rx_group, slice=self.rx_slice, doset=0, r_bk=1
        )  # read

        TX_FLOV_D_L = self.TX_D_L(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )  # read
        self.TX_D_L(
            self.rx_die, self.rx_group, slice=self.rx_slice, doset=0, r_bk=1
        )  # read

        TX_FLOV_D_H = self.TX_D_H(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )  # read
        self.TX_D_H(
            self.rx_die, self.rx_group, slice=self.rx_slice, doset=0, r_bk=1
        )  # read

        TX_FLOV_DRD = self.TX_DRD(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )  # read
        self.TX_DRD(
            self.rx_die, self.rx_group, slice=self.rx_slice, doset=0, r_bk=1
        )  # read

        RX_FLOV_CLK = self.RX_CLK(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )  # read
        self.RX_CLK(
            self.rx_die, self.rx_group, slice=self.rx_slice, doset=0, r_bk=1
        )  # read

        RX_FLOV_D_L = self.RX_D_L(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )  # read
        self.RX_D_L(
            self.rx_die, self.rx_group, slice=self.rx_slice, doset=0, r_bk=1
        )  # read

        RX_FLOV_D_H = self.RX_D_H(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )  # read
        self.RX_D_H(
            self.rx_die, self.rx_group, slice=self.rx_slice, doset=0, r_bk=1
        )  # read

        RX_FLOV_DRD = self.RX_DRD(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )  # read
        self.RX_DRD(
            self.rx_die, self.rx_group, slice=self.rx_slice, doset=0, r_bk=1
        )  # read

        print(" \n ")

        if TX_FLOV_CLK == RX_FLOV_CLK:
            print(
                f"TX_FLOV_CLK = {TX_FLOV_CLK}, RX_FLOV_CLK = {RX_FLOV_CLK}, pass !",
                flush=True,
            )
        else:
            print(
                f"TX_FLOV_CLK = {TX_FLOV_CLK}, RX_FLOV_CLK = {RX_FLOV_CLK}, failed !",
                flush=True,
            )

        if TX_FLOV_D_L == RX_FLOV_D_L:
            print(
                f"TX_FLOV_D_L = {TX_FLOV_D_L}, RX_FLOV_D_L = {RX_FLOV_D_L}, pass !",
                flush=True,
            )
        else:
            print(
                f"TX_FLOV_D_L = {TX_FLOV_D_L}, RX_FLOV_D_L = {RX_FLOV_D_L}, failed !",
                flush=True,
            )

        if TX_FLOV_D_H == RX_FLOV_D_H:
            print(
                f"TX_FLOV_D_H = {TX_FLOV_D_H}, RX_FLOV_D_H = {RX_FLOV_D_H}, pass !",
                flush=True,
            )
        else:
            print(
                f"TX_FLOV_D_H = {TX_FLOV_D_H}, RX_FLOV_D_H = {RX_FLOV_D_H}, failed !",
                flush=True,
            )

        if TX_FLOV_DRD == RX_FLOV_DRD:
            print(
                f"TX_FLOV_DRD = {TX_FLOV_DRD}, RX_FLOV_DRD = {RX_FLOV_DRD}, pass !",
                flush=True,
            )
        else:
            print(
                f"TX_FLOV_DRD = {TX_FLOV_DRD}, RX_FLOV_DRD = {RX_FLOV_DRD}, failed !",
                flush=True,
            )

        print("End Test Elapsed: ", datetime.datetime.now() - start_time)

    def Lane_Repair(self, **kargs):
        mode = kargs.get("mode", "mode")
        # hw_non_1 = kargs.get('hw_non_1', [])
        getattr(self, mode)()  # run Mx_mode()

        start_time = datetime.datetime.now()
        print(start_time, flush=True)
        print(" ==================================== ")
        print("    Lane Repair function start ")
        print(" ====================================\n ")

        # self.TX_FLOV_input(self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1) # read
        # self.TX_FLOV_input(self.rx_die, self.rx_group, slice=self.rx_slice, doset=0, r_bk=1) # read
        # self.reg1(self.tx_die, self.tx_group, slice=self.tx_slice, setv='0x9', r_bk=0) # write
        # self.reg1(self.rx_die, self.rx_group, slice=self.rx_slice, setv='0x9', r_bk=0) # write

        LR_D0_DDR = self.LR_D0(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )  # read
        LR_D1_DDR = self.LR_D1(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )  # read
        LR_D2_DDR = self.LR_D2(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )  # read
        LR_D3_DDR = self.LR_D3(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )  # read
        LR_CLK_DDR = self.LR_CLK(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )  # read
        LR_VLD_DDR = self.LR_VLD(
            self.tx_die, self.tx_group, slice=self.tx_slice, doset=0, r_bk=1
        )  # read

        if LR_D0_DDR == "0x00":
            print(f"LR_D0_DDR is {LR_D0_DDR},  = 0x0, pass !", flush=True)
        else:
            print(f"LR_D0_DDR is {LR_D0_DDR},  != 0x0, failed !", flush=True)

        if LR_D1_DDR == "0x01":
            print(f"LR_D1_DDR is {LR_D1_DDR},  = 0x1, pass !", flush=True)
        else:
            print(f"LR_D1_DDR is {LR_D1_DDR},  != 0x1, failed !", flush=True)

        if LR_D2_DDR == "0x20":
            print(f"LR_D2_DDR is {LR_D2_DDR},  = 0x20, pass !", flush=True)
        else:
            print(f"LR_D2_DDR is {LR_D2_DDR},  != 0x20, failed !", flush=True)

        if LR_D3_DDR == "0x21":
            print(f"LR_D3_DDR is {LR_D3_DDR},  = 0x21, pass !", flush=True)
        else:
            print(f"LR_D3_DDR is {LR_D3_DDR},  != 0x21, failed !", flush=True)

        if LR_CLK_DDR == "0x0":
            print(f"LR_CLK_DDR is {LR_CLK_DDR},  = 0x0, pass !", flush=True)
        else:
            print(f"LR_CLK_DDR is {LR_CLK_DDR},  != 0x0, failed !", flush=True)

        if LR_VLD_DDR == "0x0":
            print(f"LR_VLD_DDR is {LR_VLD_DDR},  = 0x0, pass !", flush=True)
        else:
            print(f"LR_VLD_DDR is {LR_VLD_DDR},  != 0x0, failed !", flush=True)

        print("End Test Elapsed: ", datetime.datetime.now() - start_time)

    """' Subprogram """

    def log_label(self, label, **kargs):
        if self.show == 1:
            print(label, flush=True)
        self.Save_i2cLog(log_name=f"{label}\n")

    def Save_i2cLog(self, **kargs):
        content = kargs.get("log_name", "NA")

        textfile = open("TestTools/i2c_log.txt", "a+")
        textfile.write(content)
        textfile.close()

    def log_info(self, info):
        self.info = info

    def TX_CLK(self, die, group, **kwargs):
        doset = kwargs.get("doset", 1)
        setv = kwargs.get("setv", "0x1")
        r_bk = kwargs.get("r_bk", 0)
        show = kwargs.get("show", 0)
        slice = kwargs.get("slice", [0, 1, 2, 3])
        ftn_name = "TX_CLK"

        offset = 0x34E0
        bit = "6:1"
        slave = self.EHOST[die][group]
        self.phy.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.phy.indirect_write(
                    slave, offset + base, bit, int(setv, 16), slice_num=slice_n
                )
            if r_bk == 1:
                rbv = self.phy.indirect_read(
                    slave, offset + base, bit, slice_num=slice_n
                )
                rbvs.append(rbv)
        if show == 1:
            print(
                f"{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} "
            )
        if r_bk == 1:
            print(
                f"{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}"
            )
        return rbv

    def TX_D_L(self, die, group, **kwargs):
        doset = kwargs.get("doset", 1)
        setv = kwargs.get("setv", "0x1")
        r_bk = kwargs.get("r_bk", 0)
        show = kwargs.get("show", 0)
        slice = kwargs.get("slice", [0, 1, 2, 3])
        ftn_name = "TX_D_L"

        offset = 0x34E4
        bit = "31:0"
        slave = self.EHOST[die][group]
        self.phy.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.phy.indirect_write(
                    slave, offset + base, bit, int(setv, 16), slice_num=slice_n
                )
            if r_bk == 1:
                rbv = self.phy.indirect_read(
                    slave, offset + base, bit, slice_num=slice_n
                )
                rbvs.append(rbv)
        if show == 1:
            print(
                f"{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} "
            )
        if r_bk == 1:
            print(
                f"{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}"
            )
        return rbv

    def TX_D_H(self, die, group, **kwargs):
        doset = kwargs.get("doset", 1)
        setv = kwargs.get("setv", "0x1")
        r_bk = kwargs.get("r_bk", 0)
        show = kwargs.get("show", 0)
        slice = kwargs.get("slice", [0, 1, 2, 3])
        ftn_name = "TX_D_H"

        offset = 0x34E8
        bit = "31:0"
        slave = self.EHOST[die][group]
        self.phy.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.phy.indirect_write(
                    slave, offset + base, bit, int(setv, 16), slice_num=slice_n
                )
            if r_bk == 1:
                rbv = self.phy.indirect_read(
                    slave, offset + base, bit, slice_num=slice_n
                )
                rbvs.append(rbv)
        if show == 1:
            print(
                f"{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} "
            )
        if r_bk == 1:
            print(
                f"{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}"
            )
        return rbv

    def TX_DRD(self, die, group, **kwargs):
        doset = kwargs.get("doset", 1)
        setv = kwargs.get("setv", "0x1")
        r_bk = kwargs.get("r_bk", 0)
        show = kwargs.get("show", 0)
        slice = kwargs.get("slice", [0, 1, 2, 3])
        ftn_name = "TX_DRD"

        offset = 0x34EC
        bit = "7:0"
        slave = self.EHOST[die][group]
        self.phy.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.phy.indirect_write(
                    slave, offset + base, bit, int(setv, 16), slice_num=slice_n
                )
            if r_bk == 1:
                rbv = self.phy.indirect_read(
                    slave, offset + base, bit, slice_num=slice_n
                )
                rbvs.append(rbv)
        if show == 1:
            print(
                f"{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} "
            )
        if r_bk == 1:
            print(
                f"{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}"
            )
        return rbv

    def RX_CLK(self, die, group, **kwargs):
        doset = kwargs.get("doset", 1)
        setv = kwargs.get("setv", "0x1")
        r_bk = kwargs.get("r_bk", 0)
        show = kwargs.get("show", 0)
        slice = kwargs.get("slice", [0, 1, 2, 3])
        ftn_name = "RX_CLK"

        offset = 0x34F0
        bit = "6:1"
        slave = self.EHOST[die][group]
        self.phy.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.phy.indirect_write(
                    slave, offset + base, bit, int(setv, 16), slice_num=slice_n
                )
            if r_bk == 1:
                rbv = self.phy.indirect_read(
                    slave, offset + base, bit, slice_num=slice_n
                )
                rbvs.append(rbv)
        if show == 1:
            print(
                f"{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} "
            )
        if r_bk == 1:
            print(
                f"{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}"
            )
        return rbv

    def RX_D_L(self, die, group, **kwargs):
        doset = kwargs.get("doset", 1)
        setv = kwargs.get("setv", "0x1")
        r_bk = kwargs.get("r_bk", 0)
        show = kwargs.get("show", 0)
        slice = kwargs.get("slice", [0, 1, 2, 3])
        ftn_name = "RX_D_L"

        offset = 0x34F4
        bit = "31:0"
        slave = self.EHOST[die][group]
        self.phy.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.phy.indirect_write(
                    slave, offset + base, bit, int(setv, 16), slice_num=slice_n
                )
            if r_bk == 1:
                rbv = self.phy.indirect_read(
                    slave, offset + base, bit, slice_num=slice_n
                )
                rbvs.append(rbv)
        if show == 1:
            print(
                f"{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} "
            )
        if r_bk == 1:
            print(
                f"{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}"
            )
        return rbv

    def RX_D_H(self, die, group, **kwargs):
        doset = kwargs.get("doset", 1)
        setv = kwargs.get("setv", "0x1")
        r_bk = kwargs.get("r_bk", 0)
        show = kwargs.get("show", 0)
        slice = kwargs.get("slice", [0, 1, 2, 3])
        ftn_name = "RX_D_H"

        offset = 0x34F8
        bit = "31:0"
        slave = self.EHOST[die][group]
        self.phy.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.phy.indirect_write(
                    slave, offset + base, bit, int(setv, 16), slice_num=slice_n
                )
            if r_bk == 1:
                rbv = self.phy.indirect_read(
                    slave, offset + base, bit, slice_num=slice_n
                )
                rbvs.append(rbv)
        if show == 1:
            print(
                f"{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} "
            )
        if r_bk == 1:
            print(
                f"{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}"
            )
        return rbv

    def RX_DRD(self, die, group, **kwargs):
        doset = kwargs.get("doset", 1)
        setv = kwargs.get("setv", "0x1")
        r_bk = kwargs.get("r_bk", 0)
        show = kwargs.get("show", 0)
        slice = kwargs.get("slice", [0, 1, 2, 3])
        ftn_name = "RX_DRD"

        offset = 0x34FC
        bit = "7:0"
        slave = self.EHOST[die][group]
        self.phy.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.phy.indirect_write(
                    slave, offset + base, bit, int(setv, 16), slice_num=slice_n
                )
            if r_bk == 1:
                rbv = self.phy.indirect_read(
                    slave, offset + base, bit, slice_num=slice_n
                )
                rbvs.append(rbv)
        if show == 1:
            print(
                f"{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} "
            )
        if r_bk == 1:
            print(
                f"{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}"
            )
        return rbv

    def LR_D0(self, die, group, **kwargs):
        doset = kwargs.get("doset", 1)
        setv = kwargs.get("setv", "0x1")
        r_bk = kwargs.get("r_bk", 0)
        show = kwargs.get("show", 0)
        slice = kwargs.get("slice", [0, 1, 2, 3])
        ftn_name = "LR_D0"

        offset = 0x110C
        bit = "7:0"
        slave = self.EHOST[die][group]
        self.phy.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.phy.indirect_write(
                    slave, offset + base, bit, int(setv, 16), slice_num=slice_n
                )
            if r_bk == 1:
                rbv = self.phy.indirect_read(
                    slave, offset + base, bit, slice_num=slice_n
                )
                rbvs.append(rbv)
        if show == 1:
            print(
                f"{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} "
            )
        if r_bk == 1:
            print(
                f"{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}"
            )
        return rbv

    def LR_D1(self, die, group, **kwargs):
        doset = kwargs.get("doset", 1)
        setv = kwargs.get("setv", "0x1")
        r_bk = kwargs.get("r_bk", 0)
        show = kwargs.get("show", 0)
        slice = kwargs.get("slice", [0, 1, 2, 3])
        ftn_name = "LR_D1"

        offset = 0x110C
        bit = "15:8"
        slave = self.EHOST[die][group]
        self.phy.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.phy.indirect_write(
                    slave, offset + base, bit, int(setv, 16), slice_num=slice_n
                )
            if r_bk == 1:
                rbv = self.phy.indirect_read(
                    slave, offset + base, bit, slice_num=slice_n
                )
                rbvs.append(rbv)
        if show == 1:
            print(
                f"{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} "
            )
        if r_bk == 1:
            print(
                f"{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}"
            )
        return rbv

    def LR_D2(self, die, group, **kwargs):
        doset = kwargs.get("doset", 1)
        setv = kwargs.get("setv", "0x1")
        r_bk = kwargs.get("r_bk", 0)
        show = kwargs.get("show", 0)
        slice = kwargs.get("slice", [0, 1, 2, 3])
        ftn_name = "LR_D2"

        offset = 0x110C
        bit = "23:16"
        slave = self.EHOST[die][group]
        self.phy.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.phy.indirect_write(
                    slave, offset + base, bit, int(setv, 16), slice_num=slice_n
                )
            if r_bk == 1:
                rbv = self.phy.indirect_read(
                    slave, offset + base, bit, slice_num=slice_n
                )
                rbvs.append(rbv)
        if show == 1:
            print(
                f"{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} "
            )
        if r_bk == 1:
            print(
                f"{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}"
            )
        return rbv

    def LR_D3(self, die, group, **kwargs):
        doset = kwargs.get("doset", 1)
        setv = kwargs.get("setv", "0x1")
        r_bk = kwargs.get("r_bk", 0)
        show = kwargs.get("show", 0)
        slice = kwargs.get("slice", [0, 1, 2, 3])
        ftn_name = "LR_D3"

        offset = 0x110C
        bit = "31:24"
        slave = self.EHOST[die][group]
        self.phy.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.phy.indirect_write(
                    slave, offset + base, bit, int(setv, 16), slice_num=slice_n
                )
            if r_bk == 1:
                rbv = self.phy.indirect_read(
                    slave, offset + base, bit, slice_num=slice_n
                )
                rbvs.append(rbv)
        if show == 1:
            print(
                f"{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} "
            )
        if r_bk == 1:
            print(
                f"{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}"
            )
        return rbv

    def LR_CLK(self, die, group, **kwargs):
        doset = kwargs.get("doset", 1)
        setv = kwargs.get("setv", "0x1")
        r_bk = kwargs.get("r_bk", 0)
        show = kwargs.get("show", 0)
        slice = kwargs.get("slice", [0, 1, 2, 3])
        ftn_name = "LR_CLK"

        offset = 0x1134
        bit = "3:0"
        slave = self.EHOST[die][group]
        self.phy.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.phy.indirect_write(
                    slave, offset + base, bit, int(setv, 16), slice_num=slice_n
                )
            if r_bk == 1:
                rbv = self.phy.indirect_read(
                    slave, offset + base, bit, slice_num=slice_n
                )
                rbvs.append(rbv)
        if show == 1:
            print(
                f"{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} "
            )
        if r_bk == 1:
            print(
                f"{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}"
            )
        return rbv

    def LR_VLD(self, die, group, **kwargs):
        doset = kwargs.get("doset", 1)
        setv = kwargs.get("setv", "0x1")
        r_bk = kwargs.get("r_bk", 0)
        show = kwargs.get("show", 0)
        slice = kwargs.get("slice", [0, 1, 2, 3])
        ftn_name = "LR_VLD"

        offset = 0x1134
        bit = "9:8"
        slave = self.EHOST[die][group]
        self.phy.die_sel(die=die)
        rbvs = []
        for slice_n in slice:
            base = slice_n * self.slice_offset
            if doset == 1:
                self.phy.indirect_write(
                    slave, offset + base, bit, int(setv, 16), slice_num=slice_n
                )
            if r_bk == 1:
                rbv = self.phy.indirect_read(
                    slave, offset + base, bit, slice_num=slice_n
                )
                rbvs.append(rbv)

        if show == 1:
            print(
                f"{ftn_name} set to {setv} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} "
            )
        if r_bk == 1:
            print(
                f"{ftn_name} for die{die} {self.GROUP_NUM[group]} S#{self.slice_offset} = {rbvs}"
            )
        return rbv
