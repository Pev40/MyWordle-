import random
import requests as requests
import json
from datetime import date, datetime
import datetime
import os
import time


class ColoresTerminal:
    CRED = '\33[31m'
    CBLUE = '\33[34m'
    JUEGOVERDE = '\x1b[6;30;42m'
    JUEGOAMARILLO = '\x1b[6;30;43m'
    JUEGOROJO = '\x1b[6;30;41m'
    PARAMETROFIN = '\x1b[0m'
    PARAMETROFIN2 = "\033[0m "
    UNICODEBLANCO = '⬜'
    UNICODEAMARILLO = '🟨'
    UNICODEVERDE = '🟩'


class Diccionario():
    def __init__(self, maximo_caracteres):
        resp = requests.get(
            'https://raw.githubusercontent.com/javierarce/palabras/master/listado-general.txt')
        fp = open('listado.txt', 'w+')
        lista = list(resp.content.decode("utf-8"))
        for i in range(lista.__len__()):
            lista[i] = self.__normalizar(lista[i])
        lista2 = "".join(lista)
        fp.write(lista2.upper())
        fp.close()
        self.clasificar_por_maximo_caracteres(maximo_caracteres)

    def clasificar_por_maximo_caracteres(self, maximo_caracteres):
        palabras = open("listado.txt").read().splitlines()
        self._diccionario_de_consulta = [
            p for p in palabras if len(p) == maximo_caracteres]

        self._guardar_diccionario(maximo_caracteres)

    def _guardar_diccionario(self, maximocaracteres):
        nombre_archivo = "palabras" + str(maximocaracteres) + ".txt"
        fp = open(nombre_archivo, 'w+')
        cadena = ""
        for i in range(0, self._diccionario_de_consulta.__len__()):
            cadena += (self._diccionario_de_consulta[i] + "\n")
        fp.write(cadena)
        fp.close()

    def __normalizar(self, s):
        letras = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
        for a, b in letras:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        return s

    def palabra_al_azar(self):
        return self._diccionario_de_consulta[random.randint(0, self._diccionario_de_consulta.__len__() - 1)]


class Teclado():
    def __init__(self):
        self.__alfabeto = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "\n", "A", "S",
                           "D", "F", "G", "H", "J", "K", "L", "Ñ", "\n", "Z", "X", "C", "V", "B", "N", "M", "\n"]
        self._colores = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "\n", " ", " ",
                         " ", " ", " ", " ", " ", " ", " ", " ", "\n", " ", " ", " ", " ", " ", " ", " ", "\n"]
        self.salida = []
        self.__lista_encontrados = []
        for i in range(self.__alfabeto.__len__()):
            ingreso = " | " + self.__alfabeto[i]
            self.salida.append(ingreso)

    def _armar_salida(self):
        self.salida = []
        for i in range(self.__alfabeto.__len__()):
            ingreso = " | " + self.__alfabeto[i]
            self.salida.append(ingreso)

    def _imprimir_alfabeto(self):
        self._armar_salida()
        _linea1 = self.salida[0:11]
        _salida1 = ""
        _linea2 = self.salida[11:22]
        _salida2 = ""
        _linea3 = self.salida[22:30]
        _salida3 = ""
        for i in range(0, 11):
            _salida1 += _linea1[i]
        for i in range(_linea2.__len__()):
            _salida2 += _linea2[i]
        for i in range(_linea3.__len__()):
            _salida3 += _linea3[i]
        print(_salida1)
        print(_salida2)
        print(_salida3)

    def _letra_encontrada(self, letra):
        if (letra in self.__alfabeto):
            posicion = self.__alfabeto.index(letra)
            armado = ColoresTerminal.JUEGOAMARILLO + " " + \
                letra + " " + ColoresTerminal.PARAMETROFIN
            self.__alfabeto[posicion] = armado

    def _letra_posicion_correcta(self, letra):
        if (letra in self.__alfabeto):
            posicion = self.__alfabeto.index(letra)
            armado = ColoresTerminal.JUEGOVERDE + " " + \
                letra + " " + ColoresTerminal.PARAMETROFIN
            self.__alfabeto[posicion] = armado

    def _letra_incorrecta(self, letra):
        if (letra in self.__alfabeto):
            posicion = self.__alfabeto.index(letra)
            armado = ColoresTerminal.JUEGOROJO + " " + \
                letra + " " + ColoresTerminal.PARAMETROFIN
            self.__alfabeto[posicion] = armado

    def verificar_palabra(self, palabra_entrada, palabra_original, salida_reporte):
        palabra_entrada = list(palabra_entrada)
        palabra_original = list(palabra_original)
        for i in range(0, salida_reporte.__len__()):
            if(salida_reporte[i]==ColoresTerminal.UNICODEVERDE or
               salida_reporte[i]==ColoresTerminal.UNICODEAMARILLO):
                if(salida_reporte[i]==ColoresTerminal.UNICODEVERDE):
                    self._letra_posicion_correcta(palabra_original[i])
                else:
                    self._letra_encontrada(palabra_entrada[i])
            elif(salida_reporte[i] == ColoresTerminal.UNICODEBLANCO):
                if(palabra_entrada[i] in self.__lista_encontrados):
                    print(palabra_entrada[i] in self.__lista_encontrados)
                    pass
                else:
                    self._letra_incorrecta(palabra_entrada[i])
        self._imprimir_alfabeto()


