import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyPDF2 import PdfReader, PdfWriter
from tempfile import NamedTemporaryFile
import subprocess
import sys
import shutil

class PDFMergerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PDF Merger")
        self.setGeometry(100, 100, 400, 300)

        self.file_list = QListWidget(self)
        self.file_list.setGeometry(10, 10, 380, 180)

        #setGeometry(x,y,Breite,Hoehe)
        self.add_btn = QPushButton("Add PDFs", self)
        self.add_btn.setGeometry(10, 200, 100, 30)
        self.add_btn.clicked.connect(self.addPDFs)

        
        self.merge_btn = QPushButton("Merge PDF", self)
        self.merge_btn.setGeometry(10, 250, 100, 30)
        self.merge_btn.clicked.connect(self.mergePDFs)

        self.view_btn = QPushButton("View Merged PDF", self)
        self.view_btn.setGeometry(120, 200, 150, 30)
        self.view_btn.clicked.connect(self.viewMergedPDF)

        self.save_btn = QPushButton("Save Merged PDF", self)
        self.save_btn.setGeometry(280, 200, 110, 30)
        self.save_btn.clicked.connect(self.saveMergedPDF)

        self.show()

    def addPDFs(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF Files", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        
        for file in files:
            #Die Dateipfade werden in die Liste eingefuegt
            self.file_list.addItem(file)

    def mergePDFs(self):
        merger = PdfWriter()
        
        for row in range(self.file_list.count()):
            #Aus der Liste werden die Elemente zugegriffen
            item = self.file_list.item(row)
            #Extrahiert den Text (in diesem Fall den Dateipfad) aus dem QListWidgetItem-Objekt item
            pdf_path = item.text()
            #Die PDF-Dateien werden gelesen
            reader = PdfReader(pdf_path)
            #Fuer jede PDF-Datei wird die erste Seite genommen und zusammengefuegt
            merger.add_page(reader.pages[0])

        #Eine temporaere Datei wird erstellt die nicht automatisch geloescht wird, wenn sie geschlossen wird.
        with NamedTemporaryFile(delete=False) as temp_pdf:
            #Die ausgewaehlten Seiten werden in temp_pdf abgespeichert (dabei werden die Seiten in der Instanz merger zwischengespeichert)
            merger.write(temp_pdf)
            temp_pdf_path = temp_pdf.name

        self.temp_pdf_path = temp_pdf_path

    def viewMergedPDF(self):
        '''Die Zeile if hasattr(self, 'temp_pdf_path') and os.path.exists(self.temp_pdf_path): überprüft, 
        ob das aktuelle Objekt (self) ein Attribut namens 'temp_pdf_path' hat 
        und ob die Datei mit dem Pfad self.temp_pdf_path tatsächlich auf dem Dateisystem existiert.'''
        if hasattr(self, 'temp_pdf_path') and os.path.exists(self.temp_pdf_path):
            '''Die Zeile subprocess.Popen(["start", "", self.temp_pdf_path], shell=True) startet einen Prozess unter Windows, 
            um eine Datei mit dem Standardprogramm für diese Dateityp zu oeffnen. 
            Im vorliegenden Fall wird versucht, die temporäre PDF-Datei self.temp_pdf_path zu öffnen.'''
            subprocess.Popen(["start", "", self.temp_pdf_path], shell=True)
        else:
            print("Merged PDF does not exist yet.")

    def saveMergedPDF(self):
        if hasattr(self, 'temp_pdf_path') and os.path.exists(self.temp_pdf_path):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
            
            if file_name:
                '''Wenn file_name einen Wert hat (d.h. der Benutzer hat einen Speicherort und einen Dateinamen ausgewählt), 
                wird die Datei am temporaeren Pfad self.temp_pdf_path (wo die zusammengeführte PDF-Datei erstellt wurde) in den ausgewaehlten Speicherort kopiert. 
                Die Funktion shutil.copy2 kopiert die Datei und behaelt dabei einige Metadaten wie Zeitstempel bei.'''
                shutil.copy2(self.temp_pdf_path, file_name)
                QMessageBox.information(self, "Save Successful", "Merged PDF has been saved.")
        else:
            print("Merged PDF does not exist yet.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFMergerApp()
    sys.exit(app.exec_())
