import cv2
import pytesseract
import numpy as np


# import time

def empty():
    pass


digits = "0123456789"

# Tesseract is used to read text in images
# Must be instaled in the computer


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


# Get Contours and detect squares
def read_img(img_in, imgContour_in):
    data0 = "None"
    data1 = "None"
    contours, hierarchy = cv2.findContours(img_in, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # Find contours

    for cnt in contours:

        peri = 0.02 * cv2.arcLength(cnt, True)  # Calculate perimeter for every contour
        approx = cv2.approxPolyDP(cnt, peri, True)

        if len(approx) == 4:  # Search for rectangles with a concrete area
            # Color detection would be nice to have
            x, y, w, h = cv2.boundingRect(approx)

            imgCropped = imgContour_in[y:y + h, x:x + w]  # Crop image using bounding rect coordinates

            # Read text form cropped image
            imgCropped = cv2.cvtColor(imgCropped, cv2.COLOR_BGR2RGB)  # tesseract works with RGB

            string = pytesseract.image_to_string(imgCropped)  # Read and put text in a string
            # print(string)
            # Using Naive Method
            res = None
            for i in range(0, len(string)):  # Search a xx\xx\xx structure in the string
                if string[i] == "/" and string[i - 3] == "/":
                    res = i + 1
                    break

            if res is None:  # If not found, pass
                pass
            else:  # If found, extract the data from the string
                data0 = string[res - 6:res + 2]
                # print(data0)

            res1 = None
            count = 0
            length = 6
            for i in range(0, len(string)):  # Search a xx\xx\xx structure in the string
                if string[i] == "L":  # If not found, pass
                    substring = string[i:i + length]
                    for j in range(0, len(digits)):
                        if digits[j] in substring:
                            count += 1
                            # print(count)
                        else:
                            # print("else")
                            pass
                        if count >= length - 2:
                            res1 = i + 1
                            break

            if res1 is None:  # If found, extract the data from the string
                pass
            else:
                data1 = string[res1 - 1:res1 + length]
                # print(data1)

    return data0, data1


while True:

    path = "Resources/Paquete1.jpg"  # Path of the img
    img = cv2.pyrDown(cv2.imread(path))  # Read img and scale it down

    # Next lines are just for preprocessing the image

    imgContour = img.copy()

    imgBlur = cv2.GaussianBlur(img, (5, 5), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    # Continue with preprocessing
    imgCanny = cv2.Canny(imgGray, 73, 34)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    # Call getContours function (read image) and store it in 'imgCroped'
    data = read_img(imgDil, imgContour)

    date = data[0]
    lote = data[1]

    print(date)
    print(lote)

    with open('Data.txt', 'w') as f:  # Create/ open 'Data.txt'
        f.write(date)  # Write string in txt
        f.write('\n')
        f.write(lote)
        f.write('\n')

    # Just some stuff to scale down the image

    """ scale_percent = 50  # percent of original size
    width = int(imgContour.shape[1] * scale_percent / 100)
    height = int(imgContour.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized = cv2.resize(imgContour, dim, interpolation=cv2.INTER_AREA)

     Show images
     cv2.imshow("Result", resized)
     cv2.imshow("Result2", imgCropped) """

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
