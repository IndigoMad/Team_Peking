import cv2
from tkinter import *
import ctypes
import numpy as np
from pickle import *
import os
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image, ImageDraw, ImageFont
import math



temp=ctypes.windll.LoadLibrary('opencv_ffmpeg342.dll')



#*********************************************
#=================主界面==================
#*********************************************

#=============主窗口===============
root=Tk()
root.overrideredirect(True)
root.wm_attributes('-topmost',1)
root.attributes("-alpha", 0.8)
root.title("Microscope Images Batching")
root.geometry("450x650")
rootlabel=Label(root,width=60,text="Microscope Images Batching",bg="aqua")
rootlabel.pack(side=TOP)

#=============主窗口移动============
x, y = 0, 0
rx,ry=1450,30
def rootmove(event):
    global x,y
    global rx,ry
    new_x = (event.x-x)+root.winfo_x()
    new_y = (event.y-y)+root.winfo_y()
    rx=new_x
    ry=new_y
    s = "450x650+"+str(new_x)+"+" + str(new_y)
    root.geometry(s)
def rootbutton_1(event):
    global x,y
    x,y = event.x,event.y
rootlabel.bind("<B1-Motion>",rootmove)
rootlabel.bind("<Button-1>",rootbutton_1)






#*********************************************
#===================软件配置==================
#*********************************************

configlabel=Label(root,text="=========Config========")
configlabel.pack(side=TOP)

"""
=====初始化配置文件=====
cf=open(os.curdir+os.sep+"config",'wb')
config={}
config["rule"]=""
config["path"]=".\\"
dump(config,cf)
"""

cf=open(os.curdir+os.sep+"config",'rb')
config=load(cf)
cf.close()


ruleslist=os.listdir(os.curdir+os.sep+"rules")

currulename=config["rule"]
VCRN=StringVar()
settingframe=Frame(root)
rulelabel=Label(settingframe,text="Current Rule")
OMframe=Frame(settingframe)
if len(ruleslist)==0:
    ruleOption=OptionMenu(OMframe,VCRN,"")
else:
    ruleOption=OptionMenu(OMframe,VCRN,*ruleslist)
VCRN.set(currulename)
settingframe.pack(side=TOP)
rulelabel.pack(side=LEFT)
OMframe.pack(side=LEFT)
ruleOption.pack(side=LEFT)

#=====规则管理=====

rulewin=Toplevel()
rulewin.overrideredirect(True)
rulewin.wm_attributes('-topmost',1)
rulewin.attributes("-alpha", 0.8)
rulewin.geometry("400x350")
rulewin.withdraw()
rulewintopline=Label(rulewin,width=50,text="Rules Manager",bg="aqua")
rulewintopline.pack(side=TOP)
leftframe=Frame(rulewin)
leftframe.pack(side=LEFT)
rightframe=Frame(rulewin)
rightframe.pack(side=LEFT)
rule=["0","0","0","0","","","","",""]
def examine():
    global currulename
    try:
        currule=open(os.curdir+os.sep+"rules"+os.sep+currulename,'rb')
        rule=load(currule)
        currule.close()
    except:
        ruleslist=os.listdir(os.curdir+os.sep+"rules")
        if len(ruleslist)==0:
            rulewin.deiconify()
            root.withdraw()
            rule=["0","0","0","0","","","","",""]
        else:
            currulename=ruleslist[0]
            VCRN.set(currulename)
            try:
                currule=open(os.curdir+os.sep+"rules"+os.sep+currulename,'rb')
                rule=load(currule)
                currule.close()
            except:
                rule=["0","0","0","0","","","","",""]
                rulewin.deiconify()
                root.withdraw()

examine()

z0=int(rule[0])
xy0=int(rule[1])
t0=int(rule[2])
c0=int(rule[3])
zn=rule[4]
xyn=rule[5]
tn=rule[6]
cn=rule[7]
namerule=rule[8]
trange,xyrange,crange,zrange=range(0),range(0),range(0),range(0)

FFF=[]

