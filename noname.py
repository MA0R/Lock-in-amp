# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui
import wx.grid

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Instrument Controller", pos = wx.DefaultPosition, size = wx.Size( 1500,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.m_mgr = wx.aui.AuiManager()
		self.m_mgr.SetManagedWindow( self )
		self.m_mgr.SetFlags(wx.aui.AUI_MGR_DEFAULT)
		
		self.m_auinotebook4 = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.Point( -1,-1 ), wx.Size( 500,-1 ), 0 )
		self.m_mgr.AddPane( self.m_auinotebook4, wx.aui.AuiPaneInfo() .Left() .CloseButton( False ).MaximizeButton( True ).MinimizeButton( True ).PinButton( True ).Dock().Resizable().FloatingSize( wx.Size( -1,-1 ) ) )
		
		self.m_panel5 = wx.Panel( self.m_auinotebook4, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		gbSizer3 = wx.GridBagSizer( 0, 0 )
		gbSizer3.SetFlexibleDirection( wx.BOTH )
		gbSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_button13 = wx.Button( self.m_panel5, wx.ID_ANY, u"Generate a table", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer3.Add( self.m_button13, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.Analysis_file_name = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer3.Add( self.Analysis_file_name, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText10 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Analysis file name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		gbSizer3.Add( self.m_staticText10, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button122 = wx.Button( self.m_panel5, wx.ID_ANY, u"Analyse data", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer3.Add( self.m_button122, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button5 = wx.Button( self.m_panel5, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer3.Add( self.m_button5, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button6 = wx.Button( self.m_panel5, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer3.Add( self.m_button6, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl81 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,250 ), wx.TE_MULTILINE )
		gbSizer3.Add( self.m_textCtrl81, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 3 ), wx.ALL, 5 )
		
		self.m_button12 = wx.Button( self.m_panel5, wx.ID_ANY, u"Make Safe", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button12.SetBackgroundColour( wx.Colour( 0, 255, 0 ) )
		
		gbSizer3.Add( self.m_button12, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText51 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Event reports", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )
		gbSizer3.Add( self.m_staticText51, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		self.m_panel5.SetSizer( gbSizer3 )
		self.m_panel5.Layout()
		gbSizer3.Fit( self.m_panel5 )
		self.m_auinotebook4.AddPage( self.m_panel5, u"Control", False, wx.NullBitmap )
		self.m_panel511 = wx.Panel( self.m_auinotebook4, wx.ID_ANY, wx.Point( -1,-1 ), wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		gbSizer311 = wx.GridBagSizer( 0, 0 )
		gbSizer311.SetFlexibleDirection( wx.BOTH )
		gbSizer311.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		LcinAdressChoices = []
		self.LcinAdress = wx.ComboBox( self.m_panel511, wx.ID_ANY, u"GPIB0::8::INSTR", wx.DefaultPosition, wx.DefaultSize, LcinAdressChoices, 0 )
		gbSizer311.Add( self.LcinAdress, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		MeterAdressChoices = []
		self.MeterAdress = wx.ComboBox( self.m_panel511, wx.ID_ANY, u"GPIB0::24::INSTR", wx.DefaultPosition, wx.DefaultSize, MeterAdressChoices, 0 )
		gbSizer311.Add( self.MeterAdress, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		SourceAdressChoices = []
		self.SourceAdress = wx.ComboBox( self.m_panel511, wx.ID_ANY, u"GPIB0::4::INSTR", wx.DefaultPosition, wx.DefaultSize, SourceAdressChoices, 0 )
		gbSizer311.Add( self.SourceAdress, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText101 = wx.StaticText( self.m_panel511, wx.ID_ANY, u"Attenuator", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText101.Wrap( -1 )
		gbSizer311.Add( self.m_staticText101, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		AttenAdressChoices = []
		self.AttenAdress = wx.ComboBox( self.m_panel511, wx.ID_ANY, u"GPIB0::1::INSTR", wx.DefaultPosition, wx.DefaultSize, AttenAdressChoices, 0 )
		gbSizer311.Add( self.AttenAdress, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText11 = wx.StaticText( self.m_panel511, wx.ID_ANY, u"Attenuator2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		gbSizer311.Add( self.m_staticText11, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		AttenAdress2Choices = []
		self.AttenAdress2 = wx.ComboBox( self.m_panel511, wx.ID_ANY, u"GPIB0::1::INSTR", wx.DefaultPosition, wx.DefaultSize, AttenAdress2Choices, 0 )
		gbSizer311.Add( self.AttenAdress2, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText12 = wx.StaticText( self.m_panel511, wx.ID_ANY, u"Lock in", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		gbSizer311.Add( self.m_staticText12, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button14 = wx.Button( self.m_panel511, wx.ID_ANY, u"Refresh instruments", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer311.Add( self.m_button14, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText13 = wx.StaticText( self.m_panel511, wx.ID_ANY, u"Meter", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		gbSizer311.Add( self.m_staticText13, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText14 = wx.StaticText( self.m_panel511, wx.ID_ANY, u"Source", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		gbSizer311.Add( self.m_staticText14, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText121 = wx.StaticText( self.m_panel511, wx.ID_ANY, u"Test instruments:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText121.Wrap( -1 )
		gbSizer311.Add( self.m_staticText121, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_comboBox8Choices = [ u"Lock in", u"Meter", u"Source", u"Attenuator", u"Attenuator2" ]
		self.m_comboBox8 = wx.ComboBox( self.m_panel511, wx.ID_ANY, u"Select instrument", wx.DefaultPosition, wx.DefaultSize, m_comboBox8Choices, 0 )
		gbSizer311.Add( self.m_comboBox8, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl18 = wx.TextCtrl( self.m_panel511, wx.ID_ANY, u"Command", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer311.Add( self.m_textCtrl18, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl23 = wx.TextCtrl( self.m_panel511, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 250,100 ), wx.TE_MULTILINE )
		gbSizer311.Add( self.m_textCtrl23, wx.GBPosition( 8, 0 ), wx.GBSpan( 6, 2 ), wx.ALL, 5 )
		
		self.m_button15 = wx.Button( self.m_panel511, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer311.Add( self.m_button15, wx.GBPosition( 7, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button16 = wx.Button( self.m_panel511, wx.ID_ANY, u"Read", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer311.Add( self.m_button16, wx.GBPosition( 7, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		self.m_panel511.SetSizer( gbSizer311 )
		self.m_panel511.Layout()
		gbSizer311.Fit( self.m_panel511 )
		self.m_auinotebook4.AddPage( self.m_panel511, u"Instruments", True, wx.NullBitmap )
		
		self.m_auinotebook5 = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.Point( -1,-1 ), wx.Size( 500,-1 ), 0 )
		self.m_mgr.AddPane( self.m_auinotebook5, wx.aui.AuiPaneInfo() .Center() .CloseButton( False ).MaximizeButton( True ).MinimizeButton( True ).PinButton( True ).Dock().Resizable().FloatingSize( wx.Size( -1,-1 ) ) )
		
		self.m_scrolledWindow1 = wx.ScrolledWindow( self.m_auinotebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.BOTH )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_panel61 = wx.Panel( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		self.m_panel61.SetMinSize( wx.Size( 500,300 ) )
		
		gbSizer1.Add( self.m_panel61, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 6 ), wx.EXPAND |wx.ALL, 5 )
		
		self.m_button2 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Pause", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_button2, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_checkBox1 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"Show Grid", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_checkBox1, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_checkBox2 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"Show X Labels", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_checkBox2, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_radioBox1Choices = [ u"Auto", u"Manual" ]
		self.m_radioBox1 = wx.RadioBox( self.m_scrolledWindow1, wx.ID_ANY, u"X min", wx.DefaultPosition, wx.DefaultSize, m_radioBox1Choices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioBox1.SetSelection( 0 )
		gbSizer1.Add( self.m_radioBox1, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_radioBox2Choices = [ u"Auto", u"Manual" ]
		self.m_radioBox2 = wx.RadioBox( self.m_scrolledWindow1, wx.ID_ANY, u"X max", wx.DefaultPosition, wx.DefaultSize, m_radioBox2Choices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioBox2.SetSelection( 0 )
		gbSizer1.Add( self.m_radioBox2, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_radioBox3Choices = [ u"Auto", u"Manual" ]
		self.m_radioBox3 = wx.RadioBox( self.m_scrolledWindow1, wx.ID_ANY, u"Y min", wx.DefaultPosition, wx.DefaultSize, m_radioBox3Choices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioBox3.SetSelection( 0 )
		gbSizer1.Add( self.m_radioBox3, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_radioBox4Choices = [ u"Auto", u"Manual" ]
		self.m_radioBox4 = wx.RadioBox( self.m_scrolledWindow1, wx.ID_ANY, u"Y max", wx.DefaultPosition, wx.DefaultSize, m_radioBox4Choices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioBox4.SetSelection( 0 )
		gbSizer1.Add( self.m_radioBox4, wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl2 = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		gbSizer1.Add( self.m_textCtrl2, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl3 = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"50", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		gbSizer1.Add( self.m_textCtrl3, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl4 = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		gbSizer1.Add( self.m_textCtrl4, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl5 = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"100", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		gbSizer1.Add( self.m_textCtrl5, wx.GBPosition( 3, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText41 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Mean", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		gbSizer1.Add( self.m_staticText41, wx.GBPosition( 1, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Stdev", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		gbSizer1.Add( self.m_staticText5, wx.GBPosition( 2, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl121 = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl121.SetMinSize( wx.Size( 150,-1 ) )
		
		gbSizer1.Add( self.m_textCtrl121, wx.GBPosition( 1, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl13 = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl13.SetMinSize( wx.Size( 150,-1 ) )
		
		gbSizer1.Add( self.m_textCtrl13, wx.GBPosition( 2, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Events", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		gbSizer1.Add( self.m_staticText7, wx.GBPosition( 3, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl14 = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_WORDWRAP )
		self.m_textCtrl14.SetMinSize( wx.Size( 200,60 ) )
		
		gbSizer1.Add( self.m_textCtrl14, wx.GBPosition( 3, 5 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		
		gbSizer1.AddGrowableCol( 5 )
		gbSizer1.AddGrowableRow( 0 )
		
		self.m_scrolledWindow1.SetSizer( gbSizer1 )
		self.m_scrolledWindow1.Layout()
		gbSizer1.Fit( self.m_scrolledWindow1 )
		self.m_auinotebook5.AddPage( self.m_scrolledWindow1, u"Graph", True, wx.NullBitmap )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu11 = wx.Menu()
		self.m_menuItem21 = wx.MenuItem( self.m_menu11, wx.ID_ANY, u"Open dictionary", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu11.AppendItem( self.m_menuItem21 )
		
		self.m_menuItem11 = wx.MenuItem( self.m_menu11, wx.ID_ANY, u"Save tables", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu11.AppendItem( self.m_menuItem11 )
		
		self.m_menuItem111 = wx.MenuItem( self.m_menu11, wx.ID_ANY, u"Analysis file", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu11.AppendItem( self.m_menuItem111 )
		
		self.m_menuItem1111 = wx.MenuItem( self.m_menu11, wx.ID_ANY, u"Reset", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu11.AppendItem( self.m_menuItem1111 )
		
		self.m_menu1 = wx.Menu()
		self.m_menuItem2 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Live instruments", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu1.AppendItem( self.m_menuItem2 )
		
		self.m_menuItem1 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Simulated instruments", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu1.AppendItem( self.m_menuItem1 )
		
		self.m_menu11.AppendSubMenu( self.m_menu1, u"Run Options" )
		
		self.m_menu2 = wx.Menu()
		self.m_menuItem26 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Complete checks", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu2.AppendItem( self.m_menuItem26 )
		self.m_menuItem26.Check( True )
		
		self.m_menuItem25 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Overide safety", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu2.AppendItem( self.m_menuItem25 )
		
		self.m_menu11.AppendSubMenu( self.m_menu2, u"Safety" )
		
		self.m_menubar1.Append( self.m_menu11, u"File" ) 
		
		self.m_menu13 = wx.Menu()
		self.m_menuItem30 = wx.MenuItem( self.m_menu13, wx.ID_ANY, u"Help", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu13.AppendItem( self.m_menuItem30 )
		
		self.m_menuItem31 = wx.MenuItem( self.m_menu13, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu13.AppendItem( self.m_menuItem31 )
		
		self.m_menubar1.Append( self.m_menu13, u"Help" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		self.m_auinotebook41 = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.Point( -1,-1 ), wx.Size( 500,-1 ), 0 )
		self.m_auinotebook41.SetMinSize( wx.Size( 200,300 ) )
		
		self.m_mgr.AddPane( self.m_auinotebook41, wx.aui.AuiPaneInfo() .Left() .CloseButton( False ).MaximizeButton( True ).MinimizeButton( True ).PinButton( True ).Dock().Resizable().FloatingSize( wx.DefaultSize ).MinSize( wx.Size( 200,300 ) ) )
		
		self.m_scrolledWindow3 = wx.ScrolledWindow( self.m_auinotebook41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow3.SetScrollRate( 5, 5 )
		self.m_scrolledWindow3.SetMinSize( wx.Size( 200,300 ) )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_grid3 = wx.grid.Grid( self.m_scrolledWindow3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid3.CreateGrid( 5, 5 )
		self.m_grid3.EnableEditing( True )
		self.m_grid3.EnableGridLines( True )
		self.m_grid3.EnableDragGridSize( False )
		self.m_grid3.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid3.EnableDragColMove( False )
		self.m_grid3.EnableDragColSize( True )
		self.m_grid3.SetColLabelSize( 30 )
		self.m_grid3.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid3.EnableDragRowSize( True )
		self.m_grid3.SetRowLabelSize( 80 )
		self.m_grid3.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid3.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer1.Add( self.m_grid3, 0, wx.ALL, 5 )
		
		
		self.m_scrolledWindow3.SetSizer( bSizer1 )
		self.m_scrolledWindow3.Layout()
		bSizer1.Fit( self.m_scrolledWindow3 )
		self.m_auinotebook41.AddPage( self.m_scrolledWindow3, u"Control settings", False, wx.NullBitmap )
		self.m_scrolledWindow4 = wx.ScrolledWindow( self.m_auinotebook41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow4.SetScrollRate( 5, 5 )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_grid2 = wx.grid.Grid( self.m_scrolledWindow4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid2.CreateGrid( 8, 4 )
		self.m_grid2.EnableEditing( True )
		self.m_grid2.EnableGridLines( True )
		self.m_grid2.EnableDragGridSize( False )
		self.m_grid2.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid2.EnableDragColMove( False )
		self.m_grid2.EnableDragColSize( True )
		self.m_grid2.SetColLabelSize( 30 )
		self.m_grid2.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid2.EnableDragRowSize( True )
		self.m_grid2.SetRowLabelSize( 80 )
		self.m_grid2.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid2.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer2.Add( self.m_grid2, 0, wx.ALL, 5 )
		
		
		self.m_scrolledWindow4.SetSizer( bSizer2 )
		self.m_scrolledWindow4.Layout()
		bSizer2.Fit( self.m_scrolledWindow4 )
		self.m_auinotebook41.AddPage( self.m_scrolledWindow4, u"Instrument commands", False, wx.NullBitmap )
		self.m_scrolledWindow41 = wx.ScrolledWindow( self.m_auinotebook41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow41.SetScrollRate( 5, 5 )
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_grid21 = wx.grid.Grid( self.m_scrolledWindow41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid21.CreateGrid( 8, 13 )
		self.m_grid21.EnableEditing( True )
		self.m_grid21.EnableGridLines( True )
		self.m_grid21.EnableDragGridSize( False )
		self.m_grid21.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid21.EnableDragColMove( False )
		self.m_grid21.EnableDragColSize( True )
		self.m_grid21.SetColLabelSize( 30 )
		self.m_grid21.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid21.EnableDragRowSize( True )
		self.m_grid21.SetRowLabelSize( 80 )
		self.m_grid21.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid21.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer21.Add( self.m_grid21, 0, wx.ALL, 5 )
		
		self.m_button151 = wx.Button( self.m_scrolledWindow41, wx.ID_ANY, u"Add Row", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.m_button151, 0, wx.ALL, 5 )
		
		
		self.m_scrolledWindow41.SetSizer( bSizer21 )
		self.m_scrolledWindow41.Layout()
		bSizer21.Fit( self.m_scrolledWindow41 )
		self.m_auinotebook41.AddPage( self.m_scrolledWindow41, u"Callibration ranges", True, wx.NullBitmap )
		
		
		self.m_mgr.Update()
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.m_button13.Bind( wx.EVT_BUTTON, self.OnGenerateTable )
		self.m_button122.Bind( wx.EVT_BUTTON, self.OnAnalyse )
		self.m_button5.Bind( wx.EVT_BUTTON, self.OnStart )
		self.m_button6.Bind( wx.EVT_BUTTON, self.OnStop )
		self.m_button12.Bind( wx.EVT_BUTTON, self.OnMakeSafe )
		self.m_button14.Bind( wx.EVT_BUTTON, self.OnRefreshInstruments )
		self.m_button15.Bind( wx.EVT_BUTTON, self.OnSendTestCommand )
		self.m_button16.Bind( wx.EVT_BUTTON, self.OnReadTestCommand )
		self.m_button2.Bind( wx.EVT_BUTTON, self.OnPauseButton )
		self.Bind( wx.EVT_MENU, self.OnOpenDict, id = self.m_menuItem21.GetId() )
		self.Bind( wx.EVT_MENU, self.OnSaveTables, id = self.m_menuItem11.GetId() )
		self.Bind( wx.EVT_MENU, self.OnAnalysisFile, id = self.m_menuItem111.GetId() )
		self.Bind( wx.EVT_MENU, self.DoReset, id = self.m_menuItem1111.GetId() )
		self.Bind( wx.EVT_MENU, self.OnLive, id = self.m_menuItem2.GetId() )
		self.Bind( wx.EVT_MENU, self.OnSimulate, id = self.m_menuItem1.GetId() )
		self.Bind( wx.EVT_MENU, self.OnCompleteChecks, id = self.m_menuItem26.GetId() )
		self.Bind( wx.EVT_MENU, self.OnOverideSafety, id = self.m_menuItem25.GetId() )
		self.Bind( wx.EVT_MENU, self.OnHelp, id = self.m_menuItem30.GetId() )
		self.Bind( wx.EVT_MENU, self.OnAbout, id = self.m_menuItem31.GetId() )
		self.m_button151.Bind( wx.EVT_BUTTON, self.OnAddRow )
	
	def __del__( self ):
		self.m_mgr.UnInit()
		
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()
	
	def OnGenerateTable( self, event ):
		event.Skip()
	
	def OnAnalyse( self, event ):
		event.Skip()
	
	def OnStart( self, event ):
		event.Skip()
	
	def OnStop( self, event ):
		event.Skip()
	
	def OnMakeSafe( self, event ):
		event.Skip()
	
	def OnRefreshInstruments( self, event ):
		event.Skip()
	
	def OnSendTestCommand( self, event ):
		event.Skip()
	
	def OnReadTestCommand( self, event ):
		event.Skip()
	
	def OnPauseButton( self, event ):
		event.Skip()
	
	def OnOpenDict( self, event ):
		event.Skip()
	
	def OnSaveTables( self, event ):
		event.Skip()
	
	def OnAnalysisFile( self, event ):
		event.Skip()
	
	def DoReset( self, event ):
		event.Skip()
	
	def OnLive( self, event ):
		event.Skip()
	
	def OnSimulate( self, event ):
		event.Skip()
	
	def OnCompleteChecks( self, event ):
		event.Skip()
	
	def OnOverideSafety( self, event ):
		event.Skip()
	
	def OnHelp( self, event ):
		event.Skip()
	
	def OnAbout( self, event ):
		event.Skip()
	
	def OnAddRow( self, event ):
		event.Skip()
	

