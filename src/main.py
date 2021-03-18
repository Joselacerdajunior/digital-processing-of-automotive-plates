from lib.myLib import *
nameImages = [
    'img1.jpg',
    'img2.jpg',
    'img3.jpg',
    'img4.jpg'
]
platesInDataBase = ["EWK-7037", "RIO2A18"]
plates = ["", "", "", ""]
authorization = ["", "", "", ""]
image = ""
height = 0
width = 0
channels = 0

def showInfo():
    print("###  START  ###")
    print("")
    print("List of authorized plates:")
    for index, plate in enumerate(platesInDataBase):
        print("Plate %d - %s" % (index+1, platesInDataBase[index]))

    print("")
    print( "|---------------------------------------------|")
    print(f"|" + "{:^15}".format("Image") + "{:^15}".format("Plate") + "{:^15}".format("Status") + "|")
    print( "|---------------------------------------------|")        
    print(f"|" + "{:^15}".format(nameImages[0]) + "{:^15}".format(plates[0]) + "{:^15}".format(authorization[0]) + "|")
    print(f"|" + "{:^15}".format(nameImages[1]) + "{:^15}".format(plates[1]) + "{:^15}".format(authorization[1]) + "|")
    print(f"|" + "{:^15}".format(nameImages[2]) + "{:^15}".format(plates[2]) + "{:^15}".format(authorization[2]) + "|")
    print(f"|" + "{:^15}".format(nameImages[3]) + "{:^15}".format(plates[3]) + "{:^15}".format(authorization[3]) + "|")
    print( "|---------------------------------------------|")
    print()

    print("###  FINISH  ###")


for x in range(0, len(nameImages)):
    image = cv2.imread('./img/%s' % nameImages[x])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   
    threshImage = thresholding(image)
    noiseImage = remove_noise(threshImage)

    #cv2.imshow("IMG-%d"%x, noiseImage)
    cv2.imwrite("imageToConvert.jpg", noiseImage)    
    custom_config = r'-c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz%#@$“‘\|/ --psm 6'
    plateText = pytesseract.image_to_string('imageToConvert.jpg', config=custom_config).replace(" ", "").replace("“", "").replace("\n","")

    if (len(plateText) > 8):
        plates[x] = plateText[:8]
    elif (len(plateText) > 7):
        plates[x] = plateText[:7]
    else:
        print ("Não identificado")
    
    if (plates[x].replace(" ", "") in platesInDataBase):
        authorization[x] = "Authorized"
    else:
        authorization[x] = "Refused"

showInfo()