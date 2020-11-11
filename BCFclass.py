import zipfile
import xml.etree.ElementTree as XML
from datetime import datetime

def getXMLtext(node, name):
  """
  Read an XML node text and returns it or "-" if the node does not exist
  """ 
  try: res = node.find(name).text
  except: res = "-"
  if res == None: res = "-"
  return res

def getXMLdate(node, name):
  """
  Read an XML node text containing an ISO date and returns it or None if the node does not exist
  """ 
  try: res = datetime.fromisoformat(node.find(name).text[:19])
  except: res = None
  return res

def getXMLattr(node, name):
  """
  Read an XML node attribute and returns it or "-" if the attribute does not exist
  """
  try: res = node.get(name)
  except: res = "-"
  if res == None: res = "-"
  return res

class BCFcomment:
  def __init__(self, Guid="", Date=None, Author="", Comment="", Viewpoint="", ModifiedDate=None, ModifiedAuthor=""):
    self.Guid = Guid
    self.Date = Date
    self.Author = Author
    self.Comment = Comment
    self.Viewpoint = Viewpoint
    self.ModifiedDate = ModifiedDate
    self.ModifiedAuthor = ModifiedAuthor

  def __str__(self):
    txt  = "COMMENT :\n========="
    #txt += "\nGuid :           " + self.Guid
    if self.Date != None:
      txt += "\nDate :           " + self.Date.strftime("%d-%m-%Y")
    else:
      txt += "\nDate :            -"
    txt += "\nAuthor :         " + self.Author
    if self.ModifiedDate != None and (self.ModifiedDate != self.Date or self.ModifiedAuthor != self.Author) :
      txt += "\nModifiedDate :   " + self.ModifiedDate.strftime("%d-%m-%Y")
      txt += "\nModifiedAuthor : " + self.ModifiedAuthor
    txt += "\nComment :        " + self.Comment 
    if self.Viewpoint!="-": txt += "\nViewpoint :      " + self.Viewpoint
    return txt

  def index(self):
    """
    Function that returns the Date of the comment as a sort key
    """
    try: res = int(self.Date.strftime("%Y%m%d%H%M%S"))
    except: res = "0000"
    return res

  def read(self, node):
    """
    Read BCF Comment from an XML node
    """
    self.Guid           = getXMLattr(node, "Guid")
    self.Date           = getXMLdate(node, "Date")
    self.Author         = getXMLtext(node, "Author")
    self.Comment        = getXMLtext(node, "Comment")
    self.ModifiedDate   = getXMLdate(node, "ModifiedDate")
    self.ModifiedAuthor = getXMLtext(node, "ModifiedAuthor")
    self.Viewpoint      = getXMLattr(node.find("Viewpoint"), "Guid")

class BCFtopic:
  def __init__(self, Guid="", TopicType="", TopicStatus="", Title="", Priority="", TopicIndex="", CreationDate=None, CreationAuthor="", ModifiedDate=None, ModifiedAuthor="", Stage="", Description=""):
    self.Guid = Guid
    self.TopicType = TopicType
    self.TopicStatus = TopicStatus
    self.Title = Title
    self.Priority = Priority
    self.TopicIndex = TopicIndex
    self.CreationDate = CreationDate
    self.CreationAuthor = CreationAuthor
    self.ModifiedDate = ModifiedDate
    self.ModifiedAuthor = ModifiedAuthor
    self.Stage = Stage
    self.Description = Description
    self.Comments = []
    self.Viewpoints = []

  def __str__(self):
    txt  = "TOPIC :\n======="
    #txt += "\nGuid :           " + self.Guid
    txt += "\nTopicType :      " + self.TopicType
    txt += "\nTopicStatus :    " + self.TopicStatus
    txt += "\nTitle :          " + self.Title
    if self.Priority!="-": txt += "\nPriority :       " + self.Priority
    txt += "\nIndex :          " + self.TopicIndex
    if self.CreationDate != None:
      txt += "\nCreationDate :   " + self.CreationDate.strftime("%d-%m-%Y")
    else:
      txt += "\nCreationDate :    -"
    txt += "\nCreationAuthor : " + self.CreationAuthor
    if self.ModifiedDate != None and (self.ModifiedDate != self.CreationDate or self.ModifiedAuthor != self.CreationAuthor) :
      txt += "\nModifiedDate :   " + self.ModifiedDate.strftime("%d-%m-%Y")
      txt += "\nModifiedAuthor : " + self.ModifiedAuthor
    if self.Stage!="-": txt += "\nStage :          " + self.Stage
    txt += "\nDescription :    " + self.Description
    return txt

  def index(self):
    """
    Function that returns the TopicIndex of the comment as a sort key
    """
    try: res = int(self.TopicIndex)
    except: res = 0
    return res

  def addComment(self, comment):
    """
    Append the "BCFcomment" to the topic's Comments list
    """ 
    self.Comments.append(comment)

  def addViewpoint(self, viewpoint):
    """
    Append the "BCFviewpoint" to the topic's Viewpoints list
    """ 
    self.Viewpoints.append(viewpoint)

  def read(self, node):
    """
    Read a BCF topic from an XML node.
    Includes Comments and Viewpoints.
    """
    self.Guid           = getXMLattr(node, "Guid")
    self.TopicType      = getXMLattr(node, "TopicType")
    self.TopicStatus    = getXMLattr(node, "TopicStatus")
    self.Title          = getXMLtext(node, "Title")
    self.Priority       = getXMLtext(node, "Priority")
    self.TopicIndex     = getXMLtext(node, "Index")
    self.CreationDate   = getXMLdate(node, "CreationDate")
    self.CreationAuthor = getXMLtext(node, "CreationAuthor")
    self.ModifiedDate   = getXMLdate(node, "ModifiedDate")
    self.ModifiedAuthor = getXMLtext(node, "ModifiedAuthor")
    self.Stage          = getXMLtext(node, "Stage")
    self.Description    = getXMLtext(node, "Description")

