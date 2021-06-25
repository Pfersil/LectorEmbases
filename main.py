import cv2
import pytesseract
import numpy as np


def empty(a):
    pass


# Tesseract is used to read text in images
# Must be instaled in the computer


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# A screen in order to change on air some parameters
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("Threshold1", "Parameters", 73, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 34, 255, empty)


# Get Contours and detect squares
def getContours(img, imgContour):
    global imgCropped
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # Find contours

    for cnt in contours:

        peri = 0.02 * cv2.arcLength(cnt, True)  # Calculate perimeter for every contour
        approx = cv2.approxPolyDP(cnt, peri, True)

        if len(approx) == 4:  # Search for rectangles with a concrete area
            # Color detection would be nice to have

            x, y, w, h = cv2.boundingRect(approx)

            imgCropped = imgContour[y:y + h, x:x + w]  # Crop image using bounding rect coordinates

            # Read text form cropped image
            imgRead = cv2.cvtColor(imgCropped, cv2.COLOR_BGR2RGB)  # tesseract works with RGB
            kernel2 = np.ones((2, 2), np.uint8)
            imgRead = cv2.dilate(imgRead, kernel2, iterations=1)
            imgRead = cv2.erode(imgRead, kernel2, iterations=1)
            string = pytesseract.image_to_string(imgRead)  # Read and put text in a string


            # Using Naive Method
            res = None
            for i in range(0, len(string)):    # Search a xx\xx\xx structure in the string
                if string[i] == "/" and string[i-3] == "/":
                    res = i + 1
                    break

            if res is None:                          # If not found, pass
                pass
            else:                                    # If found, extract the data from the string
                data = string[res-5:res+2]
                print(data)

            res1 = None
            for i in range(0, len(string)):    # Search a xx\xx\xx structure in the string
                if string[i] == "L":                 # If not found, pass
                    res1 = i + 1
                    break

            if res1 is None:                         # If found, extract the data from the string
                pass
            else:
                data1 = string[res1-1:res1 + 7]
                print(data1)

            with open('Data.txt', 'w') as f:  # Create/ open 'Data.txt'
                f.write(string)  # Wirte string in txt
                f.write('\n')

            #print(string)

    return imgCropped


while True:

    path = "Resources/Paquete1.jpg"  # Path of the img
    img = cv2.pyrDown(cv2.imread(path))  # Read img and scale it down

    # Next lines are just for preprocessing the image

    imgContour = img.copy()
    cropped = img.copy()

    imgBlur = cv2.GaussianBlur(img, (5, 5), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    # Get values from sliders
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")

    # Continue with preprocessing
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    # Call getContours function (read image) and store it in 'imgCroped'
    imgCropped = getContours(imgDil, imgContour)

    # Just some stuff to scale down the image

    """scale_percent = 50  # percent of original size
    width = int(imgContour.shape[1] * scale_percent / 100)
    height = int(imgContour.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized = cv2.resize(imgContour, dim, interpolation=cv2.INTER_AREA)

     Show images
     cv2.imshow("Result", resized)
     cv2.imshow("Result2", imgCropped)"""

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