class JuegoMain():
    def __init__(self):
        self.__diccionario = Diccionario(5)
        self.__palabra_elegida_aleatoria = self.__conseguir_palabra_aletatoria()
        self.__palabras_elegida = ["", "", "", "", "", ""]
        self.__palabras_elegida_comparadas = ["", "", "", "", "", ""]
        self.__intentos = 0
        self.__cuadricula = [
            " +---+---+---+---+---+", " |   |   |   |   |   |"]
        tablas = self.__cuadricula[1]
        self.__salida_tablero = [tablas, tablas, tablas, tablas, tablas, tablas]
        self.__salida_reporte = [" ", " ", " ", " ", " ", " "]
        self.__cantidad_letras_acertadas = 0
        self.__lista_letras_acumulado = []
        self.teclado = Teclado()
        self.__play()

    def __iniciar_juego(self):
        print(ColoresTerminal.CBLUE + "Bienvenido a mi WORDLE \- :) --/ \n" +
              ColoresTerminal.PARAMETROFIN2)
        print(self.__cuadricula[0])
        for i in range(0, 6):
            print(self.__cuadricula[1])
            print(self.__cuadricula[0])
        self.teclado._imprimir_alfabeto()

    def __mostrar_Tablero(self):
        __cambio_para_mostrar = " "
        for i in range(0, 5):
            __cambio_para_mostrar += "|" + \
                self.__palabras_elegida_comparadas[self.__intentos - 1][i]
        __cambio_para_mostrar += "|"
        self.__salida_tablero[self.__intentos - 1] = __cambio_para_mostrar
        print(self.__cuadricula[0])
        for i in range(0, 6):
            print(self.__salida_tablero[i])
            print(self.__cuadricula[0])

    def __consultar_palabra(self):
        print("PAlABRA SECRETA: ", self.__palabra_elegida_aleatoria)
        if(self.__intentos < 6):
            palabra_ingresada = str.upper(input("¿Ingresa tu palabra?\n"))
            palabra_ingresada = palabra_ingresada.strip()
            while (palabra_ingresada.__len__() > 5 or palabra_ingresada.__len__() < 5):
                if (palabra_ingresada.__len__() <= 4):
                    print(ColoresTerminal.CRED + "La palabra elegida es nula o " +
                          " menor de 4 caracteres, ingresalo otra vez " +
                          ColoresTerminal.PARAMETROFIN2)
                    palabra_ingresada = str.upper(
                        input("¿Ingresa tu palabra?\n"))
                else:
                    print(ColoresTerminal.CRED + "La palabra elegida exede las 5 letras,"
                          + " ingresalo otra vez" + ColoresTerminal.PARAMETROFIN2)
                    palabra_ingresada = str.upper(
                        input("¿Ingresa tu palabra?\n"))
            if (palabra_ingresada in self.__diccionario._diccionario_de_consulta):
                self.__limpiar_consola()
                self.__palabras_elegida[self.__intentos] = palabra_ingresada
                self.__intentos += 1
                self.__verificar_pantalla()
                self.__mostrar_Tablero()
                self.teclado.verificar_palabra(
                    self.__palabras_elegida[self.__intentos - 1],
                    self.__palabra_elegida_aleatoria,
                    self.__salida_reporte[self.__intentos - 1])
            else:
                print(ColoresTerminal.CRED + "La palabra no existe en el diccionario" +
                      ColoresTerminal.PARAMETROFIN2)
                self.__consultar_palabra()
            return
        else:
            self.__intentos += 1
            return

    def __verificar_pantalla(self):
        __lista_palabra_original = list(self.__palabra_elegida_aleatoria)
        __lista_palabra_entrada = list(
            self.__palabras_elegida[self.__intentos - 1])
        salida = []
        salida_reporte = []
        __cantidad_de_letra_eliminadas = 0
        for i in range(0, __lista_palabra_entrada.__len__()):
            if __lista_palabra_entrada[i] in __lista_palabra_original:
                indiceOrigial = __lista_palabra_original.index(
                    __lista_palabra_entrada[i])
                if (indiceOrigial == i):
                    letraCorrecta = (ColoresTerminal.JUEGOVERDE + " "
                                     + __lista_palabra_entrada[i] + " "
                                     + ColoresTerminal.PARAMETROFIN)
                    salida.append(letraCorrecta)
                    salida_reporte.append(ColoresTerminal.UNICODEVERDE)
                    if __lista_palabra_entrada[i] in self.__lista_letras_acumulado:
                        pass
                    else:
                        self.__lista_letras_acumulado.append(
                            __lista_palabra_entrada[i])
                        self.__cantidad_letras_acertadas += 1
                else:
                    if(__lista_palabra_original[i] == __lista_palabra_entrada[i]):
                        letraCorrecta = (ColoresTerminal.JUEGOVERDE + " "
                                         + __lista_palabra_entrada[i] + " "
                                         + ColoresTerminal.PARAMETROFIN)
                        salida.append(letraCorrecta)
                        salida_reporte.append(ColoresTerminal.UNICODEVERDE)
                        self.__cantidad_letras_acertadas += 1
                    else:
                        letraCorrecta = (ColoresTerminal.JUEGOAMARILLO + " "
                                         + __lista_palabra_entrada[i] + " "
                                         + ColoresTerminal.PARAMETROFIN)
                        salida_reporte.append(ColoresTerminal.UNICODEAMARILLO)
                        salida.append(letraCorrecta)
            else:
                letra = (ColoresTerminal.JUEGOROJO + " " +
                         __lista_palabra_entrada[i] + " " +
                         ColoresTerminal.PARAMETROFIN)
                salida_reporte.append(ColoresTerminal.UNICODEBLANCO)
                salida.append(letra)
        self.__palabras_elegida_comparadas[self.__intentos - 1] = salida
        self.__salida_reporte[self.__intentos -1] = salida_reporte
        return

    def __repetir_intento(self):
        while (self.__intentos <= 6):
            self.estatus_jugador = 'false'
            if(self.__cantidad_letras_acertadas >= 5):
                if(self.__palabra_elegida_aleatoria == self.__palabras_elegida[self.__intentos -1]):
                    self.estatus_jugador = 'true'
                    break
            self.__consultar_palabra()
        if (self.__cantidad_letras_acertadas>=5 and self.estatus_jugador=='true'):
            print(ColoresTerminal.JUEGOVERDE +
                  " FELICITACIONES HAS GANADO " + ColoresTerminal.PARAMETROFIN)
            self.__resumen_final()
        else:
            print(ColoresTerminal.JUEGOROJO + " GAME OVER " +
                  ColoresTerminal.PARAMETROFIN)
            self.__resumen_final()

    def __resumen_final(self):
        if (self.estatus_jugador == 'false'):
            print(ColoresTerminal.JUEGOROJO + " GAME OVER " +
                  ColoresTerminal.PARAMETROFIN)
            print(ColoresTerminal.JUEGOAMARILLO +
                  "La palabra a adivinar era: " +
                  ColoresTerminal.PARAMETROFIN)
            print(ColoresTerminal.JUEGOVERDE + " " +
                  self.__palabra_elegida_aleatoria + " " +
                  ColoresTerminal.PARAMETROFIN)
            self.__guardar_partida()
            self.__reporte_final()
        if (self.estatus_jugador == 'true'):
            print(ColoresTerminal.JUEGOVERDE +
                  " FELICITACIONES HAS GANADO " +
                  ColoresTerminal.PARAMETROFIN)
            print(ColoresTerminal.JUEGOAMARILLO +
                  "La palabra divinada fue: " +
                  ColoresTerminal.PARAMETROFIN)
            print(ColoresTerminal.JUEGOVERDE + " " +
                  self.__palabra_elegida_aleatoria + " " +
                  ColoresTerminal.PARAMETROFIN)
            self.__guardar_partida()
            self.__reporte_final()

    def __conseguir_palabra_aletatoria(self):
        palabra_alzar_diccionario = str(self.__diccionario.palabra_al_azar())
        data = json.loads(open('palabras_por_fecha.json').read())
        for i in range(data.__len__()):
            if (data[i]['palabra'] == palabra_alzar_diccionario):
                palabra_alzar_diccionario = self.__conseguir_palabra_aletatoria()
        jugadas = data
        fecha_eleccion = str(date.today())
        jugadas.append({
            "palabra": palabra_alzar_diccionario,
            "fecha": fecha_eleccion
        })
        fp = open('palabras_por_fecha.json', 'w+')
        fp.write(json.dumps(jugadas, indent=4))
        fp.close()
        return palabra_alzar_diccionario
        #return "CLAVO"

    def __guardar_partida(self):
        data = json.loads(open('partidas.json').read())
        partidas = data
        fecha_eleccion = datetime.datetime.now(datetime.timezone.utc)
        fecha_eleccion = fecha_eleccion.isoformat('T')
        fecha_eleccion = str(fecha_eleccion)
        partidas.append({
            "palabra": self.__palabra_elegida_aleatoria,
            "fecha": fecha_eleccion,
            "intentos": self.__palabras_elegida
        })
        fp = open('partidas.json', 'w+')
        fp.write(json.dumps(partidas, indent=4))
        fp.close()
        return

    def __limpiar_consola(self):
        if os.name == "posix":
            var = "clear"
        elif os.name == "ce" or os.name == "nt" or os.name == "dos":
            var = "cls"
        time.sleep(0.5)
        os.system(var)

    def __reporte_final(self):
        print("RESUMEN DE LA PARTIDA")
        mostrar = ""
        for i in range(0,self.__intentos):
            for j in range(0, self.__salida_reporte[i].__len__()):
                mostrar += self.__salida_reporte[i][j]
            print(mostrar)
            mostrar = ""

    def __play(self):
        self.__iniciar_juego()
        self.__consultar_palabra()
        self.__verificar_pantalla()
        self.__repetir_intento()

    # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = JuegoMain()
    #print(ColoresTerminal.UNICODEBLANCO + ColoresTerminal.UNICODEAMARILLO + ColoresTerminal.UNICODEVERDE)

# palabras = open("listado-general.txt", encoding="utf-8").read().splitlines()
# len(palabras)
# 80383
# [p for p in palabras if len(p) == 5]
# pip install autopep8


#   resp = requests.get(
#       'https://raw.githubusercontent.com/javierarce/palabras/master/listado-general.txt')
#   fp = open('listado.txt', 'w+')
#   fp.write(resp.content)
#   fp.close()

#   jugadas = []
#   jugadas.append({'fecha': '2022-02-23',
#                  'intentos': ["amiga", "ameba", "amago", "amigo", "susto"]})
#   fp = open('jugadas.json', 'w+')
#   fp.write(json.dumps(jugadas, indent=4))
#   fp.close()

#  data = json.loads(open('nombre.json').read())