class RuleLabel():
    
    def openrule(self,event):
        for i in FFF:
            i.pack_forget()
        self.ruleframe=Frame(rightframe)
        self.ruleframe.pack()
        FFF.append(self.ruleframe)
        currulename=self.name
        try:
            currule=open(os.curdir+os.sep+"rules"+os.sep+currulename,'rb')
            rule=load(currule)
            currule.close()
        except:
            rule=["0","0","0","0","","","","",""]

        self.nV=StringVar()
        self.nameframe=Frame(self.ruleframe)
        self.nameframe.pack()
        self.namelabel=Label(self.nameframe,text="Rule Name    ")
        self.namelabel.pack(side=LEFT)
        self.nameentry=Entry(self.nameframe,textvariable=self.nV)
        self.nameentry.pack(side=LEFT)
        self.nV.set(self.name)
        
        pname=["z zero filling  ","xy zero filling","t zero filling  ","c zero filling  ","        zn         ","       xyn        ","        tn         ","        cn         "]
        self.pname=[]
        for i in range(8):
            self.pname.append(StringVar())
            self.iF=Frame(self.ruleframe)
            self.iF.pack()
            self.iL=Label(self.iF,text=pname[i])
            self.iL.pack(side=LEFT)
            self.iE=Entry(self.iF,textvariable=self.pname[i])
            self.iE.pack(side=LEFT)
            self.pname[i].set(rule[i])
        self.rV=StringVar()
        self.rF=Frame(self.ruleframe)
        self.rF.pack()
        self.rL=Label(self.rF,text="Name Rule    ")
        self.rL.pack(side=LEFT)
        self.rE=Entry(self.rF,textvariable=self.rV)
        self.rE.pack(side=LEFT)
        self.rV.set(rule[8])
        self.exm=Label(self.ruleframe,text='Example:name+zn+z+xyn+xy+tn+t+cn+c+".tif"')
        self.exm.pack()
        
            
        def deleterule():
            self.filea.pack_forget()
            for i in FFF:
                i.pack_forget()
            ruleslist.remove(self.name)
            os.remove(os.curdir+os.sep+"rules"+os.sep+self.name)
            
            
        def saverule():
            for i in range(8):
                rule[i]=self.pname[i].get()
            rule[8]=self.rV.get()
            currulename=self.nV.get()
            VCRN.set(currulename)
            currule=open(os.curdir+os.sep+"rules"+os.sep+currulename,'wb')
            dump(rule,currule)
            currule.close()
            ruleslist=os.listdir(os.curdir+os.sep+"rules")
            for i in FFFR:
                i.filea.pack_forget()
            for i in ruleslist:
                FFFR.append(RuleLabel(i))
            FFFR.append(RuleLabel("New Rule"))

        rulesavebutton=Button(self.ruleframe,text="Save Rule",command=saverule)
        ruledeletebutton=Button(self.ruleframe,text="Delete Rule",command=deleterule)
        rulesavebutton.pack(side=LEFT)
        ruledeletebutton.pack(side=LEFT)
        
        
    def __init__(self,rname):
        self.name=rname
        self.filea=Label(leftframe,text=rname)
        self.filea.pack()
        self.filea.bind("<Button-1>",self.openrule)
        
FFFR=[]
def rulewinopen():
    rulewin.deiconify()
    ruleslist=os.listdir(os.curdir+os.sep+"rules")
    for i in FFFR:
        i.filea.pack_forget()
    for i in ruleslist:
        FFFR.append(RuleLabel(i))
    FFFR.append(RuleLabel("New Rule"))
    root.withdraw()
    
def ruledone():
    global ruleOption
    rulewin.withdraw()
    root.deiconify()
    examine()
    ruleslist=os.listdir(os.curdir+os.sep+"rules")
    ruleOption.pack_forget()
    if len(ruleslist)==0:
        ruleOption=OptionMenu(OMframe,VCRN,"")
    else:
        ruleOption=OptionMenu(OMframe,VCRN,*ruleslist)
    ruleOption.pack()


ruleslist=os.listdir(os.curdir+os.sep+"rules")
ruleOption.pack_forget()
if len(ruleslist)==0:
    ruleOption=OptionMenu(OMframe,VCRN,"")
else:
    ruleOption=OptionMenu(OMframe,VCRN,*ruleslist)
ruleOption.pack()
for i in FFFR:
    i.filea.pack_forget()
for i in ruleslist:
    FFFR.append(RuleLabel(i))
FFFR.append(RuleLabel("New Rule"))

ruledonebutton=Button(leftframe,text="Finish",command=ruledone)
ruledonebutton.pack()




rulebutton=Button(settingframe,text="Rule Manager",command=rulewinopen)
rulebutton.pack(side=LEFT)


x, y = 0, 0
rx,ry=1450,30
def rulewinmove(event):
    global x,y
    global rx,ry
    new_x = (event.x-x)+rulewin.winfo_x()
    new_y = (event.y-y)+rulewin.winfo_y()
    rx=new_x
    ry=new_y
    s = "400x350+"+str(new_x)+"+" + str(new_y)
    rulewin.geometry(s)
def rulewinbutton_1(event):
    global x,y
    x,y = event.x,event.y
rulewintopline.bind("<B1-Motion>",rulewinmove)
rulewintopline.bind("<Button-1>",rulewinbutton_1)

#currule=open(os.curdir+os.sep+"rules"+os.sep+configname,'wb')
#dump(D,a)



#*********************************************
#===================通用函数==================
#*********************************************

def getruledata():
    global z0,xy0,t0,c0,zn,xyn,tn,cn,namerule
    currulename=VCRN.get()
    currule=open(os.curdir+os.sep+"rules"+os.sep+currulename,'rb')
    rule=load(currule)
    currule.close()
    z0=int(rule[0])
    xy0=int(rule[1])
    t0=int(rule[2])
    c0=int(rule[3])
    zn=rule[4]
    xyn=rule[5]
    tn=rule[6]
    cn=rule[7]
    namerule=rule[8]
    cf=open(os.curdir+os.sep+"config",'wb')
    config["rule"]=currulename
    dump(config,cf)
    cf.close()

def getrangedata():
    global trange,xyrange,crange,zrange
    trange=range(int(Vt1.get()),int(Vt2.get())+1)
    xyrange=range(int(Vxy1.get()),int(Vxy2.get())+1)
    crange=range(int(Vc1.get()),int(Vc2.get())+1)
    zrange=range(int(Vz1.get()),int(Vz2.get())+1)

#*********************************************
#===================文件选择==================
#*********************************************

#==变量设置==
Vt1=StringVar()
Vc1=StringVar()
Vxy1=StringVar()
Vz1=StringVar()
Vpath1=StringVar()
Vt2=StringVar()
Vc2=StringVar()
Vxy2=StringVar()
Vz2=StringVar()
Vpath2=StringVar()

#==窗口==
filelabel=Label(root,text="=========Files========")
filelabel.pack(side=TOP)
fileframe=Frame(root)
fileframe.pack(side=TOP)



