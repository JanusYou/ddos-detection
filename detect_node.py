class DetNode:

    def __init__(self, bgtime, pacIn_list):

      self.pacIn_list = pacIn_list
      self.bgtime = bgtime
      self.benodes = 0
      self.afnodes = 0

    def get_velocity(self):

      number = len(self.pacIn_list)
      s_time = self.pacIn_list[0]
      e_time = self.pacIn_list[number-1]
      interval = e_time - s_time
      v = number/interval

      return v 


    def get_sipEn(self):

      

    def get_portEn(self):


    def get_dipEn(self):


    def get_beNodes():


    def get_afNodes():

    def append_beNodes(self):
      self.benodes = self.benodes + 1

    def append_afNodes(self):
      self.afnodes = self.afnodes + 1

    def del_beNodes(self):
      self.benodes = self.benodes - 1

    def del_afNodes(self):
      self.afnodes = self.afnodes - 1 
