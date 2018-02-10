class Packet_In:

    def __init__(self, bgtime, dstport, srcip, dstip):

      self.bgtime = bgtime
      self.dstport = dstport
      self.srcip = srcip
      self.dstip = dstip

    def get_bgtime(self):
      return self.bgtime

    def get_dstport(self):
      return self.dstport

    def get_srcip(self):
      return self.srcip

    def get_dstip(self):
      return self.dstip    
