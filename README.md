# Visual Odometry 


[Documentation](https://github.com/AliabbasMerchant/visualOdometry/blob/master/documentation/documentation.pdf)


## CONTENTS

- Introduction
- Technical Background
- Implementation
- Challenges and Restrictions
- Hardware Stack
- Conclusion
- References


## INTRODUCTION

In robotics and computer vision, visual odometry is the process of determining the
position and orientation of a robot by analyzing the associated camera images. It has
been used in a wide variety of robotic applications.

Algorithm:

1. Acquire input images

2. Image correction (apply image processing techniques for noise removal, etc.)

3. Feature detection (define interest operators, and match features across frames) (Use of feature extraction and correlation to establish correspondence of two images).

4. Estimation of shortest path to destination and issuing instruction set for robotic maneuver.


## TECHNICAL BACKGROUND

### Computer Vision

Exploration is an important and active area of research in field robotics, as vehicles
capable of autonomous exploration have the potential to significantly impact a wide
range of applications such as search and rescue operations, environmental
monitoring, and planetary exploration. For this work, we define the ​ _exploration
problem_ ​as 
1) covering an unknown environment

2) mapping the area

3) detecting objects of interest.

 Therefore the key component of robotic exploration are
vision systems. Several ways can be used to achieve computer vision, like visual
odometry with image processing, machine learning, convolutional neural networks,
etc. In the scope of this project we used the former for the tasks mentioned above.

There are three main challenges present in a complete solution to the exploration
problem. First, the approach should maintain a globally consistent map over long
distances with mainly relative measurement information and intermittent absolute
measurements, like magnetometers. Second, the solution should reliably identify potential objects of interest at as great a range as possible to minimize the time
spent sweeping an environment for candidate objects, as well as identify objects of
interest in varying lighting and environmental conditions. Finally, a method to plan
an efficient search path over a terrain with unknown obstacles and contours is
required. The first two are discussed next and third is discussed in a separate section.

### Stereo Cameras and Depth Perception

Using the aforementioned techniques of image processing, the tasks of detection
and mapping of an unknown area were achieved. Stereo Vision refers to 3D vision. In
a traditional sense, the images taken by both eyes combined by the mind is referred
to as a stereo image which helps in depth perception. This process is called 3D
reconstruction.

Depth perception using stereo cameras is done in the following way:

