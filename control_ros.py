import nef
#import rospy
#from std_msgs.msg import String
#from geometry_msgs.msg import Twist

try:
  import rospy
except ImportError:
  # TEMP - horrible hack to get rospy to work with nengo
  import sys
  #sys.path.append('/opt/ros/fuerte/share')
  sys.path.append('/opt/ros/fuerte/lib/python2.7/dist-packages/ros_comm-1.8.15-py2.7.egg')
  import rospy

# set up the nengo network
net=nef.Network('Cat')
net.add_to_nengo()
# create the input connections, coming from the simulator
net.make_input('semanticL',values=[0])
net.make_input('semanticR',values=[0])

L = net.make('L', neurons=30, dimensions=1) # population for the left semantic camera
R = net.make('R', neurons=30, dimensions=1) # population for the right semantic camera

# controls how the cat will move, the two dimensions represent v and w
move = net.make('move',neurons=200, dimensions=2) 

net.connect('semanticL', 'L')
net.connect('semanticR', 'R')

net.connect('L','move', transform=[[1.3],[1]])
net.connect('R','move', transform=[[1.3],[-1]])

def callbackL(data):
  print(data) # TEMP for now, to see what is in data
  #L.functions[0].value=(1 if mouse_seen_left else 0)

def callbackR(data):
  print(data) # TEMP for now, to see what is in data
  #R.functions[0].value=(1 if mouse_seen_right else 0)

def main():
  pub = rospy.Publisher('cat/motion', Twist)
  r = rospy.Rate(10) # 10 Hz
  rospy.init_node('catbrain', anonymous=True) #?? what does this do?
  rospy.Subscriber('cat/semanticR', String, callbackR)
  rospy.Subscriber('cat/semanticL', String, callbackL)
  while not rospy.is_shutdown():
    V = move.getOrigin('X').getValues().getValues()[0]
    W = move.getOrigin('X').getValues().getValues()[1]
    pub.publish({"v": V, "w": W})
    r.sleep()



if __name__ == '__main__':
  main()
