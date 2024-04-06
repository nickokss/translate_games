from PIL import Image, ImageGrab #tratamiento de imagen
import pytesseract #herramienta de recnocimiento
import cutlet #herramienta para leer simbolos raros
import os, time #herramientas del sistema
import translators as ts #herramienta de traduccion
import translators.server as tss
import wx #herramienta para la interfaz


class Translator():

    def get_lines(self, x1, y1, x2, y2):
        bbox = (x1, y1, x2, y2)
        im = ImageGrab.grab(bbox)
        # config --psm 11 es la forma en la que lee el texto, existen mas
        text_raw = pytesseract.image_to_string(im, lang='eng', config='--psm 11')
        text = text_raw.replace('/','!')
        #Borrar espacios en blanco
        text = "\n".join([linea.rstrip() for linea in text.splitlines() if linea.strip()])
        lines = text.splitlines()
        return lines
        #print(pytesseract.get_languages())

    def start_reading(self, x1, y1, x2, y2):
        katsu = cutlet.Cutlet()
        katsu.use_foreign_spelling = False

        lines = ''

        while True:
            new_lines = self.get_lines(x1,y1,x2,y2)

            if lines != new_lines:
                os.system('clear') #se usa clear en linux. En Windows seria cls
                lines = new_lines
                for line in lines:
                    print(line)
                    print(ts.translate_text(line, to_language='es')) #English -> ts.translate_text(line)
                    print('---------')
            time.sleep(0.1)

class DesktopController(wx.Frame):
   
    def __init__(self, parent, title):
        super(DesktopController, self).__init__(parent, title=title)
        self.SetTransparent(200)
        self.button = wx.Button(self)
        self.Bind(wx.EVT_BUTTON, self.on_button_click, self.button)
        self.SetPosition(wx.Point(0,0))
        self.Show()

    def on_button_click(self, event):
        print(self.button.Size)
        size = self.button.Size
        x1,y1 = self.button.GetScreenPosition()
        x2,y2 = x1 + size[0], y1 + size[1]
        print(x1,y1,x2,y2)
        self.Hide() #oculta el rectangulo
        #Iniciar la traduccion...
        Translator().start_reading(x1,y1,x2,y2)


if __name__ == '__main__':
    app = wx.App()
    mf = DesktopController(None, title="Selecciona area a traducir")
    app.MainLoop()