def fileopen():
    filetem=tkinter.filedialog.askopenfilename(initialdir=config["path"],)
    cf=open(os.curdir+os.sep+"config",'wb')
    config["path"]=filetem
    dump(config,cf)
    cf.close()
    filetem=filetem.replace("/","\\")
    a=filetem.rfind("\\")
    pathtem=filetem[0:a]
    filetem=filetem[a+1:-1]
    Vpath1.set(pathtem)
    Vpath2.set(filetem)
    

pathframe=Frame(fileframe)
pathframe.pack(side=TOP)
Lpath1=Label(pathframe,text="Path")
Lpath2=Label(pathframe,text="Name")
pathstart=Entry(pathframe,textvariable=Vpath1)
pathend=Entry(pathframe,textvariable=Vpath2)
Lpath1.pack(side=LEFT)
pathstart.pack(side=LEFT)
Lpath2.pack(side=LEFT)
pathend.pack(side=LEFT)
filebutton=Button(pathframe,text="Open",command=fileopen)
filebutton.pack(side=LEFT)

tframe=Frame(fileframe)
tframe.pack(side=TOP)
Lt=Label(tframe,text="Range of Time    ")
tstart=Entry(tframe,textvariable=Vt1)
tend=Entry(tframe,textvariable=Vt2)
Lt.pack(side=LEFT)
tstart.pack(side=LEFT)
tend.pack(side=LEFT)

cframe=Frame(fileframe)
cframe.pack(side=TOP)
Lc=Label(cframe,text="Range of Channel")
cstart=Entry(cframe,textvariable=Vc1)
cend=Entry(cframe,textvariable=Vc2)
Lc.pack(side=LEFT)
cstart.pack(side=LEFT)
cend.pack(side=LEFT)

xyframe=Frame(fileframe)
xyframe.pack(side=TOP)
Lxy=Label(xyframe,text="Range of Position")
xystart=Entry(xyframe,textvariable=Vxy1)
xyend=Entry(xyframe,textvariable=Vxy2)
Lxy.pack(side=LEFT)
xystart.pack(side=LEFT)
xyend.pack(side=LEFT)

zframe=Frame(fileframe)
zframe.pack(side=TOP)
Lz=Label(zframe,text="Range of Z Axis   ")
zstart=Entry(zframe,textvariable=Vz1)
zend=Entry(zframe,textvariable=Vz2)
Lz.pack(side=LEFT)
zstart.pack(side=LEFT)
zend.pack(side=LEFT)


#*********************************************
#===================视频输出==================
#*********************************************





videoframe=Frame(root)
videoframe.pack(side=TOP)

Lvideo=Label(videoframe,text="=========Channel and Video========")
Lvideo.pack(side=TOP)
FPSV=IntVar()
FPSF=Frame(videoframe)
FPSL=Label(FPSF,text="FPS")
FPSE=Entry(FPSF,textvariable=FPSV)
FPSF.pack(side=TOP)
FPSL.pack(side=LEFT)
FPSE.pack(side=LEFT)


#========================================Channel Merging Function==========================================
def grayscale():
#======Getting range=======
    im_dir=Vpath1.get()+"\\"
    name=Vpath2.get()
    getruledata()
    getrangedata()

#=======Merge=========
    for xy in xyrange:
        xy=str(xy).zfill(xy0)
        for z in zrange:
            z=str(z).zfill(z0)
            for t in trange:
                t=str(t).zfill(t0)
                for c in crange:
                    c=str(c).zfill(c0)
                    impath=im_dir+eval(namerule)
                    imgtem = cv2.imread(impath)
                    size = imgtem.shape
                    for i in range(size[0]):
                        for j in range(size[1]):
                            imgtem[i,j] = max(imgtem[i,j][0], imgtem[i,j][1], imgtem[i,j][2])
                    mergepath=namerule.replace("cn","'G'+cn")
                    mergepath=im_dir+eval(mergepath)
                    cv2.imwrite(mergepath,imgtem)


    tkinter.messagebox.showinfo("Done!","Done!")






#========================================Channel Merging Function==========================================
def Merge():
#======Getting range=======
    im_dir=Vpath1.get()+"\\"
    name=Vpath2.get()
    getruledata()
    getrangedata()

#=======Merge=========
    for xy in xyrange:
        xy=str(xy).zfill(xy0)
        for z in zrange:
            z=str(z).zfill(z0)
            for t in trange:
                t=str(t).zfill(t0)
                i=0
                for c in crange:
                    c=str(c).zfill(c0)
                    if i==0:
                        impath=im_dir+eval(namerule)
                        imgtem = cv2.imread(impath)
                    else:
                        impath=im_dir+eval(namerule)
                        imgtem2 = cv2.imread(impath)
                        imgtem =cv2.addWeighted(imgtem,1,imgtem2,1,0)
                    i+=1
                    mergepath=namerule.replace("cn","''")
                    mergepath=mergepath.replace("c","''")
                    mergepath=im_dir+eval(mergepath)

                    cv2.imwrite(mergepath,imgtem)

    tkinter.messagebox.showinfo("Done!","Done!")



