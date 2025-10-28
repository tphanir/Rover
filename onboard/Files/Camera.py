class Camera:
    def __init__(self, width=640, height=480, fps=30, obstacle_distance_m=1.0, decimation_magnitude=2, holes_fill=3):
        """
        Initialize the RealSense camera pipeline, configuration, and parameters.

        Args:
            width (int): Width of the depth stream resolution.
            height (int): Height of the depth stream resolution.
            fps (int): Frames per second for the depth stream.
            obstacle_distance_m (float): Distance threshold in meters for detecting obstacles.
            decimation_magnitude (int): Downsample factor for decimation filter.
            holes_fill (int): Fill option for the spatial filter (0 to 5, higher values fill larger holes).
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.obstacle_distance_m = obstacle_distance_m
        self.decimation_magnitude = decimation_magnitude
        self.holes_fill = holes_fill

        self.pipeline = None
        self.depth_scale = None
        self.obstacle_distance_units = None


        # Initialize and configure the pipeline
        self._initialize_camera()
        # Set depth scale and distance threshold
        self._retrieve_depth_scale()
        self.obstacle_distance_units = self.obstacle_distance_m / self.depth_scale

    def _initialize_camera(self):
        """Initialize the RealSense pipeline and configure the depth stream."""
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, self.fps)

        # Start the pipeline
        self.profile = self.pipeline.start(config)
        print('[INFO] Pipeline started.')

        # Allow camera to stabilize
        time.sleep(3.0)

    def _retrieve_depth_scale(self):
        """Retrieve the depth sensor's scale in meters per depth unit."""
        depth_sensor = self.profile.get_device().first_depth_sensor()
        self.depth_scale = depth_sensor.get_depth_scale()
        
    def setup_filters(self):
        """Set up RealSense filters (optional)."""
        # Decimation filter
        self.decimation_filter = rs.decimation_filter()
        self.decimation_filter.set_option(rs.option.filter_magnitude, self.decimation_magnitude)

        # Spatial filter
        self.spatial_filter = rs.spatial_filter()
        self.spatial_filter.set_option(rs.option.holes_fill, self.holes_fill)

        # Hole-filling filter
        self.hole_filling_filter = rs.hole_filling_filter()

        
    def get_obstacle_distance_threshold(self):
        """
        Get the obstacle distance threshold in depth units.
        
        Returns:
            float: Distance threshold in depth units.
        """
        return self.obstacle_distance_units

    def capture_frame(self):
        """
        Capture a single frame of depth data from the camera.

        Returns:
            numpy.ndarray: The depth frame as a 2D array.
        """
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            return None
        return depth_frame

    def apply_filters(self, depth_frame):
        """
        Apply RealSense filters to the depth frame.

        Args:
            depth_frame (pyrealsense2.depth_frame): The input depth frame.

        Returns:
            pyrealsense2.depth_frame: The filtered depth frame.
        """
        filtered_frame = self.decimation_filter.process(depth_frame)
        filtered_frame = self.spatial_filter.process(filtered_frame)
        filtered_frame = self.hole_filling_filter.process(filtered_frame)
        return filtered_frame

    def stop(self):
        """Stop the camera pipeline."""
        if self.pipeline:
            self.pipeline.stop()
            
    def __del__(self):
        """Ensure the pipeline is stopped on object destruction."""
        self.stop()
