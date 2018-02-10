import math
import numpy

class detect_list:


    def __init__(self, nodelist, extime):

      self.nodelist = nodelist
      self.extime = extime


    def expire(self, newtime):
  
      for node in self.nodelist:
        pnode = node
        if (newtime - node.bgtime) > self.extime:
          self.nodelist.remove(node)
          for node in self.nodelist:

            if math.abs(pnode.get_velocity() - node.get_velocity()) < R:


                 node.del_beNodes()

    def get_sip_average(self):
      
      number = len(self.nodelist)
      sum = 0
      for node in self.nodelist:
        sum = sum + node.get_sipEn()

      return sum/number

    def get_sip_stde(self):

      aver = get_sip_average()
      ssum = 0
      l = len(self.nodelist)
      for node in self.nodelist:
        ssum = ssum + numpy.square(aver - node.get_sipEn())

      return math.sqrt(ssum/l)

    def get_port_average(self):

      number = len(self.nodelist)
      sum = 0
      for node in self.nodelist:
        sum = sum + node.get_portEn()

      return sum/number


    def get_port_stde(self):

      aver = get_port_average()
      ssum = 0
      l = len(self.nodelist)
      for node in self.nodelist:
        ssum = ssum + numpy.square(aver - node.get_portEn())

      return math.sqrt(ssum/l)


    def get_dip_average(self):

      number = len(self.nodelist)
      sum = 0
      for node in self.nodelist:
        sum = sum + node.get_dipEn()

      return sum/number


    def get_dip_stde(self):

      aver = get_dip_average()
      ssum = 0
      l = len(self.nodelist)
      for node in self.nodelist:
        ssum = ssum + numpy.square(aver - node.get_dipEn())

      return math.sqrt(ssum/l)
