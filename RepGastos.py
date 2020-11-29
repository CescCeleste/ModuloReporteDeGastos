# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
import sqlite3
import os
import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog




class pantalla(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        
           
        self.buttonPDF = MDFillRoundFlatButton(  #BOTON PARA GENERAR PDF
                pos_hint = {"x": .05, "y": .1},
                size_hint = (.40,.1),
                text = "Crear PDF",
                on_release = lambda x: self.opcionPDF()
                )        
            
        self.buttonEXP = MDFillRoundFlatButton(  #BOTON PARA EXPORTAR PDF
                pos_hint = {"x": .55, "y": .1},
                size_hint = (.40,.1),
                text = "Exportar PDF a Drive",
                on_release = lambda x: self.exportarPDF()
                )  


        self.data_tables=  MDDataTable(  #TABLA QUE MUESTRA LOS PRODUCTOS Y SUS COSTOS
                pos_hint ={"x": .05, "y": .25},
                size_hint=(0.9, 0.6),
                use_pagination=True,
                column_data=[
                    ("Producto", dp(30)),
                    ("Costo unitario", dp(30)),
                    ("N° de unidades", dp(30)),
                    ("Costo Total", dp(30))
                ],
                row_data= self.obtiene_datos()
                   ,
               )
        
        
        #self.data_tables.open()
        self.add_widget(self.data_tables)
        self.add_widget(self.buttonPDF)
        self.add_widget(self.buttonEXP)
        #self.buttonactualizar.bind(on_press=lambda x: self.ActualizaPrecio())
        
        
    def opcionPDF(self):
        self.dialog = MDDialog(title = "Periodo de su reporte", #CUADROD DE DIALOGO PARA OBTENER EL PERIODO DEL REPORTE DE GASTOS
                               text = "¿De cuantas semanas desea el reporte?",
                               size_hint=[.9, .9],
                               auto_dismiss=True,
                               buttons=[
                                   MDFlatButton(
                                   text="UNO",
                                   on_release=lambda x: self.generaPDF('UNO')),
                                   MDFlatButton(
                                   text="DOS",
                                   on_release=lambda x: self.generaPDF('DOS')),
                                   MDFlatButton(
                                   text="TRES",
                                   on_release=lambda x: self.generaPDF('TRES')),
                                   MDFlatButton(
                                   text="CUATRO",
                                   on_release=lambda x: self.generaPDF('CUATRO')),
                                   MDFlatButton(
                                   text="Listo",
                                   on_release=self.dialog_close)
                               ]
                               )
        self.dialog.open()

    def dialog_close(self, *args): # Cierra el dialog del boton ayuda
        #print("Cerrando Dialog")
        self.dialog.dismiss()
    
    def my_callback(self, texto, popup_widget): # funcion que ayuda a cerrar el dialog del boton actualizar
        print(texto)
        print(popup_widget)

    def generaPDF(self, valor):
       if valor == 'UNO':
           semanas= 1    
       elif valor == 'DOS':
           semanas= 2
       elif valor == 'TRES':
           semanas= 3
       elif valor == 'CUATRO':
           semanas= 4
       print(semanas)
       APP_PATH = os.getcwd()
       DB_PATH = APP_PATH+'/prueba.db' #SE DEBE CAMBIAR EL NOMBRE AL NOMBRE DE LA BD FINAL
       con = sqlite3.connect(DB_PATH) #CONEXION A LA BD
       cursor = con.cursor() #CURSOR PARA EJECUTAR QUERYS
       dias= semanas*7
       base = datetime.datetime.today()
       date_list = [base - datetime.timedelta(days=x) for x in range(dias)]
       print(date_list[dias-1].date())
       fin= str(base.date())
       inicio=str(date_list[dias-1].date())
       periodo= "El periodo es: de "+inicio+" a "+fin
       print(periodo)
       fechas=[inicio, fin]
       cursor.execute("""SELECT NOMBRE,PRECIO,CANTIDAD FROM PRODUCTOS WHERE FECHA BETWEEN ? AND ? """, fechas)
       columnas=[['Producto', 'Precio Unitario', 'Unidades', 'Costo Final']] #datos que pasan al PDF
       costoTotal=0;
       for i in cursor:
           i=list(i)
           costoF= i[1]*i[2]
           costoTotal += costoF
           i.append(costoF)
           columnas.append(i)
            
       for i in columnas:
           print("valor", i)
        
       textCF= 'El costo total fue de: $'+str(costoTotal)
       print(textCF)
       fileName= 'ReporteGastos.pdf'
       pdf= SimpleDocTemplate(fileName, pagesize= letter)
       tabla= Table(columnas)
       estilo = TableStyle([
               ('BACKGROUND',(0,0),(3,0), colors.green),
               ('BACKGROUND',(0,1),(-1,-1), colors.beige),
               ('TEXTCOLOR', (0,0), (-1,0), colors.white),
               ('TEXTCOLOR', (0,1), (-1,-1), colors.green),
               ('ALIGN', (0,0), (-1,-1), 'CENTER'),
               ('FONTNAME', (0,0), (-1,-1), 'Courier'),
               ('FONTSIZE', (0,0), (-1,-1), 16)
               ])
            
       tabla.setStyle(estilo)
       elems=[]
       titulo= 'REPORTE DE GASTOS'
       estiloParrafoP =ParagraphStyle('yourtitle',fontName="Courier-Bold", fontSize=18, alignment=0,spaceAfter=18, textColor=colors.green)
       estiloParrafo= ParagraphStyle('yourtitle',fontName="Courier", fontSize=16, alignment=0, spaceBefore=18, spaceAfter=18, textColor=colors.green)
       elems.append(Paragraph(titulo, estiloParrafoP))
       elems.append(Paragraph(periodo, estiloParrafo))
       #elems.append(periodo)
       elems.append(tabla)
       elems.append(Paragraph(textCF, estiloParrafo))
       pdf.build(elems)


            
    def obtiene_datos(self): #Acceder a la BD 
           APP_PATH = os.getcwd()
           DB_PATH = APP_PATH+'/prueba.db' #CAMBIAR EL NOMBRE A LA BD FINAL
           con = sqlite3.connect(DB_PATH) #CONEXION A LA BD
           cursor = con.cursor() #CURSOR PARA EJECUTAR QUERYS
           cursor.execute("""SELECT NOMBRE,PRECIO,CANTIDAD FROM PRODUCTOS""")
               
           datos=[]
           costoTotal=0
           for i in cursor: 
               i=list(i)
               costoF= i[1]*i[2]
               costoTotal += costoF
               i.append(costoF)
               datos.append(i)
           con.close()
           return datos
       
    def exportarPDF(self): #SE DEBE BUSCAR LA FORMA DE HACERLO GENÉRICO
        import json
        import requests
        headers = {"Authorization": "Bearer ya29.a0AfH6SMDhLxJscYf1Cm4vYtjbKSPdHHIeNH3kuelzz6BgQtDk-sobO5Dzw7FwYrGf17vaKIR_qoKChEYXzc9In5lJVoTTAY5yfXdZdFxZdQ6jkZ2lcr2B6N36s5kihOV5xKjZUR5Kdsk39beA0vx7yTisCP3ulOf8fquyUugdXt0"}
        para = {
            "name": "ReporteGastos.pdf",
        }
        files = {
            'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
            'file': open("./ReporteGastos.pdf", "rb")
        }
        r = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files=files
        )
        print(r.text)

        
class RepGApp(MDApp):
    def build(self):
        self.title = "Reporte de Gastos"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.bg_light
        return pantalla()
      
    
        
        
RepGApp().run()
