import numpy as np
import cv2 as cv
import glob
import os
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
def calib():
    objp = np.zeros((6*8,3), np.float32)
    objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    # images = glob.glob('*.jpg')
    path = "/home/machine005/Hinhanh"
    store = os.listdir(path)
    print(store)
    store.sort(key=len, reverse=False)
    for fname in store:
        full = path + "/" + str(fname)
        print("Fule name: ", full)
        img = cv.imread(full)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (8,6), None)
        print(ret)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv.drawChessboardCorners(img, (8,6), corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(500)
    cv.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    return [ret, mtx, dist, rvecs, tvecs]

def save_coefficinets(mtx, dist, path):
    cv_file = cv.FileStorage(path, cv.FILE_STORAGE_WRITE)
    cv_file.write("K", mtx)
    cv_file.write("D", dist)
    cv_file.release()

def undistor_cam_left(img):
    """ Loads camera matrix and distortion coefficients. """
    # FILE_STORAGE_READ
    path = "/home/mic/backup_ktnut/TESTPOKA3speed/calibra.xml"
    cv_file = cv.FileStorage(path, cv.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()
    cv_file.release()
    undist = cv.undistort(img, camera_matrix, dist_matrix, None, camera_matrix)
    return undist

def undistor_cam_right(img):
    """ Loads camera matrix and distortion coefficients. """
    # FILE_STORAGE_READ
    path = "/home/mic/backup_ktnut/TESTPOKA3speed/calibra_right.xml"
    cv_file = cv.FileStorage(path, cv.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()
    cv_file.release()
    undist = cv.undistort(img, camera_matrix, dist_matrix, None, camera_matrix)
    return undist

def undi(img):
    mtx, dist = load_coefficients()
    undist = cv.undistort(img, mtx, dist, None, mtx)
    return undist
if __name__ == '__main__':
    ret, mtx, dist, rvecs, tvecs = calib()
    path = "/home/mic/Hinhanh/calibra.xml"
    save_coefficinets(mtx, dist, path)
    # img = cv.imread("L_True.jpg")
    # img = undistor_cam(img)
    # cv.imshow("halo", img)
    # cv.imwrite("undist.jpg", img)
    if cv.waitKey(0) & 0xFF == ord('q'):
        cv.destroyAllWindows()