class BCFviewpoint:
  def __init__(self, Guid="", Viewpoint="", Snapshot="", ViewIndex=""):
    self.Guid = Guid
    self.Viewpoint = Viewpoint
    self.Snapshot = Snapshot
    self.ViewIndex = ViewIndex
    self.CameraViewPoint = (0,0,0)
    self.CameraDirection = (0,1,0)
    self.CameraUpVector = (0,0,1)
    self.FieldOfView = 60.0

  def __str__(self):
    txt  = "VIEWPOINT :\n==========="
    #txt += "\nGuid :      " + self.Guid
    txt += "\nViewpoint :      " + self.Viewpoint
    txt += "\nSnapshot :       " + self.Snapshot
    txt += "\nIndex :          " + self.ViewIndex
    txt += "\nCameraViewPoint :" + str(self.CameraViewPoint) 
    return txt

  def index(self):
    """
    Function that returns the Viepoint Index of the comment as a sort key
    """
    try: res = int(self.ViewIndex)
    except: res = 0
    return res

  def read(self, node, bcfzip, directory):
    """
    Read BCF viewpoint from an XML node and the associated .bcfv file
    """
    if node != None :
      self.Guid      = getXMLattr(node, "Guid")
      self.Viewpoint = getXMLtext(node, "Viewpoint")
      self.Snapshot  = getXMLtext(node, "Snapshot")
      self.ViewIndex = getXMLtext(node, "Index")
    else : # no node => try "viewpoint.bcfv" file
      self.Guid      = "-"
      self.Viewpoint = "viewpoint.bcfv"
      self.Snapshot  = "snapshot.png"
      self.ViewIndex = "-"
    try:
      visualisationbcfv = bcfzip.open(directory + self.Viewpoint)
    except:
      self.Guid = None # Empty Viewpoint : file note found...
    else:
      visualisations = XML.fromstring(visualisationbcfv.read())
      camera = visualisations.find("PerspectiveCamera")
      if camera:
        point = camera.find("CameraViewPoint")
        X = point.find("X").text
        Y = point.find("Y").text
        Z = point.find("Z").text
        self.CameraViewPoint = (float(X), float(Y),float(Z))
        point = camera.find("CameraDirection")
        X = point.find("X").text
        Y = point.find("Y").text
        Z = point.find("Z").text
        self.CameraDirection = (float(X), float(Y),float(Z))
        point = camera.find("CameraUpVector")
        X = point.find("X").text
        Y = point.find("Y").text
        Z = point.find("Z").text
        self.FieldOfView = float(camera.find("FieldOfView").text)
      else:
        self.CameraViewPoint = (0.0, 0.0, 0.0)
        self.CameraDirection = (0.0, 1.0, 0.0)
        self.CameraUpVector  = (0.0, 0.0, 1.0)
        self.FieldOfView = 60.0
      visualisationbcfv.close()

class BCFfile:
  def __init__(self, filename=""):
    self.Topics = []
    self.bcfzip = zipfile.ZipFile(filename)
    if filename!="" : self.read()

  def read(self):
    """
    Read the active BCF file
    """
    self.Topics.clear()
    for fi in self.bcfzip.filelist:
      if fi.filename[-10:]=="markup.bcf":
        #print("Markup : ", fi.filename, "\n")
        markupbcf = self.bcfzip.open(fi.filename)
        markup = XML.fromstring(markupbcf.read())
        tnode = markup.find("Topic")
        topic = BCFtopic()
        topic.read(tnode)
        for cnode in markup.findall("Comment"):
          comment = BCFcomment()
          comment.read(cnode)
          topic.addComment(comment)
        topic.Comments.sort(key=BCFcomment.index)
        for vnode in markup.findall("Viewpoints"):
          viewpoint = BCFviewpoint()
          viewpoint.read(vnode, self.bcfzip, fi.filename[:-10])
          if viewpoint.Guid != None : topic.addViewpoint(viewpoint)
        if len(topic.Viewpoints) == 0: # No Viewpoint ? try "viewpoint.bcfv"
          viewpoint = BCFviewpoint()
          viewpoint.read(None, self.bcfzip, fi.filename[:-10])
          if viewpoint.Guid != None : topic.addViewpoint(viewpoint)
        topic.Viewpoints.sort(key=BCFviewpoint.index)
        self.Topics.append(topic)
        markupbcf.close()
      #endif fi is markup.bcf
    #next fi
    self.Topics.sort(key=BCFtopic.index)

  def getImage(self, filename):
    """
    Returns the image data of a snapshot file from the active BCF file
    """
    data = None
    with self.bcfzip.open(filename) as fi:
      data = fi.read()
    return data
