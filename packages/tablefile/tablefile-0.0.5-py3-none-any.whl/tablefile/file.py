from math import *
class file:

    def __init__(self,filename,*separator):   # * symbol before separator makes it optional variable for user while creating the object (also it allows more than one sparator values)
        self.filename=filename
        self.separator=separator
        f=open(self.filename,"r+")
        lineno=0
        for lns in f.readlines():
            if not lns[0:1]=="#" and not lns[0:1]=="\n":
                lineno+=1
        self.lines=lineno #len(f.readlines())
       # print(len(self.lines))
        f.close()
        
    def read(self,*operator):
        colArgs=[]
        lineIndex=0
        f=open(self.filename,"r+")
        lines=f.readlines()
        if len(self.separator)!=0:
            sep=self.separator[0]
        else:
            sep=" "
        lineTot=len(lines)
        for ln in lines:
            
            if not ln[0:1]=="#" and not ln[0:1]=="\n" :
                a=ln.split(sep)
                
                for i in range(len(a)):
                    try:
                        a[i]=float(a[i])
                    except:
                        pass
                colArgs.append(a)    
        f.close()
        if not len(operator)==0:
            if (operator[0]=="l/c") or (operator[0]=="line/col"):
                pass
            else:
                opCol=[]
                [opCol.append([]) for ax in range(len(colArgs[0]))] 
                if (operator[0]=="av") or (operator[0]=="average"):
                    for i in range(len(opCol)):
                        for j in range(len(colArgs)):
                            if not type(colArgs[j][i])==str:
                                opCol[i].append(colArgs[j][i])
                        try:
                            opCol[i]=sum(opCol[i])/len(opCol[i])
                        except:
                            opCol[i]="Error"
                if (operator[0]=="sm") or (operator[0]=="sum"):
                    for i in range(len(opCol)):
                        for j in range(len(colArgs)):
                            if not type(colArgs[j][i])==str:
                                opCol[i].append(colArgs[j][i])
                        try:
                            opCol[i]=sum(opCol[i])
                        except:
                            opCol[i]="Error"
                if (operator[0]=="sd") or (operator[0]=="sigma"):
                    for i in range(len(opCol)):
                        for j in range(len(colArgs)):
                            if not type(colArgs[j][i])==str:
                                opCol[i].append(colArgs[j][i])
                        try:
                            mean=(sum(opCol[i])/len(opCol[i]))
                        except:
                            opCol[i]="Error"
                        opCol[i]=[]
                        for j in range(len(colArgs)):
                            if not type(colArgs[j][i])==str:
                                opCol[i].append((colArgs[j][i]-mean)**2)
                        try:
                            opCol[i]=(sum(opCol[i])/len(opCol[i]))**0.5
                        except:
                            opCol[i]="Error"
                if (operator[0]=="sds") or (operator[0]=="sigma_sample"):
                    for i in range(len(opCol)):
                        for j in range(len(colArgs)):
                            if not type(colArgs[j][i])==str:
                                opCol[i].append(colArgs[j][i])
                        try:
                            mean=(sum(opCol[i])/len(opCol[i]))
                        except:
                            opCol[i]="Error"
                        opCol[i]=[]
                        for j in range(len(colArgs)):
                            if not type(colArgs[j][i])==str:
                                opCol[i].append((colArgs[j][i]-mean)**2)
                        try:
                            opCol[i]=(sum(opCol[i])/(len(opCol[i])-1))**0.5
                        except:
                            opCol[i]="Error"
                if (operator[0]=="mx") or (operator[0]=="maximum"):
                    for i in range(len(opCol)):
                        for j in range(len(colArgs)):
                            if not type(colArgs[j][i])==str:
                                opCol[i].append(colArgs[j][i])
                        try:
                            opCol[i]=max(opCol[i])
                        except:
                            opCol[i]="Error"
                if (operator[0]=="mn") or (operator[0]=="minumum"):
                    for i in range(len(opCol)):
                        for j in range(len(colArgs)):
                            if not type(colArgs[j][i])==str:
                                opCol[i].append(colArgs[j][i])
                        try:
                            opCol[i]=min(opCol[i])
                        except:
                            opCol[i]="Error"
                if (operator[0]=="c/l") or (operator[0]=="col/line"):
                    for i in range(len(opCol)):
                        for j in range(len(colArgs)):                        
                            opCol[i].append(colArgs[j][i])
                
                colArgs.clear()
                for item in opCol:
                    colArgs.append(item)
        #print(colArgs)
        return colArgs

            
def convert(List,expression):
    a=[] 
    for itm in List:
        if isinstance(itm,list):
            print('Convert error: Input list must be one dimensional.')
            return
    if not isinstance(List,list):
        print('Convert error: Not a list input. Correct input- convert(list,experssion). Example- convert([4,7,"abc",20],"(x**2+1)/5")')
        return   
    for item in List:
        if type(item)!=str:
            x=item
            try:
                a.append(eval(expression))
            except:
                print('Convert error: Could not complete operation')
        else:
            a.append(item) 
    return a
def sd(List):
    for itm in List:
        if isinstance(itm,list):
            print('sd error: Input list must be one dimensional.')
            return
    if not isinstance(List,list):
        print('sd error: Not a list input.')
        return
    sum=0
    ssum=0
    Num=0
    for item in List:
        if not isinstance(item,str):
            sum=sum+item
            Num+=1
    avg=sum/Num
    for item in List:
        if not isinstance(item,str):
            ssum=ssum+(item-avg)**2

    return (sqrt(ssum/Num))
def sds(List):
    for itm in List:
        if isinstance(itm,list):
            print('sd error: Input list must be one dimensional.')
            return
    if not isinstance(List,list):
        print('sd error: Not a list input.')
        return
    sum=0
    ssum=0
    Num=0
    for item in List:
        if not isinstance(item,str):
            sum=sum+item
            Num+=1
    avg=sum/Num
    for item in List:
        if not isinstance(item,str):
            ssum=ssum+(item-avg)**2

    return (sqrt(ssum/(Num-1)))

def av(List):
    for itm in List:
        if isinstance(itm,list):
            print('av error: Input list must be one dimensional.')
            return
    if not isinstance(List,list):
        print('av error: Not a list input.')
        return
    sum=0
    Num=0
    for item in List:
        if not isinstance(item,str):
            sum=sum+item
            Num+=1
    avg=sum/Num
    return avg
def mx(List):
    for itm in List:
        if isinstance(itm,list):
            print('mx error: Input list must be one dimensional.')
            return
    if not isinstance(List,list):
        print('mx error: Not a list input.')
        return
    maxval=-10000000000
    for item in List:
        if not isinstance(item,str):
            if item>maxval:
                maxval=item
    return maxval
def mn(List):
    for itm in List:
        if isinstance(itm,list):
            print('mn error: Input list must be one dimensional.')
            return
    if not isinstance(List,list):
        print('mn error: Not a list input.')
        return
    minval=10000000000
    for item in List:
        if not isinstance(item,str):
            if item<minval:
                minval=item
    return minval

def sm(List):
    for itm in List:
        if isinstance(itm,list):
            print('sm error: Input list must be one dimensional.')
            return
    if not isinstance(List,list):
        print('sm error: Not a list input.')
        return
    sumval=0
    for item in List:
        if not isinstance(item,str):
            sumval=sumval+item
    return sumval
    """def lines:
        f=open(self.filename,"r+")
        lines=f.readlines()
        return"""  
    