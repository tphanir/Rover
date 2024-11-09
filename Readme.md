
<h1>Rover - Team Pravartak</h1>

<p><strong>Rover</strong><br>
<strong>Category:</strong> Rover<br>
<strong>Institution:</strong> Visvesvaraya National Institute of Technology, Nagpur</p>

<hr>

<h2>Table of Contents</h2>
<ul>
    <li><a href="#project-overview">Project Overview</a></li>
    <li><a href="#rover-description">Rover Description</a></li>
    <li><a href="#hardware-components">Hardware Components</a></li>
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
    <li><strong>Structure:</strong>The rover's 6-wheel drive system, combined with a triple bogie mechanism, offers enhanced maneuverability and stability over rough and uneven terrains. This design, constructed from MDF board, aluminum extrusions, and C-shaped mild steel, allows the rover to distribute weight evenly across its wheels, ensuring that it can tackle steep inclines and rocky landscapes with minimal risk of tipping. The triple bogie setup improves ground contact, enabling each wheel to independently respond to terrain changes, maintaining stability and grip even on highly irregular surfaces.

With these robust structural materials, the rover achieves a balance between lightweight agility and structural resilience, making it suitable for both exploratory research and environmental monitoring in challenging conditions.</li>
    <li><strong>Navigation: </strong> .</li>
    <li><strong>Obstacle Detection:</strong> <p>This project enables autonomous obstacle detection and navigation for a robot using a LiDAR sensor and motor control through Jetson.GPIO. The LiDAR scans the environment, and the distance and angle data are analyzed to detect obstacles. When an obstacle is identified within preset thresholds, the robot chooses a safe direction by rotating left or right and continues forward if the path is clear. Additionally, slope detection helps the robot assess and safely navigate uneven terrain.</p>

<p>The robot’s movement functions allow it to move forward, reverse, or rotate to avoid obstacles. After avoiding an obstacle, the robot attempts to re-align to its original path for efficient navigation. This approach enables effective autonomous exploration in structured environments with basic obstacle avoidance and terrain adaptability.</p></li>
    <li><strong>Power Supply:</strong> LiPo 4S battery connected to the L298N motor driver for driving the motors with PWM signals from Jetson Nano.</li>
</ul>

