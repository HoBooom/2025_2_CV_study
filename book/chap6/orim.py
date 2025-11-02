import cv2 as cv
import numpy as np
import sys
from PyQt5.QtWidgets import *
from PIL import Image

class Orim(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Orim")
        self.setGeometry(100,100,800,600)

        fileButton=QPushButton("File",self)
        paintButton=QPushButton("Paint",self)
        cutButton=QPushButton("Cut",self)
        incButtom=QPushButton("+",self)
        decButtom=QPushButton("-",self)
        saveButton=QPushButton("Save",self)
        quitButton=QPushButton("Quit",self)

        fileButton.setGeometry(10,10,100,30)
        paintButton.setGeometry(110,10,100,30)
        cutButton.setGeometry(210,10,100,30)
        incButtom.setGeometry(310,10,100,30)
        decButtom.setGeometry(410,10,100,30)
        saveButton.setGeometry(510,10,100,30)
        quitButton.setGeometry(610,10,100,30)

        fileButton.clicked.connect(self.fileFunction)
        paintButton.clicked.connect(self.paintFunction)
        cutButton.clicked.connect(self.cutFunction)
        incButtom.clicked.connect(self.incFunction)
        decButtom.clicked.connect(self.decFunction)
        saveButton.clicked.connect(self.saveFunction)
        quitButton.clicked.connect(self.quitFunction)

        self.BrushSiz=5
        self.LColor,self.RColor=(255,0,0),(0,0,255)

    def fileFunction(self):
        fname=QFileDialog.getOpenFileName(self,"Open Image","./image/","Image Files(*.jpg *.jpeg *.png *.bmp)")
        print(fname)
        
        # 파일이 선택되었는지 확인
        if not fname[0]:
            return
            
        # 한글 경로 문제 해결을 위해 PIL을 사용한 이미지 로드
        try:
            # PIL로 먼저 읽기 (한글 경로 지원)
            pil_img = Image.open(fname[0])
            # PIL을 numpy 배열로 변환
            img_array = np.array(pil_img)
            # RGB를 BGR로 변환 (OpenCV 형식)
            if len(img_array.shape) == 3:
                self.img = cv.cvtColor(img_array, cv.COLOR_RGB2BGR)
            else:
                self.img = img_array
                
        except Exception as e:
            print(f"PIL 로드 실패: {e}")
            # 기본 방법으로 시도
            self.img = cv.imread(fname[0])
            
        # 기본 이미지로 대체
        if self.img is None:
            try:
                self.img = cv.imread('./image/bed1.jpeg')
                if self.img is None:
                    self.img = cv.imread('./book/chap6/image/bed1.jpeg')
            except:
                pass
        
        if self.img is None: 
            QMessageBox.warning(self, "Error", "Cannot find or open file")
            return
            
        # mask 초기화 (기본값은 GC_PR_BGD = 3)
        self.mask = np.zeros(self.img.shape[:2], np.uint8) + cv.GC_PR_BGD
        # grabImg 초기화
        self.grabImg = None
        
        # 이미지를 화면에 표시
        cv.namedWindow('Painting', cv.WINDOW_NORMAL)
        cv.imshow('Painting', self.img)
        print(f"이미지 로드 성공: {self.img.shape}")

    def paintFunction(self):
        if not hasattr(self, 'img') or self.img is None:
            QMessageBox.warning(self, "Error", "Please open an image first")
            return
        # 'Painting' 윈도우가 없으면 생성
        try:
            if cv.getWindowProperty('Painting', cv.WND_PROP_VISIBLE) < 1:
                cv.namedWindow('Painting', cv.WINDOW_NORMAL)
                cv.imshow('Painting', self.img)
        except:
            cv.namedWindow('Painting', cv.WINDOW_NORMAL)
            cv.imshow('Painting', self.img)
        # 마우스 콜백 설정
        cv.setMouseCallback('Painting', self.painting)

    def painting(self,event,x,y,flags,param):
        if event==cv.EVENT_LBUTTONDOWN:
            cv.circle(self.img,(x,y),self.BrushSiz,self.LColor,-1)
            cv.circle(self.mask,(x,y),self.BrushSiz,cv.GC_FGD,-1)
        elif event==cv.EVENT_RBUTTONDOWN:
            cv.circle(self.img,(x,y),self.BrushSiz,self.RColor,-1)
            cv.circle(self.mask,(x,y),self.BrushSiz,cv.GC_BGD,-1)
        elif event==cv.EVENT_MOUSEMOVE and flags==cv.EVENT_FLAG_LBUTTON:
            cv.circle(self.img,(x,y),self.BrushSiz,self.LColor,-1)
            cv.circle(self.mask,(x,y),self.BrushSiz,cv.GC_FGD,-1)
        elif event==cv.EVENT_MOUSEMOVE and flags==cv.EVENT_FLAG_RBUTTON:
            cv.circle(self.img,(x,y),self.BrushSiz,self.RColor,-1)
            cv.circle(self.mask,(x,y),self.BrushSiz,cv.GC_BGD,-1)
        cv.imshow('Painting',self.img)

    def cutFunction(self):
        if not hasattr(self, 'img') or self.img is None:
            QMessageBox.warning(self, "Error", "Please open an image first")
            return
        if not hasattr(self, 'mask'):
            QMessageBox.warning(self, "Error", "Please paint foreground/background first")
            return
        background=np.zeros((1,65),np.float64)
        foreground=np.zeros((1,65),np.float64)
        cv.grabCut(self.img,self.mask,None,background,foreground,5,cv.GC_INIT_WITH_MASK)
        mask2=np.where((self.mask==2)|(self.mask==0),0,1).astype('uint8')
        self.grabImg=self.img*mask2[:,:,np.newaxis]
        cv.namedWindow('Scissoring', cv.WINDOW_NORMAL)
        cv.imshow('Scissoring',self.grabImg)
    
    def incFunction(self):
        self.BrushSiz=min(20,self.BrushSiz+1)

    def decFunction(self):
        self.BrushSiz=max(1,self.BrushSiz-1)
    
    def saveFunction(self):
        if not hasattr(self, 'grabImg') or self.grabImg is None:
            QMessageBox.warning(self, "Error", "Please perform cut operation first")
            return
        fname=QFileDialog.getSaveFileName(self,"Save Image","./image/","Image Files(*.jpg *.jpeg *.png *.bmp)")
        if fname[0]:  # 파일명이 선택되었는지 확인
            # 한글 경로 문제 해결을 위해 PIL 사용
            try:
                # BGR을 RGB로 변환
                rgb_img = cv.cvtColor(self.grabImg, cv.COLOR_BGR2RGB)
                pil_img = Image.fromarray(rgb_img)
                pil_img.save(fname[0])
                QMessageBox.information(self, "Success", "Image saved successfully")
            except Exception as e:
                print(f"PIL 저장 실패: {e}")
                # 기본 방법으로 시도
                cv.imwrite(fname[0], self.grabImg)
    
    def quitFunction(self):
        cv.destroyAllWindows()
        self.close()

app=QApplication(sys.argv)
win=Orim()
win.show()
sys.exit(app.exec_())


