import numpy as np
import cv2
import time
import serial
import pyrealsense2 as rs

def main():
    # --------------------------------------------------
    # 0. Configure serial port for Arduino Mega
    # --------------------------------------------------
    port1 = '/dev/ttyUSB1'
    baud_rate1 = 115200

    port2 = '/dev/ttyUSB0'
    baud_rate2 = 57600

    autonomous = False
    manual = False
    timeout = 1

    amega = serial.Serial(port1, baud_rate1, timeout=timeout)
    radio = serial.Serial(port2, baud_rate2, timeout=timeout)

    time.sleep(2)

    # --------------------------------------------------
    # 1. Configure and start the RealSense pipeline
    # --------------------------------------------------
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    #print("[INFO] Starting pipeline...")
    profile = pipeline.start(config)

    # --------------------------------------------------
    # 2. Retrieve depth sensor & scale
    # --------------------------------------------------
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    #print("[INFO] Depth scale (meters per depth unit):", depth_scale)

    # --------------------------------------------------
    # 3. (Optional) Set up RealSense filters
    # --------------------------------------------------
    decimation = rs.decimation_filter()
    decimation.set_option(rs.option.filter_magnitude, 2)  # downsample 2x

    spatial = rs.spatial_filter()
    spatial.set_option(rs.option.holes_fill, 3)  # fill small holes

    hole_filling = rs.hole_filling_filter()

    # Give the camera a moment to settle
    time.sleep(1.0)

    # --------------------------------------------------
    # 4. Define obstacle threshold in meters
    #    (Anything closer than this distance is an obstacle)
    # --------------------------------------------------
    obstacle_distance_m =   1.0  # 1.0 meter
    obstacle_distance_units = obstacle_distance_m / depth_scale
    #print(f"[INFO] Obstacle distance threshold in depth units: {obstacle_distance_units:.2f}")

    # --------------------------------------------------
    # 5. Define camera parameters
    # --------------------------------------------------
    image_width = 640
    fov_h = 57  # Horizontal FOV of the RealSense camera in degrees
    angle_per_pixel = fov_h / image_width  # Angle covered by each pixel

    # --------------------------------------------------
    # 6. Main loop
    # --------------------------------------------------
    forward_delay = None
    try:
        while True:
            if radio.in_waiting > 0:
                command = radio.readline().decode('utf-8').strip()
                print(command)
                if command == 'Semi-Autonomous':
                    autonomous = True
                elif command == 'Manual':
                    manual = True
                elif command == 'stop':
                    autonomous = False
                    manual = False
                    continue

                if manual:
                    if command == 'W':
                        amega.write(f"f\n".encode('utf-8'))
                    elif command == 'A':
                        amega.write(f"l\n".encode('utf-8'))
                    elif command == 'S':
                        amega.write(f"b\n".encode('utf-8'))
                    elif command == 'D':
                        amega.write(f"r\n".encode('utf-8'))
                    elif command == 'X':
                        amega.write(f"s\n".encode('utf-8'))
                    continue

            if manual:
                continue
            elif not autonomous:
                amega.write(f"s\n".encode('utf-8'))
                continue

            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            if not depth_frame:
                ##print("[DEBUG] No depth frame, continuing...")
                continue

            # --------------------------------------------------
            # 5A. Optionally apply filters to depth_frame
            # --------------------------------------------------
            # depth_frame = decimation.process(depth_frame)
            # depth_frame = spatial.process(depth_frame)
            # depth_frame = hole_filling.process(depth_frame)

            depth_image = np.asanyarray(depth_frame.get_data())

            # --------------------------------------------------
            # 5B. Replace zero (invalid) depth with large value
            # --------------------------------------------------
            zero_mask = (depth_image == 0)
            depth_image[zero_mask] = 9999

            # Debug: display min/max depth in the current frame
            min_val, max_val = depth_image.min(), depth_image.max()
            ##print(f"[DEBUG] Depth image range: min={min_val}, max={max_val}")

            # --------------------------------------------------
            # 5C. Convert depth to an 8-bit image for visualization
            # --------------------------------------------------
            # alpha=0.03 is just a scaling factor to map 16-bit depth to 8-bit grayscale
            depth_8u = cv2.convertScaleAbs(depth_image, alpha=0.03)

            # --------------------------------------------------
            # 5D. Create a colorized depth image (just for visualization)
            # --------------------------------------------------
            depth_colormap = cv2.applyColorMap(depth_8u, cv2.COLORMAP_JET)

            # --------------------------------------------------
            # 6A. Simple distance threshold map
            #     - anything < obstacle_distance_units => 255
            # --------------------------------------------------
            _, threshold_map = cv2.threshold(
                depth_image,
                obstacle_distance_units,
                255,
                cv2.THRESH_BINARY_INV
            )
            threshold_map = threshold_map.astype(np.uint8)

            # --------------------------------------------------
            # 6B. Use Canny to detect edges in the (8-bit) depth image
            # --------------------------------------------------
            # Tune these thresholds as needed:
            canny_threshold1 = 50
            canny_threshold2 = 150
            edges = cv2.Canny(depth_8u, canny_threshold1, canny_threshold2)

            # --------------------------------------------------
            # 6C. Combine threshold + edge detection
            #     - We want areas that are BOTH "within obstacle distance" AND have sharp edges
            # --------------------------------------------------
            combined_mask = cv2.bitwise_and(threshold_map, edges)

            # --------------------------------------------------
            # 7. Morphological operations to reduce noise
            # --------------------------------------------------
            kernel = np.ones((3, 3), np.uint8)
            combined_mask = cv2.dilate(combined_mask, kernel, iterations=2)
            combined_mask = cv2.erode(combined_mask, kernel, iterations=1)

            # --------------------------------------------------
            # 8. Find contours on the combined mask
            # --------------------------------------------------
            contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # --------------------------------------------------
            # 9. Filter out small contours
            # --------------------------------------------------
            obstacles = []
            min_area = 1500  # Adjust based on your environment
            for c in contours:
                area = cv2.contourArea(c)
                if area > min_area:
                    obstacles.append(c)

            # --------------------------------------------------
            # 10. Draw bounding boxes for debugging
            # --------------------------------------------------
            for c in obstacles:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(depth_colormap, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # --------------------------------------------------
            # 11. Simple logic: If obstacles exist, pick a direction
            # --------------------------------------------------
            # Depends on battery life
            complete_turn_time = 6.67 # 6.67 s
            rover_length = 0.6
            linear_buffer = 0.5
            linear_vel = 0.2 # 0.2 m/s
            sleep_time = None

            if len(obstacles) == 0:
                print('F')
                amega.write(f"f\n".encode('utf-8'))
                ##print("[INFO] No obstacles < 1m (with edge). Moving forward.")
                if forward_delay:
                    sleep_time = forward_delay
                    forward_delay = None
                # Switch GPS back on
                else:
                    print("Turn GPS on & stop")
                    amega.write(f"GPS on\n".encode('utf-8'))
                    amega.write(f"s\n".encode('utf-8'))
            else:
                print("Turn GPS off")
                amega.write(f"GPS off\n".encode('utf-8'))
                # Count obstacles, do a simple left/right check using average contour center
                # print(f"[INFO] Detected {len(obstacles)} obstacle(s).")

                # Compute average x-center of all obstacles
                cX_sum = 0
                avg_cXs = []
                obstacle_index = None # Index of obstacle (in obstacle list) to be avoided
                for c in obstacles:
                    M = cv2.moments(c)
                    if M["m00"] != 0:
                        cX = M["m10"] / M["m00"]
                        cX_sum += cX
                        avg_cXs.append(cX)
                avg_cX = cX_sum / len(obstacles)

                mid_width = depth_colormap.shape[1] // 2
                if avg_cX < mid_width:
                    #print("Obstacle(s) mostly on LEFT side => Move RIGHT.")
                    # Calculate rotation angle to clear obstacle
                    rightmost_point = None
                    for i, c in enumerate(obstacles):
                        # Use avg_cXs[i] to get the corresponding avg_cX for the current obstacle
                        if avg_cXs[i] < mid_width:  # Only consider obstacles on the left side
                            x, y, w, h = cv2.boundingRect(c)
                            curr_rightmost_point = x + w  # Rightmost point of the object
                            if rightmost_point is None or curr_rightmost_point > rightmost_point:
                                rightmost_point = curr_rightmost_point
                                obstacle_index = i
                    if rightmost_point is not None:
                        angle_to_clear = abs(rightmost_point - mid_width) * angle_per_pixel
                        total_rotation_angle = angle_to_clear + 10  # Add 10 degrees
                        #print(f"R by {total_rotation_angle:.2f} degrees to clear.")
                        print(f"R {total_rotation_angle:.2f}")
                        amega.write(f"r\n".encode('utf-8'))
                        sleep_time = total_rotation_angle/360 * complete_turn_time

                else:
                    #print("Obstacle(s) mostly on RIGHT side => Move LEFT.")
                    # Calculate rotation angle to clear obstacle
                    leftmost_point = None
                    for i, c in enumerate(obstacles):
                        # Use avg_cXs[i] to get the corresponding avg_cX for the current obstacle
                        if avg_cXs[i] > mid_width:  # Only consider obstacles on the right side
                            x, y, w, h = cv2.boundingRect(c)
                            curr_leftmost_point = x  # Leftmost point of the object
                            if leftmost_point is None or curr_leftmost_point < leftmost_point:
                                leftmost_point = curr_leftmost_point
                                obstacle_index = i
                    if leftmost_point is not None:
                        angle_to_clear = abs(mid_width - leftmost_point) * angle_per_pixel
                        total_rotation_angle = angle_to_clear + 10  # Add 10 degrees
                        #print(f"[INFO] Rotate LEFT by {total_rotation_angle:.2f} degrees to clear.")
                        print(f"L {total_rotation_angle:.2f}")
                        amega.write(f"l\n".encode('utf-8'))
                        sleep_time = total_rotation_angle/360 * complete_turn_time
                
                if obstacle_index is not None:
                    points = np.array([pt[0] for pt in obstacles[obstacle_index]])

                    # Find the farthest point (maximum depth value) and angle alpha that it makes with the mid-line of the screen
                    farthest_point = None
                    max_depth = 0

                    for x, y in points:
                        if depth_image[y, x] > max_depth and depth_image[y, x] is not 9999:
                            max_depth = depth_image[y, x]
                            farthest_point = (x, y)

                    max_depth *= depth_scale
                    max_depth *=  0.07 / 9.99
                    print(f'max depth {max_depth}')
                    if farthest_point:
                        # Compute pixel offset from the mid-width pixel
                        mid_pixel_x = image_width // 2
                        pixel_offset_x = abs(farthest_point[0] - mid_pixel_x)

                        # Calculate angle alpha (in radians)
                        alpha = pixel_offset_x * angle_per_pixel

                        # Debugging output
                        #print(f"Farthest point: {farthest_point}, Depth: {max_depth}, Alpha: {alpha:.2f}°")
                        

                        mid_width_distance_to_farthest_point = max_depth * np.cos(np.radians(alpha)) 
                        print('mid width to farthest point', mid_width_distance_to_farthest_point)

                        if total_rotation_angle < 85 or total_rotation_angle > 95:
                            dist_to_avoid_obstacle = mid_width_distance_to_farthest_point / np.cos(np.radians(total_rotation_angle))

                        else:
                            dist_to_avoid_obstacle = mid_width_distance_to_farthest_point / np.cos(np.radians(85))
                        
                        dist_to_avoid_obstacle += rover_length + linear_buffer
                        forward_delay = dist_to_avoid_obstacle/ linear_vel

                        print(f'dist to avoid: {dist_to_avoid_obstacle}')
                        print(f'alpha : {alpha}, theta : {total_rotation_angle}')

            # --------------------------------------------------
            # 12. Show windows for debugging
            # --------------------------------------------------
            #cv2.imshow("Depth Colormap", depth_colormap)
            #cv2.imshow("Threshold Map (<1m)", threshold_map)
            #cv2.imshow("Canny Edges", edges)
            #cv2.imshow("Combined Mask", combined_mask)

            # --------------------------------------------------
            # 13. Break on ESC
            # --------------------------------------------------
            
            if sleep_time:
                print(f'sleep{sleep_time}')
                time.sleep(sleep_time)
            key = cv2.waitKey(1)
            if key == 27:
                  # ESC
                ##print("[INFO] Exiting main loop.")
                break

    finally:
        # Stop RealSense pipeline and close windows
        pipeline.stop()
        amega.write(f"s\n".encode('utf-8'))
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
