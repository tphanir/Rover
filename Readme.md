
<h1>Rover - Team Pravartak</h1>

<hr>

<h2>Table of Contents</h2>
<ul>
    <li><a href="#project-overview">Project Overview</a></li>
    <li><a href="#rover-description">Rover Description</a></li>
    <li><a href="#physical-components">Physical Components</a></li>
    <li><a href="#software-components">Software Components</a></li>
    <li><a href="#additional-features">Additional Features</a></li>
    <li><a href="#deviations">Deviations</a></li>
    <li><a href="#media">Media</a></li>
</ul>

<hr>
<h2 id="project-overview">Project Overview</h2>
<p>Team Pravartak developed a rover prototype for robust exploration on uneven terrains and inclines up to 45 degrees, capabilities in autonomous navigation, obstacle detection, and adaptability to harsh environments.</p>

<hr>
<h2 id="rover-description">Rover Description</h2>
<ul>
    <li><strong>Structure:</strong> The rover's 6-wheel drive system, combined with a triple bogie mechanism, offers enhanced maneuverability and stability over rough and uneven terrains. This design, constructed from MDF board, aluminum extrusions, and C-shaped mild steel, allows the rover to distribute weight evenly across its wheels, ensuring that it can tackle steep inclines and rocky landscapes with minimal risk of tipping. The triple bogie setup improves ground contact, enabling each wheel to independently respond to terrain changes, maintaining stability and grip even on highly irregular surfaces.
    <br><br>With these robust structural materials, the rover achieves a balance between lightweight agility and structural resilience, making it suitable for both exploratory research and environmental monitoring in challenging conditions.</li>
    <li><strong>Navigation:</strong> The manual navigation of the robot through serial communication, using a control interface connected to the Jetson board. The program receives directional commands from an external controller via serial input, which it interprets to control the movement of the robot's motors. The movement options include forward, backward, left rotation, and right rotation, and each command is executed based on the received serial input.

<h3>Functions:</h3>
<ul>
    <li>move_forward(): Activates the motors to drive the robot forward.</li>
    <li>move_backward(): Activates the motors to drive the robot backward.</li>
    <li>stop(): Stops all motor activity, bringing the robot to a halt.</li>
    <li>rotate_continuous(direction): Rotates the robot continuously in the specified direction ('left' or 'right') until a different command is received.</li>
    <li>receive_data(): Listens for serial input data, which determines the direction of movement.</li>
</ul>

<p>The robot’s movements are controlled by the following commands received through serial input:</p>
<ul>
    <li><strong>'w':</strong> Move forward</li>
    <li><strong>'s':</strong> Move backward</li>
    <li><strong>'a':</strong> Rotate continuously to the left</li>
    <li><strong>'d':</strong> Rotate continuously to the right</li>
    <li><strong>'q':</strong> Stop the robot</li>
    <li><strong>'exit':</strong> Exit the manual control loop and clean up resources</li>
</ul> </strong> .</li>
    <li><strong>Obstacle Detection:</strong> <p>This project enables autonomous obstacle detection and navigation for a robot using a LiDAR sensor and motor control through Jetson.GPIO. The LiDAR scans the environment, and the distance and angle data are analyzed to detect obstacles. When an obstacle is identified within preset thresholds, the robot chooses a safe direction by rotating left or right and continues forward if the path is clear. Additionally, slope detection helps the robot assess and safely navigate uneven terrain.</p><p>The robot’s movement functions allow it to move forward, reverse, or rotate to avoid obstacles. After avoiding an obstacle, the robot attempts to re-align to its original path for efficient navigation. This approach enables effective autonomous exploration in structured environments with basic obstacle avoidance and terrain adaptability.</p></li>
    <li><strong>Power Supply:</strong> LiPo 4S battery connected to the L298N motor driver for driving the motors with PWM signals from Jetson Nano.</li><br>
    <li><strong>45° Incline Sploe Climbing:</strong>
