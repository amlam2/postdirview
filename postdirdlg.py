#coding=utf-8

import wx

###############################################################################
# Начало класса диалога просмотра текстового файла (TxtViewDialog)
#
class TxtViewDialog(wx.Dialog):
    def __init__(self, dlgTitle, parentTxt, pathTxtFile, appIcon, parent):
        self.dlgTitle    = u'%s - [ содержимое "%s" ]' % dlgTitle
        self.parentTxt   = parentTxt
        self.pathTxtFile = pathTxtFile
        self.appIcon     = appIcon
        wx.Dialog.__init__(self, None, -1, self.dlgTitle, size=(950, 850))
        
        ### > иконка окна
        self.SetIcon(wx.IconFromBitmap(wx.Bitmap(self.appIcon)))
        ###
        
        ### > надпись на форме
        txt = wx.StaticText(self, -1, u"Каталог отправки на ОПС: " + parentTxt)
        ###
        
        ### > окно для просмотра содержимого текстового файла
        self.textView = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_RICH2)
        
        font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD, False)
        self.textView.SetStyle(0, 1, wx.TextAttr("black", wx.NullColor, font))
        
        for line in open(pathTxtFile, 'r'):
            self.textView.AppendText(line)
        self.textView.AppendText('\r')
        
        self.textView.SetInsertionPoint(0)
        
        self.textView.SetEditable(False)
        self.textView.SetFocus()
        ###
        
        ### > кнопка "ОК"
        self.okButton = wx.Button(self, wx.ID_OK, u"ОК", size =(100, 25))
        ###
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(txt, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        sizer.Add(self.textView, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.okButton, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        self.SetSizer(sizer)
        self.Layout()
#
# Конец класса диалога TxtViewDialog
###############################################################################

###############################################################################
# Начало класса диалога отправки файлов на ОПС (SendDialog)
#
class SendDialog(wx.Dialog):
    def __init__(self, dlgTitle, appIcon, parent):
        self.dlgTitle = '%s - [ %s ]' % (dlgTitle, u"отправка файлов")
        self.appIcon  = appIcon
        wx.Dialog.__init__(
                            self,
                            None,
                            -1,
                            self.dlgTitle,
                            size=(480, 650)
                           )
        
        ### > надпись на форме
        #self.txtOps = wx.StaticText(self, -1, u"Выберите ОПС")
        ###
        
        
        #self.txtFiles = wx.StaticText(self, -1, u"Выберите файлы")
        
        self.line = wx.StaticLine(self, -1)
        
        
        
        ### > создание панели инструментов
        self.toolBarOps = wx.ToolBar(self,
                                  style = wx.TB_HORIZONTAL
                                        | wx.NO_BORDER
                                        | wx.TB_FLAT)
        
        #self.expandBmp   = wx.Bitmap("expand_16.png", wx.BITMAP_TYPE_PNG)
        #self.alldevBmp   = wx.Bitmap("network_group_16.png", wx.BITMAP_TYPE_PNG)
        #self.terminalBmp = wx.Bitmap("card_reader_terminal_16.png", wx.BITMAP_TYPE_PNG)
        #self.pstBmp      = wx.Bitmap("pst_16.png", wx.BITMAP_TYPE_PNG)
        
        self.toolBarOps.SetToolBitmapSize((16, 16))
        
        #self.toolBarOps.AddSimpleTool(10, self.expandBmp, u"Развернуть")
        #self.Bind(wx.EVT_TOOL, self.OnExpand, id=10)
        
        self.toolBarOps.AddSeparator()
        
        #self.toolBarOps.AddCheckTool(30, self.alldevBmp, shortHelp = u"Все устройства")
        #self.Bind(wx.EVT_TOOL, self.OnToggle, id=30)
        
        #self.toolBarOps.AddCheckTool(40, self.terminalBmp, shortHelp = u"Терминалы")
        #self.Bind(wx.EVT_TOOL, self.OnToggle, id=40)
        
        #self.toolBarOps.AddCheckTool(50, self.pstBmp, shortHelp = u"ПСТ")
        #self.Bind(wx.EVT_TOOL, self.OnToggle, id=50)
        
        self.toolBarOps.Realize()
        ###
        
        
        
        ### > создание панели инструментов
        self.toolBarFiles = wx.ToolBar(self,
                                  style = wx.TB_HORIZONTAL
                                        | wx.NO_BORDER
                                        | wx.TB_FLAT)
        
        #self.expandBmp   = wx.Bitmap("expand_16.png", wx.BITMAP_TYPE_PNG)
        #self.alldevBmp   = wx.Bitmap("network_group_16.png", wx.BITMAP_TYPE_PNG)
        #self.terminalBmp = wx.Bitmap("card_reader_terminal_16.png", wx.BITMAP_TYPE_PNG)
        #self.pstBmp      = wx.Bitmap("pst_16.png", wx.BITMAP_TYPE_PNG)
        
        self.toolBarFiles.SetToolBitmapSize((16, 16))
        
        #self.toolBarFiles.AddSimpleTool(10, self.expandBmp, u"Развернуть")
        #self.Bind(wx.EVT_TOOL, self.OnExpand, id=10)
        
        self.toolBarFiles.AddSeparator()
        
        #self.toolBarFiles.AddCheckTool(30, self.alldevBmp, shortHelp = u"Все устройства")
        #self.Bind(wx.EVT_TOOL, self.OnToggle, id=30)
        
        #self.toolBarFiles.AddCheckTool(40, self.terminalBmp, shortHelp = u"Терминалы")
        #self.Bind(wx.EVT_TOOL, self.OnToggle, id=40)
        
        #self.toolBarFiles.AddCheckTool(50, self.pstBmp, shortHelp = u"ПСТ")
        #self.Bind(wx.EVT_TOOL, self.OnToggle, id=50)
        
        self.toolBarFiles.Realize()
        ###
        
        from libs.liblore import opsDict
        
        ### > формирование списка ОПС с установленными БПК
        self.allOPSNameList = []
        for key in opsDict:
            nameOPS = '%s - %s' % (key, opsDict[key].get('nameOPS'))
            self.allOPSNameList.append(nameOPS)
        self.allOPSNameList = sorted(self.allOPSNameList)
        ###
        
        ### > окно выбора ОПС
        self.chkLstBoxOps = wx.CheckListBox(self, -1, (0, 0), (300, -1),\
                                self.allOPSNameList, wx.LB_SINGLE)
        #self.chkLstBoxOps.SetChecked(self.allOPSNameList)
        ###
        
        sampleList = [u'NP123456.HKB', u'NT456789.012', u'NL852753.456']
        self.lstBoxFiles = wx.ListBox(self, -1, (0, 0), (150, -1),\
                                sampleList, wx.LB_SINGLE)
        
        
        ### > иконка окна
        
        ###
        
        ### > надпись на форме
        #txt = wx.StaticText(self, -1, u"Каталог отправки на ОПС: " + parentTxt)
        ###
        
        ### > окно для просмотра содержимого текстового файла
        #self.textView = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_RICH2)
        
        #font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD, False)
        #self.textView.SetStyle(0, 1, wx.TextAttr("black", wx.NullColor, font))
        
        #for line in open(pathTxtFile, 'r'):
        #    self.textView.AppendText(line)
        #self.textView.AppendText('\r')
        
        #self.textView.SetInsertionPoint(0)
        
        #self.textView.SetEditable(False)
        #self.textView.SetFocus()
        ###
        
        ### > кнопка "ОК"
        self.okButton = wx.Button(self, wx.ID_OK, u"ОК", size =(100, 25))
        ###
        
        #sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(txt, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        #sizer.Add(self.textView, 1, wx.EXPAND | wx.ALL, 5)
        #sizer.Add(self.okButton, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        #self.SetSizer(sizer)
        #self.Layout()
        
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        #self.SetTitle(windowTitle)
        #self.SetSize((400, 670))
        #self.Centre()
    
        ### > иконка окна
        self.SetIcon(wx.IconFromBitmap(wx.Bitmap(self.appIcon)))
        ###
    
        ### > построить дерево всех устройств
        #self.BuildDevTree('all')
        ###
    
        ### > начальные установки элементов интерфейса
        #self.toolBarOps.ToggleTool(30, True)
        ###

    def __do_layout(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        
        leftSizer  = wx.BoxSizer(wx.VERTICAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        
        leftSizer.Add(self.toolBarFiles, 0, wx.EXPAND|wx.ALL, 5)
        #leftSizer.Add(self.txtFiles, 0, wx.EXPAND|wx.ALL, 5)
        leftSizer.Add(self.lstBoxFiles,  1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        
        
        
        rightSizer.Add(self.toolBarOps, 0, wx.EXPAND|wx.ALL, 5)
        #rightSizer.Add(self.txtOps, 0, wx.EXPAND|wx.ALL, 5)
        rightSizer.Add(self.chkLstBoxOps,  1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        
        
        
        
        panelSizer.Add(leftSizer, 0, wx.EXPAND, 5)
        panelSizer.Add(rightSizer, 0, wx.EXPAND, 5)
        
        mainSizer.Add(panelSizer, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 0)
        mainSizer.Add(self.line, 0, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(self.okButton,        0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
    
        self.SetSizer(mainSizer)
        self.Layout()
    
#
# Конец класса диалога SendDialog
###############################################################################