[Source](​https://en.wikipedia.org/wiki/Computer_stereo_vision)


### Path Finding

The aforementioned approach needs to accomplish the objective to reach the goal
from the current position. Autonomous navigation using visual odometry utilizes
path-planning algorithms for finding shortest path from source to destination.
Algorithms used for path-planning tasks include dijkstra, depth-first search and
a-star(which we have used in this project).

The algorithm works by expanding the so-called '​ _frontier_ ​' of the map being parsed
node-wise from the starting position until the destination is reached; by looking at its


neighbours. The number of neighbouring moves considered valid depends on the
use-case, and in ours, they number ​ _4_ ​, with diagonal moves being illegal.

Any neighbours not visited yet, are added to the '​ _nodes_to_visit_ ​' priority-based
queue. To find the shortest route we add the concept of path cost to the design. The
first cost is the weight associated with traversing a node, for example, blocked paths
have a weight of ​ _infinity_ ​ for disincentivization. The standard weight for all other
nodes was assumed as ​ _one_ ​. An additional cost was introduced to find the path faster,
i.e. a ​ _heuristic cost_ ​, which helps us know if we are en route towards the destination.

The heuristic we chose was the ​ _Manhattan norm_ ​ which is, given nodes a(to be visited
node) and b(destination) is:

```cpp
heuristic_cost = (a.x - b.x) + (a.y - b.y)
```


Hence the final cost of any node traversal is :
```cpp
cost = cost_so_far + weight_of_node
```

And hence the priority of the neighboring node in the queue structure nodes_to_visit
is:

```cpp
priority = cost+heuristic_cost
```

This node is then pushed into the queue according to priority.

This process happens in a loop until the number of nodes to be visited is zero or we
have reached the goal index; and the resulting path from start to goal is the shortest
path.

The next step was to issue actionable instructions for the actual robotic motion. To
solve this, given the shortest path coordinates and an initial orientation, the legal
orientations were mapped and correspondingly, the directives to reach the next
node were added to a list of instructions. The first term was a boolean value
signifying whether to move or not, and the second being the angle of rotation


needed to reach the next node. Thus after parsing through the shortest path, a
complete set of instructions to reach the goal was ready.

Artificial Intelligence

The above mentioned approach can be encapsulated under the domain of AI since
the approach allows the robot to travel autonomously without human intervention.
The subject of AI is very broad, including various sub-disciplines of Machine Learning,
Deep Learning, Heuristic models, Visual Odometry etc. The purpose is to make
machines more intelligent for automating tasks that humans are bad at, hence
increasing accuracy and decreasing costs. AI is used in diverse areas like medicine,
economics, and of course robotics. Extensive research has been directed towards
developing newer, faster algorithms for accomplishing tasks like classification,
prediction and detection. The most prominent fields of AI in recent times are
Machine Learning and Deep Learning, which works by teaching machines the task
with enormous amounts of data. Other fields like heuristics are also rising with
semi-rule-based algorithms making the trade-off between speed and accuracy.


## Implementation

The bot works in the following way:

0. The destination coordinates are given to the robot, in cms. (along +ve X-axis
    and +ve Y-axis, just like in normal graphs.)
1. It takes a picture of its surroundings using dual cameras and applies noise
    reduction techniques to filter out the noise. The below 2 images are the ones
    which have been captured by the cameras and processed.
2. The bot (using Raspberry Pi and OpenCV via Python) then converts the 2
    images from BGR to HSV format.


3. Assuming ideal conditions (uniform ground and uniform background), the
    background and ground are then removed from the image. The resulting
    images are:
4. Contours are detected in the resulting images and the contours are matched,
    so as to match the images of the same object in both the cameras.


5. The distance, height, and other properties of the object are then calculated
    using the detected object contours.
6. Next, using all the detected objects, an internal map (having block size 30 cm x
    30 cm) is created, consisting of the objects(denoted by 9), bot
    position(denoted by 2) and the destination(denoted by 3). (Please note that
    we have assumed a depth of 30cm for each object. Hence, there is no gap
    between the detected objects. Also, the detected dimensions are 60 cm, as
    the objects lie on the boundaries of the blocks of the map, and hence occupy
    not 1, but parts of both the blocks.)


7. Now, using the A-Star algorithm, the best route from the bot(denoted by 2) to
    the destination(denoted by 3) is calculated. (​The first term is a boolean value
    signifying whether to move or not, and the second value is the angle of
    rotation(anticlockwise positive) needed to reach the next node.​)

Detected Path: [True, 0], [True, 0], [False, -90], [True, 0], [False, 90], [True, 0], [True,
0], [True, 0], [True, 0], [True, 0], [True, 0], [False, -270] ,[True, 0]

8. Each action in the path of the bot is then executed. The movement/rotation
    command is then sent from Raspberry Pi to Arduino, using UART. For each
    movement command, the bot wheels rotate for a constant amount of time, so
    that the bot can cover 30 cm(the block size of the internal map). For rotation
    (spot-rotation), a magnetometer and I2C communication have been used, so
    that the bot can be rotated the desired number of degrees.
9. The bot finally reaches its destination.


## Challenges, Restrictions and Limitations

1. The processing on Raspberry Pi is very slow, so we can’t process the camera
    feed live. Hence, we take the images, only once, at the start, and then we
    follow the map so generated.
2. The objects are properly detected only under ideal conditions, i.e. when we
    have uniformly coloured background and uniformly coloured ground.
3. The distance mapping is not 100% accurate.
4. Since it is not possible to calculate the depth of the objects using just the
    images from the front, we have to assume a standard depth (say, 30 cm.) for
    each object.
5. The angle of rotation of the bot is sometimes not accurate, because of slipping
    of the bot wheels.


## Hardware Stack

1. Raspberry Pi 3 B
2. SRA Development Board
3. Magnetometer (QMC5883L)
4. 4x GearMotors
5. 2x USB Camera
6. Li-ion battery
7. Powerbank
8. CP2102 (USB to UART)
9. 4-wheel generic bot chassis


## Conclusion

This project enabled an extremely fruitful utilization of our summer and also helped
further our understanding of autonomous vehicles. The team understood the
incredible value of precision in the design of these vehicles and the real-life
implications of its lack thereof. Even as such vehicles may be safer than human
drivers, even the slightest miscalculation can cause severe loss of life and property,
not to mention the loss of faith of the general public in the industry.

The primary deliverable of this project, an autonomous delivery robot, was
successfully realized. The team would love to pursue several improvements in the
both the software and hardware design of the bot and have it tested in real scenarios
to automate the delivery of small to medium sized articles in confined places like restaurants and offices.

## REFERENCES


[A* algorithm](https://www.redblobgames.com/pathfinding/a-star/introduction.html)

[A* GeeksForGeeks](https://www.geeksforgeeks.org/a-search-algorithm/)

[Python C++ wrapping](http://intermediate-and-advanced-software-carpentry.readthedocs.io/en/latest/c++-wrapping.html)

[OpenCV](http://opencv-python-tutroals.readthedocs.io/en/latest/)

[PyImageSearch](https://www.pyimagesearch.com/)

[Computer Stereo Vision](https://en.wikipedia.org/wiki/Computer_stereo_vision)

[Magnetometer API](https://github.com/keepworking/Mecha_QMC5883L)








