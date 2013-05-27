from __future__ import with_statement
import nef

from pymorse import Morse

def is_mouse_visible(semantic_camera_stream):
    """ Read data from the semantic camera, and determine if a specific
    object is within the field of view of the robot """
    data = semantic_camera_stream.get()
    visible_objects = data['visible_objects']
    for visible_object in visible_objects:
        if visible_object['name'] == "MOUSE":
            return True
    return False

def main():
    """ Use the semantic cameras to locate the target and follow it """
    
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
    


    with Morse() as morse:
        semanticL = morse.cat.semanticL
        semanticR = morse.cat.semanticR
        motion = morse.cat.motion

        dt = 0.001

        while True:
            mouse_seen_left = is_mouse_visible(semanticL)
            mouse_seen_right = is_mouse_visible(semanticR)
            
            L.functions[0].value=(1 if mouse_seen_left else 0)
            R.functions[0].value=(1 if mouse_seen_right else 0)

            V = move.getOrigin('X').getValues().getValues()[0]
            W = move.getOrigin('X').getValues().getValues()[1]

            """

            if mouse_seen_left and mouse_seen_right:
                v_w = {"v": 2, "w": 0}
            elif mouse_seen_left:
                v_w = {"v": 1.5, "w": 1}
            elif mouse_seen_right:
                v_w = {"v": 1.5, "w": -1}
            else:
                v_w = {"v": 0, "w": -1}
        
            """

            v_w = {"v": V, "w": W}

            motion.publish(v_w)
            yield dt

main()
