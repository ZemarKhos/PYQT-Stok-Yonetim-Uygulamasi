from PyQt5 import QtWidgets
import os
import datetime
import manipulation as mp  #veri tabanı bağlantı işlemleri vs manipulation.py isimli dosya içerisinde gerçekleştirilmiştir.
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import (QWidget, QPushButton,QMainWindow,
                             QHBoxLayout, QAction)

#Yukarıda gerekli modülleri import ediyoruz




import sqlite3

try:
    conn = sqlite3.connect('stock.db') #stock.db adlı veri tabanına bağlanıyoruz. Gerekli tabloları oluşturuyoruz eğer dosya zaten var ise konsola yazdırıyoruz.
    c = conn.cursor()
    c.execute("""CREATE TABLE stock (
                name text,
                quantity integer,
                cost integer
                ) """)
    conn.commit()
except Exception:
    print('DB bulundu')


class Login(QtWidgets.QDialog):  #Login isimli authentication işlemlerini yapacak bir sınıf oluşturuyoruz
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Yönetici Girişi', self)
        self.buttonLogin.clicked.connect(self.handleLogin)  #giriş denetimi yapacak fonksiyon çağırılıyor

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)


    def handleLogin(self): #giriş denetimi yapacak fonksiyon yapılıyor.
        if (self.textName.text() == 'Admin' and  #Kullanıcı adı
            self.textPass.text() == '1234'):     #Şifre
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Kullanıcı adı veya şifre hatalı')  #eğer giriş başarısız ise uyarı verdiriyoruz

class Example(QMainWindow):


    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.st = stackedExample()
        exitAct = QAction(QIcon('exit_icon.png'), 'Exit', self) 
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Uygulamayı Kapat')
        exitAct.triggered.connect(self.close)

        self.statusBar()

        toolbar = self.addToolBar('Çıkış')
        toolbar.addAction(exitAct)

        self.setCentralWidget(self.st)

        self.show()

