import pathlib
import math
import time

class DataPoint:
    def __init__(self, x, y):
        self.x=float(x)
        self.y=float(y)
        self.inflection=False
        self.active=True
        self.max_at_x=False
    def __eq__(self, other):
        try:
            return self.x==other.x and self.y==other.y
        except:
            return False
    def __lt__(self, other):
        try:
            if self.x<other.x:
                return False
            elif self.x==other.x and self.y>other.y:
                return True
            elif self.x==other.x and self.y<=other.y:
                return False
            else:
                return True
        except:
            return False

class DataSet:
    """expects a CSVFile object as the argument."""
    def __init__(self, csvfile):
        self.csv = csvfile
        self.path = pathlib.Path(csvfile.path)
        self.name = self.path.parts[len(self.path.parts)-1]
        start = time.time()
        self.parse()
        end = time.time()
        #print('Parse time: {}'.format(end-start))
        start = time.time()
        self._max_values_sorted()
        end = time.time()
        #print('Max time: {}'.format(end-start))
        start = time.time()
        self.inflections()
        end = time.time()
        #print('Inflections time: {}'.format(end-start))
        start = time.time()
        self.calc_average_non_inflections()
        end = time.time()
        #print('Calc time: {}'.format(end-start))
    def parse(self):
        if self.csv.maxColumns!=2 or self.csv.minColumns!=2:
            raise Exception("CSV File does not have expected number of columns (2). File: {}".format(self.csv.path))
        self.data = []
        row=0
        for i in self.csv.data:
            try:
                self.data.append(DataPoint(float(i[0]),float(i[1])))
                row+=1
            except ValueError as e:
                row+=1
                raise ValueError("Can't convert row: {} to float in file {}. \nValues: {}".format(row, self.path, i))
        self.data.sort()
    def __len__(self):
        return len(self.data)
    def __getitem__(self, position):
        return self.data[position]
    
    """List must be sorted before calling this function."""
    def _max_values_sorted(self):
        i = 0
        self.max_points = []
        temp = []
        while i<len(self.data):
            if len(temp)==0:
                temp.append(self.data[i])
            elif self.data[i].x==temp[0].x:
                temp.append(self.data[i])
            else:
                temp.sort()
                if temp[0].y>float(0):
                    temp[0].max_at_x=True
                    self.max_points.append(temp[0])
                temp = []
                temp.append(self.data[i])
            i += 1
        self.max_points.sort()

    """Will take a very long time for large lists, can be used on unsorted lists."""
    def _max_values_unsorted(self):
        self.max_points = []
        for i in self.data:
            temp = []
            for j in self.data:
                if i.x==j.x:
                    temp.append(j)
            temp.sort()
            temp[0].max_at_x=True
        for i in self.data:
            if i.max_at_x:
                self.max_points.append(i)
        self.max_points.sort()
                

    def inflections(self):
        if len(self.max_points)>=2:
            if self.max_points[0].y>self.max_points[1].y:
                self.max_points[0].inflection=True
            for i in range(1, len(self.max_points)-1):
                if self.max_points[i].y>self.max_points[i-1].y and self.max_points[i].y>self.max_points[i+1].y:
                    self.max_points[i].inflection=True
            if self.max_points[len(self.max_points)-1].y>self.max_points[len(self.max_points)-2].y:
                self.max_points[len(self.max_points)-1].inflection=True
    def calc_average_non_inflections(self):
        count = 0
        sum = 0
        for i in self.data:
            if not i.inflection and i.y>float(0):
                count+=float(1)
                sum+=float(i.y)
        if count>float(0):
            self.average_non_inflections=float(sum/count)
        else: 
            self.average_non_inflections=float(0)
    def _getListInWindowSorted(self, x_value, window_size=float(0.2), index=0):
        return_list = []
        current_index = index-1
        in_range=True
        while current_index>=0 and in_range:
            if abs(x_value-self.max_points[current_index].x)<=float(window_size):
                if self.max_points[current_index].active:
                    return_list.append(self.max_points[current_index])
            else:
                in_range = False
            current_index -= 1
        current_index = index + 1
        in_range = True
        while current_index<len(self.max_points) and in_range:
            if abs(x_value-self.max_points[current_index].x)<=float(window_size):
                if self.max_points[current_index].active:
                    return_list.append(self.max_points[current_index])
            else:
                in_range = False
            current_index += 1
        return return_list
            
    def _getListInWindowUnsorted(self, x_value, window_size=float(0.2), index=None):
        return_list = []
        for i in self.max_points:
            if abs(i.x-x_value)<=float(window_size) and i.active:
                return_list.append(i)
        return return_list
    def window_max(self, window_size=float(0.2)):
        p = 0
        for i in self.max_points:
            if i.active and i.inflection:
                neighbors = self._getListInWindowSorted(i.x, window_size, p)
                for j in neighbors:
                    if j.y>i.y:
                        i.active=False
                    else:
                        j.active=False
            p += 1
    

class Filters:
    def __init__(self, dataset):
        self.dataset = dataset
    def inflections(self):
        if len(self.dataset.data)>=2:
            if self.dataset.data[0].y>self.dataset.data[1].y:
                self.dataset.data[0].inflection=True
            for i in range(1, len(self.dataset.data)-1):
                if self.dataset.data[i].y>self.dataset.data[i-1].y and self.dataset.data[i].y>self.dataset.data[i+1].y:
                    self.dataset.data[i].inflection=True
            if self.dataset.data[len(self.dataset.data)-1].y>self.dataset.data[len(self.dataset.data)-2].y:
                self.dataset.data[len(self.dataset.data)-1].inflection=True
                
    def calc_average_non_inflections(self):
        count = 0
        sum = 0
        for i in self.dataset.data:
            if not i.inflection and i.y>float(1):
                count+=float(1)
                sum+=float(i.y)
        self.average_non_inflections=float(sum/count)
