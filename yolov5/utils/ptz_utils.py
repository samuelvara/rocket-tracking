import numpy as np 
import cv2

def get_zoom_focus(boxes, h, w):
    if not boxes:
        return 1, (h//2, w//2)
    boxes = list(boxes)
    boxes.sort()
    lt = boxes[0]
    rb = boxes[-1]

    p, q = rb[0] - lt[0], rb[1] - lt[1]

    return 1/max(2*q/h, 3*p/w), ((lt[0]+rb[0])//2, (lt[1]+rb[1])//2)

def calc_mid(a, b):
    (x1, y1), (x2, y2) = a, b
    return (x1+x2) // 2, (y1+y2)//2

def zoom_at(img, zoom=1, coordinates = None):
    h, w, _ = img.shape
    if coordinates is None:
        coordinates = w//2, h//2
    
    nh, nw = int(h*zoom), int(w*zoom)
    new_coordinates = [int(coordinates[0]*zoom), int(coordinates[1]*zoom)]

    if new_coordinates[0]-w//2 < 0:
        new_coordinates[0] = w//2
    elif new_coordinates[0]+w//2 > nw:
        new_coordinates[0] = (nw - w//2)
    
    if new_coordinates[1]-h//2 < 0:
        new_coordinates[1] = h//2
    elif new_coordinates[1]+h//2 > nh:
        new_coordinates[1] = (nh - h//2)

    
    new_img = cv2.resize(img, None, fx=zoom, fy=zoom)
    sw, ew = new_coordinates[0] - w//2, new_coordinates[0] + w//2
    sh, eh = new_coordinates[1] - h//2, new_coordinates[1] + h//2
    print(img.shape, new_img.shape, sw, ew, sh, eh)
    new_img = new_img[sh:eh, sw:ew]
    return new_img

def center_auto_zoom_at(img, boxes):
    h, w, _ = img.shape
    zoom_f, focus_pt = get_zoom_focus(boxes, h, w)
    cv2.circle(img, center=focus_pt, radius=5, color=(0, 255, 0), thickness=10)
    if zoom_f < 1:
        zoom_f = 1
    elif zoom_f > 3:
        zoom_f = 3
    zoom_f = min(zoom_f, 1)
    zoomed_img = zoom_at(img, zoom_f, focus_pt)
    return zoomed_img