#==视频输出函数==
def tvideo():
    global z0,xy0,t0,c0,zn,xyn,tn,cn,namerule,trange,xyrange,crange,zrange
    im_dir=Vpath1.get()+"\\"
    video_dir=Vpath1.get()+"\\"
    name=Vpath2.get()
    getruledata()
    getrangedata()

    for xy in xyrange:
        xy=str(xy).zfill(xy0)
        for z in zrange:
            z=str(z).zfill(z0)
            for c in crange:
                c=str(c).zfill(c0)
                fps = FPSV.get()
                t=int(Vt1.get())
                t=str(t).zfill(t0)
                impath=im_dir+eval(namerule)
                print(impath)
                frame = cv2.imread(impath)
                img_size = (len(frame[0]),len(frame))
                fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
                videopath=namerule.replace("tn","''")
                videopath=videopath.replace("tif","avi")
                videopath=videopath.replace("t","''")
                videopath=im_dir+eval(videopath)
                videoWriter = cv2.VideoWriter(videopath, fourcc, fps, img_size)
                for t in trange:
                    t=str(t).zfill(t0)
                    impath=im_dir+eval(namerule)
                    frame = cv2.imread(impath)
                    videoWriter.write(frame)
                videoWriter.release()
    tkinter.messagebox.showinfo("Done!","Done!")

def zvideo():
    im_dir=Vpath1.get()+"\\"
    video_dir=Vpath1.get()+"\\"
    name=Vpath2.get()
    getruledata()
    getrangedata()
    for xy in xyrange:
        xy=str(xy).zfill(xy0)
        for c in crange:
            c=str(c).zfill(c0)
            fps = FPSV.get()
            for t in trange:
                t=str(t).zfill(z0)
                z=int(Vz1.get())
                z=str(z).zfill(z0)
                impath=im_dir+eval(namerule)
                frame = cv2.imread(impath)
                img_size = (len(frame[0]),len(frame))
                fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
                videopath=namerule.replace("zn","''")
                videopath=videopath.replace("tif","avi")
                videopath=videopath.replace("z","''")
                videopath=im_dir+eval(videopath)
                print(videopath)
                videoWriter = cv2.VideoWriter(videopath, fourcc, fps, img_size)
                for z in zrange:
                    z=str(z).zfill(z0)    
                    impath=im_dir+eval(namerule)
                    frame = cv2.imread(impath)
                    videoWriter.write(frame)
                videoWriter.release()
    tkinter.messagebox.showinfo("Done!","Done!")

VideoBF=Frame(videoframe)
VideoBF.pack(side=TOP)
GrayB=Button(VideoBF,text="Grayscale",command=grayscale)
GrayB.pack(side=LEFT)
MergeB=Button(VideoBF,text="Channel Merging",command=Merge)
MergeB.pack(side=LEFT)
buttontvideo=Button(VideoBF,text="Export Video",command=tvideo)
buttonzvideo=Button(VideoBF,text="Export Z Stack",command=zvideo)
buttontvideo.pack(side=LEFT)
buttonzvideo.pack(side=LEFT)



#*********************************************
#===================图片处理==================
#*********************************************

sx,sy,ex,ey=-1,-1,-1,-1
dsx,dsy,dex,dey=-1,-1,-1,-1
asy,asx,aex,aey=-1,-1,-1,-1


drawing=False

imgL=Label(root,text="=======Images cropping=======")
imgL.pack(side=TOP)
cropargF=Frame(root)
cropargF.pack(side=TOP)

LUF=Frame(cropargF)
LUF.pack(side=TOP)

LUXV=IntVar()
LUXL=Label(LUF,text="Upper Left X")
LUXE=Entry(LUF,textvariable=LUXV)
LUYV=IntVar()
LUYL=Label(LUF,text="Y")
LUYE=Entry(LUF,textvariable=LUYV)

LUXL.pack(side=LEFT)
LUXE.pack(side=LEFT)
LUYL.pack(side=LEFT)
LUYE.pack(side=LEFT)

RDF=Frame(cropargF)
RDF.pack(side=TOP)

RDXV=IntVar()
RDXL=Label(RDF,text="Low Right  X")
RDXE=Entry(RDF,textvariable=RDXV)
RDYV=IntVar()
RDYL=Label(RDF,text="Y")
RDYE=Entry(RDF,textvariable=RDYV)

RDXL.pack(side=LEFT)
RDXE.pack(side=LEFT)
RDYL.pack(side=LEFT)
RDYE.pack(side=LEFT)





#========================================坐标裁剪函数==========================================
def croppos():
#======获取裁剪范围=======
    im_dir=Vpath1.get()+"\\"
    name=Vpath2.get()
    getruledata()
    getrangedata()

#=======执行裁剪=========
    sx=LUXV.get()
    sy=LUYV.get()
    ex=RDXV.get()
    ey=RDYV.get()
    for xy in xyrange:
        xy=str(xy).zfill(xy0)
        for z in zrange:
            z=str(z).zfill(z0)
            for c in crange:
                c=str(c).zfill(c0)
                for t in trange:
                    t=str(t).zfill(t0)
                    impath=im_dir+eval(namerule)
                    imgtem = cv2.imread(impath)
                    imgtem=imgtem[sy:ey,sx:ex]
                    cv2.imwrite(impath,imgtem)
    tkinter.messagebox.showinfo("Done!","Done!")