One of the key features of this rover is its ability to climb slopes up to 45 degrees. The combination of the 6-wheel drive system and the triple bogie mechanism allows the rover to maintain traction and balance while ascending steep inclines. This capability is crucial for environments with uneven terrain, making the rover suitable for exploration in areas with challenging topography such as rocky landscapes, hills, or even simulated extraterrestrial environments.</li>

</ul>

<h2>Electronics Components</h2>

<p>The rover is equipped with various electronic components to support autonomous navigation and terrain exploration. The components used are as follows:</p>

<ul>
    <li><strong>NVIDIA Jetson</strong> (e.g., Jetson Nano): The onboard processing unit for running algorithms and controlling the rover's systems.</li>
    <li><strong>Ultrasonic Distance Sensor</strong> (HC-SR04): Used for obstacle detection by measuring the distance between the rover and surrounding objects.</li>
    <li><strong>L298N Dual H-Bridge Motor Driver</strong>: Powers and controls the rover's motors, allowing for precise movement in both directions (forward and backward).</li>
    <li><strong>Orange High Torque DC Motors (555 series)</strong>: Provides the necessary torque to drive the rover on various surfaces, including steep inclines.</li>
    <li><strong>Radio Telemetry Module</strong> (3DR): Enables wireless communication between the rover and remote control systems for telemetry data transmission.</li>
    <li><strong>LiDAR Sensor</strong> (2D-YDLIDAR): Used for 180-degree scanning of the environment, aiding in obstacle detection and mapping.</li>
    <li><strong>NEO-6M GPS Module</strong>: Provides accurate location data, enabling autonomous navigation and geospatial tracking.</li>
</ul>

<p>These components work together to ensure the rover can navigate difficult terrains, detect and avoid obstacles, and provide real-time feedback to operators through telemetry.</p>

<h2>Software Components</h2>

<p>The rover's software stack integrates various libraries and tools to provide full control and functionality for autonomous navigation, communication, and data processing. The software components used are as follows:</p>

<ul>
    <li><strong>Autodesk Fusion 360</strong>: A powerful 3D CAD and CAM tool used for designing the rover's mechanical components. It enables precise modeling of parts, assemblies, and simulations to ensure the rover can withstand real-world conditions. Fusion 360 also supports collaboration for team projects, allowing easy sharing of design files.</li>
    
<li><strong>Serial Communication</strong> (Python Serial Library): The <code>serial</code> library in Python is used to handle communication between the rover and external devices like remote controllers, GPS modules, and other sensors. It enables the transmission of commands and data over UART, allowing real-time control and feedback.</li>
    
<li><strong>YDLIDAR SDK</strong>: The YDLIDAR library allows seamless integration of LiDAR sensors with the rover's onboard system. It is used to process data from the LiDAR sensor, providing distance measurements to aid in obstacle detection and mapping. The SDK supports various LiDAR models, and it is crucial for real-time environmental scanning, enabling the rover to navigate autonomously in dynamic surroundings.</li>
</ul>




<h2 id="project-overview">Additional Feature</h2><p>Modular Design: The rover’s modular design allows easy customization and upgrades, with interchangeable components like the chassis, motors, sensors, and electronics. This makes maintenance simpler and enables future enhancements without redesigning the whole system.</p>

<p>Lightweight: The rover's lightweight design, using MDF board for the chassis and aluminum extrusions for structure, enhances performance and maneuverability. It improves speed, agility, and reduces power consumption, allowing longer operational time and efficient navigation across various terrains.</p></li>

<h2>Team Members</h2>
<ol>
<li><a href="https://www.linkedin.com/in/yuvraj-gupta11/" target="_blank">Yuvraj Gupta</a></li>
<li><a href="mailto:phanirajtelukunta@gmail.com" target="_blank">Telukunta Phani Raj</a></li>
<li><a href="https://www.linkedin.com/in/koyaneni-yaswanth-988a92220/" target="_blank">Koyaneni Yashwant</a></li>
<li><a href="https://www.linkedin.com/in/shubham-pandere-72b240259/?originalSubdomain=in">Shubham Pandere</a></li>
<li><a href="https://www.linkedin.com/in/aiden-dsouza/" target="_blank">Aiden D'souza</a></li>
</ol>

<hr>
<hr>
