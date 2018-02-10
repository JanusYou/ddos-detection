from detect_list import detect_list
import detect_node

def detect(newnode, newtime):
  
  flag = 1
  
  detect_list.expire(newtime)

  ###
  srcip_En_line = detect_list.get_sip_average() + detect_list.get_sip_stde() 
  
  if newnode.get_sipEn > srcip_En_line:

    flag = 0

  ###
  dstip_En_line = detect_list.get_dip_average() - 2*detect_list.get_dip_stde()
  if newnode.get_dipEn < dstip_En_line:

    flag = 0

  ###
  dstport_En_line = detect_list.get_port_average() - 2*detect_list.get_port_stde()
  if newnode.get_portEn < dstport_En_line:

    flag = 0


  return flag
