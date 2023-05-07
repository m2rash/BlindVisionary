import copy
import pyrealsense2 as rs
import numpy as np
import cv2
from bbToVtx import bbToVtx
import bounding_boxer
from beep import beeper
from guidance import draw_divided_circle
from PIL import Image
import pyaudio


def showImages(color_image, depth_image, hand_image, object_image):
     # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    
    images = np.hstack((depth_colormap, hand_image, object_image))
    cv2.imshow('RealSense', images)
    
    
def getAlignedImagesAndVtx(pipeline, pc) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    align_to = rs.stream.color
    align = rs.align(align_to)
    
    frames = pipeline.wait_for_frames()
        
    # Align the depth frame to color frame
    aligned_frames = align.process(frames)

    # Get aligned frames
    depth_frame = aligned_frames.get_depth_frame()# aligned_depth_frame is a 640x480 depth image
    color_frame = aligned_frames.get_color_frame()
    
    pc.map_to(color_frame) # WTF does this do? 
    points = pc.calculate(depth_frame)
    vtx = np.asanyarray(points.get_vertices())
    tex = np.asanyarray(points.get_texture_coordinates())
    
    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    
    return color_image, depth_image, vtx


    

if __name__ == "__main__":

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    pc = rs.pointcloud()
    pipeline.start(config)

    handVtx = (0,0,0)
    objectVtx = (0,0,0)

    meep = beeper()
    
    # cap = cv2.VideoCapture(0)
    while True:
        
        color_image, depth_image, vtx = getAlignedImagesAndVtx(pipeline, pc)
        # _, color_image = cap.read()
                
        
        handBBs, hand_image = bounding_boxer.getHandBB(copy.deepcopy(color_image))
        objectBBs, object_image = bounding_boxer.getMockBB(copy.deepcopy(color_image))
        
        #print("Hands: ", handBBs)
        #print("Objects: ", objectBBs)
        
        
        if len(handBBs) > 0: handVtx = bbToVtx(handBBs[0], vtx.reshape((480, 640)))
        if len(objectBBs) > 0: objectVtx = bbToVtx(objectBBs, vtx.reshape((480, 640)))
        
        # print("Hand: ", handVtx, len(handBBs))
        # print("Object: ", objectVtx, len(objectBBs))
        
        #circleImage = draw_divided_circle(42, objectVtx, handVtx, 10, None)
        dist = np.sqrt((objectVtx[0] - handVtx[0]) **2 + (objectVtx[1] - handVtx[1]) **2 + (objectVtx[2] - handVtx[2]) **2)
        print(dist)
        meep.feedDistAndBeep(dist)
        cv2.namedWindow('Guidance', cv2.WINDOW_AUTOSIZE)
        #cv2.imshow('Guidance', np.asarray(circleImage))
    
        proximityBar = np.zeros((40,200,3), np.uint8)
        cv2.rectangle(proximityBar,(3,3), (min(197-int(np.floor(dist*100)),197), 37),color=(0,255,0))
        cv2.imshow("Porgress",proximityBar)
        
        showImages(color_image, depth_image, hand_image, object_image)

        if cv2.waitKey(1) == ord('q'):
            break
        
                
    pipeline.stop()



    