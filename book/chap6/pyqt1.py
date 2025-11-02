from PyQt5.QtWidgets import *
import sys
import platform
import os
import subprocess
import threading
import time

class BeepSound(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beep Sound")
        self.setGeometry(200,200,500,100)
        shortBeepButton=QPushButton('Short Beep',self)
        longBeepButton=QPushButton('Long Beep',self)
        quitButton=QPushButton('Quit',self)
        
        self.label=QLabel('welcome',self)

        shortBeepButton.setGeometry(10,10,100,30)
        longBeepButton.setGeometry(110,10,100,30)
        quitButton.setGeometry(210,10,100,30)
        self.label.setGeometry(10,50,180,30)

        shortBeepButton.clicked.connect(self.shortBeepFunction)
        longBeepButton.clicked.connect(self.longBeepFunction)
        quitButton.clicked.connect(self.quitFunction)

    def play_beep(self, duration_ms, sound_type='short'):
        """플랫폼에 따라 적절한 소리 재생"""
        system = platform.system()
        if system == 'Windows':
            try:
                import winsound
                winsound.Beep(1000, duration_ms)
            except ImportError:
                print("winsound 모듈을 사용할 수 없습니다.")
        elif system == 'Darwin':  # macOS
            # macOS에서 시스템 사운드 재생 (백그라운드에서 실행)
            def play_sound():
                # 짧은 비프: Glass.aiff, 긴 비프: 여러 번 재생 또는 다른 사운드
                if sound_type == 'short':
                    subprocess.Popen(['afplay', '/System/Library/Sounds/Glass.aiff'], 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL)
                else:  # long
                    # 긴 비프는 여러 번 재생하거나 더 긴 사운드 사용
                    for _ in range(3):
                        subprocess.Popen(['afplay', '/System/Library/Sounds/Glass.aiff'], 
                                      stdout=subprocess.DEVNULL, 
                                      stderr=subprocess.DEVNULL).wait()
                        time.sleep(0.2)
            threading.Thread(target=play_sound, daemon=True).start()
        else:  # Linux 등
            # 터미널 벨 문자 사용
            os.system(f'printf "\a"')

    def shortBeepFunction(self):
        self.label.setText('short beep')
        self.play_beep(500, 'short')

    def longBeepFunction(self):
        self.label.setText('long beep')
        self.play_beep(3000, 'long')

    def quitFunction(self):
        self.close()

app=QApplication(sys.argv)
beepSound=BeepSound()
beepSound.show()
sys.exit(app.exec_())