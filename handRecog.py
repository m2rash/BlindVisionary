import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pc = rs.pointcloud()
pipeline.start(config)


align_to = rs.stream.color
align = rs.align(align_to)

while True:
    
    frames = pipeline.wait_for_frames()
    
    # Align the depth frame to color frame
    aligned_frames = align.process(frames)

    # Get aligned frames
    depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
    color_frame = aligned_frames.get_color_frame()
    
    pc.map_to(color_frame)
    points = pc.calculate(depth_frame)
    vtx = np.asanyarray(points.get_vertices())
    tex = np.asanyarray(points.get_texture_coordinates())
    # testDepthImg = (np.reshape([e[2] for e in vtx], (480,640)) * 255).astype("uint8")
    
    # Convert images to numpy arrays
    # depth_image = np.asanyarray(testDepthImg)
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    depth_colormap_dim = depth_colormap.shape
    color_colormap_dim = color_image.shape

    
    cv2.namedWindow('Color', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Color', color_image)
    cv2.namedWindow('Depth', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Depth', depth_colormap)
    if cv2.waitKey(1) == ord('q'):
            break
        
pipeline.stop()