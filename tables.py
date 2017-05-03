import xlrd
import xlwt
import wx
import wx.grid
import os
import time

"""
This module is about extracting information from Excel to display in a wxGrid using xlwt and xlrd. Can only read xls.
"""

class TABLES(object):
    """
    Reads data from Excel.
    """
    def __init__(self, other_self):
        self.other_self = other_self
        
    def excel_to_grid(self, source, sheet, grid):
        """
        Opens the Excel file in source and loads the sheet into the grid
        nx is the number of extra columns required.
        """
        
        wb = xlrd.open_workbook(source)
        names = wb.sheet_names()
        
        if sheet in names:
            grid.ClearGrid()
            if grid.GetNumberRows()>0:
                grid.DeleteRows(0,grid.GetNumberRows() ,True)
            if grid.GetNumberCols()>0:
                grid.DeleteCols(0,grid.GetNumberCols() ,True)

            
            sh = wb.sheet_by_name(sheet)
            num_rows = sh.nrows
            num_cols = sh.ncols
            self.SetGridRows(grid, num_rows)
            self.SetGridCols(grid, num_cols)#extra columns for results
            #print 'number of rows = ', num_rows
            #print 'number of columns = ', num_cols
            curr_row = -1
            while curr_row < num_rows-1:
                curr_row += 1
                for i in range(num_cols):
                    grid.SetCellValue(curr_row, i, self.style(sh, curr_row,i))
            return True
        else:
            return False


    def grid_to_excel(self,target,grids):
        """Reads the grid and writes to the excel file, then saves. each input grid is a tuple, grid followed by sheet name"""
        wb = xlwt.Workbook()
        sheets = [None]*len(grids) #array for all the sheets
        if len(grids)>0:
            for grid,num in zip(grids,range(len(grids)) ):
                if target == "File name (optional)" or target=="":
                    values = time.localtime(time.time())
                    target = str(values[0])+'.'+str(values[1])+'.'+str(values[2])+'.'+str(values[3])+'.'+str(values[4])
                
                sheets[num] = wb.add_sheet(grid[1])
                
                for r in range(grid[0].GetNumberRows()):
                    for c in range(grid[0].GetNumberCols()):
                        sheets[num].write(r,c, grid[0].GetCellValue(r,c))
                
            wb.save(str(target)+'.xls')
            
                     
    def style(self,worksheet, row, column):
        """
        Determines type of cell content and returns appropriate string
         for placing in wxGrid cell. Without this you get additional 
         characters (u : ") to confuse the presentation in the grid.
        """
        cell_type = worksheet.cell_type(row, column)
        if cell_type == 0: #Empty
                return ''
        if cell_type == 1: #Text
                return str(worksheet.cell_value(row, column))
        elif cell_type == 2: #Number
                return repr(worksheet.cell_value(row, column))
        elif cell_type == 6: #Blank
                return ''
        else:
                return repr(worksheet.cell_value(row, column))
        # might also want to handle 3=Date, 4=Boolean, 5 = Error				
                    
    def SetGridRows(self, grid_name, no_of_rows):
        """
        Set grid, *grid_name*, to have rows, *no_of_rows*.
        """
        grid_name.ClearGrid() #clear all data first
        change_rows = no_of_rows - grid_name.GetNumberRows()
        if change_rows > 0:
                grid_name.AppendRows(change_rows) #always to end
        elif change_rows < 0:
                grid_name.DeleteRows(0, -change_rows) #from posn 0
        self.other_self.m_scrolledWindow3.SendSizeEvent() # make sure new size is fitted
                    
    def SetGridCols(self, grid_name, no_of_cols):
        """
        Set grid, *grid_name*, to have columns, *no_of_cols*.
        """
        grid_name.ClearGrid() #clear all data first
        change_cols = no_of_cols - grid_name.GetNumberCols()
        if change_cols > 0:
                grid_name.AppendCols(change_cols) #always to end
        elif change_cols < 0:
                grid_name.DeleteRows(0, -change_cols) #from posn 0
        self.other_self.m_scrolledWindow3.SendSizeEvent() # make sure new size is fitted



if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = wx.Frame(None, -1, size=(700,500), title = "Testing tables.py")
    grid = wx.grid.Grid(frame)
    grid.CreateGrid(20,6)
    b = '' #substitute for a namespace
    a = TABLES(b)
    a.excel_to_grid('RefStepE052.xlsx', 'Sheet1',grid)
    
    frame.Show(True)
    app.MainLoop()
