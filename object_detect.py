from vision.ssd.mobilenetv1_ssd import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor
import cv2
# from .s125_check_base import OBJ
import time



def object_detection(img):
    """Hàm chạy dựa trên hình ảnh đưa vào. Định dạng đầu vào của ảnh là BGR
    mô hình yêu cầu hình RGB, nên trước đi chạy phải kiểm tra định dạng màu
    Hàm trả ra các giá trị đặc trưng của vât thể: danh sách vật thể, vị trí
    và hình có đánh nhãn
    """
    label_path = 'models/labels.txt' 
    model_path = 'models/mb1-ssd-Epoch-42-Loss-1.2704596519470215.pth'
    # lưu các giá trị đọc được từ file labels.txt
    class_names = [name.strip()
                        for name in open(label_path).readlines()]
    # Tạo mảng với các nhãn đã đọc được
    net = create_mobilenetv1_ssd(len(class_names), is_test=True)
    # Tải mô hình vào bộ nhớ
    net.load(model_path)
    predictor = create_mobilenetv1_ssd_predictor(net, candidate_size=200)


    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes, labels, probs = predictor.predict(image, 10, 0.2)
    obj_list = labels.tolist()
    prob = probs.tolist()
    cordi = []
    for i in range(boxes.size(0)):
        box = boxes[i, :]
        box_1 = int(boxes[i, 0])
        box_2 = int(boxes[i, 1])
        box_3 = int(boxes[i, 2])
        box_4 = int(boxes[i, 3])
        x = int((box_1 + box_3) / 2)
        y = int((box_2 + box_4) / 2)
        # cor = int((x + y) / 2)
        label = f"{class_names[labels[i]]}: {probs[i]:.2f}"
        cv2.putText(img, label,(int(box[0]-25), int(box[1]) + 25),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 255),2)
        cv2.rectangle(img, (box_1, box_2), (box_3, box_4), (255, 0, 255), thickness=1)
        # cordi.append(cor)
        # print(cordi)
    if len(obj_list) == 2:
        print("Phat hien duoc 2 tem")
        #Xet toa do cua 2 tem
        #.....
        signal_left = True
        signal_right = True
    else:
        print("Loi thieu tem hoac du tem - bao NG")
        signal_left = False
        signal_right = False
    # cv2.imshow("object detection",img)
    return signal_left,signal_right,img
    # return obj_list, cordi, prob,img



if __name__ == '__main__':
    start = time.time()
    img = cv2.imread('test_img/test5.jpg')
    a,b,im = object_detection(img)
    print("time: ",time.time()-start)
    cv2.imshow("IM",im)
    cv2.waitKey()
#     image = cv2.imread(r"D:\MinhVo\Deep\data\data\JPEGImages\Left180_1.jpg")
#     a, b, c, img = run.object_detection(image)
#     cv2.imshow("img", img)
#     cv2.waitKey()
#     print(a, b, c)