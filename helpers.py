import csv

def write_dict(file_name, _dict):
    with open(file_name, 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in _dict.items():
            writer.writerow([key, value])
def plt_csv(file ,xlabel,ylabel, ytype: type, xtype:type, min, plotf):
    xy = OrderedDict()
    x = []
    y = []
    with open(file,'r') as csvfile: 
        plots = csv.reader(csvfile, delimiter = ',') 
        
        for row in plots: 
        
            if not not row and ytype(row[1]) > min:
                xy[ytype(row[1])] =  xtype(row[0])
    for key, value in xy.items() :
        x.append(value)
        y.append(key)
    plotf(  x,y, color = 'g', label = ylabel) 

    plt.xlabel(xlabel) 
    plt.ylabel(ylabel) 
    plt.xticks(rotation=70)
    plt.legend() 
    plt.show() 
                