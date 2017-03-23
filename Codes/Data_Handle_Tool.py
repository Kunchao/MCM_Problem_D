import xlrd
import xlwt
import datetime

class Tool:

    def __init__(self):
        pass
        
    def filter_col(self,old_col):
        col=filter(lambda x: x!='', old_col)
        col.sort()
        return col
        
    def get_percentage(self,old_col,step):
        col=self.filter_col(old_col)
        lenth=int(max(col))/step*step+step+1
        raw=[]
        result={}
        for num in range(lenth)[::step]:
            raw.append(num)
            result[num]=0
        print raw
        for item in col:
            item_floor=int(item)
            print '[%d-%d]:'%(item_floor/step*step,item_floor/step*step+step), item
            result[item_floor/step*step+step]+=1
        print 'result dic:',result
        for index in range(len(raw)):
            raw[index]='%d : %.2f%%' % (raw[index],float(result[raw[index]]*100)/len(col))
        return raw

    def get_col(self,filename,col_num):
        xls_file = xlrd.open_workbook(filename)
        sheet = xls_file.sheet_by_index(0)
        return sheet.col_values(col_num)
    
    def get_all_col(self,filename):
        col_list=[]
        xls_file = xlrd.open_workbook(filename)
        sheet = xls_file.sheet_by_index(0)
        for col in range(sheet.ncols):
            col_list.append(sheet.col_values(col))
        return col_list

    def get_time_dif(self,old_col):
        col=self.filter_col(old_col)
        result=[]
        for rownum in range(len(col)-1):
            time_dif=(xlrd.xldate.xldate_as_datetime(col[rownum+1], 0)-xlrd.xldate.xldate_as_datetime(col[rownum], 0)).total_seconds()
            print xlrd.xldate.xldate_as_datetime(col[rownum], 0)
            print xlrd.xldate.xldate_as_datetime(col[rownum], 0).timetuple()
            result.append(time_dif)
        return result
    def get_col_dif(self,old_col):
        col=self.filter_col(old_col)
        result=[]
        for rownum in range(len(col)-1):
            time_dif=col[rownum+1]-col[rownum]
            result.append(time_dif)
        return result
    def get_time(self,old_col,switch):
        col=filter(lambda x: x!='', old_col)
        result=[]
        for rownum in range(len(col)):
            #print xlrd.xldate.xldate_as_datetime(col[rownum], 0)
            #print col[rownum]
            time=xlrd.xldate.xldate_as_datetime(col[rownum], 0)
            time_tuple=time.timetuple()
            if switch==0:
                result.append((time - datetime.datetime(time_tuple[0], time_tuple[1],time_tuple[2],0, 0,0,0)).total_seconds())
            if switch==1:
                result.append((time - datetime.datetime(time_tuple[0], time_tuple[1],time_tuple[2],0, 0,0,0)).total_seconds()/60)
        return result

    def save_xls(self,col_list,filename):
        workbook = xlwt.Workbook(encoding = 'ascii')
        worksheet = workbook.add_sheet(filename)
        for col_index in range(len(col_list)):
            for col_item_index in range(len(col_list[col_index])):
                worksheet.write(col_item_index,col_index,col_list[col_index][col_item_index])
        workbook.save('%s.xls'%filename)
        
    def get_format(self,col):
        index="'"
        result=''
        for item in col:
            a,b=item.split(' : ')
            index+=a+"','"
            result+=b+','
        print index[:-3]
        print result[:-1]

























