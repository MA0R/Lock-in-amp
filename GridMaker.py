import wx
import wx.grid
import numpy as np

"""
This code makes a printer to a specified grid, capable of printing columns and rows.
It also generates the necessary columns for the ref-step algorithm based on the ranges of the instruments sent
"""

class GridPrinter(object):
    """
    Prints to a wx grid
    """
    def __init__(self, other_self,grid):
        self.other_self = other_self
        self.grid = grid
        
    def ColMaker(self,rm,rs,rx,cal_ranges):
        #create empty arrays
        info = []
        for Range in cal_ranges:
            cols = self.SetMaker(rm,rs,rx,Range)
            neg_cols = [cols[0],[-1*x for x in cols[1]],cols[2],[-1*x for x in cols[3]],cols[4],[-1*x for x in cols[5]],cols[6],cols[7],cols[8]]
            for i in range(int(float(Range[5]))):
                info.append(cols)
                info.append(neg_cols)
            
        full_cols = self.JoinCols(info)
        return full_cols
        
    def SetMaker(self,rm,rs,rx,single_range):
        rx_use = None
        rm_use = None
        #want to find the X range that encompases the max output, to 0.5%?
        #the following if statements are incase someone does not input a range covered by the instruments.
        #It should ideally never be used.
        for r in rx[::-1]: #similar process to above
            if float(single_range[1]) <=float(r[1]): #tolerance of 0.5%?
                rx_use = r
        if rx_use ==None: #here the max output of X is not sufficient to reach top of the calibration range
            print("can not reach top of range "+str(single_range[1])+" with source X")
            rx_use = rx[-1]
            print("max voltage stepped down to "+str(rx_use[1]))
            single_range[1] = rx[-1][1]
        for r in rm[::-1]: #similar process to above
            if float(single_range[1]) <= float(r[1]): #tolerance of 0.5%?
                rm_use = r
        if rm_use ==None: #here the max output of X is not sufficient to reach top of the calibration range
            print("can not reach top of range "+str(single_range[1])+" with meter")
            rm_use = rm[-1]
            print("max voltage stepped down to "+str(rm_use[1]))
            single_range[1] = rm[-1][1]
            
        #now update the minimum of the range, there could be the odd case in which
        #either the meter or the source cannot reach 0 on the particular range.
        single_range[0] = max(rx_use[0],rm_use[0])

        #Now can calculate the size of the refstep, and identify a suitable source S range.
        ref_step = (float(single_range[1])-float(single_range[0]))/float(single_range[6])
        for r in rs[::-1]: #similar process to above
            if float(ref_step)+float(single_range[0]) <= float(r[1]): #tolerance of 0.5%?
                rs_use = r
        #Need to determine the range below current ranges of x and m, for the use of gain ratios.
        m_index = rm.index(rm_use)
        m_envelope = rm_use
        x_index =rx.index(rx_use)
        x_envelope = rx_use
        #need to check that these ranges encompass the entire ref step. 
        if m_index >0:
            if rm[m_index-1][1] >= ref_step+single_range[0] and rm[m_index-1][0] <= single_range[0]:
                m_envelope = rm[m_index-1]
        if x_index>0:
            if rx[x_index-1][1] >= ref_step+single_range[0] and rx[x_index-1][0] <= single_range[0]:
                x_envelope = rx[x_index-1]
                
        x_settings = []
        for n in np.arange(float(single_range[0]),float(single_range[1]),ref_step):
            x_settings.append(n+ref_step)
            x_settings.append(n+ref_step)
        x_settings = [ref_step+single_range[0],single_range[0],ref_step+single_range[0],single_range[0]]+x_settings
        
        s_settings = [ref_step,0]*(len(x_settings)/2)
        s_settings[0] = 0 #update first value to the minimum.

        #Ranges for all instruments:
        #x and m will have the first three range settings given by envelope.
        x_ranges = self.mirror([x_envelope[2]]*3+[rx_use[2]]*(len(x_settings)-3))
        m_ranges = self.mirror([m_envelope[2]]*3+[rm_use[2]]*(len(x_settings)-3))
        s_ranges = self.mirror([rs_use[2]]*len(x_settings))
        x_settings = self.mirror(x_settings)
        s_settings = self.mirror(s_settings)
        nominal = [x-s for x,s in zip(x_settings,s_settings)]
        reading_num = [single_range[2]]*len(x_settings)
        pre_reading_delay = [single_range[3]]*len(x_settings)
        inter_reading_delay = [single_range[4]]*len(x_settings)
        
        cols = [x_ranges,x_settings,s_ranges,s_settings,m_ranges,nominal,reading_num,pre_reading_delay,inter_reading_delay]

        return cols
        
    def mirror(self,array): #mirrors array about last value
        temp = array[0:-1]
        return array+temp[::-1]
        
    
    def JoinCols(self,info):
        """
        Make a measuremnt set for a given source X range. From the ranges
        for the DVM and source S also determines the settings for thsoe.
        """
        x_ranges,x_settings,s_ranges,s_settings,m_ranges,nominal,num_readings,delay,delay2 = [[]]*9
        #from list of lists of partial columns return list of entire columns
        for col in info:
            xr,xs,sr,ss,mr,nom,num_r,dl,dl2 = col #xr=x ranges, xs=x settings, sr=s ranges, ss=s settings,mr= meter ranges,nom = nominal readigs,num = number readings, dl=delay.
            x_settings = x_settings+xs
            s_settings =s_settings+ss
            x_ranges = x_ranges+xr
            s_ranges = s_ranges+sr
            m_ranges = m_ranges+mr
            nominal = nominal+nom
            num_readings = num_readings+num_r
            delay = delay+dl
            delay2 = delay2+dl2
            
        return [x_ranges,x_settings,s_ranges,s_settings,m_ranges,nominal,num_readings,delay,delay2]
        
    def PrintCol(self, col, start_col,start_row):
        """
        Prints a column from specified starting point
        """
        #check if there are enough rows:
        min_rows = start_row+len(col)-1 #minimum rows required
        if min_rows>self.grid.GetNumberRows():
            #add rows so column can fit
            self.AddGridRows(min_rows-self.grid.GetNumberRows())
        min_cols = start_col+1
        if min_cols>self.grid.GetNumberCols():
            #add cols so rows can fit
            self.AddGridCols(min_cols-self.grid.GetNumberCols())
            
        for value,row in zip(col,range(start_row,start_row+len(col))):
            self.grid.SetCellValue(int(row)-1,int(start_col),str(value))
        

    def PrintRow(self, row, start_col,start_row):
        """
        Prints a row from specified starting point
        """
        #check if there are enough rows:
        min_cols = start_col+len(row) #minimum rows required
        min_rows = start_row+1
        if min_rows>self.grid.GetNumberRows():
            #add rows so column can fit
            self.AddGridRows(min_rows-self.grid.GetNumberRows())
        
        if min_cols>self.grid.GetNumberCols():
            #add cols so rows can fit
            self.AddGridCols(min_cols-self.grid.GetNumberCols())
            
        for value,col in zip(row,range(start_col,start_col+len(row))):
            self.grid.SetCellValue(int(start_row)-1,int(col),str(value))
            
    def AddGridRows(self, no_of_rows):
        """
        Add to grid, *self.grid*, some rows, *no_of_rows*.
        """
        if no_of_rows > 0:
                self.grid.AppendRows(no_of_rows) #always to end
        elif no_of_rows < 0:
                self.grid.DeleteRows(0, -no_of_rows) #from posn 0
        self.other_self.m_scrolledWindow3.SendSizeEvent() # make sure new size is fitted
                    
    def AddGridCols(self, no_of_cols):
        """
        Set grid, *self.grid*, to have columns, *no_of_cols*.
        """
        if no_of_cols > 0:
                self.grid.AppendCols(no_of_cols) #always to end
        elif no_of_cols < 0:
                self.grid.DeleteRows(0, -no_of_cols) #from posn 0
        self.other_self.m_scrolledWindow3.SendSizeEvent() # make sure new size is fitted

    def ClearGrid(self):
        self.grid.ClearGrid()


if __name__ == "__main__":
    GridFactory = GridPrinter(None,None)
    info = GridFactory.ColMaker([(0,10,'10')],[(0,10,'10')],[(0,10,'10')],[[0,5,6,7,8,2,10]])
    import csv

    with open("output.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(info)




