import numpy as np
import cv2
import open3d as o3d

fx = 525.0
fy = 525.0
cx = 320.0
cy = 240.0

def main():
    depth_image = cv2.imread("/home/shri/development/Computer-Vision/tools/Synthetic_Depth_Image/depth_image.png", cv2.IMREAD_UNCHANGED)
    if depth_image is None:
        raise RuntimeError("Could not read depth_image.png")
    
    # Convert from mm → meters
    depth_image_meters = (depth_image.astype(np.float32)) * 0.001
    height, width = depth_image.shape
    
    # Wrap it as an Open3D image and define intrinsic matrix
    o3d_depth = o3d.geometry.Image(depth_image_meters)
    intrinsic = o3d.camera.PinholeCameraIntrinsic(width, height, fx, fy, cx, cy)
    pcd = o3d.geometry.PointCloud.create_from_depth_image(o3d_depth, intrinsic, project_valid_depth_only=True)

    o3d.io.write_point_cloud("depth_pointcloud.pcd", pcd)
    print("Saved: depth_pointcloud.pcd")

if __name__ == "__main__":
    main()