#========================================绘制裁剪函数==========================================
def cropdraw():
#======绘制裁剪范围=======
    drawing = False # true if mouse is pressed
    im_dir=Vpath1.get()+"\\"
    name=Vpath2.get()
    getruledata()
    getrangedata()
    t=int(Vt1.get())
    z=int(Vz1.get())
    xy=int(Vxy1.get())
    c=int(Vc1.get())
    t=str(t).zfill(t0)
    z=str(z).zfill(z0)
    xy=str(xy).zfill(xy0)
    c=str(c).zfill(c0)
    try:
        impath=im_dir+eval(namerule)
        imgt=cv2.imread(impath)
        size = imgt.shape
    except:
        tkinter.messagebox.showinfo("No such file","No such file, check the rule and all your settings")
    imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
    cv2.imshow('Draw the crop range, press "Enter" to comfirm',imgt)
    def drawrectangle(event,x,y,flags,param):#mouse callback function
        global sx,sy,ex,ey,drawing

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            imgt=cv2.imread(impath)
            size = imgt.shape
            imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
            sx,sy = x,y
            cv2.imshow('Draw the crop range, press "Enter" to comfirm',imgt)


        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                imgt=cv2.imread(impath)
                size = imgt.shape
                imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                cv2.rectangle(imgt,(sx,sy),(x,y),(0,255,0),1)
                cv2.imshow('Draw the crop range, press "Enter" to comfirm',imgt)


        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            imgt=cv2.imread(impath)
            size = imgt.shape
            imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
            ex,ey = x,y
            cv2.rectangle(imgt,(sx,sy),(x,y),(0,255,0),1)
            cv2.imshow('Draw the crop range, press "Enter" to comfirm',imgt)


    cv2.setMouseCallback('Draw the crop range, press "Enter" to comfirm',drawrectangle)

    while(1):
        k = cv2.waitKey(1) & 0xFF
        if k == 13:
            break
    cv2.destroyAllWindows()
#=======执行裁剪=========
    for xy in xyrange:
        xy=str(xy).zfill(xy0)
        for z in zrange:
            z=str(z).zfill(z0)
            for c in crange:
                c=str(c).zfill(c0)
                for t in trange:
                    t=str(t).zfill(t0)
                    impath=im_dir+eval(namerule)
                    imgtem = cv2.imread(impath)
                    imgtem=imgtem[sy*2:ey*2,sx*2:ex*2]
                    cv2.imwrite(impath,imgtem)
    tkinter.messagebox.showinfo("Done!","Done!")

#========================================漂移校正函数==========================================
def driftfix():
    drawing = False # true if mouse is pressed
    im_dir=Vpath1.get()+"\\"
    name=Vpath2.get()
    getruledata()
    getrangedata()
    for xy in xyrange:
        xy=str(xy).zfill(xy0)
        for z in zrange:
            z=str(z).zfill(z0)
            #======绘制裁剪范围=======
            t=int(Vt1.get())
            t=str(t).zfill(t0)
            c=int(Vc1.get())
            c=str(c).zfill(c0)
            try:
                impath=im_dir+eval(namerule)
                imgt=cv2.imread(impath)
                size = imgt.shape
            except:
                tkinter.messagebox.showinfo("No such file","No such file, check the rule and all your settings")
            imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
            cv2.imshow('Draw the crop range, press "Enter" to comfirm',imgt)
            def drawrectangle(event,x,y,flags,param):#mouse callback function
                global sx,sy,ex,ey,drawing

                if event == cv2.EVENT_LBUTTONDOWN:
                    drawing = True
                    imgt=cv2.imread(impath)
                    size = imgt.shape
                    imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                    sx,sy = x,y
                    cv2.imshow('Draw the crop range, press "Enter" to comfirm',imgt)


                elif event == cv2.EVENT_MOUSEMOVE:
                    if drawing == True:
                        imgt=cv2.imread(impath)
                        size = imgt.shape
                        imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                        cv2.rectangle(imgt,(sx,sy),(x,y),(0,255,0),1)
                        cv2.imshow('Draw the crop range, press "Enter" to comfirm',imgt)


                elif event == cv2.EVENT_LBUTTONUP:
                    drawing = False
                    imgt=cv2.imread(impath)
                    size = imgt.shape
                    imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                    ex,ey = x,y
                    cv2.rectangle(imgt,(sx,sy),(x,y),(0,255,0),1)
                    cv2.imshow('Draw the crop range, press "Enter" to comfirm',imgt)


            cv2.setMouseCallback('Draw the crop range, press "Enter" to comfirm',drawrectangle)

            while(1):
                k = cv2.waitKey(1) & 0xFF
                if k == 13:
                    break
            cv2.destroyAllWindows()

            try:
                impath=im_dir+eval(namerule)
                imgt=cv2.imread(impath)
                size = imgt.shape
            except:
                tkinter.messagebox.showinfo("No such file","No such file, check the rule and all your settings")
            imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
            cv2.imshow('click the original position, press "Enter" to comfirm',imgt)
            def drawcircles(event,x,y,flags,param):#mouse callback function
                global dsx,dsy

                if event == cv2.EVENT_LBUTTONUP:
                    imgt=cv2.imread(impath)
                    size = imgt.shape
                    imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                    dsx,dsy = x,y
                    cv2.circle(imgt,(x,y), 3, (0,255,0), 1)
                    cv2.imshow('click the original position, press "Enter" to comfirm',imgt)


            cv2.setMouseCallback('click the original position, press "Enter" to comfirm',drawcircles)

            while(1):
                k = cv2.waitKey(1) & 0xFF
                if k == 13:
                    break
            cv2.destroyAllWindows()


            t=int(Vt2.get())
            t=str(t).zfill(t0)
            impath=im_dir+eval(namerule)
            imgt=cv2.imread(impath)
            size = imgt.shape
            imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
            cv2.imshow('click the corrected position, press "Enter" to comfirm',imgt)
            def drawcircled(event,x,y,flags,param):#mouse callback function
                global dex,dey

                if event == cv2.EVENT_LBUTTONUP:
                    imgt=cv2.imread(impath)
                    size = imgt.shape
                    imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                    dex,dey = x,y
                    cv2.circle(imgt,(x,y), 3, (0,255,0), 1)
                    cv2.imshow('click the corrected position, press "Enter" to comfirm',imgt)


            cv2.setMouseCallback('click the corrected position, press "Enter" to comfirm',drawcircled)

            while(1):
                k = cv2.waitKey(1) & 0xFF
                if k == 13:
                    break
            cv2.destroyAllWindows()
                #=======执行裁剪=========
            for c in crange:
                c=str(c).zfill(c0)
                i=0
                for t in trange:
                    t=str(t).zfill(t0)
                    xd=float(dex-dsx)/(int(Vt2.get())-int(Vt1.get()))
                    yd=float(dey-dsy)/(int(Vt2.get())-int(Vt1.get()))
                    syt,sxt,eyt,ext=int(sy*2+yd*i*2),int(sx*2+xd*i*2),int(ey*2+yd*i*2),int(ex*2+xd*i*2)
                    impath=im_dir+eval(namerule)
                    imgtem = cv2.imread(impath)
                    imgtem=imgtem[syt:eyt,sxt:ext]
                    cv2.imwrite(impath,imgtem)
                    i+=1
    tkinter.messagebox.showinfo("cropping finished","cropping finished")

