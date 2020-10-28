import numpy as np
import cv2 
import os

def check_annotations(file_name, img_dir, ann_dir, show=True, outputdir=None):
    img = img_dir + file_name + '.png'
    ann_file = ann_dir + file_name + '.txt'
    
    print ("Processing: ", filename)
    
    ann_list = []
    img = cv2.imread(img)
    
    def convert_float(x):
        try:
            return int(float(x))
        except ValueError:
            return x
    
    
    with open(ann_file, 'r') as ann:
        lines = ann.readlines()
        for line in lines[2:]:
            arr = [convert_float(item) for item in line.split(' ')]
            try:
                x1, y1, x2, y2, x3, y3, x4,y4, classname, difficult = arr
            except ValueError:
                print ("{} has NOT ENOUGH VALUES.".format(filename))
                return
            ann_list.append((x1, y1, x2, y2, x3, y3, x4, y4, classname))


    for item in ann_list:
        x1, y1, x2, y2, x3, y3, x4, y4, classname = item
        pts = np.array([[x1,y1], [x2,y2], [x3,y3], [x4,y4]], np.int32)
        pts = pts.reshape(-1, 1, 2)
        img = cv2.polylines(img, [pts], True, (0,255,255))
        img = cv2.putText(img, classname, (x1-5, y1-5), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)
    
    if show:    
        cv2.imshow("COLORED", img)
        cv2.waitKey(0)
    else:
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            cv2.imwrite(output_dir + file_name + '.png', img)
        
if __name__ == '__main__':
    img_dir = 'images/'
    ann_dir = 'orig_labelTxt/'
    
    filenames = os.listdir(ann_dir)
    for filename in filenames:
        if '.txt' in filename:
            if 'fold' in filename or 'annotation1024' in filename:
                continue
            filename = filename.replace('.txt', '')
            check_annotations(file_name=filename, img_dir=img_dir, ann_dir=ann_dir, show=True)