class stackedExample(QWidget):
    def __init__(self):

        super(stackedExample, self).__init__()
        self.leftlist = QListWidget()
        self.leftlist.setFixedWidth(250)
        self.leftlist.insertItem(0, 'Stok Ekle')
        self.leftlist.insertItem(1, 'Stok Düzenle')
        self.leftlist.insertItem(2, 'Stoğu Listele')
        self.leftlist.insertItem(3, 'İşlem Geçmişini Görüntüle')

        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()

        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        self.Stack.addWidget(self.stack4)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.leftlist.currentRowChanged.connect(self.display)
        self.setGeometry(500,350, 200, 200)
        self.setWindowTitle('Stok Yönetimi')
        self.show()


    def stack1UI(self):
        layout = QFormLayout()


        self.ok = QPushButton('Ürün Ekle', self)
        cancel = QPushButton('İptal', self)

        self.stock_name = QLineEdit()
        layout.addRow("Ürün Adı", self.stock_name)

        self.stock_count = QLineEdit()
        layout.addRow("Ürün Adeti", self.stock_count)

        self.stock_cost = QLineEdit()
        layout.addRow("Ürün Fiyatı (Adet Başı)", self.stock_cost)

        layout.addWidget(self.ok)
        layout.addWidget(cancel)

        self.ok.clicked.connect(self.on_click)

        cancel.clicked.connect(self.stock_name.clear)
        cancel.clicked.connect(self.stock_cost.clear)
        cancel.clicked.connect(self.stock_count.clear)
        self.stack1.setLayout(layout)

    def on_click(self):
        now = datetime.datetime.now()
        stock_name_inp = self.stock_name.text().replace(' ','_').lower()
        stock_count_inp = int(self.stock_count.text())
        stock_cost_inp = int(self.stock_cost.text())
        #print(stock_name_inp,stock_count_inp,stock_cost_inp)
        stock_add_date_time = now.strftime("%Y-%m-%d %H:%M")
        d = mp.insert_prod(stock_name_inp,stock_count_inp,stock_cost_inp,stock_add_date_time)
        print(d)
        #Yukarıdaki ayrıntıları tabloya eklemeniz gerekiyor

    def stack2UI(self):

        layout = QHBoxLayout()
        layout.setGeometry(QRect(0,300,1150,500))
        tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        tabs.addTab(self.tab1, 'Adet Ekle')
        tabs.addTab(self.tab2, 'Adet Azalt')
        tabs.addTab(self.tab3, 'Ürün Sil')

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

        layout.addWidget(tabs)
        self.stack2.setLayout(layout)

    def tab1UI(self):
        layout = QFormLayout()
        self.ok_add = QPushButton('Ürün Ekle', self)
        cancel = QPushButton('İptal', self)

        self.stock_name_add = QLineEdit()
        layout.addRow("Ürün Adı", self.stock_name_add)

        self.stock_count_add = QLineEdit()
        layout.addRow("Eklenecek Miktar", self.stock_count_add)

        layout.addWidget(self.ok_add)
        layout.addWidget(cancel)
        self.tab1.setLayout(layout)

        self.ok_add.clicked.connect(self.call_add)       #miktar eklemek için fonksiyon yazmanız gerekiyor
        cancel.clicked.connect(self.stock_name_add.clear)
        cancel.clicked.connect(self.stock_count_add.clear)

    def tab2UI(self):
        layout = QFormLayout()
        self.ok_red = QPushButton('Stoku Azalt', self)
        cancel = QPushButton('Cancel', self)

        self.stock_name_red = QLineEdit()
        layout.addRow("Ürün Adı", self.stock_name_red)

        self.stock_count_red = QLineEdit()
        layout.addRow("Azaltılacak miktar", self.stock_count_red)


        layout.addWidget(self.ok_red)
        layout.addWidget(cancel)
        self.tab2.setLayout(layout)

        self.ok_red.clicked.connect(self.call_red)  # miktarı azaltmak için fonksiyon yazmanız gerekiyor
        cancel.clicked.connect(self.stock_name_red.clear)
        cancel.clicked.connect(self.stock_count_red.clear)

    def tab3UI(self):
        layout = QFormLayout()
        self.ok_del = QPushButton('Ürün Sil', self)
        cancel = QPushButton('Cancel', self)

        self.stock_name_del = QLineEdit()
        layout.addRow("Ürün Adı", self.stock_name_del)
        layout.addWidget(self.ok_del)
        layout.addWidget(cancel)
        self.tab3.setLayout(layout)

        self.ok_del.clicked.connect(self.call_del)  # stoğu silmek için fonksiyon yazmanız gerekiyor
        cancel.clicked.connect(self.stock_name_del.clear)

    def call_del(self):
        now = datetime.datetime.now()
        stock_del_date_time = now.strftime("%Y-%m-%d %H:%M")
        stock_name = self.stock_name_del.text().replace(' ','_').lower()
        mp.remove_stock(stock_name,stock_del_date_time)

    def call_red(self):
        now = datetime.datetime.now()
        stock_red_date_time = now.strftime("%Y-%m-%d %H:%M")
        stock_name = self.stock_name_red.text().replace(' ','_').lower()
        try:
            stock_val = -(int(self.stock_count_red.text()))
            print(stock_val)
            print(type(stock_val))
            mp.update_quantity(stock_name, stock_val, stock_red_date_time)
        except Exception:
            print('İstisna')



    def call_add(self):
        now = datetime.datetime.now()
        stock_call_add_date_time = now.strftime("%Y-%m-%d %H:%M")
        stock_name = self.stock_name_add.text().replace(' ','_').lower()
        stock_val = int(self.stock_count_add.text())
        mp.update_quantity(stock_name, stock_val, stock_call_add_date_time)


    def stack3UI(self):

        table = mp.show_stock()
        print('show')
        print(table)
        layout = QVBoxLayout()
        self.srb = QPushButton()
        self.srb.setText("Ürünleri Göster veya Arama Yap")
        self.View = QTableWidget()
        self.lbl3 = QLabel()
        self.lbl_conf_text = QLabel()
        self.lbl_conf_text.setText("Aranacak Ürün:")
        self.conf_text = QLineEdit()

        self.View.setColumnCount(3)
        self.View.setColumnWidth(0, 250)
        self.View.setColumnWidth(1, 250)
        self.View.setColumnWidth(2, 200)
        self.View.insertRow(0)
        self.View.setItem(0, 0, QTableWidgetItem('Ürün Adı'))
        self.View.setItem(0, 1, QTableWidgetItem('Adet'))
        self.View.setItem(0, 2, QTableWidgetItem('Fiyat(Adet başına)'))



        layout.addWidget(self.View)
        layout.addWidget(self.lbl_conf_text)
        layout.addWidget(self.conf_text)
        layout.addWidget(self.srb)
        layout.addWidget(self.lbl3)
        self.srb.clicked.connect(self.show_search)
        self.stack3.setLayout(layout)

    def show_search(self):
        if self.View.rowCount()>1:
            for i in range(1,self.View.rowCount()):
                self.View.removeRow(1)


        x_act = mp.show_stock()
        x = []
        if self.conf_text.text() != '':
            for i in range(0,len(x_act)):
                a = list(x_act[i])
                if self.conf_text.text().lower() in a[0].lower():
                    x.append(a)
        else:
            x = mp.show_stock()

        if len(x)!=0:
            for i in range(1,len(x)+1):
                self.View.insertRow(i)
                a = list(x[i-1])
                self.View.setItem(i, 0, QTableWidgetItem(a[0].replace('_',' ').upper()))
                self.View.setItem(i, 1, QTableWidgetItem(str(a[1])))
                self.View.setItem(i, 2, QTableWidgetItem(str(a[2])))
                self.View.setRowHeight(i, 50)
            self.lbl3.setText('Stok Veritabanını Görüntüleme.')
        else:
            self.lbl3.setText('Veritabanında geçerli bilgi yok.')

    def stack4UI(self):
        layout = QVBoxLayout()
        self.srt = QPushButton()
        self.srt.setText("İşlem Geçmişini Göster.")
        self.Trans = QTableWidget()
        self.lbl4 = QLabel()
        self.lbl_trans_text = QLabel()
        self.lbl_trans_text.setText("Arama anahtarını girin:")
        self.trans_text = QLineEdit()

        self.Trans.setColumnCount(6)
        self.Trans.setColumnWidth(0, 150)
        self.Trans.setColumnWidth(1, 150)
        self.Trans.setColumnWidth(2, 150)
        self.Trans.setColumnWidth(3, 100)
        self.Trans.setColumnWidth(4, 100)
        self.Trans.setColumnWidth(5, 500)
        self.Trans.insertRow(0)
        self.Trans.setItem(0, 0, QTableWidgetItem('İşlem ID'))
        self.Trans.setItem(0, 1, QTableWidgetItem('Ürün Adı'))
        self.Trans.setItem(0, 2, QTableWidgetItem('İşlem Tipi'))
        self.Trans.setItem(0, 3, QTableWidgetItem('Tarih'))
        self.Trans.setItem(0, 4, QTableWidgetItem('Saat'))
        self.Trans.setItem(0, 5, QTableWidgetItem('İşlem Özelliği'))
        self.Trans.setRowHeight(0, 50)

        layout.addWidget(self.Trans)
        layout.addWidget(self.lbl_trans_text)
        layout.addWidget(self.trans_text)
        layout.addWidget(self.srt)
        layout.addWidget(self.lbl4)
        self.srt.clicked.connect(self.show_trans_history)
        self.stack4.setLayout(layout)

    def show_trans_history(self):
        if self.Trans.rowCount()>1:
            for i in range(1,self.Trans.rowCount()):
                self.Trans.removeRow(1)

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'transaction.txt')  #İşlem geçmişini transaction.txt olarak çıktı alıcağız.
        if os.path.exists(path):
            tsearch = open(path, 'r')
            x_c = tsearch.readlines()
            tsearch.close()
            x = []
            if self.trans_text.text() != '':
                key = self.trans_text.text()
                for i in range(0,len(x_c)):
                    a = x_c[i].split(" ")
                    name = a[0]
                    action = a[-2]
                    if (key.lower() in name.lower()) or (key.lower() in action.lower()) :
                        x.append(a)
            else:
                x = x_c.copy()

            for i in range(0,len(x)):
                x.sort(key=lambda a: a[4])
            #print(x)
            tid = 1900001
            for i in range(1,len(x)+1):
                self.Trans.insertRow(i)

                a = x[i-1].split(" ")
                if a[-2] == 'Güncelleme':
                    p = 'Değişen Stok Miktarı '+a[1]+' to '+a[2]
                elif a[-2] == 'Ekleme':
                    p = 'Eklenen stok : '+a[1]+' Ve Fiyat(Birim Başına) : '+a[2]
                elif a[-2] == 'Silme':
                    p = 'Stok bilgileri silindi.'
                else:
                    p = 'Yok'


                self.Trans.setItem(i, 0, QTableWidgetItem(str(tid)))
                self.Trans.setItem(i, 1, QTableWidgetItem(a[0].replace('_',' ')))
                self.Trans.setItem(i, 2, QTableWidgetItem(a[-2]))
                self.Trans.setItem(i, 3, QTableWidgetItem(a[3]))
                self.Trans.setItem(i, 4, QTableWidgetItem(a[4]))
                self.Trans.setItem(i, 5, QTableWidgetItem(p))
                self.Trans.setRowHeight(i, 50)
                tid += 1

            self.lbl4.setText('İşlem geçmişi.')
        else:
            self.lbl4.setText('Geçerli bilgi bulunamadı.')



    def display(self, i):
        self.Stack.setCurrentIndex(i)




if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = Example()
        sys.exit(app.exec_())