#========================================旋转漂移校正函数==========================================




def rotatedriftfix():
    drawing = False # true if mouse is pressed
    im_dir=Vpath1.get()+"\\"
    name=Vpath2.get()
    getruledata()
    getrangedata()
    for xy in xyrange:
        xy=str(xy).zfill(xy0)
        for z in zrange:
            z=str(z).zfill(z0)
            #======绘制裁剪范围=======
            t=int(Vt1.get())
            t=str(t).zfill(t0)
            c=int(Vc1.get())
            c=str(c).zfill(c0)
            try:
                impath=im_dir+eval(namerule)
                imgt=cv2.imread(impath)
                size = imgt.shape
            except:
                tkinter.messagebox.showinfo("No such file","No such file, check the rule and all your settings")
            imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
            cv2.imshow('Draw the crop range, press "Enter" to comfirm',imgt)
            def drawrectangle(event,x,y,flags,param):#mouse callback function
                global sx,sy,ex,ey,drawing

                if event == cv2.EVENT_LBUTTONDOWN:
                    drawing = True
                    imgt=cv2.imread(impath)
                    size = imgt.shape
                    imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                    sx,sy = x,y
                    cv2.imshow('Draw the crop range, press "Enter" to comfirm',imgt)


                elif event == cv2.EVENT_MOUSEMOVE:
                    if drawing == True:
                        imgt=cv2.imread(impath)
                        size = imgt.shape
                        imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                        cv2.rectangle(imgt,(sx,sy),(x,y),(0,255,0),1)
                        cv2.imshow('Draw the crop range, press "Enter" to comfirm',imgt)


                elif event == cv2.EVENT_LBUTTONUP:
                    drawing = False
                    imgt=cv2.imread(impath)
                    size = imgt.shape
                    imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                    ex,ey = x,y
                    cv2.rectangle(imgt,(sx,sy),(x,y),(0,255,0),1)
                    cv2.imshow('Draw the crop range, press "Enter" to comfirm',imgt)


            cv2.setMouseCallback('Draw the crop range, press "Enter" to comfirm',drawrectangle)

            while(1):
                k = cv2.waitKey(1) & 0xFF
                if k == 13:
                    break
            cv2.destroyAllWindows()

            try:
                impath=im_dir+eval(namerule)
                imgt=cv2.imread(impath)
                size = imgt.shape
            except:
                tkinter.messagebox.showinfo("No such file","No such file, check the rule and all your settings")
            imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
            cv2.imshow('Draw the original line, press "Enter" to comfirm',imgt)
            
            def drawlineS(event,x,y,flags,param):#mouse callback function
                global dsx,dsy,asy,asx,drawing

                if event == cv2.EVENT_LBUTTONDOWN:
                    drawing = True
                    imgt=cv2.imread(impath)
                    size = imgt.shape
                    imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                    dsx,dsy = x,y
                    cv2.imshow('Draw the original line, press "Enter" to comfirm',imgt)


                elif event == cv2.EVENT_MOUSEMOVE:
                    if drawing == True:
                        imgt=cv2.imread(impath)
                        size = imgt.shape
                        imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                        cv2.line(imgt,(dsx,dsy),(x,y),(255,255,255),1)
                        cv2.imshow('Draw the original line, press "Enter" to comfirm',imgt)


                elif event == cv2.EVENT_LBUTTONUP:
                    drawing = False
                    imgt=cv2.imread(impath)
                    size = imgt.shape
                    imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                    asx,asy = x,y
                    cv2.line(imgt,(dsx,dsy),(x,y),(255,255,255),1)
                    cv2.imshow('Draw the original line, press "Enter" to comfirm',imgt)


            cv2.setMouseCallback('Draw the original line, press "Enter" to comfirm',drawlineS)

            while(1):
                k = cv2.waitKey(1) & 0xFF
                if k == 13:
                    break
            cv2.destroyAllWindows()


            t=int(Vt2.get())
            t=str(t).zfill(t0)
            impath=im_dir+eval(namerule)
            imgt=cv2.imread(impath)
            size = imgt.shape
            imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
            cv2.imshow('Draw the rotated line, press "Enter" to comfirm',imgt)
            
            def drawlineE(event,x,y,flags,param):#mouse callback function
                global dex,dey,aex,aey,drawing

                if event == cv2.EVENT_LBUTTONDOWN:
                    drawing = True
                    imgt=cv2.imread(impath)
                    size = imgt.shape
                    imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                    dex,dey = x,y
                    cv2.imshow('Draw the rotated line, press "Enter" to comfirm',imgt)


                elif event == cv2.EVENT_MOUSEMOVE:
                    if drawing == True:
                        imgt=cv2.imread(impath)
                        size = imgt.shape
                        imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                        cv2.line(imgt,(dex,dey),(x,y),(255,255,255),1)
                        cv2.imshow('Draw the rotated line, press "Enter" to comfirm',imgt)


                elif event == cv2.EVENT_LBUTTONUP:
                    drawing = False
                    imgt=cv2.imread(impath)
                    size = imgt.shape
                    imgt = cv2.resize(imgt,(int(size[1]/2),int(size[0]/2)),cv2.INTER_LINEAR)
                    aex,aey = x,y
                    cv2.line(imgt,(dex,dey),(x,y),(255,255,255),1)
                    cv2.imshow('Draw the rotated line, press "Enter" to comfirm',imgt)


            cv2.setMouseCallback('Draw the rotated line, press "Enter" to comfirm',drawlineE)

            while(1):
                k = cv2.waitKey(1) & 0xFF
                if k == 13:
                    break
            cv2.destroyAllWindows()
                #=======执行裁剪=========
            def rotate(image, angle, center=None, scale=1.0):
                (h, w) = image.shape[:2] 
                if center is None:
                    center = (w//2, h//2)
                M=cv2.getRotationMatrix2D(center,angle,scale)
                rotated=cv2.warpAffine(image,M,(w, h))
                return rotated
            for c in crange:
                c=str(c).zfill(c0)
                i=0
                for t in trange:
                    t=str(t).zfill(t0)
                    xd=float(dex-dsx)/(int(Vt2.get())-int(Vt1.get()))
                    yd=float(dey-dsy)/(int(Vt2.get())-int(Vt1.get()))
                    syt,sxt,eyt,ext=int(sy*2+yd*i*2),int(sx*2+xd*i*2),int(ey*2+yd*i*2),int(ex*2+xd*i*2)
                    dsxt,dsyt=int(dsy*2+yd*i*2),int(dsx*2+xd*i*2)
                    def getangle(x,y):
                        if y>0:
                            return math.degrees(math.acos(x/((x*x+y*y)**(0.5))))
                        else:
                            return math.degrees(math.pi+math.acos(x/((x*x+y*y)**(0.5))))

                    dangle=(getangle(asx-dsx,asy-dsy)-getangle(aex-dex,aey-dey))/(int(Vt2.get())-int(Vt1.get()))
                    print(dangle)
                    dsyt,dsxt=int(dsy*2+yd*i*2),int(dsx*2+xd*i*2)
                    anglet=dangle*i
                    impath=im_dir+eval(namerule)
                    imgtem = cv2.imread(impath)
                    imgtem=rotate(imgtem, anglet, center=(dsxt,dsyt))
                    imgtem=imgtem[syt:eyt,sxt:ext]
                    cv2.imwrite(impath,imgtem)
                    i+=1
    tkinter.messagebox.showinfo("cropping finished","cropping finished")


#========================================按钮区==========================================



cropF=Frame(root)
cropF.pack(side=TOP)


cropposB=Button(cropF,text="Position cropping",command=croppos)
cropposB.pack(side=LEFT)
cropdrawB=Button(cropF,text="Drawing cropping",command=cropdraw)
cropdrawB.pack(side=LEFT)
driftB=Button(cropF,text="Drift Fix",command=driftfix)
driftB.pack(side=LEFT)
driftRB=Button(cropF,text="Rotation and Drift Fix",command=rotatedriftfix)
driftRB.pack(side=LEFT)

#*********************************************
#==================添加信息==================
#*********************************************


imgL=Label(root,text="=======Information Addition=======")
imgL.pack(side=TOP)

#========================================添加时间==========================================
timeF=Frame(root)
timeF.pack(side=TOP)
timeSV=StringVar()
timeDV=StringVar()
timeUV=StringVar()
timeL=Label(timeF,text="start                          interval                           unit")
timeEF=Frame(timeF)
timeSE=Entry(timeEF,textvariable=timeSV)
timeDE=Entry(timeEF,textvariable=timeDV)
timeUE=Entry(timeEF,textvariable=timeUV)
timeL.pack(side=TOP)
timeEF.pack(side=TOP)
timeSE.pack(side=LEFT)
timeDE.pack(side=LEFT)
timeUE.pack(side=LEFT)


def addtime():
    im_dir=Vpath1.get()+"\\"
    name=Vpath2.get()
    getruledata()
    getrangedata()
    for xy in xyrange:
        xy=str(xy).zfill(xy0)
        for z in zrange:
            z=str(z).zfill(z0)
            t=int(Vt1.get())
            t=str(t).zfill(t0)
            c=int(Vc1.get())
            c=str(c).zfill(c0)

            impath=im_dir+eval(namerule)
            imgt=cv2.imread(impath)
            cv2.imshow('click the corrected position, press "Enter" to comfirm',imgt)
            def writetime(event,x,y,flags,param):#mouse callback function
                global dsx,dsy

                if event == cv2.EVENT_LBUTTONUP:
                    imgt=cv2.imread(impath)
                    dsx,dsy = x,y
                    cv2img = cv2.cvtColor(imgt, cv2.COLOR_BGR2RGB)
                    pilimg = Image.fromarray(cv2img)
                    draw = ImageDraw.Draw(pilimg)
                    font = ImageFont.truetype(os.curdir+os.sep+"Arial.ttf", 24, encoding="utf-8")
                    draw.text((dsx,dsy), timeSV.get()+timeUV.get(), (255,255,255), font=font)
                    imgt = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
                    cv2.imshow('click the corrected position, press "Enter" to comfirm',imgt)


            cv2.setMouseCallback('click the corrected position, press "Enter" to comfirm',writetime)
            while(1):
                k = cv2.waitKey(1) & 0xFF
                if k == 13:
                    break
            cv2.destroyAllWindows()

            for c in crange:
                c=str(c).zfill(c0)
                i=int(timeSV.get())
                for t in trange:
                    t=str(t).zfill(t0)
                    impath=im_dir+eval(namerule)
                    imgtem = cv2.imread(impath)
                    cv2img = cv2.cvtColor(imgtem, cv2.COLOR_BGR2RGB)
                    pilimg = Image.fromarray(cv2img)
                    draw = ImageDraw.Draw(pilimg)
                    font = ImageFont.truetype(os.curdir+os.sep+"Arial.ttf", 24, encoding="utf-8")
                    draw.text((dsx,dsy), str(i)+timeUV.get(), (255,255,255), font=font)
                    imgtem = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
                    cv2.imwrite(impath,imgtem)
                    i+=int(timeDV.get())
    
timeB=Button(timeF,text="Time scale",command=addtime)
timeB.pack(side=TOP)


#========================================添加标尺==========================================
scaleplateF=Frame(root)
scaleplateF.pack(side=TOP)
scaleplateSV=StringVar()
scaleplateDV=StringVar()
scaleplateUV=StringVar()
scaleplateL=Label(scaleplateF,text="length                       length per pixel                        unit")
scaleplateEF=Frame(scaleplateF)
scaleplateSE=Entry(scaleplateEF,textvariable=scaleplateSV)
scaleplateDE=Entry(scaleplateEF,textvariable=scaleplateDV)
scaleplateUE=Entry(scaleplateEF,textvariable=scaleplateUV)
scaleplateL.pack(side=TOP)
scaleplateEF.pack(side=TOP)
scaleplateSE.pack(side=LEFT)
scaleplateDE.pack(side=LEFT)
scaleplateUE.pack(side=LEFT)


def addscaleplate():
    im_dir=Vpath1.get()+"\\"
    name=Vpath2.get()
    getruledata()
    getrangedata()
    for xy in xyrange:
        xy=str(xy).zfill(xy0)
        for z in zrange:
            z=str(z).zfill(z0)

            t=int(Vt1.get())
            t=str(t).zfill(t0)
            c=int(Vc1.get())
            c=str(c).zfill(c0)

            plen=int(float(scaleplateSE.get())/float(scaleplateDE.get()))


            impath=im_dir+eval(namerule)
            imgt=cv2.imread(impath)
            cv2.imshow('click the corrected position, press "Enter" to comfirm',imgt)
            def writescaleplate(event,x,y,flags,param):#mouse callback function
                global dsx,dsy

                if event == cv2.EVENT_LBUTTONUP:
                    imgt=cv2.imread(impath)
                    dsx,dsy = x,y
                    cv2img = cv2.cvtColor(imgt, cv2.COLOR_BGR2RGB)
                    pilimg = Image.fromarray(cv2img)
                    draw = ImageDraw.Draw(pilimg)
                    font = ImageFont.truetype(os.curdir+os.sep+"Arial.ttf", 20, encoding="utf-8")
                    draw.text((dsx,dsy+6), scaleplateSV.get()+scaleplateUV.get(), (255,255,255), font=font)
                    imgt = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
                    cv2.line(imgt,(dsx,dsy),(dsx+plen,dsy),(255,255,255),3)
                    cv2.imshow('click the corrected position, press "Enter" to comfirm',imgt)


            cv2.setMouseCallback('click the corrected position, press "Enter" to comfirm',writescaleplate)
            while(1):
                k = cv2.waitKey(1) & 0xFF
                if k == 13:
                    break
            cv2.destroyAllWindows()

            for c in crange:
                c=str(c).zfill(c0)
                for t in trange:
                    t=str(t).zfill(t0)
                    impath=im_dir+eval(namerule)
                    imgt = cv2.imread(impath)
                    cv2img = cv2.cvtColor(imgt, cv2.COLOR_BGR2RGB)
                    pilimg = Image.fromarray(cv2img)
                    draw = ImageDraw.Draw(pilimg)
                    font = ImageFont.truetype(os.curdir+os.sep+"Arial.ttf", 20, encoding="utf-8")
                    draw.text((dsx,dsy+6), scaleplateSV.get()+scaleplateUV.get(), (255,255,255), font=font)
                    imgt = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
                    cv2.line(imgt,(dsx,dsy),(dsx+plen,dsy),(255,255,255),3)
                    cv2.imwrite(impath,imgt)

    
scaleplateB=Button(scaleplateF,text="Scaleplate",command=addscaleplate)
scaleplateB.pack(side=TOP)




#cv2.destroyWindow()

#*********************************************
#==================窗口控制==================
#*********************************************

def iconifyroot():
    root.overrideredirect(False)
    root.iconify()
windowlabel=Label(root,text="=========Window========")
windowlabel.pack(side=TOP)
windowsframe=Frame(root)
windowsframe.pack(side=TOP)
quitbutton=Button(windowsframe,text="Minimize",command=iconifyroot)
quitbutton.pack(side=LEFT)
quitbutton=Button(windowsframe,text="Exit",command=root.quit)
quitbutton.pack(side=LEFT)

mainloop()
