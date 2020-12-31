import cv2


def save_video(idx=3):
    vid = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output' + str(idx) + '.avi', fourcc, 8, (1280, 720))
    while True:
        ret, img = vid.read()  # frame shape 640*480*3
        if not ret:
            break
        out.write(img)
        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    out.release()
    vid.release()


def video_to_pics(video_path='/home/jiantang/work_datample_video.avi', video_out_path='/home/jiantang/work_data/'):
    print("video_to_pics start...")
    interval = 8
    vc = cv2.VideoCapture(video_path)
    c = 416
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        print('open error!')
        rval = False
    count_c = 1
    while rval:
        rval, frame = vc.read()
        if rval and count_c % interval == 0:
            print("dealing with frame : ", count_c)
            cv2.imwrite(video_out_path + str(int(c)) + '.jpg', frame)
            c += 1
        cv2.waitKey(1)
        count_c += 1
    vc.release()
    print("video_to_pics finished...")


if __name__ == '__main__':
    # save_video()
    video_path = "D:\\kang\\face_API\\output3.avi"
    video_out_path = "D:\\kang\\face_API\\trainset\\"
    video_to_pics(video_path, video_out_path)