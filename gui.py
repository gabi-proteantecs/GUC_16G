# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext
import wx.dataview

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"UCIe AutoTest V01", pos = wx.Point( 0,0 ), size = wx.Size( 1018,706 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer132 = wx.BoxSizer( wx.HORIZONTAL )

		spec_version_wxChoices = [ u"\"GLink_2.5D\"", u"GLink_3D" ]
		self.spec_version_wx = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 160,25 ), spec_version_wxChoices, 0 )
		self.spec_version_wx.SetSelection( 0 )
		self.spec_version_wx.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "@Arial Unicode MS" ) )

		bSizer132.Add( self.spec_version_wx, 0, 0, 5 )

		ip_version_wxChoices = [ u"EZ0005A", u"EZA001A" ]
		self.ip_version_wx = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 160,25 ), ip_version_wxChoices, 0 )
		self.ip_version_wx.SetSelection( 0 )
		self.ip_version_wx.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "@Arial Unicode MS" ) )

		bSizer132.Add( self.ip_version_wx, 0, 0, 5 )

		self.m_toggleBtn_connect = wx.ToggleButton( self, wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.Size( 180,25 ), 0 )
		self.m_toggleBtn_connect.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, "@Arial Unicode MS" ) )

		bSizer132.Add( self.m_toggleBtn_connect, 0, 0, 0 )

		self.I2C_info = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 510,25 ), 0 )
		self.I2C_info.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "@Arial Unicode MS" ) )
		self.I2C_info.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		self.I2C_info.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )

		bSizer132.Add( self.I2C_info, 0, 0, 0 )


		bSizer1.Add( bSizer132, 0, wx.EXPAND, 0 )

		self.m_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 1200,650 ), 0|wx.BORDER_RAISED )
		self.m_notebook.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True, "Arial Rounded MT Bold" ) )

		self.Main = wx.ScrolledWindow( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.Main.SetScrollRate( 5, 5 )
		self.Main.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer18 = wx.BoxSizer( wx.VERTICAL )

		bSizer191 = wx.BoxSizer( wx.VERTICAL )

		Eye = wx.StaticBoxSizer( wx.StaticBox( self.Main, wx.ID_ANY, u"Receiver Eye Sacn Setup" ), wx.VERTICAL )

		scan_cycle_tree = wx.BoxSizer( wx.HORIZONTAL )

		self.scan_cycle_wx = wx.TextCtrl( Eye.GetStaticBox(), wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 160,-1 ), 0 )
		scan_cycle_tree.Add( self.scan_cycle_wx, 0, 0, 5 )

		self.Chip_Number_wx2 = wx.StaticText( Eye.GetStaticBox(), wx.ID_ANY, u"Eye Scan Cycle", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.Chip_Number_wx2.Wrap( -1 )

		self.Chip_Number_wx2.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		scan_cycle_tree.Add( self.Chip_Number_wx2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Eye.Add( scan_cycle_tree, 1, wx.EXPAND, 5 )

		Eye_scan_ON_OFF = wx.BoxSizer( wx.HORIZONTAL )

		self.data_training_en = wx.ToggleButton( Eye.GetStaticBox(), wx.ID_ANY, u"Enable", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.data_training_en.SetValue( True )
		self.data_training_en.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )
		self.data_training_en.SetMinSize( wx.Size( 160,-1 ) )

		Eye_scan_ON_OFF.Add( self.data_training_en, 0, 0, 0 )

		self.Data_Training = wx.StaticText( Eye.GetStaticBox(), wx.ID_ANY, u"Data Training Only", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Data_Training.Wrap( -1 )

		self.Data_Training.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Eye_scan_ON_OFF.Add( self.Data_Training, 0, wx.ALL, 5 )


		Eye.Add( Eye_scan_ON_OFF, 1, wx.EXPAND, 5 )

		Start_eye_scan = wx.BoxSizer( wx.HORIZONTAL )

		self.eye_scan_wx = wx.ToggleButton( Eye.GetStaticBox(), wx.ID_ANY, u"Press Run Eye Scan", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.eye_scan_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )
		self.eye_scan_wx.SetMinSize( wx.Size( 160,-1 ) )

		Start_eye_scan.Add( self.eye_scan_wx, 0, wx.BOTTOM, 0 )

		self.Power_Select_Main111 = wx.StaticText( Eye.GetStaticBox(), wx.ID_ANY, u"Eye Scan Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_Select_Main111.Wrap( -1 )

		self.Power_Select_Main111.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Start_eye_scan.Add( self.Power_Select_Main111, 0, wx.ALL, 5 )


		Eye.Add( Start_eye_scan, 0, wx.BOTTOM, 5 )

		seach_range = wx.BoxSizer( wx.HORIZONTAL )

		self.seach_min = wx.TextCtrl( Eye.GetStaticBox(), wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 67,-1 ), 0 )
		self.seach_min.SetForegroundColour( wx.Colour( 255, 128, 64 ) )

		seach_range.Add( self.seach_min, 0, 0, 5 )

		self.seach_label = wx.StaticText( Eye.GetStaticBox(), wx.ID_ANY, u" / ", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.seach_label.Wrap( -1 )

		self.seach_label.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )
		self.seach_label.SetForegroundColour( wx.Colour( 255, 128, 64 ) )

		seach_range.Add( self.seach_label, 0, wx.RIGHT|wx.LEFT, 5 )

		self.seach_max = wx.TextCtrl( Eye.GetStaticBox(), wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 67,-1 ), 0 )
		self.seach_max.SetForegroundColour( wx.Colour( 255, 128, 64 ) )

		seach_range.Add( self.seach_max, 0, 0, 5 )

		self.seach_min_max = wx.StaticText( Eye.GetStaticBox(), wx.ID_ANY, u"Show Fail Count(Min/Max )", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.seach_min_max.Wrap( -1 )

		self.seach_min_max.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )
		self.seach_min_max.SetForegroundColour( wx.Colour( 255, 128, 64 ) )

		seach_range.Add( self.seach_min_max, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		Eye.Add( seach_range, 0, wx.TOP, 5 )

		Eye_scan = wx.BoxSizer( wx.HORIZONTAL )

		eye_scan_typeChoices = []
		self.eye_scan_type = wx.ComboBox( Eye.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 160,-1 ), eye_scan_typeChoices, 0 )
		self.eye_scan_type.SetSelection( 0 )
		self.eye_scan_type.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )
		self.eye_scan_type.SetForegroundColour( wx.Colour( 255, 128, 64 ) )

		Eye_scan.Add( self.eye_scan_type, 0, 0, 0 )

		self.m_staticText291 = wx.StaticText( Eye.GetStaticBox(), wx.ID_ANY, u"Eye Sane Type", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText291.Wrap( -1 )

		self.m_staticText291.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )
		self.m_staticText291.SetForegroundColour( wx.Colour( 255, 128, 64 ) )

		Eye_scan.Add( self.m_staticText291, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Eye.Add( Eye_scan, 1, wx.EXPAND, 5 )

		Re_show_count = wx.BoxSizer( wx.HORIZONTAL )

		self.retry_show_count = wx.ToggleButton( Eye.GetStaticBox(), wx.ID_ANY, u"Press Update Fail Count", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.retry_show_count.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )
		self.retry_show_count.SetForegroundColour( wx.Colour( 255, 128, 64 ) )
		self.retry_show_count.SetMinSize( wx.Size( 160,-1 ) )

		Re_show_count.Add( self.retry_show_count, 0, 0, 0 )

		self.retry_show_fail_count = wx.StaticText( Eye.GetStaticBox(), wx.ID_ANY, u"Update Fail Count Application", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.retry_show_fail_count.Wrap( -1 )

		self.retry_show_fail_count.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )
		self.retry_show_fail_count.SetForegroundColour( wx.Colour( 255, 128, 64 ) )

		Re_show_count.Add( self.retry_show_fail_count, 0, wx.ALL, 5 )


		Eye.Add( Re_show_count, 1, wx.EXPAND, 5 )


		bSizer191.Add( Eye, 0, wx.EXPAND, 5 )

		Start_Test = wx.StaticBoxSizer( wx.StaticBox( self.Main, wx.ID_ANY, u"Test Condition" ), wx.VERTICAL )

		Run_Times = wx.BoxSizer( wx.HORIZONTAL )

		self.Test_Cycle_wx = wx.SpinCtrl( Start_Test.GetStaticBox(), wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 160,-1 ), 0, 1, 100000000, 4 )
		self.Test_Cycle_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Run_Times.Add( self.Test_Cycle_wx, 0, 0, 0 )

		self.m_staticText221 = wx.StaticText( Start_Test.GetStaticBox(), wx.ID_ANY, u"Test Cycle", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText221.Wrap( -1 )

		self.m_staticText221.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Run_Times.Add( self.m_staticText221, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )


		Start_Test.Add( Run_Times, 0, 0, 5 )

		Corner_Version11 = wx.BoxSizer( wx.HORIZONTAL )

		self.chip_number_wx = wx.TextCtrl( Start_Test.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 160,-1 ), 0 )
		Corner_Version11.Add( self.chip_number_wx, 0, 0, 5 )

		self.chip_number_name = wx.StaticText( Start_Test.GetStaticBox(), wx.ID_ANY, u"Chip Number(Name)", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.chip_number_name.Wrap( -1 )

		self.chip_number_name.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Corner_Version11.Add( self.chip_number_name, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Start_Test.Add( Corner_Version11, 1, wx.EXPAND, 5 )

		Corner_Version1 = wx.BoxSizer( wx.HORIZONTAL )

		Corner_Version_wxChoices = [ u"TT", u"SS", u"FF" ]
		self.Corner_Version_wx = wx.ComboBox( Start_Test.GetStaticBox(), wx.ID_ANY, u"TT", wx.DefaultPosition, wx.Size( 160,-1 ), Corner_Version_wxChoices, 0 )
		self.Corner_Version_wx.SetSelection( 0 )
		self.Corner_Version_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Corner_Version1.Add( self.Corner_Version_wx, 0, 0, 0 )

		self.Corner_Version = wx.StaticText( Start_Test.GetStaticBox(), wx.ID_ANY, u"Corner Version(Name)", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.Corner_Version.Wrap( -1 )

		self.Corner_Version.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Corner_Version1.Add( self.Corner_Version, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Start_Test.Add( Corner_Version1, 0, 0, 0 )

		Function_Select = wx.BoxSizer( wx.HORIZONTAL )

		Function_select_wxChoices = []
		self.Function_select_wx = wx.ComboBox( Start_Test.GetStaticBox(), wx.ID_ANY, u"(Function Select )", wx.DefaultPosition, wx.Size( 160,-1 ), Function_select_wxChoices, 0 )
		self.Function_select_wx.SetSelection( 0 )
		self.Function_select_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Function_Select.Add( self.Function_select_wx, 0, 0, 0 )

		self.m_staticText29 = wx.StaticText( Start_Test.GetStaticBox(), wx.ID_ANY, u"Function Select", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )

		self.m_staticText29.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Function_Select.Add( self.m_staticText29, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Start_Test.Add( Function_Select, 0, 0, 0 )

		voltage_sense = wx.BoxSizer( wx.HORIZONTAL )

		self.voltage_sense = wx.ToggleButton( Start_Test.GetStaticBox(), wx.ID_ANY, u"Voltage Sense", wx.DefaultPosition, wx.Size( 160,-1 ), 0 )
		self.voltage_sense.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		voltage_sense.Add( self.voltage_sense, 0, 0, 5 )

		self.voltage_sense_lable = wx.StaticText( Start_Test.GetStaticBox(), wx.ID_ANY, u"Voltage Sense ON/OFF", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.voltage_sense_lable.Wrap( -1 )

		self.voltage_sense_lable.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		voltage_sense.Add( self.voltage_sense_lable, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		Start_Test.Add( voltage_sense, 0, 0, 5 )

		Thermal_ON_OFF = wx.BoxSizer( wx.HORIZONTAL )

		self.ThermalOn_OFF = wx.ToggleButton( Start_Test.GetStaticBox(), wx.ID_ANY, u"Thermal OFF", wx.DefaultPosition, wx.Size( 160,-1 ), 0 )
		self.ThermalOn_OFF.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Thermal_ON_OFF.Add( self.ThermalOn_OFF, 0, 0, 0 )

		self.Thermal_Select_Main = wx.StaticText( Start_Test.GetStaticBox(), wx.ID_ANY, u"Thermal ON/OFF", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Thermal_Select_Main.Wrap( -1 )

		self.Thermal_Select_Main.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Thermal_ON_OFF.Add( self.Thermal_Select_Main, 0, wx.ALL, 5 )


		Start_Test.Add( Thermal_ON_OFF, 0, 0, 5 )

		Save_Register_Sequence = wx.BoxSizer( wx.HORIZONTAL )

		self.reg_sequence = wx.ToggleButton( Start_Test.GetStaticBox(), wx.ID_ANY, u"Save In Log File", wx.DefaultPosition, wx.Size( 160,-1 ), 0 )
		self.reg_sequence.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Save_Register_Sequence.Add( self.reg_sequence, 0, 0, 0 )

		self.reg_sequence_save = wx.StaticText( Start_Test.GetStaticBox(), wx.ID_ANY, u"Register Sequence Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.reg_sequence_save.Wrap( -1 )

		self.reg_sequence_save.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Save_Register_Sequence.Add( self.reg_sequence_save, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		Start_Test.Add( Save_Register_Sequence, 0, 0, 5 )

		Start_test = wx.BoxSizer( wx.HORIZONTAL )

		self.m_toggleBtn_run_test = wx.ToggleButton( Start_Test.GetStaticBox(), wx.ID_ANY, u"Run", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_toggleBtn_run_test.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )
		self.m_toggleBtn_run_test.SetMinSize( wx.Size( 160,-1 ) )

		Start_test.Add( self.m_toggleBtn_run_test, 0, wx.ALL, 0 )

		self.Power_Select_Main11 = wx.StaticText( Start_Test.GetStaticBox(), wx.ID_ANY, u"Start Test", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_Select_Main11.Wrap( -1 )

		self.Power_Select_Main11.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Start_test.Add( self.Power_Select_Main11, 0, wx.ALL, 5 )


		Start_Test.Add( Start_test, 0, 0, 5 )


		bSizer191.Add( Start_Test, 0, wx.TOP|wx.EXPAND, 5 )

		bSizer137 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText87 = wx.StaticText( self.Main, wx.ID_ANY, u"GUC", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText87.Wrap( -1 )

		self.m_staticText87.SetFont( wx.Font( 36, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "@Yu Gothic UI" ) )
		self.m_staticText87.SetForegroundColour( wx.Colour( 0, 147, 0 ) )

		bSizer137.Add( self.m_staticText87, 0, wx.ALIGN_CENTER_HORIZONTAL, 0 )

		self.m_staticText881 = wx.StaticText( self.Main, wx.ID_ANY, u"The Advanced ASIC Leader", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText881.Wrap( -1 )

		self.m_staticText881.SetFont( wx.Font( 7, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Segoe UI Emoji" ) )

		bSizer137.Add( self.m_staticText881, 0, wx.ALIGN_CENTER_HORIZONTAL, 0 )


		bSizer191.Add( bSizer137, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer18.Add( bSizer191, 0, 0, 5 )


		bSizer17.Add( bSizer18, 0, wx.TOP, 5 )

		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )

		Test_Info = wx.StaticBoxSizer( wx.StaticBox( self.Main, wx.ID_ANY, u"Test Information" ), wx.VERTICAL )

		Test_Log = wx.BoxSizer( wx.VERTICAL )

		self.info_window_wx = wx.Notebook( Test_Info.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 580,460 ), 0 )
		self.Eye_Diagram_Graph = wx.ScrolledWindow( self.info_window_wx, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.Eye_Diagram_Graph.SetScrollRate( 5, 5 )
		bSizer1941 = wx.BoxSizer( wx.VERTICAL )

		self.eye_graph_info_wx = wx.StaticBitmap( self.Eye_Diagram_Graph, wx.ID_ANY, wx.Bitmap( u"TestTools/blank.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 800,4000 ), 0 )
		self.eye_graph_info_wx.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer1941.Add( self.eye_graph_info_wx, 0, wx.ALL, 5 )


		self.Eye_Diagram_Graph.SetSizer( bSizer1941 )
		self.Eye_Diagram_Graph.Layout()
		bSizer1941.Fit( self.Eye_Diagram_Graph )
		self.info_window_wx.AddPage( self.Eye_Diagram_Graph, u"Eye Diagram Graph", False )
		self.Test_Info = wx.ScrolledWindow( self.info_window_wx, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.HSCROLL|wx.VSCROLL )
		self.Test_Info.SetScrollRate( 5, 5 )
		bSizer1901 = wx.BoxSizer( wx.VERTICAL )

		self.m_richText1 = wx.richtext.RichTextCtrl( self.Test_Info, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 550,430 ), wx.TE_AUTO_URL|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB|wx.HSCROLL|wx.VSCROLL|wx.WANTS_CHARS|wx.BORDER_SUNKEN )
		self.m_richText1.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )
		self.m_richText1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		self.m_richText1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

		bSizer1901.Add( self.m_richText1, 0, 0, 5 )


		self.Test_Info.SetSizer( bSizer1901 )
		self.Test_Info.Layout()
		bSizer1901.Fit( self.Test_Info )
		self.info_window_wx.AddPage( self.Test_Info, u"Test Log Information", False )
		self.Chip_Block = wx.ScrolledWindow( self.info_window_wx, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.Chip_Block.SetScrollRate( 5, 5 )
		bSizer202 = wx.BoxSizer( wx.VERTICAL )

		self.m_bitmap2 = wx.StaticBitmap( self.Chip_Block, wx.ID_ANY, wx.Bitmap( u"TestTools/Chip Slice.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 530,-1 ), 0 )
		bSizer202.Add( self.m_bitmap2, 0, wx.ALL, 5 )


		self.Chip_Block.SetSizer( bSizer202 )
		self.Chip_Block.Layout()
		bSizer202.Fit( self.Chip_Block )
		self.info_window_wx.AddPage( self.Chip_Block, u"Test Chip Block", True )

		Test_Log.Add( self.info_window_wx, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Test_Info.Add( Test_Log, 0, 0, 5 )

		TestItem_message = wx.BoxSizer( wx.VERTICAL )

		self.TestItem_Now2_wx = wx.TextCtrl( Test_Info.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 580,25 ), 0 )
		self.TestItem_Now2_wx.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		self.TestItem_Now2_wx.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

		TestItem_message.Add( self.TestItem_Now2_wx, 0, 0, 5 )

		self.TestItem_Now_wx = wx.TextCtrl( Test_Info.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 580,25 ), 0 )
		self.TestItem_Now_wx.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		self.TestItem_Now_wx.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

		TestItem_message.Add( self.TestItem_Now_wx, 0, wx.BOTTOM, 5 )


		Test_Info.Add( TestItem_message, 0, 0, 5 )

		Test_Step = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button_clear = wx.Button( Test_Info.GetStaticBox(), wx.ID_ANY, u"Clear Text", wx.DefaultPosition, wx.Size( 100,25 ), 0 )
		self.m_button_clear.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		Test_Step.Add( self.m_button_clear, 0, wx.ALIGN_CENTER_VERTICAL, 0 )

		self.Step_count = wx.Gauge( Test_Info.GetStaticBox(), wx.ID_ANY, 100, wx.Point( -1,-1 ), wx.Size( 180,25 ), 0 )
		self.Step_count.SetValue( 0 )
		self.Step_count.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
		self.Step_count.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		self.Step_count.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )

		Test_Step.Add( self.Step_count, 0, 0, 5 )

		self.m_textCtrl9 = wx.TextCtrl( Test_Info.GetStaticBox(), wx.ID_ANY, u"(Test Item Number)", wx.DefaultPosition, wx.Size( 300,25 ), 0 )
		self.m_textCtrl9.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
		self.m_textCtrl9.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.m_textCtrl9.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

		Test_Step.Add( self.m_textCtrl9, 0, wx.ALIGN_CENTER_VERTICAL, 5 )


		Test_Info.Add( Test_Step, 0, 0, 0 )


		bSizer19.Add( Test_Info, 0, 0, 5 )


		bSizer17.Add( bSizer19, 0, wx.TOP|wx.LEFT, 5 )


		self.Main.SetSizer( bSizer17 )
		self.Main.Layout()
		bSizer17.Fit( self.Main )
		self.m_notebook.AddPage( self.Main, u"Main", True )
		self.Configure = wx.ScrolledWindow( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.Size( 930,620 ), wx.HSCROLL|wx.VSCROLL )
		self.Configure.SetScrollRate( 5, 5 )
		self.Configure.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
		self.Configure.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
		self.Configure.Hide()

		bSizer23 = wx.BoxSizer( wx.VERTICAL )

		self.GUC = wx.Notebook( self.Configure, wx.ID_ANY, wx.DefaultPosition, wx.Size( 920,620 ), 0 )
		self.GUC.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )
		self.GUC.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.GUC.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		self.guc_chip = wx.ScrolledWindow( self.GUC, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.guc_chip.SetScrollRate( 5, 5 )
		self.guc_chip.SetMaxSize( wx.Size( 300,-1 ) )

		bSizer1911 = wx.BoxSizer( wx.VERTICAL )

		bSizer1271 = wx.BoxSizer( wx.VERTICAL )

		thermal_die_en = wx.BoxSizer( wx.HORIZONTAL )

		self.Thermal_die_en = wx.ToggleButton( self.guc_chip, wx.ID_ANY, u"Thermal Die ", wx.DefaultPosition, wx.Size( 160,-1 ), 0 )
		self.Thermal_die_en.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		thermal_die_en.Add( self.Thermal_die_en, 0, 0, 5 )

		self.Thermal_die_lable = wx.StaticText( self.guc_chip, wx.ID_ANY, u"Termal Die ON/OFF", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Thermal_die_lable.Wrap( -1 )

		self.Thermal_die_lable.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		thermal_die_en.Add( self.Thermal_die_lable, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1271.Add( thermal_die_en, 0, wx.TOP|wx.LEFT, 5 )


		bSizer1911.Add( bSizer1271, 1, wx.EXPAND, 5 )


		self.guc_chip.SetSizer( bSizer1911 )
		self.guc_chip.Layout()
		bSizer1911.Fit( self.guc_chip )
		self.GUC.AddPage( self.guc_chip, u"GUC Chip Setup", False )
		self.I2C_page = wx.ScrolledWindow( self.GUC, wx.ID_ANY, wx.DefaultPosition, wx.Size( 920,660 ), wx.HSCROLL|wx.VSCROLL )
		self.I2C_page.SetScrollRate( 5, 5 )
		self.I2C_page.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )
		self.I2C_page.Hide()

		bSizer15212 = wx.BoxSizer( wx.VERTICAL )

		bSizer158 = wx.BoxSizer( wx.HORIZONTAL )

		sbSizer12 = wx.StaticBoxSizer( wx.StaticBox( self.I2C_page, wx.ID_ANY, u"Single Read/Write Register Tree" ), wx.HORIZONTAL )

		self.tree_item = wx.dataview.TreeListCtrl( sbSizer12.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 620,520 ), wx.dataview.TL_DEFAULT_STYLE )
		self.tree_item.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial Unicode MS" ) )

		self.tree_item.AppendColumn( u"Name", wx.COL_WIDTH_AUTOSIZE, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.tree_item.AppendColumn( u"Offset", wx.COL_WIDTH_AUTOSIZE, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.tree_item.AppendColumn( u"Bit", wx.COL_WIDTH_AUTOSIZE, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.tree_item.AppendColumn( u"Map_Value", wx.COL_WIDTH_AUTOSIZE, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.tree_item.AppendColumn( u"Type  ", wx.COL_WIDTH_AUTOSIZE, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.tree_item.AppendColumn( u"Note                           ", wx.COL_WIDTH_AUTOSIZE, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.tree_item.AppendColumn( u"BK1", wx.COL_WIDTH_DEFAULT, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.tree_item.AppendColumn( u"BK2", wx.COL_WIDTH_DEFAULT, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.tree_item.AppendColumn( u"BK3", wx.COL_WIDTH_DEFAULT, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.tree_item.AppendColumn( u"BK4", wx.COL_WIDTH_DEFAULT, wx.ALIGN_LEFT, wx.COL_RESIZABLE )

		sbSizer12.Add( self.tree_item, 0, 0, 5 )


		bSizer158.Add( sbSizer12, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		bSizer130 = wx.BoxSizer( wx.VERTICAL )

		sbSizer11 = wx.StaticBoxSizer( wx.StaticBox( self.I2C_page, wx.ID_ANY, u"Load/Modify Register Map" ), wx.VERTICAL )

		Pll_map_sheet1 = wx.BoxSizer( wx.VERTICAL )

		self.Sheet_select11 = wx.StaticText( sbSizer11.GetStaticBox(), wx.ID_ANY, u"PLL Map Excel Sheet / Sheet Column Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Sheet_select11.Wrap( -1 )

		self.Sheet_select11.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer129 = wx.BoxSizer( wx.HORIZONTAL )

		pll_sheet_name_treeChoices = []
		self.pll_sheet_name_tree = wx.ComboBox( sbSizer11.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), pll_sheet_name_treeChoices, 0 )
		self.pll_sheet_name_tree.SetSelection( 2 )
		self.pll_sheet_name_tree.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer129.Add( self.pll_sheet_name_tree, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

		pll_sheet_col_numChoices = [ u"A", u"B", u"C", u"D", u"E", u"F", u"G", u"H", u"I", u"J", u"K", u"L", u"M", u"N", u"O", u"P", u"Q", u"R", u"S", u"T", u"U", u"V", u"W", u"X", u"Y", u"Z" ]
		self.pll_sheet_col_num = wx.ComboBox( sbSizer11.GetStaticBox(), wx.ID_ANY, u"E", wx.DefaultPosition, wx.Size( 40,-1 ), pll_sheet_col_numChoices, 0 )
		self.pll_sheet_col_num.SetSelection( 4 )
		self.pll_sheet_col_num.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer129.Add( self.pll_sheet_col_num, 0, 0, 5 )


		Pll_map_sheet1.Add( bSizer129, 1, wx.EXPAND, 5 )


		sbSizer11.Add( Pll_map_sheet1, 0, wx.TOP, 5 )

		slice_map_sheet11 = wx.BoxSizer( wx.VERTICAL )

		self.Sheet_select111 = wx.StaticText( sbSizer11.GetStaticBox(), wx.ID_ANY, u"Slice Map Excel Sheet / Sheet Column Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Sheet_select111.Wrap( -1 )

		self.Sheet_select111.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer1301 = wx.BoxSizer( wx.HORIZONTAL )

		slice_sheet_name_treeChoices = []
		self.slice_sheet_name_tree = wx.ComboBox( sbSizer11.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), slice_sheet_name_treeChoices, 0 )
		self.slice_sheet_name_tree.SetSelection( 4 )
		self.slice_sheet_name_tree.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer1301.Add( self.slice_sheet_name_tree, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

		slice_sheet_col_numChoices = [ u"A", u"B", u"C", u"D", u"E", u"F", u"G", u"H", u"I", u"J", u"K", u"L", u"M", u"N", u"O", u"P", u"Q", u"R", u"S", u"T", u"U", u"V", u"W", u"X", u"Y", u"Z" ]
		self.slice_sheet_col_num = wx.ComboBox( sbSizer11.GetStaticBox(), wx.ID_ANY, u"E", wx.DefaultPosition, wx.Size( 40,-1 ), slice_sheet_col_numChoices, 0 )
		self.slice_sheet_col_num.SetSelection( 4 )
		self.slice_sheet_col_num.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer1301.Add( self.slice_sheet_col_num, 0, 0, 5 )


		slice_map_sheet11.Add( bSizer1301, 1, wx.EXPAND, 5 )


		sbSizer11.Add( slice_map_sheet11, 0, wx.TOP, 5 )

		bSizer125 = wx.BoxSizer( wx.VERTICAL )

		self.reg_map_load = wx.Button( sbSizer11.GetStaticBox(), wx.ID_ANY, u"Press Load Register Map", wx.DefaultPosition, wx.Size( 240,-1 ), 0 )
		self.reg_map_load.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer125.Add( self.reg_map_load, 0, wx.BOTTOM, 5 )


		sbSizer11.Add( bSizer125, 0, wx.TOP, 5 )


		bSizer130.Add( sbSizer11, 0, wx.EXPAND|wx.TOP|wx.RIGHT, 5 )

		sbSizer121 = wx.StaticBoxSizer( wx.StaticBox( self.I2C_page, wx.ID_ANY, u"Modify Register" ), wx.VERTICAL )

		bSizer140 = wx.BoxSizer( wx.VERTICAL )

		bSizer128 = wx.BoxSizer( wx.HORIZONTAL )

		self.tree_seach = wx.TextCtrl( sbSizer121.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		bSizer128.Add( self.tree_seach, 0, wx.LEFT, 5 )

		self.m_staticText922 = wx.StaticText( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Edit Seach Keyword", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText922.Wrap( -1 )

		bSizer128.Add( self.m_staticText922, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer140.Add( bSizer128, 0, 0, 5 )

		reg_type1 = wx.BoxSizer( wx.HORIZONTAL )

		reg_sourceChoices = [ u"Register_Tree", u"User_Define" ]
		self.reg_source = wx.ComboBox( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Register_Tree", wx.DefaultPosition, wx.Size( 120,-1 ), reg_sourceChoices, 0 )
		self.reg_source.SetSelection( 0 )
		self.reg_source.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		reg_type1.Add( self.reg_source, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

		self.m_staticText149221 = wx.StaticText( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Register Source", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText149221.Wrap( -1 )

		reg_type1.Add( self.m_staticText149221, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer140.Add( reg_type1, 1, wx.EXPAND, 5 )

		reg_type = wx.BoxSizer( wx.HORIZONTAL )

		reg_typeChoices = [ u"TPORT", u"PLL/SLICE", u"Normal I2C" ]
		self.reg_type = wx.ComboBox( sbSizer121.GetStaticBox(), wx.ID_ANY, u"PLL/SLICE", wx.DefaultPosition, wx.Size( 120,-1 ), reg_typeChoices, 0 )
		self.reg_type.SetSelection( 1 )
		self.reg_type.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		reg_type.Add( self.reg_type, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText14922 = wx.StaticText( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Register Type", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14922.Wrap( -1 )

		reg_type.Add( self.m_staticText14922, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer140.Add( reg_type, 1, wx.EXPAND|wx.LEFT, 5 )

		die_select = wx.BoxSizer( wx.HORIZONTAL )

		die_selectChoices = [ u"0", u"1", u"2" ]
		self.die_select = wx.ComboBox( sbSizer121.GetStaticBox(), wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 120,-1 ), die_selectChoices, 0 )
		self.die_select.SetSelection( 0 )
		self.die_select.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		die_select.Add( self.die_select, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText1492 = wx.StaticText( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Die Select", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1492.Wrap( -1 )

		die_select.Add( self.m_staticText1492, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer140.Add( die_select, 0, wx.LEFT, 5 )

		group_select = wx.BoxSizer( wx.HORIZONTAL )

		group_selectChoices = [ u"TPORT", u"H", u"V" ]
		self.group_select = wx.ComboBox( sbSizer121.GetStaticBox(), wx.ID_ANY, u"H", wx.DefaultPosition, wx.Size( 120,-1 ), group_selectChoices, 0 )
		self.group_select.SetSelection( 1 )
		self.group_select.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		group_select.Add( self.group_select, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.LEFT, 5 )

		self.m_staticText14921 = wx.StaticText( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Group Select", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14921.Wrap( -1 )

		group_select.Add( self.m_staticText14921, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer140.Add( group_select, 1, wx.EXPAND, 5 )

		slice_select = wx.BoxSizer( wx.HORIZONTAL )

		slice_selectChoices = [ u"0", u"1", u"2", u"3" ]
		self.slice_select = wx.ComboBox( sbSizer121.GetStaticBox(), wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 120,-1 ), slice_selectChoices, 0 )
		self.slice_select.SetSelection( 0 )
		self.slice_select.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		slice_select.Add( self.slice_select, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

		self.m_staticText149211 = wx.StaticText( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Slice Select", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText149211.Wrap( -1 )

		slice_select.Add( self.m_staticText149211, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer140.Add( slice_select, 1, wx.EXPAND, 5 )

		sbSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_textCtrl_i2c_off_len = wx.TextCtrl( sbSizer121.GetStaticBox(), wx.ID_ANY, u"8", wx.DefaultPosition, wx.Size( 20,-1 ), 0 )
		self.m_textCtrl_i2c_off_len.Hide()

		sbSizer6.Add( self.m_textCtrl_i2c_off_len, 0, 0, 5 )

		self.m_staticText731 = wx.StaticText( sbSizer121.GetStaticBox(), wx.ID_ANY, u"off_len", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText731.Wrap( -1 )

		self.m_staticText731.Hide()

		sbSizer6.Add( self.m_staticText731, 0, wx.ALIGN_CENTER, 5 )


		bSizer140.Add( sbSizer6, 0, wx.LEFT, 0 )

		bSizer143 = wx.BoxSizer( wx.HORIZONTAL )

		self.i2c_offset = wx.TextCtrl( sbSizer121.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		self.i2c_offset.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer143.Add( self.i2c_offset, 0, 0, 0 )

		self.m_staticText1512 = wx.StaticText( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Offset", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1512.Wrap( -1 )

		bSizer143.Add( self.m_staticText1512, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer140.Add( bSizer143, 0, wx.LEFT, 5 )

		bSizer1462 = wx.BoxSizer( wx.HORIZONTAL )

		self.i2c_bit_MSB = wx.TextCtrl( sbSizer121.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 53,-1 ), 0 )
		self.i2c_bit_MSB.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer1462.Add( self.i2c_bit_MSB, 0, 0, 0 )

		self.m_staticText1531 = wx.StaticText( sbSizer121.GetStaticBox(), wx.ID_ANY, u":", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1531.Wrap( -1 )

		bSizer1462.Add( self.m_staticText1531, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.i2c_bit_LSB = wx.TextCtrl( sbSizer121.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 53,-1 ), 0 )
		self.i2c_bit_LSB.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer1462.Add( self.i2c_bit_LSB, 0, 0, 5 )

		self.m_staticText153 = wx.StaticText( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Bit (MSB:LSB )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText153.Wrap( -1 )

		bSizer1462.Add( self.m_staticText153, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer140.Add( bSizer1462, 0, wx.LEFT, 5 )

		bSizer147 = wx.BoxSizer( wx.HORIZONTAL )

		self.i2c_register_value = wx.TextCtrl( sbSizer121.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		bSizer147.Add( self.i2c_register_value, 0, 0, 0 )

		self.m_staticText154 = wx.StaticText( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Register Value", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText154.Wrap( -1 )

		bSizer147.Add( self.m_staticText154, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )


		bSizer140.Add( bSizer147, 0, wx.LEFT, 5 )

		bSizer1482 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button_i2c_write = wx.Button( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Write", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		bSizer1482.Add( self.m_button_i2c_write, 0, 0, 0 )

		self.m_staticText92 = wx.StaticText( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Write Register", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText92.Wrap( -1 )

		bSizer1482.Add( self.m_staticText92, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer140.Add( bSizer1482, 0, wx.LEFT, 5 )

		bSizer862 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button_i2c_read = wx.Button( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Read", wx.Point( -1,-1 ), wx.Size( 120,-1 ), 0 )
		bSizer862.Add( self.m_button_i2c_read, 0, 0, 0 )

		self.m_staticText931 = wx.StaticText( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Read Register", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText931.Wrap( -1 )

		bSizer862.Add( self.m_staticText931, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer140.Add( bSizer862, 0, wx.LEFT, 5 )

		bSizer1251 = wx.BoxSizer( wx.HORIZONTAL )

		self.reg_compare = wx.Button( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Run Compare", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		self.reg_compare.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer1251.Add( self.reg_compare, 0, wx.BOTTOM|wx.LEFT, 5 )

		self.m_staticText9311 = wx.StaticText( sbSizer121.GetStaticBox(), wx.ID_ANY, u"Register Compare", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9311.Wrap( -1 )

		bSizer1251.Add( self.m_staticText9311, 0, wx.ALL, 5 )


		bSizer140.Add( bSizer1251, 1, wx.EXPAND, 5 )


		sbSizer121.Add( bSizer140, 0, 0, 5 )


		bSizer130.Add( sbSizer121, 0, wx.EXPAND|wx.TOP|wx.RIGHT, 5 )


		bSizer158.Add( bSizer130, 1, wx.EXPAND, 5 )


		bSizer15212.Add( bSizer158, 1, wx.EXPAND, 5 )


		self.I2C_page.SetSizer( bSizer15212 )
		self.I2C_page.Layout()
		self.GUC.AddPage( self.I2C_page, u"I2C Program", True )
		self.Power_Select = wx.ScrolledWindow( self.GUC, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.Power_Select.SetScrollRate( 5, 5 )
		self.Power_Select.SetFont( wx.Font( 8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Power_Supply = wx.BoxSizer( wx.VERTICAL )

		Power_Domain_Setup = wx.StaticBoxSizer( wx.StaticBox( self.Power_Select, wx.ID_ANY, u"Power Domain Setup" ), wx.VERTICAL )

		bSizer148 = wx.BoxSizer( wx.VERTICAL )

		bSizer146 = wx.BoxSizer( wx.VERTICAL )

		bSizer1692 = wx.BoxSizer( wx.VERTICAL )

		Power_Title = wx.BoxSizer( wx.HORIZONTAL )

		self.m_textCtrl49 = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"(Power Source Select )", wx.DefaultPosition, wx.Size( 180,-1 ), 0 )
		Power_Title.Add( self.m_textCtrl49, 0, 0, 5 )

		self.m_textCtrl50 = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"(Level )", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		Power_Title.Add( self.m_textCtrl50, 0, 0, 5 )

		self.m_textCtrl51 = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"(Current )", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		Power_Title.Add( self.m_textCtrl51, 0, 0, 5 )


		bSizer1692.Add( Power_Title, 0, 0, 5 )

		Power1 = wx.BoxSizer( wx.HORIZONTAL )

		power_select1Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select1 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select1Choices, 0 )
		self.power_select1.SetSelection( 1 )
		Power1.Add( self.power_select1, 0, 0, 5 )

		self.power_value1 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.750000, 1 )
		self.power_value1.SetDigits( 4 )
		Power1.Add( self.power_value1, 0, 0, 5 )

		self.power_current1 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current1.SetDigits( 4 )
		Power1.Add( self.power_current1, 0, 0, 5 )

		self.Power_label1 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"VDD(TPSM831D31 Channel A )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label1.Wrap( -1 )

		Power1.Add( self.Power_label1, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1692.Add( Power1, 1, wx.EXPAND, 5 )

		Power2 = wx.BoxSizer( wx.HORIZONTAL )

		power_select2Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select2 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select2Choices, 0 )
		self.power_select2.SetSelection( 1 )
		Power2.Add( self.power_select2, 0, 0, 5 )

		self.power_value2 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 1.200000, 1 )
		self.power_value2.SetDigits( 4 )
		Power2.Add( self.power_value2, 0, 0, 5 )

		self.power_current2 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current2.SetDigits( 4 )
		Power2.Add( self.power_current2, 0, 0, 5 )

		self.Power_label2 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"IOVDD(TPSM831D31 Channel B )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label2.Wrap( -1 )

		Power2.Add( self.Power_label2, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1692.Add( Power2, 1, wx.EXPAND, 5 )

		Power3 = wx.BoxSizer( wx.HORIZONTAL )

		power_select3Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select3 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select3Choices, 0 )
		self.power_select3.SetSelection( 1 )
		Power3.Add( self.power_select3, 0, 0, 5 )

		self.power_value3 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.75, 1 )
		self.power_value3.SetDigits( 4 )
		Power3.Add( self.power_value3, 0, 0, 5 )

		self.power_current3 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current3.SetDigits( 4 )
		Power3.Add( self.power_current3, 0, 0, 5 )

		self.Power_label3 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"D0_AVDD_V2(TPSM831D31 Channel A )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label3.Wrap( -1 )

		Power3.Add( self.Power_label3, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1692.Add( Power3, 1, wx.EXPAND, 5 )

		Power4 = wx.BoxSizer( wx.HORIZONTAL )

		power_select4Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select4 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select4Choices, 0 )
		self.power_select4.SetSelection( 1 )
		Power4.Add( self.power_select4, 0, 0, 5 )

		self.power_value4 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 1.200000, 1 )
		self.power_value4.SetDigits( 4 )
		Power4.Add( self.power_value4, 0, 0, 5 )

		self.power_current4 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current4.SetDigits( 4 )
		Power4.Add( self.power_current4, 0, 0, 5 )

		self.Power_label4 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"D0_AVDD12_V2(TPSM831D31 Channel B )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label4.Wrap( -1 )

		Power4.Add( self.Power_label4, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1692.Add( Power4, 1, wx.EXPAND, 5 )

		Power5 = wx.BoxSizer( wx.HORIZONTAL )

		power_select5Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select5 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select5Choices, 0 )
		self.power_select5.SetSelection( 1 )
		Power5.Add( self.power_select5, 0, 0, 5 )

		self.power_value5 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.75, 1 )
		self.power_value5.SetDigits( 4 )
		Power5.Add( self.power_value5, 0, 0, 5 )

		self.power_current5 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current5.SetDigits( 4 )
		Power5.Add( self.power_current5, 0, 0, 5 )

		self.Power_label5 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"D0_AVDD_V1_D1_V1(TPSM831D31 Channel A )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label5.Wrap( -1 )

		Power5.Add( self.Power_label5, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1692.Add( Power5, 1, wx.EXPAND, 5 )

		Power6 = wx.BoxSizer( wx.HORIZONTAL )

		power_select6Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select6 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select6Choices, 0 )
		self.power_select6.SetSelection( 1 )
		Power6.Add( self.power_select6, 0, 0, 5 )

		self.power_value6 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 1.200000, 1 )
		self.power_value6.SetDigits( 4 )
		Power6.Add( self.power_value6, 0, 0, 5 )

		self.power_current6 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current6.SetDigits( 4 )
		Power6.Add( self.power_current6, 0, 0, 5 )

		self.Power_label6 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"D0_AVDD12_V1_D1_V1(TPSM831D31 Channel B )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label6.Wrap( -1 )

		Power6.Add( self.Power_label6, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1692.Add( Power6, 1, wx.EXPAND, 5 )

		Power7 = wx.BoxSizer( wx.HORIZONTAL )

		power_select7Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select7 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select7Choices, 0 )
		self.power_select7.SetSelection( 1 )
		Power7.Add( self.power_select7, 0, 0, 5 )

		self.power_value7 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.75, 1 )
		self.power_value7.SetDigits( 4 )
		Power7.Add( self.power_value7, 0, 0, 5 )

		self.power_current7 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current7.SetDigits( 4 )
		Power7.Add( self.power_current7, 0, 0, 5 )

		self.Power_label7 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"D1_AVDD_V2_D2_V1(TPSM831D31 Channel A )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label7.Wrap( -1 )

		Power7.Add( self.Power_label7, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1692.Add( Power7, 1, wx.EXPAND, 5 )

		Power8 = wx.BoxSizer( wx.HORIZONTAL )

		power_select8Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select8 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select8Choices, 0 )
		self.power_select8.SetSelection( 1 )
		Power8.Add( self.power_select8, 0, 0, 5 )

		self.power_value8 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 1.200000, 1 )
		self.power_value8.SetDigits( 4 )
		Power8.Add( self.power_value8, 0, 0, 5 )

		self.power_current8 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current8.SetDigits( 4 )
		Power8.Add( self.power_current8, 0, 0, 5 )

		self.Power_label8 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"D1_AVDD12_V2_D2_V1(TPSM831D31 Channel B )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label8.Wrap( -1 )

		Power8.Add( self.Power_label8, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1692.Add( Power8, 1, wx.EXPAND, 5 )

		Power9 = wx.BoxSizer( wx.HORIZONTAL )

		power_select9Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select9 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select9Choices, 0 )
		self.power_select9.SetSelection( 1 )
		Power9.Add( self.power_select9, 0, 0, 5 )

		self.power_value9 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.75, 1 )
		self.power_value9.SetDigits( 4 )
		Power9.Add( self.power_value9, 0, 0, 5 )

		self.power_current9 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current9.SetDigits( 4 )
		Power9.Add( self.power_current9, 0, 0, 5 )

		self.Power_label9 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"D2_AVDD_V2(TPSM831D31 Channel A )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label9.Wrap( -1 )

		Power9.Add( self.Power_label9, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1692.Add( Power9, 1, wx.EXPAND, 5 )

		Power10 = wx.BoxSizer( wx.HORIZONTAL )

		power_select10Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select10 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select10Choices, 0 )
		self.power_select10.SetSelection( 1 )
		Power10.Add( self.power_select10, 0, 0, 5 )

		self.power_value10 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 1.200000, 1 )
		self.power_value10.SetDigits( 4 )
		Power10.Add( self.power_value10, 0, 0, 5 )

		self.power_current10 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current10.SetDigits( 4 )
		Power10.Add( self.power_current10, 0, 0, 5 )

		self.Power_label10 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"D2_AVDD12_V2(TPSM831D31 Channel B )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label10.Wrap( -1 )

		Power10.Add( self.Power_label10, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1692.Add( Power10, 1, wx.EXPAND, 5 )


		bSizer146.Add( bSizer1692, 0, 0, 5 )

		bSizer1871 = wx.BoxSizer( wx.VERTICAL )

		Power11 = wx.BoxSizer( wx.HORIZONTAL )

		power_select11Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select11 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select11Choices, 0 )
		self.power_select11.SetSelection( 1 )
		Power11.Add( self.power_select11, 0, 0, 5 )

		self.power_value11 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.75, 1 )
		self.power_value11.SetDigits( 4 )
		Power11.Add( self.power_value11, 0, 0, 5 )

		self.power_current11 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current11.SetDigits( 4 )
		Power11.Add( self.power_current11, 0, 0, 5 )

		self.Power_label11 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Power Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label11.Wrap( -1 )

		Power11.Add( self.Power_label11, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1871.Add( Power11, 0, 0, 5 )

		Power12 = wx.BoxSizer( wx.HORIZONTAL )

		power_select12Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select12 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select12Choices, 0 )
		self.power_select12.SetSelection( 1 )
		Power12.Add( self.power_select12, 0, 0, 5 )

		self.power_value12 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.75, 1 )
		self.power_value12.SetDigits( 4 )
		Power12.Add( self.power_value12, 0, 0, 5 )

		self.power_current12 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current12.SetDigits( 4 )
		Power12.Add( self.power_current12, 0, 0, 5 )

		self.Power_label12 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Power Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label12.Wrap( -1 )

		Power12.Add( self.Power_label12, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1871.Add( Power12, 0, 0, 5 )

		Power13 = wx.BoxSizer( wx.HORIZONTAL )

		power_select13Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select13 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select13Choices, 0 )
		self.power_select13.SetSelection( 1 )
		Power13.Add( self.power_select13, 0, 0, 5 )

		self.power_value13 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.75, 1 )
		self.power_value13.SetDigits( 4 )
		Power13.Add( self.power_value13, 0, 0, 5 )

		self.power_current13 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current13.SetDigits( 4 )
		Power13.Add( self.power_current13, 0, 0, 5 )

		self.Power_label13 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Power Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label13.Wrap( -1 )

		Power13.Add( self.Power_label13, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1871.Add( Power13, 0, 0, 5 )

		Power14 = wx.BoxSizer( wx.HORIZONTAL )

		power_select14Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select14 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select14Choices, 0 )
		self.power_select14.SetSelection( 1 )
		Power14.Add( self.power_select14, 0, 0, 5 )

		self.power_value14 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.75, 1 )
		self.power_value14.SetDigits( 4 )
		Power14.Add( self.power_value14, 0, 0, 5 )

		self.power_current14 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current14.SetDigits( 4 )
		Power14.Add( self.power_current14, 0, 0, 5 )

		self.Power_label14 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Power Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label14.Wrap( -1 )

		Power14.Add( self.Power_label14, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1871.Add( Power14, 0, 0, 5 )

		Power15 = wx.BoxSizer( wx.HORIZONTAL )

		power_select15Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select15 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select15Choices, 0 )
		self.power_select15.SetSelection( 1 )
		Power15.Add( self.power_select15, 0, 0, 5 )

		self.power_value15 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.75, 1 )
		self.power_value15.SetDigits( 4 )
		Power15.Add( self.power_value15, 0, 0, 5 )

		self.power_current15 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current15.SetDigits( 4 )
		Power15.Add( self.power_current15, 0, 0, 5 )

		self.Power_label15 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Power Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label15.Wrap( -1 )

		Power15.Add( self.Power_label15, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1871.Add( Power15, 0, 0, 5 )

		Power16 = wx.BoxSizer( wx.HORIZONTAL )

		power_select16Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select16 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select16Choices, 0 )
		self.power_select16.SetSelection( 1 )
		Power16.Add( self.power_select16, 0, 0, 5 )

		self.power_value16 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.75, 1 )
		self.power_value16.SetDigits( 4 )
		Power16.Add( self.power_value16, 0, 0, 5 )

		self.power_current16 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current16.SetDigits( 4 )
		Power16.Add( self.power_current16, 0, 0, 5 )

		self.Power_label16 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Power Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label16.Wrap( -1 )

		Power16.Add( self.Power_label16, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1871.Add( Power16, 0, 0, 5 )

		Power17 = wx.BoxSizer( wx.HORIZONTAL )

		power_select17Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select17 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select17Choices, 0 )
		self.power_select17.SetSelection( 1 )
		Power17.Add( self.power_select17, 0, 0, 5 )

		self.power_value17 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.75, 1 )
		self.power_value17.SetDigits( 4 )
		Power17.Add( self.power_value17, 0, 0, 5 )

		self.power_current17 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current17.SetDigits( 4 )
		Power17.Add( self.power_current17, 0, 0, 5 )

		self.Power_label17 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Power Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label17.Wrap( -1 )

		Power17.Add( self.Power_label17, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1871.Add( Power17, 0, 0, 5 )

		Power18 = wx.BoxSizer( wx.HORIZONTAL )

		power_select18Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select18 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select18Choices, 0 )
		self.power_select18.SetSelection( 1 )
		Power18.Add( self.power_select18, 0, 0, 5 )

		self.power_value18 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.75, 1 )
		self.power_value18.SetDigits( 4 )
		Power18.Add( self.power_value18, 0, 0, 5 )

		self.power_current18 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current18.SetDigits( 4 )
		Power18.Add( self.power_current18, 0, 0, 5 )

		self.Power_label18 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Power Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label18.Wrap( -1 )

		Power18.Add( self.Power_label18, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1871.Add( Power18, 0, 0, 5 )

		Power19 = wx.BoxSizer( wx.HORIZONTAL )

		power_select19Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select19 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select19Choices, 0 )
		self.power_select19.SetSelection( 1 )
		Power19.Add( self.power_select19, 0, 0, 5 )

		self.power_value19 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.75, 1 )
		self.power_value19.SetDigits( 4 )
		Power19.Add( self.power_value19, 0, 0, 5 )

		self.power_current19 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current19.SetDigits( 4 )
		Power19.Add( self.power_current19, 0, 0, 5 )

		self.Power_label19 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Power Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label19.Wrap( -1 )

		Power19.Add( self.Power_label19, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1871.Add( Power19, 0, 0, 5 )

		Power20 = wx.BoxSizer( wx.HORIZONTAL )

		power_select20Choices = [ u"Bypass", u"PMIC", u"LDO", u"Power_Supply_1_CH1", u"Power_Supply_1_CH2", u"Power_Supply_1_CH3", u"Power_Supply_2_CH1", u"Power_Supply_2_CH2", u"Power_Supply_2_CH3", u"Power_Supply_3_CH1", u"Power_Supply_3_CH2", u"Power_Supply_3_CH3", u"Power_Supply_4_CH1", u"Power_Supply_4_CH2", u"Power_Supply_4_CH3", u"Power_Supply_5_CH1", u"Power_Supply_5_CH2", u"Power_Supply_5_CH3" ]
		self.power_select20 = wx.ComboBox( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"PMIC", wx.DefaultPosition, wx.Size( 180,-1 ), power_select20Choices, 0 )
		self.power_select20.SetSelection( 1 )
		Power20.Add( self.power_select20, 0, 0, 5 )

		self.power_value20 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 1.2, 0.75, 1 )
		self.power_value20.SetDigits( 4 )
		Power20.Add( self.power_value20, 0, 0, 5 )

		self.power_current20 = wx.SpinCtrlDouble( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 120, 5, 1 )
		self.power_current20.SetDigits( 4 )
		Power20.Add( self.power_current20, 0, 0, 5 )

		self.Power_label20 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Power Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Power_label20.Wrap( -1 )

		Power20.Add( self.Power_label20, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer1871.Add( Power20, 1, wx.EXPAND, 5 )


		bSizer146.Add( bSizer1871, 1, wx.EXPAND, 5 )


		bSizer148.Add( bSizer146, 1, wx.EXPAND, 5 )


		Power_Domain_Setup.Add( bSizer148, 0, 0, 5 )

		bSizer116 = wx.BoxSizer( wx.HORIZONTAL )

		self.power_update_wx = wx.Button( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Press Update Voltage", wx.DefaultPosition, wx.Size( 180,-1 ), 0 )
		self.power_update_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer116.Add( self.power_update_wx, 0, wx.TOP|wx.ALIGN_CENTER_VERTICAL, 5 )


		Power_Domain_Setup.Add( bSizer116, 0, 0, 5 )

		bSizer150 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText95 = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"                       (VISA Address )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText95.Wrap( -1 )

		bSizer150.Add( self.m_staticText95, 0, wx.ALL, 5 )

		Power1_visa = wx.BoxSizer( wx.HORIZONTAL )

		self.power1_visa_wx = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"USB0::0x2A8D::0x3302::MY61001409::0::INSTR", wx.DefaultPosition, wx.Size( 300,22 ), 0 )
		self.power1_visa_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Power1_visa.Add( self.power1_visa_wx, 0, 0, 5 )

		self.power1_visa_status_wx = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,22 ), 0 )
		Power1_visa.Add( self.power1_visa_status_wx, 0, 0, 5 )

		self.power1_title = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Keysight E36000 Series(Power_Supply_1 )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.power1_title.Wrap( -1 )

		self.power1_title.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Power1_visa.Add( self.power1_title, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer150.Add( Power1_visa, 0, 0, 5 )

		Power2_visa = wx.BoxSizer( wx.HORIZONTAL )

		self.power2_visa_wx = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"USB0::0x2A8D::0x1102::MY59142062::0::INSTR", wx.DefaultPosition, wx.Size( 300,22 ), 0 )
		self.power2_visa_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Power2_visa.Add( self.power2_visa_wx, 0, 0, 5 )

		self.power2_visa_status_wx = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,22 ), 0 )
		Power2_visa.Add( self.power2_visa_status_wx, 0, 0, 5 )

		self.power2_title = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Keysight E36000 Series(Power_Supply_2 )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.power2_title.Wrap( -1 )

		self.power2_title.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Power2_visa.Add( self.power2_title, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer150.Add( Power2_visa, 1, wx.EXPAND, 5 )

		Power3_visa = wx.BoxSizer( wx.HORIZONTAL )

		self.power3_visa_wx = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"USB0::0x2A8D::0x3302::MY61001202::0::INSTR", wx.DefaultPosition, wx.Size( 300,22 ), 0 )
		self.power3_visa_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Power3_visa.Add( self.power3_visa_wx, 0, 0, 5 )

		self.power3_visa_status_wx = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,22 ), 0 )
		Power3_visa.Add( self.power3_visa_status_wx, 0, 0, 5 )

		self.power3_title = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Keysight E36000 Series(Power_Supply_3 )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.power3_title.Wrap( -1 )

		self.power3_title.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Power3_visa.Add( self.power3_title, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer150.Add( Power3_visa, 1, wx.EXPAND, 5 )

		Power4_visa = wx.BoxSizer( wx.HORIZONTAL )

		self.power4_visa_wx = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"USB0::0x2A8D::0x1202::MY59001046::0::INSTR", wx.DefaultPosition, wx.Size( 300,22 ), 0 )
		self.power4_visa_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Power4_visa.Add( self.power4_visa_wx, 0, 0, 5 )

		self.power4_visa_status_wx = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,22 ), 0 )
		Power4_visa.Add( self.power4_visa_status_wx, 0, 0, 5 )

		self.power4_title = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Keysight E36000 Series(Power_Supply_4 )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.power4_title.Wrap( -1 )

		self.power4_title.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Power4_visa.Add( self.power4_title, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer150.Add( Power4_visa, 1, wx.EXPAND, 5 )

		Power5_visa = wx.BoxSizer( wx.HORIZONTAL )

		self.power5_visa_wx = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"USB0::0x2A8D::0x3302::MY59001241::0::INSTR", wx.DefaultPosition, wx.Size( 300,22 ), 0 )
		self.power5_visa_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Power5_visa.Add( self.power5_visa_wx, 0, 0, 5 )

		self.power5_visa_status_wx = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,22 ), 0 )
		Power5_visa.Add( self.power5_visa_status_wx, 0, 0, 5 )

		self.power5_title = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Keysight E36000 Series(Power_Supply_5 )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.power5_title.Wrap( -1 )

		self.power5_title.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		Power5_visa.Add( self.power5_title, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer150.Add( Power5_visa, 1, wx.EXPAND, 5 )

		All_Power_Cycle = wx.BoxSizer( wx.HORIZONTAL )

		self.power_cycle_visa = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"USB0::0x2A8D::0x3302::MY59001241::0::INSTR", wx.DefaultPosition, wx.Size( 300,22 ), 0 )
		self.power_cycle_visa.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		All_Power_Cycle.Add( self.power_cycle_visa, 0, 0, 5 )

		self.power_cycle_visa_status = wx.TextCtrl( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,22 ), 0 )
		All_Power_Cycle.Add( self.power_cycle_visa_status, 0, 0, 5 )

		self.power_cycle_visa_title = wx.StaticText( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Keysight E36000 Series(Power_Supply_For Power Cycle Use )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.power_cycle_visa_title.Wrap( -1 )

		self.power_cycle_visa_title.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		All_Power_Cycle.Add( self.power_cycle_visa_title, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer150.Add( All_Power_Cycle, 1, wx.EXPAND, 5 )

		self.power_info_wx = wx.Button( Power_Domain_Setup.GetStaticBox(), wx.ID_ANY, u"Press Check VISA Bus", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		self.power_info_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer150.Add( self.power_info_wx, 0, wx.TOP, 5 )


		Power_Domain_Setup.Add( bSizer150, 0, 0, 5 )


		Power_Supply.Add( Power_Domain_Setup, 0, wx.EXPAND|wx.TOP|wx.RIGHT, 5 )


		self.Power_Select.SetSizer( Power_Supply )
		self.Power_Select.Layout()
		Power_Supply.Fit( self.Power_Select )
		self.GUC.AddPage( self.Power_Select, u"DC Power", False )
		self.Meter_Select = wx.ScrolledWindow( self.GUC, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.HSCROLL|wx.VSCROLL )
		self.Meter_Select.SetScrollRate( 5, 5 )
		self.Meter_Select.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer113 = wx.BoxSizer( wx.VERTICAL )

		bSizer212 = wx.BoxSizer( wx.VERTICAL )

		bSizer196 = wx.BoxSizer( wx.VERTICAL )

		DataLog_VISA = wx.StaticBoxSizer( wx.StaticBox( self.Meter_Select, wx.ID_ANY, u"DataLog VISA(Measure Power Sense Pin / REXT10K Voltage )" ), wx.VERTICAL )

		bSizer1481 = wx.BoxSizer( wx.VERTICAL )

		bSizer1461 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer16921 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText93 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u" (Measure Voltage )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText93.Wrap( -1 )

		bSizer16921.Add( self.m_staticText93, 0, wx.ALL, 5 )

		point1 = wx.BoxSizer( wx.HORIZONTAL )

		self.VDD_V_SENSE = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point1.Add( self.VDD_V_SENSE, 0, wx.LEFT, 5 )

		self.m_staticText1321 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 101_VDD(TPSM831D31 Channel A )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1321.Wrap( -1 )

		point1.Add( self.m_staticText1321, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		bSizer16921.Add( point1, 0, 0, 5 )

		point2 = wx.BoxSizer( wx.HORIZONTAL )

		self.IOVDD_SENSE = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point2.Add( self.IOVDD_SENSE, 0, wx.LEFT, 5 )

		self.m_staticText1331 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 102_IOVDD(TPSM831D31 Channel B )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1331.Wrap( -1 )

		point2.Add( self.m_staticText1331, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point2, 0, wx.EXPAND, 5 )

		point3 = wx.BoxSizer( wx.HORIZONTAL )

		self.D0_AVDD_V2_SENSE = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point3.Add( self.D0_AVDD_V2_SENSE, 0, wx.LEFT, 5 )

		self.m_staticText1341 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 103_D0_AVDD_V2(TPSM831D31 Channel A )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1341.Wrap( -1 )

		self.m_staticText1341.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		point3.Add( self.m_staticText1341, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point3, 0, wx.EXPAND, 5 )

		point4 = wx.BoxSizer( wx.HORIZONTAL )

		self.D0_AVDD12_V2_SENSE = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point4.Add( self.D0_AVDD12_V2_SENSE, 0, wx.LEFT, 5 )

		self.m_staticText1351 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 104_D0_AVDD12_V2(TPSM831D31 Channel B )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1351.Wrap( -1 )

		point4.Add( self.m_staticText1351, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point4, 0, wx.EXPAND, 5 )

		point5 = wx.BoxSizer( wx.HORIZONTAL )

		self.D0_AVDD_V1_D1_V1_SENSE = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point5.Add( self.D0_AVDD_V1_D1_V1_SENSE, 0, wx.LEFT, 5 )

		self.m_staticText1361 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 105_D0_AVDD_V1_D1_V1(TPSM831D31 Channel A )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1361.Wrap( -1 )

		point5.Add( self.m_staticText1361, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point5, 0, 0, 5 )

		point6 = wx.BoxSizer( wx.HORIZONTAL )

		self.D0_AVDD12_V1_D1_V1_SENSE = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point6.Add( self.D0_AVDD12_V1_D1_V1_SENSE, 0, wx.LEFT, 5 )

		self.m_staticText1371 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 106_D0_AVDD12_V1_D1_V1(TPSM831D31 Channel B )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1371.Wrap( -1 )

		point6.Add( self.m_staticText1371, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point6, 0, 0, 5 )

		point7 = wx.BoxSizer( wx.HORIZONTAL )

		self.D1_AVDD_V2_D2_V1_SENSE = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point7.Add( self.D1_AVDD_V2_D2_V1_SENSE, 0, wx.LEFT, 5 )

		self.m_staticText1461 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 107_D1_AVDD_V2_D2_V1(TPSM831D31 Channel A )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1461.Wrap( -1 )

		point7.Add( self.m_staticText1461, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point7, 0, 0, 5 )

		point8 = wx.BoxSizer( wx.HORIZONTAL )

		self.D1_AVDD12_V2_D2_V1_SENSE = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point8.Add( self.D1_AVDD12_V2_D2_V1_SENSE, 0, wx.LEFT, 5 )

		self.m_staticText1471 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 108_D1_AVDD12_V2_D2_V1(TPSM831D31 Channel B )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1471.Wrap( -1 )

		point8.Add( self.m_staticText1471, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point8, 0, 0, 5 )

		point9 = wx.BoxSizer( wx.HORIZONTAL )

		self.D2_AVDD_V2_SENSE = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point9.Add( self.D2_AVDD_V2_SENSE, 0, wx.LEFT, 5 )

		self.m_staticText1481 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 109_D2_AVDD_V2(TPSM831D31 Channel A )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1481.Wrap( -1 )

		point9.Add( self.m_staticText1481, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point9, 0, 0, 5 )

		point10 = wx.BoxSizer( wx.HORIZONTAL )

		self.D2_AVDD12_V2_SENSE = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point10.Add( self.D2_AVDD12_V2_SENSE, 0, wx.LEFT, 5 )

		self.m_staticText1491 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 110_D2_AVDD12_V2(TPSM831D31 Channel B )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1491.Wrap( -1 )

		point10.Add( self.m_staticText1491, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point10, 0, 0, 5 )

		point11 = wx.BoxSizer( wx.HORIZONTAL )

		self.D0_VDD_V_SENSE_wx = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point11.Add( self.D0_VDD_V_SENSE_wx, 0, wx.LEFT, 5 )

		self.m_staticText1501 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 111", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1501.Wrap( -1 )

		point11.Add( self.m_staticText1501, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point11, 0, 0, 5 )

		point12 = wx.BoxSizer( wx.HORIZONTAL )

		self.SYS_AVDD12_PLL_SENSE_wx = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point12.Add( self.SYS_AVDD12_PLL_SENSE_wx, 0, wx.LEFT, 5 )

		self.m_staticText15111 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 112", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15111.Wrap( -1 )

		point12.Add( self.m_staticText15111, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point12, 0, 0, 5 )

		point13 = wx.BoxSizer( wx.HORIZONTAL )

		self.D1_REXT_V2_wx = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point13.Add( self.D1_REXT_V2_wx, 0, wx.LEFT, 5 )

		self.m_staticText14611 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 113", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14611.Wrap( -1 )

		point13.Add( self.m_staticText14611, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point13, 0, 0, 5 )

		point14 = wx.BoxSizer( wx.HORIZONTAL )

		self.D1_REXT_V1 = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point14.Add( self.D1_REXT_V1, 0, wx.LEFT, 5 )

		self.m_staticText14711 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 114", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14711.Wrap( -1 )

		point14.Add( self.m_staticText14711, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point14, 0, 0, 5 )

		point15 = wx.BoxSizer( wx.HORIZONTAL )

		self.D2_REXT_V2_wx = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point15.Add( self.D2_REXT_V2_wx, 0, wx.LEFT, 5 )

		self.m_staticText14811 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 115", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14811.Wrap( -1 )

		point15.Add( self.m_staticText14811, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point15, 0, 0, 5 )

		point16 = wx.BoxSizer( wx.HORIZONTAL )

		self.D2_REXT_V1_wx = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point16.Add( self.D2_REXT_V1_wx, 0, wx.LEFT, 5 )

		self.m_staticText14911 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 116", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14911.Wrap( -1 )

		point16.Add( self.m_staticText14911, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point16, 0, 0, 5 )

		point17 = wx.BoxSizer( wx.HORIZONTAL )

		self.D0_REXT_V1_wx = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point17.Add( self.D0_REXT_V1_wx, 0, wx.LEFT, 5 )

		self.m_staticText15011 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 117", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15011.Wrap( -1 )

		point17.Add( self.m_staticText15011, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point17, 0, 0, 5 )

		point18 = wx.BoxSizer( wx.HORIZONTAL )

		self.D0_REXT_V2_wx = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		point18.Add( self.D0_REXT_V2_wx, 0, wx.LEFT, 5 )

		self.m_staticText151111 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"DataLog_Channel 118", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText151111.Wrap( -1 )

		point18.Add( self.m_staticText151111, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16921.Add( point18, 0, 0, 5 )


		bSizer1461.Add( bSizer16921, 0, 0, 5 )

		bSizer16911 = wx.BoxSizer( wx.VERTICAL )


		bSizer1461.Add( bSizer16911, 0, wx.LEFT, 5 )


		bSizer1481.Add( bSizer1461, 0, 0, 5 )


		DataLog_VISA.Add( bSizer1481, 0, wx.BOTTOM, 5 )

		self.datalog_meas_wx = wx.Button( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"Press Measure Voltage", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		self.datalog_meas_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		DataLog_VISA.Add( self.datalog_meas_wx, 0, wx.LEFT, 5 )

		self.datalog_visa1 = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"                                (VISA Address )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.datalog_visa1.Wrap( -1 )

		DataLog_VISA.Add( self.datalog_visa1, 0, wx.ALL, 5 )

		datalog1 = wx.BoxSizer( wx.HORIZONTAL )

		self.datalog1_visa_wx = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"USB0::0x2A8D::0x5101::MY58014090::0::INSTR", wx.DefaultPosition, wx.Size( 300,22 ), 0 )
		self.datalog1_visa_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		datalog1.Add( self.datalog1_visa_wx, 0, 0, 5 )

		self.datalog1_visa_status_wx = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,22 ), 0 )
		datalog1.Add( self.datalog1_visa_status_wx, 0, 0, 5 )

		self.datalog1_title = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"Keysight DAQ970A VISA", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.datalog1_title.Wrap( -1 )

		self.datalog1_title.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		datalog1.Add( self.datalog1_title, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )


		DataLog_VISA.Add( datalog1, 0, wx.LEFT, 5 )

		datalog2 = wx.BoxSizer( wx.HORIZONTAL )

		self.datalog2_visa_wx = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"GPIB1::7::INSTR", wx.DefaultPosition, wx.Size( 300,22 ), 0 )
		self.datalog2_visa_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		datalog2.Add( self.datalog2_visa_wx, 0, 0, 5 )

		self.datalog2_visa_status_wx = wx.TextCtrl( DataLog_VISA.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,22 ), 0 )
		datalog2.Add( self.datalog2_visa_status_wx, 0, 0, 5 )

		self.datalog2_title = wx.StaticText( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"Keysight 34970A VISA", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.datalog2_title.Wrap( -1 )

		self.datalog2_title.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		datalog2.Add( self.datalog2_title, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )


		DataLog_VISA.Add( datalog2, 0, wx.LEFT, 5 )

		self.meter_info_wx = wx.Button( DataLog_VISA.GetStaticBox(), wx.ID_ANY, u"Press Check VISA Bus", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		self.meter_info_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		DataLog_VISA.Add( self.meter_info_wx, 0, wx.TOP|wx.LEFT, 5 )


		bSizer196.Add( DataLog_VISA, 1, wx.TOP, 5 )


		bSizer212.Add( bSizer196, 0, 0, 5 )


		bSizer113.Add( bSizer212, 0, wx.EXPAND, 5 )


		self.Meter_Select.SetSizer( bSizer113 )
		self.Meter_Select.Layout()
		bSizer113.Fit( self.Meter_Select )
		self.GUC.AddPage( self.Meter_Select, u"Meter", False )
		self.ThermalAir = wx.ScrolledWindow( self.GUC, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.HSCROLL|wx.VSCROLL )
		self.ThermalAir.SetScrollRate( 5, 5 )
		self.ThermalAir.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer21 = wx.BoxSizer( wx.VERTICAL )

		bSizer154 = wx.BoxSizer( wx.VERTICAL )

		sbSizer201 = wx.StaticBoxSizer( wx.StaticBox( self.ThermalAir, wx.ID_ANY, u"Thermal Instrument VISA" ), wx.VERTICAL )

		bSizer174 = wx.BoxSizer( wx.HORIZONTAL )

		self.TA5000A_visa_wx = wx.TextCtrl( sbSizer201.GetStaticBox(), wx.ID_ANY, u"TCPIP0::192.168.1.1::inst0::INSTR", wx.DefaultPosition, wx.Size( 200,22 ), 0 )
		self.TA5000A_visa_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer174.Add( self.TA5000A_visa_wx, 0, wx.ALL, 0 )

		self.TA5000A_visa_status_wx = wx.TextCtrl( sbSizer201.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,22 ), 0 )
		bSizer174.Add( self.TA5000A_visa_status_wx, 0, 0, 5 )

		self.TA5000A_title = wx.StaticText( sbSizer201.GetStaticBox(), wx.ID_ANY, u"MPI Thermal TA5000A", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.TA5000A_title.Wrap( -1 )

		self.TA5000A_title.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer174.Add( self.TA5000A_title, 0, wx.ALL, 5 )


		sbSizer201.Add( bSizer174, 0, 0, 5 )

		bSizer28 = wx.BoxSizer( wx.HORIZONTAL )

		self.Termal_Delay = wx.SpinCtrl( sbSizer201.GetStaticBox(), wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 200,-1 ), wx.SP_ARROW_KEYS, 0, 99999999, 120 )
		self.Termal_Delay.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer28.Add( self.Termal_Delay, 0, 0, 0 )

		self.m_staticText111 = wx.StaticText( sbSizer201.GetStaticBox(), wx.ID_ANY, u"Termal Delay Time(Unit : Second)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )

		self.m_staticText111.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer28.Add( self.m_staticText111, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		sbSizer201.Add( bSizer28, 0, wx.LEFT, 0 )

		bSizer1731 = wx.BoxSizer( wx.VERTICAL )

		self.thermal_info_wx = wx.Button( sbSizer201.GetStaticBox(), wx.ID_ANY, u"Press Check VISA Bus", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		self.thermal_info_wx.SetFont( wx.Font( 8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "@Arial Unicode MS" ) )

		bSizer1731.Add( self.thermal_info_wx, 0, 0, 5 )


		sbSizer201.Add( bSizer1731, 0, 0, 5 )


		bSizer154.Add( sbSizer201, 0, wx.TOP, 5 )


		bSizer21.Add( bSizer154, 0, 0, 5 )


		self.ThermalAir.SetSizer( bSizer21 )
		self.ThermalAir.Layout()
		bSizer21.Fit( self.ThermalAir )
		self.GUC.AddPage( self.ThermalAir, u"Thermal Air", False )
		self.Others = wx.ScrolledWindow( self.GUC, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.Others.SetScrollRate( 5, 5 )
		bSizer186 = wx.BoxSizer( wx.HORIZONTAL )

		Power_Source1 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer186.Add( Power_Source1, 0, wx.LEFT, 5 )

		bSizer187 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer186.Add( bSizer187, 0, wx.LEFT, 5 )

		bSizer188 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer186.Add( bSizer188, 0, 0, 5 )

		bSizer122 = wx.BoxSizer( wx.VERTICAL )


		bSizer186.Add( bSizer122, 1, wx.EXPAND, 5 )


		self.Others.SetSizer( bSizer186 )
		self.Others.Layout()
		bSizer186.Fit( self.Others )
		self.GUC.AddPage( self.Others, u"Others", False )

		bSizer23.Add( self.GUC, 0, 0, 15 )


		self.Configure.SetSizer( bSizer23 )
		self.Configure.Layout()
		self.m_notebook.AddPage( self.Configure, u"Configure", False )

		bSizer1.Add( self.m_notebook, 0, 0, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_toggleBtn_connect.Bind( wx.EVT_TOGGLEBUTTON, self.connect )
		self.data_training_en.Bind( wx.EVT_TOGGLEBUTTON, self.data_training_event )
		self.eye_scan_wx.Bind( wx.EVT_TOGGLEBUTTON, self.eye_scan_even )
		self.retry_show_count.Bind( wx.EVT_TOGGLEBUTTON, self.retry_show_fail_count_event )
		self.voltage_sense.Bind( wx.EVT_TOGGLEBUTTON, self.reg_sequence_even )
		self.ThermalOn_OFF.Bind( wx.EVT_TOGGLEBUTTON, self.Thermal_OnOff )
		self.reg_sequence.Bind( wx.EVT_TOGGLEBUTTON, self.reg_sequence_even )
		self.m_toggleBtn_run_test.Bind( wx.EVT_TOGGLEBUTTON, self.run )
		self.m_richText1.Bind( wx.EVT_TEXT_ENTER, self.stop_infinite )
		self.m_button_clear.Bind( wx.EVT_BUTTON, self.clear_text )
		self.Thermal_die_en.Bind( wx.EVT_TOGGLEBUTTON, self.reg_sequence_even )
		self.tree_item.Bind( wx.dataview.EVT_TREELIST_SELECTION_CHANGED, self.select_tree_item_event )
		self.reg_map_load.Bind( wx.EVT_BUTTON, self.reg_map_load_event )
		self.tree_seach.Bind( wx.EVT_TEXT, self.tree_seach_event )
		self.m_button_i2c_write.Bind( wx.EVT_BUTTON, self.i2c_write )
		self.m_button_i2c_read.Bind( wx.EVT_BUTTON, self.i2c_read )
		self.reg_compare.Bind( wx.EVT_BUTTON, self.reg_compare_event )
		self.power_update_wx.Bind( wx.EVT_BUTTON, self.power_update_even )
		self.power1_visa_wx.Bind( wx.EVT_TEXT, self.power1_visa_even )
		self.power2_visa_wx.Bind( wx.EVT_TEXT, self.power2_visa_even )
		self.power3_visa_wx.Bind( wx.EVT_TEXT, self.power3_visa_even )
		self.power4_visa_wx.Bind( wx.EVT_TEXT, self.power4_visa_even )
		self.power5_visa_wx.Bind( wx.EVT_TEXT, self.power5_visa_even )
		self.power_cycle_visa.Bind( wx.EVT_TEXT, self.power5_visa_even )
		self.power_info_wx.Bind( wx.EVT_BUTTON, self.power_info_even )
		self.datalog_meas_wx.Bind( wx.EVT_BUTTON, self.datalog_meas_even )
		self.datalog1_visa_wx.Bind( wx.EVT_TEXT, self.datalog1_visa_even )
		self.datalog2_visa_wx.Bind( wx.EVT_TEXT, self.datalog2_visa_even )
		self.meter_info_wx.Bind( wx.EVT_BUTTON, self.meter_info_even )
		self.TA5000A_visa_wx.Bind( wx.EVT_TEXT, self.TA5000A_visa_even )
		self.thermal_info_wx.Bind( wx.EVT_BUTTON, self.thermal_info_even )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def connect( self, event ):
		event.Skip()

	def data_training_event( self, event ):
		event.Skip()

	def eye_scan_even( self, event ):
		event.Skip()

	def retry_show_fail_count_event( self, event ):
		event.Skip()

	def reg_sequence_even( self, event ):
		event.Skip()

	def Thermal_OnOff( self, event ):
		event.Skip()


	def run( self, event ):
		event.Skip()

	def stop_infinite( self, event ):
		event.Skip()

	def clear_text( self, event ):
		event.Skip()


	def select_tree_item_event( self, event ):
		event.Skip()

	def reg_map_load_event( self, event ):
		event.Skip()

	def tree_seach_event( self, event ):
		event.Skip()

	def i2c_write( self, event ):
		event.Skip()

	def i2c_read( self, event ):
		event.Skip()

	def reg_compare_event( self, event ):
		event.Skip()

	def power_update_even( self, event ):
		event.Skip()

	def power1_visa_even( self, event ):
		event.Skip()

	def power2_visa_even( self, event ):
		event.Skip()

	def power3_visa_even( self, event ):
		event.Skip()

	def power4_visa_even( self, event ):
		event.Skip()

	def power5_visa_even( self, event ):
		event.Skip()


	def power_info_even( self, event ):
		event.Skip()

	def datalog_meas_even( self, event ):
		event.Skip()

	def datalog1_visa_even( self, event ):
		event.Skip()

	def datalog2_visa_even( self, event ):
		event.Skip()

	def meter_info_even( self, event ):
		event.Skip()

	def TA5000A_visa_even( self, event ):
		event.Skip()

	def thermal_info_even( self, event ):
		event.Skip()


