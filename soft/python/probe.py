from yolo_detection_multi import multi_object_detect
import yolo_detection_multi
import cv2
import time
from math import sqrt


class Object():

    def __init__(self,number_obj):
        self.coordinates = [width//2+30*(number_obj-1), height//2]
        self.id_obj = number_obj
        self.find = False
        self.counter=0

    def get_nearest_point(self,data):
        min_vector = sqrt(height ** 2 + width ** 2)
        x_obj, y_obj = self.coordinates
        find_i=0
        i=0
        for x, y in data:
            vector = sqrt((x - x_obj) ** 2 + (y - y_obj) ** 2)
            if vector<min_vector:
                min_vector=vector
                find_i=i
            i+=1
        return data[find_i]






class Wheel(Object):
    id=0

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


def sort_coordinates(data,objects,img):
    id = objects[0].id
    length=len(data[id])
    if length==0:
        return
    #print(f'length is equal {length}')
    i = 0
    while data[id]!=[]:
        min_vector = sqrt(height ** 2 + width ** 2)
        x,y=data[id][i]
        for object in objects:
            if object.find==False:
                x_obj,y_obj=object.coordinates
                vector=sqrt((x-x_obj)**2+(y-y_obj)**2)
                if vector<min_vector:
                    min_vector=vector
                    ind_find=object.id_obj

        nearest_point=objects[ind_find-1].get_nearest_point(data[id])
        if (objects[ind_find - 1].find == False) and (nearest_point==[x,y]):
            objects[ind_find-1].coordinates=[x,y]
            objects[ind_find-1].find=True
            data[id].pop(i)
            length-=1

        i+=1
        if i>(length-1):
            i=0

    print('+++++++++')

    for object in objects:
        if object.counter>1:
            object.coordinates=[0,0]
        if object.find==False:
            object.counter+=1
        else:
            object.counter=0

    for object in objects:
        cv2.putText(img, str(object.id_obj), object.coordinates, cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
        object.find=False



if __name__=='__main__':
    # config camera and port
    cap = cv2.VideoCapture(0)
    height = 480
    width = 640

    wheels = []

    for i in range(1, 3):
        wheels.append(Wheel(number_obj=i))

    while True:
        _, img = cap.read()
        img = cv2.resize(img, (width,height))
        img = cv2.flip(img, 1)
        start = time.time()
        return_list = multi_object_detect(img)

        sort_coordinates(data=return_list,objects=wheels,img=img)

        end = time.time()
        cv2.putText(img, "{} fps".format(round(1 / (end - start), 2)), (20, 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
        cv2.imshow("Image", img)
        cv2.waitKey(1)