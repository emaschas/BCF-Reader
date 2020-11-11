from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import xml.etree.ElementTree as XML
from datetime import datetime
from BCFclass import *

backref = {}

def tvselect(event):
  global tv
  sel = tv.selection()
  for item in sel:
    if item[0:3] == "Top":
      i = backref[item]
      display_topic(i)
    else:
      j = backref[item]
      parent = tv.parent(item)
      i = backref[parent]
      display_comment(i, j)
  #next
  
def display_topic(i):
  global bcf, im, image
  if len(bcf.Topics)==0:
    TopicGUID.set("No topic found in this file")
    return
  #endif
  topic = bcf.Topics[i]
  Details.set(str(topic))
  image = None
  if len(topic.Viewpoints) != 0:
    vpt = topic.Viewpoints[0]
    snapshot = topic.Guid + "/" + vpt.Snapshot
    snapdata = bcf.getImage(snapshot)
    if snapdata != None :
      imgobj = PhotoImage(data=snapdata)
      w = imgobj.width()
      h = imgobj.height()
      zw = int(w / 290 + 0.9)
      zh = int(h / 290 + 0.9)
      zoom = zh if zh > zw else zw
      image = imgobj.subsample(zoom,zoom)
      im.create_image(145, 145, image=image)
  #endif
#enddef display_topic

def display_comment(i, j):
  global bcf, im, image
  if len(bcf.Topics)==0:
    TopicGUID.set("No topic found in this file")
    return
  #endif
  topic = bcf.Topics[i]
  comment = topic.Comments[j]
  Details.set(str(comment))
  image = None
  snapshot = "-"
  if comment.Viewpoint != "-":
    vpguid = comment.Viewpoint
    for vp in topic.Viewpoints:
      if vp.Guid == vpguid:
        snapshot = topic.Guid + "/" + vp.Snapshot
  elif len(topic.Viewpoints) != 0:
    vpt = topic.Viewpoints[0]
    snapshot = topic.Guid + "/" + vpt.Snapshot
  if snapshot != "-":
    snapdata = bcf.getImage(snapshot)
    if snapdata != None :
      imgobj = PhotoImage(data=snapdata)
      w = imgobj.width()
      h = imgobj.height()
      zw = int(w / 290 + 0.9)
      zh = int(h / 290 + 0.9)
      zoom = zh if zh > zw else zw
      image = imgobj.subsample(zoom,zoom)
      im.create_image(145, 145, image=image)
  #endif
#enddef display_topic


#----------------- MAIN -----------------

root = Tk()
root.title("BCF Reader")
root.geometry("1000x600")
root.resizable(0,0)
#root.bind("<MouseWheel>", eventWheel)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)

ftv = Frame(root, width=990, height = 290)
ftv.place(x=5, y=5)
tv = ttk.Treeview(ftv, selectmode=BROWSE)
tv.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
tv['columns'] = ("Da", "Au", "St", "Ty", "Vp")
tv.column("#0", width=300, minwidth=100)
tv.column("Da", width=60,  minwidth= 50, anchor="center")
tv.column("Au", width=150, minwidth=100)
tv.column("St", width=60,  minwidth= 50, anchor="center")
tv.column("Ty", width=80,  minwidth= 50, anchor="center")
tv.column("Vp", width=50,  minwidth= 30, anchor="center")
tv.heading("#0", text="Title",  anchor=W)
tv.heading("Da", text="Date")
tv.heading("Au", text="Author", anchor=W)
tv.heading("St", text="Status")
tv.heading("Ty", text="Type")
tv.heading("Vp", text="View")
tv.bind("<<TreeviewSelect>>", tvselect)

Details = StringVar()
flb = Frame(root, width=690, height=290)
flb.place(x=5, y=305)
lb = Label(flb, justify=LEFT, textvariable=Details, relief="groove", borderwidth=2, anchor=NW, font=("Consolas", 10))
lb.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

fim = Frame(root, width=294, height=294)
fim.place(x=703, y=303)
im = Canvas(fim, relief="groove", borderwidth=2)
im.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
#dessin.bind("<Button-1>", eventNext)
#dessin.bind("<Button-3>", eventPrev)

#--------------------------------------------------------------------------------------------------

filename = filedialog.askopenfilename(
  initialdir = ".",
  title = "Select BCF file",
  filetypes = (("BCF Zip Files","*.bcfzip"), ("BCF Files","*.bcf"), ("All Files","*.*")) )
if filename != "":
  root.title("BCF Reader - " + filename)
  bcf = BCFfile(filename)
  for i in range(len(bcf.Topics)):
    top = bcf.Topics[i]
    try: dat = top.CreationDate.strftime("%d-%m-%Y")
    except: dat = "-"
    nbvp = str(len(top.Viewpoints))
    tv.insert("", "end", "Top="+top.Guid, text=top.Title, values=(dat, top.CreationAuthor, top.TopicStatus, top.TopicType, nbvp), open=True)
    backref["Top="+top.Guid] = i
    for j in range(len(top.Comments)):
      com = top.Comments[j]
      txt = com.Comment
      if txt == None: txt = "-"
      try: dat = com.Date.strftime("%d-%m-%Y")
      except: dat = "-"
      nbvp = 0 if com.Viewpoint == "-" else 1
      tv.insert("Top="+top.Guid, "end", "Com="+com.Guid, text=txt, values=(dat, com.Author, "-", "-", nbvp))
      backref["Com="+com.Guid] = j
  display_topic(0)
  root.mainloop()
#endif