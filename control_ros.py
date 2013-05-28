import numpy as np
from nengo import nef_theano as nef
#import nef
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def is_mouse_visible(semantic_camera_stream):
    """ Read data from the semantic camera, and determine if a specific
    object is within the field of view of the robot """
    #data = semantic_camera_stream.get()
    #visible_objects = data['visible_objects']
    #for visible_object in visible_objects:
    #    if visible_object['name'] == "MOUSE":
    #        return True
    #return False
    if "MOUSE" in str(semantic_camera_stream):
        return True
    return False

# set up the nengo network
net=nef.Network('Cat')
#net.add_to_nengo()
# create the input connections, coming from the simulator
semanticL = net.make_input('semanticL',value=[0])
semanticR = net.make_input('semanticR',value=[0])

L = net.make('L', neurons=30, dimensions=1) # population for the left semantic camera
R = net.make('R', neurons=30, dimensions=1) # population for the right semantic camera

# controls how the cat will move, the two dimensions represent v and w
move = net.make('move',neurons=200, dimensions=2) 

net.connect('semanticL', 'L')
net.connect('semanticR', 'R')

net.connect('L','move', transform=[[1.3],[1]])
net.connect('R','move', transform=[[1.3],[-1]])

def callbackL(data):
  semanticL.origin['X'].decoded_output.set_value(np.float32([(1 if is_mouse_visible(data) else 0)])) 

def callbackR(data):
  semanticR.origin['X'].decoded_output.set_value(np.float32([(1 if is_mouse_visible(data) else 0)])) 

def main():
  rospy.init_node('catbrain', anonymous=True) #?? what does this do?
  pub = rospy.Publisher('cat/motion', Twist)
  r = rospy.Rate(10) # 10 Hz
  rospy.Subscriber('cat/semanticR', String, callbackR)
  rospy.Subscriber('cat/semanticL', String, callbackL)
  while not rospy.is_shutdown():
    V = move.origin['X'].decoded_output.get_value()[0]
    W = move.origin['X'].decoded_output.get_value()[1]
    #print("V: ",V)
    #print("W: ",W)
    twist = Twist()
    twist.linear.x = V
    twist.angular.z = W
    pub.publish( twist )
    net.run(0.01) # TODO: step the right amount of time
    r.sleep()



if __name__ == '__main__':
  main()
#net.view()
