import detect_list
import detect_node
import List
import math
import List
def trigger(newnode, newtime, R, K):

  detect_list.expire(newtime)

  for node in detect_list:

    if math.abs(newnode.get_velocity() - node.get_velocity()) < R:

      newnode.append_beNodes()
      node.append_afNodes()

  detect_list.append(newnode)
  for node in detect_list:
    
    if ((node.get_beNodes() + node.get_afNodes()) < K) and len(detect_list) > 2*K:
 
      return 0

  return 1
