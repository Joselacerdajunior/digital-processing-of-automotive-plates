from lib.myLib import *
import os

nameImages = [
    'img1.jpg',
    'img2.jpg',
    'img3.jpg',
    'img4.jpg'
]
platesInDataBase = ["EWK-7037", "RIO2A18", "AAA-3333"]
plates = ["", "", "", ""]
authorization = ["", "", "", ""]
image = ""
height = [ 0, 0, 0, 0]
width = [ 0, 0, 0, 0]
channels = [ 0, 0, 0, 0]
red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
default = '\033[0m'
bold = '\033[1m'

def showInfo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\033[95m' + "{:#^92}".format("   START   ") + '\033[0m')
    print("")
    print("List of authorized plates:")
    for index, plate in enumerate(platesInDataBase):
        print(" - Plate %d -> %s%s%s" % (index+1, bold, platesInDataBase[index], default))
    print("")
    print( ".------------------------------------------------------------------------------------------.")
    print(f"|" + yellow + "{:^15}".format("Image") + "{:^15}".format("Plate") + "{:^15}".format("Status") + "{:^15}".format("Width") + "{:^15}".format("Height") + "{:^15}".format("Channels") + default + "|")
    print( "|------------------------------------------------------------------------------------------|")        
    print(f"|" + "{:^15}".format(nameImages[0]) + bold + "{:^15}".format(plates[0]) + default + (red if authorization[0] == "Refused" else green) + "{:^15}".format(authorization[0]) + default + "{:^15}".format("%d%s" % (width[0], " px")) + "{:^15}".format("%d%s" % (height[0], " px")) + "{:^15}".format(channels[0]) + "|")
    print(f"|" + "{:^15}".format(nameImages[1]) + bold + "{:^15}".format(plates[1]) + default + (red if authorization[1] == "Refused" else green) + "{:^15}".format(authorization[1]) + default + "{:^15}".format("%d%s" % (width[1], " px")) + "{:^15}".format("%d%s" % (height[1], " px")) + "{:^15}".format(channels[1]) + "|")
    print(f"|" + "{:^15}".format(nameImages[2]) + bold + "{:^15}".format(plates[2]) + default + (red if authorization[2] == "Refused" else green) + "{:^15}".format(authorization[2]) + default + "{:^15}".format("%d%s" % (width[2], " px")) + "{:^15}".format("%d%s" % (height[2], " px")) + "{:^15}".format(channels[2]) + "|")
    print(f"|" + "{:^15}".format(nameImages[3]) + bold + "{:^15}".format(plates[3]) + default + (red if authorization[3] == "Refused" else green) + "{:^15}".format(authorization[3]) + default + "{:^15}".format("%d%s" % (width[3], " px")) + "{:^15}".format("%d%s" % (height[3], " px")) + "{:^15}".format(channels[3]) + "|")
    print( "'------------------------------------------------------------------------------------------'")
    print()
    print('\033[95m' + "{:#^92}".format("   STOP   ") + '\033[0m')


for x in range(0, len(nameImages)):
    image = cv2.imread('./img/%s' % nameImages[x])
    height[x] = image.shape[0]
    width[x] = image.shape[1]
    channels[x] = image.shape[2]   
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)   
    threshImage = thresholding(image)
    noiseImage = remove_noise(threshImage)
    noiseImage = remove_noise(noiseImage)
    #cv2.imshow("IMG-%d"%x, noiseImage)
    cv2.imwrite("imageToConvert" + str(x) + ".jpg", noiseImage)

    if (width[x] < 700):
        #custom_config = r'-c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz%#()@$“‘\|/ --psm 7'
        custom_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ-0123456789 --psm 7'
    else:
        #custom_config = r'-c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz%#()@$“‘\|/ --psm 8'
        custom_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ-0123456789 --psm 8'

    plateText = pytesseract.image_to_string('imageToConvert' + str(x) + '.jpg', config=custom_config).replace(" ", "").replace("\n", "")
    if (len(plateText) >= 8):
        #plates[x] = plateText[:8]
        plates[x] = plateText
    elif (len(plateText) >= 7):
        #plates[x] = plateText[:7]
        plates[x] = plateText
    else:
        print ("Não identificado")    
    if (plates[x].replace(" ", "") in platesInDataBase):
        authorization[x] = "Authorized"
    else:
        authorization[x] = "Refused"

showInfo()