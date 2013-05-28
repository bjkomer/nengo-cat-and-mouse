from morse.builder import *

mouse = ATRV()
mouse.translate(x=1.0, z=0.2)
mouse.properties(Object = True, Graspable = False, Label = "MOUSE")

keyboard = Keyboard()
keyboard.properties(Speed=3.0)
mouse.append(keyboard)

cat = ATRV()
cat.translate(x=-6.0, z=0.2)

semanticL = SemanticCamera()
semanticL.translate(x=0.2, y=0.3, z=0.9)
semanticL.rotate(x=0.25, y=0.0, z=0.0)
semanticL.frequency(frequency=30)
cat.append(semanticL)

semanticR = SemanticCamera()
semanticR.translate(x=0.2, y=-0.3, z=0.9)
semanticR.rotate(x=-0.25, y=0.0, z=0.0)
semanticR.frequency(frequency=30)
cat.append(semanticR)

motion = MotionVW()
cat.append(motion)

motion.add_interface('ros', topic='/cat/motion')
semanticL.add_interface('ros', topic='/cat/semanticL')
semanticR.add_interface('ros', topic='/cat/semanticR')

env = Environment('land-1/trees')
env.place_camera([10.0, -10.0, 10.0])
env.aim_camera([1.0470, 0, 0.7854])
env.select_display_camera(semanticL)
