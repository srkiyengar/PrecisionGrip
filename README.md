# PrecisionGrip

At the neurobotics lab at University of Waterloo, we are attempting to collect data associated with human grasping actions while picking up of objects in the YCB model set. The setup consists of a Reflex_SF (in future also Reflex Takktile) from Righthandrobotics controlled through a Logitech Extreme joystick, an NDI Polaris capturing the coordinates and the quaternion vectors based on rigid body reflectors attached to the Reflex, and an image processing mechanism to capture the position of the YCB object while gripping. 

Control of Reflex_SF
The control of the Reflex_SF is accomplished through sending commands to the 4 Dynamixel servos. A USB2Dynamixel interface is built in to the Reflex_SF.  
