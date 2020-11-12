'''
Collection of classes for BCF file reader.

The main class is BCFfile that reads a *.bcfzip file content.

Emmanuel Maschas - November 2020
'''

import os
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
  def __init__(self):
    self.Guid           = ""
    self.Date           = None
    self.Author         = ""
    self.Comment        = ""
    self.Viewpoint      = ""
    self.ModifiedDate   = None
    self.ModifiedAuthor = ""

  def __repr__(self):
    txt  = "COMMENT :\n========="
    #txt += "\nGuid :           " + self.Guid
    if self.Date != None:
      txt += "\nDate :           " + self.Date.strftime("%d-%m-%Y")
    else:
      txt += "\nDate :           -"
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
  def __init__(self):
    self.Guid = ""
    self.TopicType = ""
    self.TopicStatus = ""
    self.Title = ""
    self.Priority = ""
    self.Index = ""
    self.Labels = ""
    self.CreationAuthor = ""
    self.CreationDate = None
    self.ModifiedAuthor = ""
    self.ModifiedDate = None
    self.DueDate = None
    self.AssignedTo = ""
    self.Description = ""
    self.Stage = ""
    self.ReferenceLink = ""
    self.Comments = []
    self.Viewpoints = []

  def __repr__(self):
    txt  = "TOPIC :\n======="
    #txt += "\nGuid :           " + self.Guid
    txt += "\nTopicType :      " + self.TopicType
    txt += "\nTopicStatus :    " + self.TopicStatus
    txt += "\nTitle :          " + self.Title
    txt += "\nDescription :    " + self.Description
    if self.Priority != "-":   txt += "\nPriority :       " + self.Priority
    txt += "\nIndex :          " + self.Index
    if self.CreationDate != None:
      txt += "\nCreationDate :   " + self.CreationDate.strftime("%d-%m-%Y")
    else: # Should not happen...
      txt += "\nCreationDate :   -"
    txt += "\nCreationAuthor : " + self.CreationAuthor
    if self.ModifiedDate != None and (self.ModifiedDate != self.CreationDate or self.ModifiedAuthor != self.CreationAuthor) :
      txt += "\nModifiedDate :   " + self.ModifiedDate.strftime("%d-%m-%Y")
      txt += "\nModifiedAuthor : " + self.ModifiedAuthor
    if self.AssignedTo != "-": txt += "\nAssignedTo :     " + self.AssignedTo
    if self.DueDate != None:   txt += "\nDueDate :        " + self.DueDate
    if self.Stage != "-":      txt += "\nStage :          " + self.Stage
    return txt

  def index(self):
    """
    Function that returns the Index of the comment as a sort key
    """
    try: res = int(self.Index)
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
    self.Index          = getXMLtext(node, "Index")
    self.Labels         = getXMLtext(node, "Labels")
    self.CreationAuthor = getXMLtext(node, "CreationAuthor")
    self.CreationDate   = getXMLdate(node, "CreationDate")
    self.ModifiedAuthor = getXMLtext(node, "ModifiedAuthor")
    self.ModifiedDate   = getXMLdate(node, "ModifiedDate")
    self.DueDate        = getXMLdate(node, "DueDate")
    self.AssignedTo     = getXMLtext(node, "AssignedTo")
    self.Description    = getXMLtext(node, "Description")
    self.Stage          = getXMLtext(node, "Stage")
    self.ReferenceLink  = getXMLtext(node, "ReferenceLink")

class BCFviewpoint:
  def __init__(self):
    self.Guid            = ""
    self.Viewpoint       = ""
    self.Snapshot        = ""
    self.ViewIndex       = ""
    self.CameraViewPoint = (0.0, 0.0, 0.0)
    self.CameraDirection = (0.0, 1.0, 0.0)
    self.CameraUpVector  = (0.0, 0.0, 1.0)
    self.FieldOfView     = 60.0

  def __repr__(self):
    txt  = "VIEWPOINT :\n==========="
    #txt += "\nGuid :      " + self.Guid
    txt += "\nViewpoint :      " + self.Viewpoint
    txt += "\nSnapshot :       " + self.Snapshot
    txt += "\nIndex :          " + self.ViewIndex
    txt += "\nCameraViewPoint : X=%.3f Y=%.3f Z=%.3f" % self.CameraViewPoint
    txt += "\nCameraDirection : X=%.3f Y=%.3f Z=%.3f" % self.CameraDirection
    txt += "\nCameraUpVector  : X=%.3f Y=%.3f Z=%.3f" % self.CameraUpVector
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
    self.filename = filename
    self.Topics = []
    self.bcfzip = None
    if os.path.exists(filename):
      if os.path.isfile(filename):
        self.bcfzip = zipfile.ZipFile(filename)
        self.read()

  def __repr__(self):
    txt  = "BCF FILE\n========"
    txt += "\nFile name :      " + self.filename
    for topic in self.Topics:
      txt += "\n\n" + str(topic)
      for comment in topic.Comments:
        txt += "\n\n" + str(comment)
    txt += "\n\n--------"
    return txt

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
