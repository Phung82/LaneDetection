#Import các thư viện hỗ trợ
import cv2
import numpy as np
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog as fd
import PIL
from PIL import Image, ImageTk, ImageEnhance
from bin import model

class Application(Frame):
    def __init__(self):
        super().__init__()
        self.master.title("Đồ Án Môn Học")
        self.pack()

        menubar = Menu(self.master)
        #menu
        filemenu = Menu(menubar, tearoff = 0)
        filemenu.add_command(label= "Open", command=self.Open_file)
        filemenu.add_command(label= "Connect", command=self.Show_dis)
        filemenu.add_separator()
        filemenu.add_command(label= "Exit", command=self.master.destroy)
        menubar.add_cascade(label= "Chức năng", menu=filemenu)

        controlmenu = Menu(menubar, tearoff=0)
        controlmenu.add_command(label = "Bảng điều khiển",command=self.master.destroy)
        menubar.add_cascade(label = "Điều khiển", menu=controlmenu)

        aboutmenu = Menu(menubar, tearoff=0)
        aboutmenu.add_command(label = "Thông tin",command=self.About)
        aboutmenu.add_command(label = "Hướng dẫn",command=self.hdsd)
        menubar.add_cascade(label= "Giới thiệu", menu = aboutmenu)
        self.master.config(menu = menubar)
        #top

        frame = Frame(self.master)
        frame.pack()
        self.label_tieude = Label(frame,pady=20, text="NHẬN DIỆN LÀN ĐƯỜNG CHO XE TỰ LÁI",fg="Blue",font=("arial", 24,"bold"),padx=20)
        self.label_tieude.pack()
        
        #middel frame
        left = Frame(self.master, borderwidth=2, relief="solid")
        right = Frame(self.master, borderwidth=2, relief="solid")
        container = Frame(left, borderwidth=2, relief="solid")
        self.fr_button = Frame(left, borderwidth=2, relief="solid")
        self.box_left = Frame(right, borderwidth=2, relief="solid")
         
        label3 = Label(self.fr_button, text=' Các tùy chọn',padx=50,height="1",font=("arial", 12))
        label3.pack()

        left.pack(side="left", expand=True, fill="both")
        right.pack(side="right", expand=True, fill="both")
        container.pack(expand=True, padx=1, pady=1)
        self.fr_button.pack(expand=True, fill="both", padx=1, pady=1)
        self.box_left.pack(expand=True, fill="both", padx=1, pady=1)

        
        #hiển thị ảnh nền
        self.img_fn = Image.open("./bin/anh-fn.jpg")
        #reimg=self.img.resize((1000,600),Image.ANTIALIAS)
        self.tatras_fn = ImageTk.PhotoImage(self.img_fn)        
        canvas_fn = Canvas(container, width=693, height=416)
        canvas_fn.create_image(1, 1, anchor=NW, image=self.tatras_fn)
        canvas_fn.pack()
        #hiển thị logo bìa
        self.img_lg = Image.open("./bin/logo.png")
        reimg=self.img_lg.resize((100,100),Image.ANTIALIAS)
        self.tatras_lg = ImageTk.PhotoImage(reimg)        
        canvas_lg = Canvas(self.box_left, width=220, height=130)
        canvas_lg.create_image(80, 10,anchor=NW, image=self.tatras_lg)
        canvas_lg.pack(fill=Y)

        #mục bìa
        Label(self.box_left, text="    ĐỒ ÁN MÔN HỌC",height="1",fg="Blue",font=("arial", 18,"bold"),pady=20).pack()
        Label(self.box_left, text="ĐỀ TÀI: TÌM HIỂU THƯ VIỆN OPENCV, NGÔN NGỮ LẬP TRÌNH PYTHON",height="1",fg="Red",font=("arial", 14),pady=5).pack()
        Label(self.box_left, text="VIẾT ỨNG DỤNG NHẬN DIỆN LÀN ĐƯỜNG CHO XE TỰ LÁI",height="1",fg="Red",font=("arial", 14),pady=20).pack()
        Label(self.box_left, text="  Nhóm Thực Hiện",height="1",fg="Blue",font=("arial", 14),pady=20).pack()
        Label(self.box_left,anchor="w", text=" Giáo viên hướng dẫn:",height="1",font=("arial", 14)).pack(fill=X)
        Label(self.box_left,anchor="w", text=' Thạc sĩ    Ngô Thanh Tú',padx=50,height="1",font=("arial", 14)).pack(fill=X)
        Label(self.box_left,anchor="w", text=" Thành viên thực hiện:",height="1",font=("arial", 14),pady=10).pack(fill=X)
        Label(self.box_left,anchor="w", text=' Nguyễn Tiểu Phụng       17DDS0703132',padx=50,height="1",font=("arial", 14)).pack(fill=X)
        Label(self.box_left,anchor="w", text=' Huỳnh Đức Anh Tuấn    17DDS0703143',padx=50,height="1",font=("arial", 14)).pack(fill=X)

        #button
        
        bottomframe = Frame(self.fr_button,pady=20)
        bottomframe.pack()
        bottomframe_1 = Frame(bottomframe,padx=20)
        bottomframe_1.pack(side = LEFT)
        # Tạo button xử lý hiệu hứng - gọi lại hàm locanh()
        self.process_btn = Button(bottomframe_1, text = "Chọn kết nối", fg = "black",bg='#0caffc',padx=20,command=self.Open_file)
        self.process_btn.pack( )
        bottomframe_3 = Frame(bottomframe,padx=20)
        bottomframe_3.pack(side = LEFT)
        #tạo button để mở chọn ảnh - gọi lại hàm Open_file()
        self.choose_btn = Button(bottomframe_3, text = "Kết nối",state=DISABLED, fg = "black",bg='#00ccff',padx=20,command=self.Show_dis)
        self.choose_btn.pack()
        bottomframe_2 = Frame(bottomframe,padx=20)
        bottomframe_2.pack(side = LEFT)
        #tạo button để save ảnh - gọi lại hàm Save_file()
        self.exit_btn = Button(bottomframe_2, text = "Thoát", fg="black",bg='#00f6ff',padx=20,command=self.master.destroy)
        self.exit_btn.pack()

    #Hàm lấy đường dẫn liên kết
    def Open_file(self):
        try:
            File=fd.askopenfilename(title="Open",filetype=[("file .mp4","*.mp4"),("file .avi","*.avi"),("All files","*")])

            self.img_bathname=File
            #xử lý đường dẫn file bằng cawsch loại bỏ "/"
            self.path=self.img_bathname.split('/')
            #lấy tên file
            self.name_img=self.path[len( self.path)-1]
        except:
            #Xử lý lỗi không tìm thấy đường dẫn
            self.path_link = "Không tìm thấy đường dẫn - Chọn lại đường dẫn!"
        
        label2 = Label(self.fr_button, text=self.path[-1])
        self.choose_btn["state"]=NORMAL
        self.choose_btn["bg"]="#00ff1e"
        #self.process_btn["bg"]="#00ff1e"
        label2.pack()


    #hàm xử lý và hiển thị các khung hình
    def Show_dis(self):
        
        cameraFeed= False
        #videoPath = 'project_video.mp4'
        #videoPath = 'test5.mp4'
        videoPath = self.img_bathname
        print(videoPath)
        cameraNo= 1
            #qui định kích thước các khung hình
        frameWidth= 600    
        frameHeight = 400

        if cameraFeed:intialCotrol = [24,55,12,100] #  #wT,hT,wB,hB
        else:intialCotrol = [42,63,14,87]   #wT,hT,wB,hB

        ####################################################
        try:
            if cameraFeed:
                cap = cv2.VideoCapture(cameraNo)
                cap.set(3, frameWidth)
                cap.set(4, frameHeight)
            else:
                cap = cv2.VideoCapture(videoPath)
            count=0
            noOfArrayValues =10
            global arrayCurve, arrayCounter
            arrayCounter=0
            arrayCurve = np.zeros([noOfArrayValues])
            myVals=[]
            model.intialCotrol(intialCotrol)
        except:
            #Xử lý lỗi không tìm thấy đường dẫn
            label2 = Label(self.fr_button, text="Không tìm thấy kết nối!",fg = "Red")
            label2.pack()


        while True:
            success, img = cap.read()
            #img = cv2.imread('test-3.png')
            if cameraFeed== False:img = cv2.resize(img, (frameWidth, frameHeight), None)
            imgWarpPoints = img.copy()
            imgFinal = img.copy()
            imgCanny = img.copy()

            imgUndis = model.undistort(img)
            imgThres,imgCanny,imgColor = model.thresholding(imgUndis)
            src = model.valTrackbars()
            imgWarp = model.perspective_warp(imgThres, dst_size=(frameWidth, frameHeight), src=src)
            imgWarpPoints = model.drawPoints(imgWarpPoints, src)
            imgSliding, curves, lanes, ploty = model.sliding_window(imgWarp, draw_windows=True)

            try:
                curverad =model.get_curve(imgFinal, curves[0], curves[1])
                lane_curve = np.mean([curverad[0], curverad[1]])
                imgFinal = model.draw_lanes(img, curves[0], curves[1],frameWidth,frameHeight,src=src)

                # ## Average
                currentCurve = lane_curve // 50
                if  int(np.sum(arrayCurve)) == 0:averageCurve = currentCurve
                else:
                    averageCurve = np.sum(arrayCurve) // arrayCurve.shape[0]
                if abs(averageCurve-currentCurve) >200: arrayCurve[arrayCounter] = averageCurve
                else :arrayCurve[arrayCounter] = currentCurve
                arrayCounter +=1
                if arrayCounter >=noOfArrayValues : arrayCounter=0
                cv2.putText(imgFinal, str(int(averageCurve)), (frameWidth//2-70, 70), cv2.FONT_HERSHEY_DUPLEX, 1.75, (0, 0, 255), 2, cv2.LINE_AA)

            except:
                lane_curve=00
                pass

            imgFinal= model.drawLines(imgFinal,lane_curve)           
            
            imgThres = cv2.cvtColor(imgThres,cv2.COLOR_GRAY2BGR)
            imgBlank = np.zeros_like(img)
            

            #dặt tên khung hình
            img = cv2.putText(img,"Input", (50, 25), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0) ,2, cv2.LINE_AA, False)
            iimgCanny = cv2.putText(imgCanny,"Canny", (50, 25), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0) ,2, cv2.LINE_AA, False)
            imgWarp = cv2.putText(imgWarp,"Warp", (50, 25), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0) ,2, cv2.LINE_AA, False)
            imgThres = cv2.putText(imgThres,"Thresh", (50, 25), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0) ,2, cv2.LINE_AA, False)
            imgWarpPoints = cv2.putText(imgWarpPoints,"WarpPoints", (50, 25), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0) ,2, cv2.LINE_AA, False)
            imgFinal = cv2.putText(imgFinal,"Output", (50, 25), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0) ,2, cv2.LINE_AA, False)
            #Quy định vị trí các khung hình
            imgStacked = model.stackImages(0.7, ([imgWarp, imgCanny, imgThres],
                                                [img,imgWarpPoints,imgFinal]
                                                ))
            #hiển thị các khung hình
            cv2.imshow("Creen",imgStacked)
            #cv2.imshow("Result", imgFinal)
            #tắt screen
            c = cv2.waitKey(1) 
            if c == 27:
                break 

        cap.release()
        cv2.destroyAllWindows()

    #tạo cửa xổ giới thiệu
    def About(self):
       self.box_left = Toplevel(self.master)
       self.box_left.title("About")
       Label(self.box_left,fg="red", text="HỌC PHẦN NHẬP MÔN XỬ LÝ ẢNH",height="1",font=("arial", 17),padx=200).pack()
       Label(self.box_left, text="    ĐỒ ÁN MÔN HỌC",height="1",fg="Blue",font=("arial", 18,"bold"),pady=20).pack()
       Label(self.box_left, text="ĐỀ TÀI: TÌM HIỂU THƯ VIỆN OPENCV, NGÔN NGỮ LẬP TRÌNH PYTHON",height="1",fg="Red",font=("arial", 14),pady=5).pack()
       Label(self.box_left, text="VIẾT ỨNG DỤNG NHẬN DIỆN LÀN ĐƯỜNG CHO XE TỰ LÁI",height="1",fg="Red",font=("arial", 14),pady=20).pack()
       Label(self.box_left, text="  Nhóm Thực Hiện",height="1",fg="Blue",font=("arial", 14),pady=20).pack()
       Label(self.box_left,anchor="w", text=" Giáo viên hướng dẫn:",height="1",font=("arial", 14)).pack(fill=X)
       Label(self.box_left,anchor="w", text=' Thạc sĩ    Ngô Thanh Tú',padx=50,height="1",font=("arial", 14)).pack(fill=X)
       Label(self.box_left,anchor="w", text=" Thành viên thực hiện:",height="1",font=("arial", 14),pady=10).pack(fill=X)
       Label(self.box_left,anchor="w", text=' Nguyễn Tiểu Phụng       17DDS0703132',padx=50,height="1",font=("arial", 14)).pack(fill=X)
       Label(self.box_left,anchor="w", text=' Huỳnh Đức Anh Tuấn    17DDS0703143',padx=50,height="1",font=("arial", 14)).pack(fill=X)
       self.box_left.mainloop()

    #cửa sổ hướng dẫn sử dụng
    def hdsd(self):
       filewin = Toplevel(self.master)
       filewin.title("Hướng dẫn sử dụng")
       Label(filewin,fg="red", text="HƯỚNG DẪN SỬ DỤNG PHẦN MỀM",height="1",font=("arial", 17),padx=200,pady=20).pack()
       Label(filewin,anchor="w", text="- Bước 1: Chọn kết nối",height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text='+ Cách 1: Click vào button "Chọn kết nối"',padx=30,height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text='+ Cách 2: Chức năng -> Open',padx=30,height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text="- Bước 2: Tiến hành kết nối",height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text='+ Cách 1: Click vào button "Kết nối"',padx=30,height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text='+ Cách 2: Chức năng -> Connect"',padx=30,height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text="- Bước 3: Điều chỉnh thông số",height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text='+ Điều khiển thông số trên cửa sổ "Control"',padx=50,height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text='+ Width top: Điều chỉnh độ rộng khung nhìn tầm xa',padx=50,height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text='+ Height top: Điều chỉnh độ cao khung nhìn tầm xa',padx=50,height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text='+ Width bottom: Điều chỉnh độ rộng khung nhìn tầm gần',padx=50,height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text='+ Height bottom: Điều chỉnh độ cao khung nhìn tầm gần',padx=50,height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text="- Bước 4: Thoát khỏi cửa sổ Screen: Nhấn phím 'ESC:'",height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text="- Đóng ứng dụng:",height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text='+ Click Button "Thoát"',padx=50,height="1",font=("arial", 14)).pack(fill=X)
       Label(filewin,anchor="w", text='+ Chức năng -> Exit',padx=50,height="1",font=("arial", 14)).pack(fill=X)
       filewin.mainloop()  

def main():
    try:
        window = Tk()
        window.geometry("1400x700")
        app = Application()
        window.mainloop()
    except:
        pass


if __name__ == '__main__':
    main()     
