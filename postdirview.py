#!/usr/bin/env python
# coding=utf-8

# подключение необходимых модулей
import os
import wx.gizmos
from libs.liblore import opsDict, codeSDODict
from libs.libwork import SFInfo, toUserView

# Глобальные переменные
###############################################################################
# каталоги программы
###############################################################################
startDir = os.getcwd()
#sendDir = os.path.join(startDir, 'send')
sendDir = 'd:\\#_Send'
tempDir = os.path.join(startDir, 'temp')
picsDir = os.path.join(startDir, 'pics')
iconDir = os.path.join(picsDir, 'icons')
#destDir = os.path.join(startDir, 'bases')
destDir = 'U:\\Bases'

windowTitle = u'Каталоги ОПС'                          # заголовок окна
appIcon     = os.path.join(iconDir, 'postdirview.png') # иконка приложения

# подключение диалогов
import postdirdlg

###############################################################################
# Начало класса окна приложения (MainWindowApp)
#
class MainWindowApp(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, *args, **kwds)

        #######################################################################
        # создание виджетов
        #
        self.panel = wx.Panel(self, -1)

        ### > дерево каталогов с изображениями
        self.treeView = wx.gizmos.TreeListCtrl(self.panel,
                                               -1,
                                               size=(-1, -1),
                                               #pos=(5, 2),
                                               #ize=(705, 650),
                                       style = wx.TR_DEFAULT_STYLE
                                             #| wx.TR_FULL_ROW_HIGHLIGHT
                                             | wx.TR_HAS_BUTTONS
                                             | wx.TR_ROW_LINES
                                             | wx.TR_COLUMN_LINES
                                             | wx.TR_TWIST_BUTTONS
                                              )

        ### > словарь уникальных файлов
        self.treeDict = {}

        il = wx.ImageList(16,16)
        #self.fldridx        = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,        wx.ART_OTHER, (16,16)))
        #self.fldropenidx    = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,     wx.ART_OTHER, (16,16)))
        #self.fileidx        = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE,   wx.ART_OTHER, (16,16)))
        #self.contidx        = il.Add(wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW,   wx.ART_OTHER, (16,16)))

        #self.fileidx  = il.Add(wx.Image(os.path.join(picsDir, 'database.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())

        self.fldridx  = il.Add(wx.Image(os.path.join(picsDir,    'folder.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.baseidx  = il.Add(wx.Image(os.path.join(picsDir,  'database.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.textidx  = il.Add(wx.Image(os.path.join(picsDir, 'text-docs.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.archidx  = il.Add(wx.Image(os.path.join(picsDir,  'archives.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.unknidx  = il.Add(wx.Image(os.path.join(picsDir,   'unknown.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.contidx  = il.Add(wx.Image(os.path.join(picsDir,     'table.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())

        #self.treeView.AssignImageList(il)
        self.treeView.SetImageList(il)
        self.il = il
        ###

        ### > названия и ширина колонок
        colNamesSizes = (
                        (u"ОПС назначения:", 320),
                        (u"Размер:",          80),
                        (u"Описание:",       360)
                        )
        ###

        ### > создание колонок
        for colNumber, colName in enumerate(colNamesSizes):
            self.treeView.AddColumn(colName[0])
            self.treeView.SetColumnWidth(colNumber, colName[1])
        self.treeView.SetMainColumn(0)
        ###

        #self.treeView.SetColumnAlignment(1, wx.ALIGN_RIGHT) # выравнивание столбца
        ###

        ### > событие двойной клик по элементу дерева каталогов
        #http://www.mentby.com/Group/wxpython-users/gizmos-treelistctrl-bug.html
        self.treeView.GetMainWindow().Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        ###

        ### > начальное состояние элементов интерфейса
        #self.treeView.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        ###
        #
        #######################################################################

        self.__do_layout()
        self.__set_properties()
        self.__do_preparation()


    # --- начальные установки -------------------------------------------------
    def __set_properties(self):
        self.SetTitle('%s - [ %s ]' % (windowTitle, u"состояние"))
        self.SetSize((800, 750))
        self.Centre()
        #self.CenterOnScreen()
        #self.Show(True)

        # установка иконки приложения
        self.SetIcon(wx.IconFromBitmap(wx.Bitmap(appIcon)))

        # создание панели инструментов и строки состояния
        self.MakeToolBar()
        self.MakeStatusBar()

    # --- размещение виджетов на сайзерах -------------------------------------
    def __do_layout(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        vSizer = wx.BoxSizer(wx.VERTICAL)

        vSizer.Add(self.treeView, 1, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(vSizer)

        mainSizer.Add(self.panel, 1, wx.EXPAND, 0)

        self.SetSizer(mainSizer)

        mainSizer.Fit(self)

        self.Layout()

    def __do_preparation(self):
        #self.BuildOPSTreeDev()
        self.BuildOPSTree()
        self.FillStatusBar()

    # --- создание панели инструментов ----------------------------------------
    def MakeToolBar(self):
        toolbar = self.CreateToolBar()

        toolSend  = toolbar.AddSimpleTool(wx.NewId(),
                    wx.BitmapFromImage(wx.Image(os.path.join(picsDir, 'send.png'),
                                       wx.BITMAP_TYPE_PNG)),
                    u"Отправка на ОПС", u"Отправка файлов на ОПС")
        self.Bind(wx.EVT_TOOL, self.OnSend, toolSend)

        #toolbar.AddSeparator()

        toolClear = toolbar.AddSimpleTool(wx.NewId(),
                    wx.BitmapFromImage(wx.Image(os.path.join(picsDir, 'clear.png'),
                                       wx.BITMAP_TYPE_PNG)),
                    u"Экстренная очистка", u"Очистить все каталоги ОПС")
        self.Bind(wx.EVT_TOOL, self.OnClear, toolClear)

        #toolbar.AddSeparator()
        toolbar.AddSeparator()

        toolExpand = toolbar.AddSimpleTool(wx.NewId(),
                    wx.BitmapFromImage(wx.Image(os.path.join(picsDir, 'plus.png'),
                                       wx.BITMAP_TYPE_PNG)),
                    u"Развернуть", u"Развернуть все каталоги ОПС")
        self.Bind(wx.EVT_TOOL, self.OnExpand, toolExpand)

        toolRefresh = toolbar.AddSimpleTool(wx.NewId(),
                    wx.BitmapFromImage(wx.Image(os.path.join(picsDir, 'refresh.png'),
                                       wx.BITMAP_TYPE_PNG)),
                    u"Обновить", u"Обновить дерево каталогов ОПС")
        self.Bind(wx.EVT_TOOL, self.OnRefresh, toolRefresh)

        toolbar.AddSeparator()

        toolExit = toolbar.AddSimpleTool(wx.NewId(),
                    wx.BitmapFromImage(wx.Image(os.path.join(picsDir, 'exit.png'),
                                       wx.BITMAP_TYPE_PNG)),
                    u"Выход", u"Выход из программы")
        self.Bind(wx.EVT_TOOL, self.OnExit, toolExit)

        toolbar.Realize()

    # --- создание строки состояния -------------------------------------------
    def MakeStatusBar(self):
        self.sb = wx.StatusBar(self, -1)
        self.sb.SetFieldsCount(4)                       # количество полей
        self.sb.SetStatusWidths([200, 160, 160, -1])    # ширина полей
        self.SetStatusBar(self.sb)

        self.sb.SetStatusText(u"Готово!", 0)

    # --- вычисление размера файла --------------------------------------------
    def CalcFileSize(self, path):
        line = toUserView(str(os.stat(path).st_size))
        countSpace = 15 - len(line)
        if   len(line) == 7: countSpace += 1
        elif len(line) == 6: countSpace += 2
        elif len(line) == 5: countSpace += 3
        elif len(line) == 3: countSpace += 4
        elif len(line) == 2: countSpace += 5
        elif len(line) == 1: countSpace += 6
        return ' ' * countSpace + line

    # --- построение дерева ОПС (разработка) ----------------------------------
    def BuildOPSTreeDev(self):
        busy = wx.BusyInfo(u"Построение дерева ОПС, пожалуйста подождите...")
        wx.Yield()

        self.root = self.treeView.AddRoot(destDir)
        self.treeView.SetItemBold(self.root, bold=True)
        self.treeView.SetItemTextColour(self.root, "blue")

        self.treeView.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)

        for idxOps in sorted(opsDict):
            newItem = self.treeView.AppendItem(self.root, idxOps +' - '+ opsDict[idxOps].get('nameOPS'))
            self.treeView.SetItemTextColour(newItem, "gray")
            self.treeView.SetItemText(newItem, u"<каталог>", 1)

            self.treeView.SetItemImage(newItem, self.fldridx, wx.TreeItemIcon_Normal)

            fileList = os.listdir(os.path.join(destDir, idxOps))
            if fileList:
                for fileName in fileList:
                    newItem2 = self.treeView.AppendItem(newItem, os.path.basename(fileName))
                    self.treeView.SetItemTextColour(newItem, "black")
                    self.treeView.SetItemBold(newItem, bold=True)

                    self.PutItemImage(newItem2)

                    fullPath = os.path.join(destDir, idxOps, fileName)
                    fST = os.stat(fullPath)
                    fileKey = (fileName, fST.st_size, fST.st_mode, fST.st_mtime)
                    fileInfo = self.treeDict.get(fileKey)
                    if not fileInfo:
                        fileInfo = SFInfo.sfInfo(fullPath)
                        self.treeDict[fileKey] = fileInfo

                    infoStr = SFInfo.sfInfoShortString(fileInfo)
                    self.treeView.SetItemText(newItem2, infoStr, 2)

                    self.treeView.SetItemText(newItem2,
                                              self.CalcFileSize(fullPath),
                                              1) # размер файла в ячейке

                    # отобразить содержимое базы ЕЛС в дереве каталогов
                    self.UnPackELS(newItem2, fullPath)
                    # отобразить содержимое базы лотерей в дереве каталогов
                    self.UnPackLot(newItem2, fullPath)

                self.treeView.SetItemText(newItem, u"файлов - " + str(len(fileList)), 2)
                self.treeView.SortChildren(newItem)
            else:
                self.treeView.SetItemText(newItem, u"<пусто>", 2)

        self.treeView.Expand(self.root)
        self.treeView.SetFocus()
        '''
        ####
        print '*'*80
        print self.treeDict
        print '*'*80
        print len(self.treeDict)
        print '*'*80
        ####
        '''
    # --- построение дерева ОПС -----------------------------------------------
    def BuildOPSTree(self):
        busy = wx.BusyInfo(u"Построение дерева ОПС, пожалуйста подождите...")
        wx.Yield()

        self.root = self.treeView.AddRoot(destDir)
        self.treeView.SetItemBold(self.root, bold=True)
        self.treeView.SetItemTextColour(self.root, "blue")

        self.treeView.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
        ###self.treeView.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)###

        for item in sorted(opsDict):
            fullPath = os.path.join(destDir, item)
            ###
            #print u"Наличие каталога ОПС - %s" % os.path.exists(fullPath)
            ###
            if os.path.exists(fullPath):
                ###
                #print u"Текущее ОПС - %s" % opsDict[item].get('nameOPS')
                ###
                newItem = self.treeView.AppendItem(self.root, item +' - '+ opsDict[item].get('nameOPS'))
                self.treeView.SetItemTextColour(newItem, "gray")
                self.treeView.SetItemText(newItem, u"<каталог>", 1)

                self.treeView.SetItemImage(newItem, self.fldridx, wx.TreeItemIcon_Normal)
                ###self.treeView.SetItemImage(newItem, self.fldropenidx, wx.TreeItemIcon_Expanded)###

                fileList = os.listdir(fullPath)
                ###
                #print u"Список файлов - %s" % fileList
                ###
                if fileList:
                    for item2 in fileList:
                        newItem2 = self.treeView.AppendItem(newItem, os.path.basename(item2))
                        self.treeView.SetItemTextColour(newItem, "black")
                        self.treeView.SetItemBold(newItem, bold=True)
                        #self.treeView.SetItemText(newItem2, u"<файл>", 1)

                        #self.treeView.SetItemImage(newItem2, self.fileidx, wx.TreeItemIcon_Normal)
                        self.PutItemImage(newItem2)

                        analisedSF  = os.path.join(destDir, item, item2)
                        ###
                        #print u"Список кодов: %s" % SFInfo.sfInfo(analisedSF)
                        ###

                        infoStr = SFInfo.sfInfoShortString(SFInfo.sfInfo(analisedSF))
                        self.treeView.SetItemText(newItem2, infoStr, 2)

                        self.treeView.SetItemText(newItem2,
                                                  self.CalcFileSize(analisedSF),
                                                  1) # размер файла в ячейке

                        # отобразить содержимое базы ЕЛС в дереве каталогов
                        self.UnPackELS(newItem2, analisedSF)
                        # отобразить содержимое базы лотерей в дереве каталогов
                        self.UnPackLot(newItem2, analisedSF)

                    self.treeView.SetItemText(newItem, u"файлов - " + str(len(fileList)), 2)
                    self.treeView.SortChildren(newItem)
                else:
                    self.treeView.SetItemText(newItem, u"<пусто>", 2)

        self.treeView.Expand(self.root)
        self.treeView.SetFocus()

    # --- отображение содержимого базы ЕЛС в дереве каталогов -----------------
    def UnPackELS(self, item, analisedSF):
        baseList = SFInfo.sfInfo(analisedSF)
        typeBase = baseList.pop(0)
        if typeBase == 'db_els':
            for sdo in baseList:
                sepBase = []
                sepBase.append('db_sep')
                sepBase.append(sdo)
                infoStr = SFInfo.sfInfoShortString(sepBase).split(u':')[1].strip()

                newItem = self.treeView.AppendItem(item, infoStr)
                self.treeView.SetItemImage(newItem, self.contidx, wx.TreeItemIcon_Normal)

    # --- отображение содержимого базы лотерей в дереве каталогов -------------
    def UnPackLot(self, item, analisedSF):
        lotList = SFInfo.sfInfo(analisedSF)
        typeBase = lotList.pop(0)
        if len(lotList) > 1:
            if typeBase == 'db_lot':
                for lot in lotList:
                    lotBase = []
                    lotBase.append('db_lot')
                    lotBase.append(lot)
                    infoStr = SFInfo.sfInfoShortString(lotBase)

                    newItem = self.treeView.AppendItem(item, infoStr)
                    self.treeView.SetItemImage(newItem, self.contidx, wx.TreeItemIcon_Normal)

    # --- пиктограмма элемента дерева каталогов в зависимости от типа файла ---
    def PutItemImage(self, item):
        itemTxt = self.treeView.GetItemText(item)
        if itemTxt[:2].lower() in ['np', 'nt', 'nl', 'ns', 'vn', 'li']:
            image = self.baseidx
        elif os.path.splitext(itemTxt)[1].lower() in ['.txt', '.doc', '.docx']:
            image = self.textidx
        elif os.path.splitext(itemTxt)[1].lower() in ['.zip', '.rar']:
            image = self.archidx
        else:
            image = self.unknidx
        self.treeView.SetItemImage(item, image, wx.TreeItemIcon_Normal)

    # --- заполнение строки состояния -----------------------------------------
    def FillStatusBar(self):
        fileCount   = 0
        opsCount    = 0
        allOpsCount = 0

        curRootChild = self.treeView.GetFirstChild(self.root)[0]
        while True:
            ### > тело цикла
            allOpsCount += 1
            if self.treeView.ItemHasChildren(curRootChild):
                opsCount += 1
                curOPSChild = self.treeView.GetFirstChild(curRootChild)[0]
                while True:
                    fileCount += 1
                    if curOPSChild == self.treeView.GetLastChild(curRootChild)[0]:
                        break
                    curOPSChild = self.treeView.GetNextSibling(curOPSChild)
            ###
            if curRootChild == self.treeView.GetLastChild(self.root)[0]:
                break
            curRootChild = self.treeView.GetNextSibling(curRootChild)

        self.sb.SetStatusText(u"Осталось файлов: %s" % fileCount,   1)
        self.sb.SetStatusText(u"Не забрали ОПС: %s"  % opsCount,    2)
        self.sb.SetStatusText(u"Всего ОПС: %s"       % allOpsCount, 3)

    # --- актуализация списка файлов на отправку в отдельном каталоге ОПС -----
    def RefreshFileTree(self, item):
        if self.treeView.ItemHasChildren(item):
            children  = []
            treeFiles = []
            currentChild = self.treeView.GetFirstChild(item)[0]
            while True:
                children.append(currentChild)
                treeFiles.append(self.treeView.GetItemText(currentChild))
                if currentChild == self.treeView.GetLastChild(item)[0]:
                    break
                currentChild = self.treeView.GetNextSibling(currentChild)

            itemDir   = self.treeView.GetItemText(item)[:6]
            sendFiles = os.listdir(os.path.join(destDir, itemDir))

            for child in children:
                file = self.treeView.GetItemText(child)
                pathSendFile = os.path.join(destDir, itemDir, file)
                if not os.path.exists(pathSendFile):
                    self.treeView.Delete(child)
                    treeFiles.remove(file)

            # добавить вновь появившиеся файлы в дерево каталогов
            for addedFile in set(sendFiles)-set(treeFiles):
                newItem = self.treeView.AppendItem(item, addedFile)
                #self.treeView.SetItemText(newItem, u"<файл>", 1)

                #self.treeView.SetItemImage(newItem, self.fileidx, wx.TreeItemIcon_Normal)
                self.PutItemImage(newItem)

                analisedSF = os.path.join(destDir, itemDir, addedFile)

                infoStr = SFInfo.sfInfoShortString(SFInfo.sfInfo(analisedSF))
                self.treeView.SetItemText(newItem, infoStr, 2)

                self.treeView.SetItemText(newItem,
                                          self.CalcFileSize(analisedSF),
                                          1) # размер файла в ячейке

                # отобразить содержимое базы ЕЛС в дереве каталогов
                self.UnPackELS(newItem, analisedSF)

        if self.treeView.ItemHasChildren(item):
            childrenCount = self.treeView.GetChildrenCount(item)
            self.treeView.SetItemText(item, u"файлов - " + str(childrenCount), 2)
        else:
            self.treeView.SetItemBold(item, bold=False)
            self.treeView.SetItemTextColour(item, "gray")
            self.treeView.SetItemText(item, u"<пусто>", 2)


    ###########################################################################
    # Функции-обработчики событий
    ###########################################################################


    # --- вызывается при закрытии окна програмы крестиком ---------------------
    def OnCloseWindow(self, event):
        self.Show(False)
        self.Destroy()

    # --- выход из программы --------------------------------------------------
    def OnExit(self, event):
        self.Show(False)
        self.Close()

    # --- обновить дерево каталогов -------------------------------------------
    def OnRefresh(self, event):
        self.treeView.DeleteAllItems()
        self.BuildOPSTree()
        self.FillStatusBar()

    # --- развернуть дерево каталогов -----------------------------------------
    def OnExpand(self, event):
        self.treeView.ExpandAll(self.root)

    # --- двойной клик на элементе дерева каталогов ---------------------------
    def OnLeftDClick(self, event):
        item    = self.treeView.GetSelections()[0]
        itemTxt     = self.treeView.GetItemText(item)

        if not itemTxt == destDir:
            if not itemTxt[:6] in opsDict:
                if not itemTxt[:3] in codeSDODict:
                    parent  = self.treeView.GetItemParent(item)
                    parentTxt   = self.treeView.GetItemText(parent)

                    pathSendFile = os.path.join(destDir, parentTxt[:6], itemTxt)
                    if os.path.exists(pathSendFile):
                        if os.path.splitext(pathSendFile)[1].lower() == '.txt':
                            ### > отображение диалога просмотра текстового файла
                            dlgViewInfo = postdirdlg.TxtViewDialog(
                                                         (windowTitle, itemTxt),
                                                         parentTxt,
                                                         pathSendFile,
                                                         appIcon,
                                                         self
                                                                  )
                            dlgViewInfo.ShowModal()
                            dlgViewInfo.Destroy()
                            ###
                        else:
                            pass
                            # здесь можно поместить код для обработки
                            # файлов с другим расширением
                    else:
                        # актуализация списка файлов на отправку в отдельном каталоге ОПС
                        self.RefreshFileTree(parent)

                        # отсортировать список файлов на отправку в дереве каталогов
                        self.treeView.SortChildren(parent)

                        # заполнение строки состояния
                        self.FillStatusBar()

                        self.Refresh()
                        #self.Update()

                        wx.MessageBox(u'Файл не найден!',
                                      windowTitle,
                                      wx.OK | wx.ICON_ERROR,
                                      self)

    # ---очистка директорий соответствующих ОПС -------------------------------
    def OnClear(self, event):
        filePresence = False    # флаг наличия хотя бы одного файла в директориях ОПС
        for opsDir in opsDict:
            fullPath = os.path.join(destDir, opsDir)
            fileList = os.listdir(fullPath)
            if len(fileList) != 0:
                filePresence = True
                break
        if filePresence:
            deleteFileCount     = 0 # счётчик кол-ва удалённых файлов
            failureDelFileCount = 0 # счётчик кол-ва файлов, которые не удалось удалить
            deleteDirCount      = 0 # счётчик кол-ва директорий, в которых удалены файлы
            failureDelDirCount  = 0 # счётчик кол-ва директорий, в которых не удалось удалить файлы
            userResponse = wx.MessageBox(u"Вы действительно хотите очистить все каталоги ОПС?" + 10 * " ",
                                         windowTitle,
                                         wx.YES_NO | wx.ICON_QUESTION,
                                         self)
            if userResponse == wx.YES:
                for opsDir in opsDict:
                    fullPath = os.path.join(destDir, opsDir)
                    fileList = os.listdir(fullPath)
                    if len(fileList) != 0:
                        deleteDirCount += 1
                        tmp = failureDelFileCount
                        for file in fileList:
                            try:
                                os.remove(os.path.join(fullPath, file))
                                deleteFileCount += 1
                            except:
                                failureDelFileCount += 1
                        if tmp < failureDelFileCount:
                            failureDelDirCount += 1
                self.treeView.DeleteAllItems()
                self.BuildOPSTree()
                if deleteDirCount == 1:
                    katalog = u" каталоге"
                else:
                    katalog = u" каталогах"
                if failureDelFileCount == 0:
                    wx.MessageBox(u"Каталоги ОПС успешно очищены! Удалено файлов: " + str(deleteFileCount)\
                                        + u" в " + str(deleteDirCount) + katalog + u" ОПС" + 10 * " ",
                                  windowTitle,
                                  wx.OK | wx.ICON_INFORMATION,
                                  self)
                else:
                    wx.MessageBox(u"Каталоги ОПС частично очищены! Удалено файлов: " + str(deleteFileCount)\
                                        + u" в " + str(deleteDirCount) + katalog + u" ОПС. Не удалось "\
                                        + u"удалить файлов: " + str(failureDelFileCount)\
                                        + u" в " + str(failureDelDirCount) + katalog + u" ОПС" + 10 * " ",
                                  windowTitle,
                                  wx.OK | wx.ICON_WARNING,
                                  self)
        else:
            wx.MessageBox(u"Каталоги ОПС пусты!" + 10 * " ",
                          windowTitle,
                          wx.OK | wx.ICON_INFORMATION,
                          self)

    # --- отправка файлов на ОПС ----------------------------------------------
    def OnSend(self, event):
        dlgSend = postdirdlg.SendDialog(
                                        windowTitle,
                                        appIcon,
                                        self
                                       )
        dlgSend.ShowModal()
        dlgSend.Destroy()

        '''
        wx.MessageBox(u"Отправка файлов на ОПС!" + 10 * " ",
                      windowTitle,
                      wx.OK | wx.ICON_INFORMATION,
                      self)
        '''
#
# Конец класса MainWindowApp
###############################################################################


###############################################################################
# Начало класса приложения (App)
#
class App(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame = MainWindowApp(None, -1, "")
        self.SetTopWindow(frame)
        frame.Show()
        return True
#
# Конец класса App
###############################################################################

def main():
    #os.chdir(sendDir)
    app = App(0)
    app.MainLoop()

if __name__ == "__main__":
    main()
