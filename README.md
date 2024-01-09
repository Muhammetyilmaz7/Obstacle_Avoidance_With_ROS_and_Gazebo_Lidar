# Obstacle Avoidance Project with Lidar

This project is a robot project that provides obstacle avoidance capability with lidar sensor using Robot Operating System (ROS) and Gazebo simulation environment.

## Setup

For the project to run successfully, follow these steps:

1. Download and install ROS Melodic or Noetic version from [ROS official website](http://wiki.ros.org/ROS/Installation).

2. Make sure Gazebo is installed:

     ```bash
     sudo apt-get install gazebo9
     ```

3. Clone this repository:

     ```bash
     git clone https://github.com/Muhammetyilmaz7/Obstacle_Avoidance_With_ROS_and_Gazebo_Lidar.git
     ```
   
4. Make sure that the source code you download is in a ROS runtime environment.

5. Compile the packages by running the following commands in the root directory of the project:

     ```bash
     catkin_make
     ```

6. Launch the world of TURTLEBOT3 in the Gazebo simulation environment.

7. After the robot appears in the Gazebo world, run the code in the workspace.

## Use

Once the project is successfully installed and launched, your robot will demonstrate obstacle avoidance ability with its lidar sensor and operate in the Gazebo simulation environment. Take a detailed look at the code for more information about controls and parameters.

## Contribute

If you would like to contribute to this project, please get in touch by opening a topic or submitting a pull request.

## Licence

This project is licensed under the MIT License - see [LICENSE].
