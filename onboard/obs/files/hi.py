import numpy as np
import cv2
import time
import pyrealsense2 as rs


def configure_realsense():
    """ Configure and start the RealSense pipeline. """
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    profile = pipeline.start(config)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    return pipeline, depth_scale


def apply_filters(depth_frame):
    """ Apply filters to the depth frame. """
    decimation = rs.decimation_filter()
    spatial = rs.spatial_filter()
    hole_filling = rs.hole_filling_filter()
    
    depth_frame = decimation.process(depth_frame)
    depth_frame = spatial.process(depth_frame)
    depth_frame = hole_filling.process(depth_frame)
    
    return np.asanyarray(depth_frame.get_data())


def process_depth_image(depth_image, depth_scale, obstacle_distance_m):
    """ Process the depth image for obstacle detection. """
    # Convert 16-bit depth to 8-bit for visualization
    depth_image[depth_image == 0] = 9999  # Replace invalid depth (0)
    depth_8u = cv2.convertScaleAbs(depth_image, alpha=0.03)

    # Convert to colorized depth map for visualization
    depth_colormap = cv2.applyColorMap(depth_8u, cv2.COLORMAP_JET)

    # Threshold map for obstacles
    obstacle_distance_units = obstacle_distance_m / depth_scale
    _, threshold_map = cv2.threshold(depth_image, obstacle_distance_units, 255, cv2.THRESH_BINARY_INV)
    threshold_map = threshold_map.astype(np.uint8)

    return depth_colormap, threshold_map


def find_obstacles(combined_mask):
    """ Find contours (obstacles) from the combined mask. """
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    obstacles = [c for c in contours if cv2.contourArea(c) > 1500]  # min_area = 1500
    return obstacles


def calculate_obstacle_direction(obstacles, depth_colormap, angle_per_pixel):
    """ Calculate the obstacle's direction (left or right). """
    avg_cX = np.mean([cv2.moments(c)["m10"] / cv2.moments(c)["m00"] for c in obstacles if cv2.moments(c)["m00"] != 0])
    mid_width = depth_colormap.shape[1] // 2
    sleep_time = 0.5

    if avg_cX < mid_width:
        rightmost_point = max([x + w for (x, y, w, h) in [cv2.boundingRect(c) for c in obstacles] if x + w < mid_width], default=None)
        if rightmost_point is not None:
            angle_to_clear = abs(rightmost_point - mid_width) * angle_per_pixel
            sleep_time = angle_to_clear / 360 * 5.39
    else:
        leftmost_point = min([x for (x, y, w, h) in [cv2.boundingRect(c) for c in obstacles] if x > mid_width], default=None)
        if leftmost_point is not None:
            angle_to_clear = abs(mid_width - leftmost_point) * angle_per_pixel
            sleep_time = angle_to_clear / 360 * 5.39

    return sleep_time


def main():
    # Setup and configure RealSense
    pipeline, depth_scale = configure_realsense()

    obstacle_distance_m = 1.0  # Threshold for obstacle distance in meters
    image_width = 640
    fov_h = 57
    angle_per_pixel = fov_h / image_width  # Horizontal angle per pixel

    # Main loop
    try:
        while True:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            if not depth_frame:
                continue

            depth_image = apply_filters(depth_frame)
            depth_colormap, threshold_map = process_depth_image(depth_image, depth_scale, obstacle_distance_m)

            # Edge detection and combined mask
            canny_edges = cv2.Canny(cv2.convertScaleAbs(depth_image, alpha=0.03), 50, 150)
            combined_mask = cv2.bitwise_and(threshold_map, canny_edges)
            combined_mask = cv2.dilate(combined_mask, np.ones((3, 3), np.uint8), iterations=2)
            combined_mask = cv2.erode(combined_mask, np.ones((3, 3), np.uint8), iterations=1)

            # Find obstacles
            obstacles = find_obstacles(combined_mask)

            # Determine robot direction (left or right)
            sleep_time = calculate_obstacle_direction(obstacles, depth_colormap, angle_per_pixel)

            # Debug: Display sleep time
            print(sleep_time)

            time.sleep(sleep_time)

            key = cv2.waitKey(1)
            if key == 27:  # ESC
                break

    finally:
        # Stop RealSense pipeline and close windows
        pipeline.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
