# img_viewer.py

import PySimpleGUI as sg
import os.path
from PIL import Image
import math
import cmath





## resoulution handaling stuff


# n,m are coords of the box
# l, h are the length and height of a box
def getInd(n,m,w,h):
    points = []

    for i in range(w):
        for j in range(h):
            points.append((i + w*n, j + h*m))

    return points


# give img and another of the same size
def Compress(im, newImg, R):

    pixelMap = im.load()
    W, H = im.size

    Wn = int(W/R)
    Hn = int(H/R)

    pixelsNew = newImg.load()

    for n in range(Wn):
        for m in range(Hn):
            points = getInd(n, m, R, R)
            counter = 0
            sumo = 0
            sumt = 0
            sumth = 0
            for p in points:
                pix = pixelMap[p]
                if (pix == None or pix == (255,255,255)):
                    continue
                sumo += pix[0]
                sumt += pix[1]
                sumth += pix[2]
                counter += 1

            if counter == 0:
                counter = 1

            # avergae out the color and app\y
            sumo = int(sumo/counter)
            sumt = int(sumt/counter)
            sumth = int(sumth/counter)
            val = (sumo, sumt, sumth)
            for p in points:
                pixelsNew[p] = val


    return newImg















### complex number stuff









# Complex transformation
LW = 0
LH = 0

# Compute Function
def functionComp(z, eq):
    try:
        return (eval(eq), True)
    except (ZeroDivisionError):
        return (z, False)




def CompTrans(r,i,W,H,eq):

    sR = 1.0/W
    sC = 1.0/H

    #make number
    F = complex(r,i)

    # center
    F -= complex(W,H)/2

    # adjusting scale
    # z *= scale
    z = complex(F.real * sR, F.imag * sC)


    # do math
    z, status = functionComp(z,eq)


    # un scale + uncenter
    n = round((z.real * W) + W/2)
    m = round((z.imag * H) + H/2)


    if (n < W and n >= 0 and m < H and m >= 0):
        return (n, m, status)

    # if its not within the screen dont show
    return (n, m, False)




def transform(file, eq, R):

    im = Image.open(file)
    pixelMap = im.load()
    W, H = im.size



    # make new image (output)
    img = Image.new(im.mode, im.size)
    pixelsNew = img.load()

    # set background
    for i in range(W):
        for j in range(H):
            pixelsNew[i,j] = (255,255,255)


    # transform
    for i in range(W):
        for j in range(H):
            n, m, status = CompTrans(i, j, W, H, eq)
            if status:
                pixelsNew[n,m] = pixelMap[i,j]


    # Compress
    compressedImg = Image.new(im.mode, im.size)
    Compress(img, compressedImg, R)


    im.close()
    img.close()
    compressedImg.save("output.png")
    compressedImg.close()



































# First the window layout in 2 columns

file_list_column = [
 [
    sg.Text("Image Folder"),
    sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
    sg.FolderBrowse(),
 ],

 [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")],

 [sg.Text('Resoulution'), sg.Input(key='-IN-')],

 [sg.Text('Function'), sg.InputText(key='-INPUT-')],

 [sg.Button('Transform', enable_events=True, key='-TRANSFORM-',font=('Arial Bold', 12))]

]

# For now will only show the name of the file that was chosen
image_viewer_column = [
[sg.Text("Choose an image from list on left:")],
[sg.Text(size=(40, 1), key="-TOUT-")],
[sg.Image(key="-IMAGE-")],
]

# ----- Full layout -----
layout = [
[
   sg.Column(file_list_column),
   sg.VSeperator(),
   sg.Column(image_viewer_column),
]
]

window = sg.Window("Image Transformer", layout, resizable=True)


# get file Directory
dir_path = os.path.dirname(os.path.realpath(__file__))






# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break


# Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
           f
           for f in file_list
           if os.path.isfile(os.path.join(folder, f))
           and f.lower().endswith((".png", ".jpeg"))
        ]
        window["-FILE LIST-"].update(fnames)


    # A file was chosen from the listbox
    elif event == "-FILE LIST-":
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)

            im = Image.open(filename)
            im.save("temp.png", "PNG")

            window["-IMAGE-"].update(filename="temp.png")

        except:
            pass


    elif event == "-TRANSFORM-":
        try:
            func = values["-INPUT-"]
        except:
            funx = "z"

        try:
            res = int(values['-IN-'])
        except:
            res = 1

        transform(filename, func, res)
        




        window["-IMAGE-"].update(filename = dir_path + "/output.png")



window.close()
