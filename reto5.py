import os
import numpy as np
from math import asin,cos,sin,sqrt,radians,degrees

os.system ("cls")
#RF01:mensaje de bienvenida
print("Bienvenido al sistema de ubicación para zonas públicas WIFI")

#RF02:ingreso de usuario y contraseña

default_usuario = "51607" #Código del grupo, Fundamentos de programación
default_password = "70615" #Código del grupo, Fundamentos de programación de forma inversa

#RF03:configuración captcha
codigo_grupo = 607
operacion = (5 % 7)+1-6

#definicion de variables
opcion1="Cambiar contraseña"
opcion2="Ingresar coordenadas actuales"
opcion3="Ubicar zona wifi más cercana" 
opcion4="Guardar archivo con ubicación cercana"
opcion5="Actualizar registros de zonas wifi desde archivo"
opcion6="Elegir opción de menú favorita"
opcion7="Cerrar sesión"
menu = {1:opcion1, 2:opcion2, 3:opcion3, 4:opcion4, 5:opcion5, 6:opcion6, 7:opcion7}
opcion=""
repetir=True
errores = 0


coordenadas = np.zeros((3,2))  # matriz que contendrá las coordenadas del usuario

#RF01: El programa dispone de manera predefinida la ubicación de cuatro zonas wifi con su respectivo promedio de usuarios
#Matriz que almacena las 4 zonas wifi predefinidas
zonas_wifi=[[-3.777, -70.302, 91],
            [-4.134, -69.983, 233],
            [-4.006, -70.132, 149],
            [-3.846, -70.222, 211]]

listadistancias=[]
radio_tierra=6372.795477598
ubicacion_usuario=[]
zonawifi_usuario=[]
recorrido_usuario=[]

#Reto 5, declaro el diccionario
informacion = { 'actual': [],
                'zonawifi1': [],
                'recorrido': []}


captcha = codigo_grupo + operacion

#RF01: El programa muestra el menú 

#Función para imprimir menú de acuerdo al orden del usuario
def imprimir_menu(favorita=1):
    global menu
    if favorita==1:
        for item in menu:
            print ("{}.".format(item), menu[item])
    else:
        #Reordenar menu 
        temporal=""       
        for item in menu:
            if item==1:
                temporal=menu[item]
                menu[item] = menu[favorita]
            else:
                if menu[favorita]==menu[item]:
                    menu[item] =temporal
                else:
                    menu[item] =menu[item]
                            
                for item in menu:
                    print ("{}.".format(item), menu[item])
    opcion_menu =int(input("\nElija una opción "))
    return opcion_menu

#Función para validar la opcion del menú elegida por el usuario
def validar_opcion_menu(menu_elegido):
    global errores
    if menu_elegido >=1 and menu_elegido<=7:
        if menu_elegido==6:
            favorita=int(input("Seleccione opción favorita "))
            if favorita>=1 and favorita<=5:
                #adivinanzas de confirmación con el código de grupo 51607, donde las respuestas deben ser los últimos dos dígitos
                #adivinanza 1 debe responder 0
                adivinanza1=int(input("Para confirmar por favor responda: Si me giras pierdo tres unidades por eso debes colocarme siempre de pie, la respuesta es "))
                if adivinanza1==0:
                    #adivinanza 2 debe responder 7
                    adivinanza2=int(input("Para confirmar por favor responda: Me separaron de mi hermano siamés, antes era un ocho y ahora soy un… la respuesta es "))
                    if adivinanza2==7:
                        os.system ("cls")
                        opcion_menu = imprimir_menu(favorita)
                        validar_opcion_menu(opcion_menu)
                        exit
                    else:
                        print("Error")
                        opcion_menu = imprimir_menu()
                        validar_opcion_menu(opcion_menu)
                else:
                    print("Error")
                    opcion_menu = imprimir_menu()
                    validar_opcion_menu(opcion_menu)
            else:
                print("Error")
                exit
        elif menu_elegido==7:
            os.system ("cls")
            print("Hasta pronto")
            exit
        else:
            os.system ("cls")
            print("Usted ha elegido la opción", menu_elegido)
            #reto 3
            #RF01: El programa permite al usuario actualizar su contraseña.
            if menu[menu_elegido]=="Cambiar contraseña":
                cambiar_password()  
            #RF02: El programa permite al usuario ingresar las coordenadas de los tres sitios que más frecuenta (trabajo, casa, parque).
            if menu[menu_elegido]=="Ingresar coordenadas actuales":
                sitios_coordenadas()
            #Reto 4
            #RF02: El programa permite al usuario encontrar dos (2) zonas wifi más cercanas a su ubicación y saber en cuál de estas hay menos personas conectadas.
            if menu[menu_elegido]=="Ubicar zona wifi más cercana":
                ubicar_zona_wifi()
            #Reto 5
            #RF01: El programa prepara los resultados de las zonas de conexión wifi más cercanas en un diccionario de datos para ser exportado a un archivo.
            if menu[menu_elegido]=="Guardar archivo con ubicación cercana":
                guardar_informacion()
            #RF02: El programa utiliza un archivo externo para actualizar la información de las 4 zonas conexión wifi en el municipio.
            if menu[menu_elegido]=="Actualizar registros de zonas wifi desde archivo":
                actualizar_wifi_archivo()
            exit
    elif menu_elegido==2021:
        latitud=float(input("Dame una latitud y te diré cual hemisferio es... "))
        os.system ("cls")
        if latitud > 0:
            print("Usted está en hemisferio norte")
        else:
            print("Usted está en hemisferio sur")
    elif menu_elegido==2022:
        os.system ("cls")
        longitud=float(input("Escribe una la coordenada de una longitud en Sudamérica y te diré su huso horario "))
        if longitud >= -67.401 or longitud <= 81.296:
            print("El huso horario es -5")
        elif longitud >= -54.316 or longitud <= 67.402:
            print("El huso horario es -4")
        elif longitud >= -35.833 or longitud <= -35.833:
            print("El huso horario es -3")
    else:
        #RF03: El programa genera una alerta si el usuario elige una opción incorrecta.
        errores +=1
        print("Error")
        print(errores)
        if errores <= 2:
            opcion_menu =int(input("\nElija una opción "))
            validar_opcion_menu(opcion_menu)
        else:
            exit

#permite cambiar la contraseña del usuario
def cambiar_password():  
    global default_password
    print("Cambiar contraseña")
    old_password=input("Para confirmar el cambio de contraseña debes ingresar tu contraseña actual: ")
    if old_password==default_password:
        nueva_password=input("Escriba su nueva contraseña: ")
        if old_password!=nueva_password:
            default_password=nueva_password
            opcion_menu = imprimir_menu()
            validar_opcion_menu(opcion_menu)
        else:
            print("Error")
            exit
    else:
        print("Error")
        exit

#permite almacenar coordenadas favoritas
def sitios_coordenadas():
    global coordenadas
    lugares={1:"Trabajo", 2:"Casa", 3:"Parque"}
    print("Coordenadas actuales")
    if np.all((coordenadas != 0)):
        #RF03: El programa permite al usuario actualizar las coordenadas de los tres sitios más frecuentados.
        os.system("cls")
        for x in range(0, len(coordenadas)):
            i = 0
            print("Coordenada {}".format(x+1),": {} - [latitud,longitud]".format(lugares[x+1]),' = [',"{0:.3f}".format(coordenadas[x][i]),", {0:.3f}".format(coordenadas[x][i+1]),"]")
        
        # Hallaremos la coordenada posicionada mas al oriente
        #oriente=coordenadas.index(min(coordenadas, key=lambda posicion: posicion[1]))
        #print("La coordenada {}".format(oriente+1),"({}".format(lugares[oriente+1]),") es la que está mas al oriente ")
        # Hallaremos la coordenada posicionada mas al occidente
        #occidente=coordenadas.index(max(coordenadas, key=lambda posicion: posicion[1]))
        #print("La coordenada {}".format(occidente+1),"({}".format(lugares[occidente+1]),") es la que está mas al occidente ")
        oriente = None
        #Recorreremos cada lista de la matriz y compararemos su valor para hallar la variable mas al oriente
        for coor_or in range(0, len(coordenadas)):
            for ori in range(1, len(coordenadas[coor_or])):
                if oriente is None or coordenadas[coor_or][ori] < oriente:
                    oriente = coordenadas[coor_or][ori]
                    menosOriente = coor_or+1
        print("La coordenada", menosOriente,"({})".format(lugares[menosOriente]),"es la que está más al oriente")

        occidente = None
        #Recorreremos cada lista de la matriz y compararemos su valor para hallar la variable mas al occidente
        for coor_occ in range(0, len(coordenadas)):
            for oc in range(1, len(coordenadas[coor_occ])):
                if occidente is None or coordenadas[coor_occ][oc] > occidente:
                    occidente = coordenadas[coor_occ][oc]
                    masOccidente = coor_occ+1
        print("La coordenada", masOccidente,"({})".format(lugares[masOccidente]),"es la que está más al occidente")

        actualizar_coordenada = int(input("Presione 1,2 ó 3 para actualizar la respectiva coordenada. \nPresione 0 para regresar al menú "))
        #Actualizaremos la coordenada de acuerdo a la elección del usuario
        if actualizar_coordenada >=1 and actualizar_coordenada<=3:
            latitud = input("Ingresa latitud: ")
            if latitud != '':
                latitud = float(latitud)
                if latitud >= -4.227 and latitud <= -3.002:
                    longitud = input("Ingresa longitud: ") 
                    if longitud!= '':
                        longitud = float(longitud)
                        if longitud >= -70.365 and longitud <= -69.714:
                            coordenadas[actualizar_coordenada-1][0] = latitud
                            coordenadas[actualizar_coordenada-1][1] = longitud
                            opcion_menu = imprimir_menu()
                            validar_opcion_menu(opcion_menu)
                        else:
                            print("Error coordenada")
                            quit()
                    else:
                        print("Error")
                        quit()     
                else:
                    print("Error coordenada")
                    quit()
            else:
                print("Error")
                quit()
        elif actualizar_coordenada==0:
            opcion_menu = imprimir_menu()
            validar_opcion_menu(opcion_menu)
        else:
            print("Error actualización")
            quit()    
    else:
        print("Debes guardar las coordenadas de los tres sitios que más frecuentas (Trabajo, Casa, Parque).")
        #Ciclo para el ingreso de las tres coordenadas del usuario
        for i in range (0,3):
            print("Coordenadas de tu:", lugares[i+1])
            latitud = input("Ingresa latitud: ")
            while latitud == "" or latitud == " ":
                print("Error")
                latitud=input("La latitud no puede estar en blanco, por favor ingrésala de nuevo: ")
            latitud=float(latitud)
            if latitud >= -4.227 and latitud <= -3.002:
                longitud = input("Ingrese longitud: ")
                while longitud == "" or longitud == " ":
                    print("Error")
                    longitud=input("La longitud no puede estar en blanco, por favor ingrésala de nuevo: ")
                longitud=float(longitud)
                if longitud >= -70.365  and longitud <= -69.714 :
                    coordenadas = np.append(coordenadas, [[latitud, longitud]], axis = 0)
                else:
                    print("Error coordenada")
                    coordenadas=[]
                    quit()
            else:
                print("Error coordenada")
                coordenadas=[]
                quit()
        coordenadas = coordenadas[~np.all(coordenadas == 0, axis=1)]
        opcion_menu = imprimir_menu()
        validar_opcion_menu(opcion_menu)

#permite ubicar las zonas wifi mas cercanas al usuario
def ubicar_zona_wifi():
    os.system("cls")
    global coordenadas
    global ubicacion_usuario
    lugares={1:"Trabajo", 2:"Casa", 3:"Parque"}
    if np.all((coordenadas != 0)):
        for x in range(0, len(coordenadas)):
            i = 0
            print("Coordenada {}".format(x+1),": {} - [latitud,longitud]".format(lugares[x+1]),' = [',"{0:.3f}".format(coordenadas[x][i]),", {0:.3f}".format(coordenadas[x][i+1]),"]")
        ubicacion_actual=int(input("Por favor elija su ubicación actual (1,2 ó 3) para calcular la distancia a los puntos de conexión "))
        if ubicacion_actual>=1 and ubicacion_actual<=3:
            ubicacion_usuario=coordenadas[ubicacion_actual-1, :]
            for z in range(0, len(zonas_wifi)):
                listadistancias.append(calcular_distancia(ubicacion_usuario, np.array(zonas_wifi)[z, :]))
            #almaceno el indice de los puntos mas cercanos al usuario de la matriz de zona_wifi
            puntos_cerca=puntos_cercanos(listadistancias)
            os.system("cls")
            print("Zonas wifi cercanas con menos usuarios")
            wifi_ordenado=[]
            #punto con menor promedio de usuarios
            if np.array(zonas_wifi)[puntos_cerca[0], 2] < np.array(zonas_wifi)[puntos_cerca[1], 2]:
                print("La zona wifi {}".format(puntos_cerca[0]+1), ": ubicada en ['{}'".format(np.array(zonas_wifi)[puntos_cerca[0], 0]),", '{}'".format(np.array(zonas_wifi)[puntos_cerca[0], 1]),"] a {}".format(listadistancias[puntos_cerca[0]]*1000), "metros , tiene en promedio {}".format(int(np.array(zonas_wifi)[puntos_cerca[0], 2])), "usuarios")
                wifi_ordenado.append(np.array(zonas_wifi)[puntos_cerca[0], :])
            else:
                print("La zona wifi {}".format(puntos_cerca[1]+1), ": ubicada en ['{}'".format(np.array(zonas_wifi)[puntos_cerca[1], 0]),", '{}'".format(np.array(zonas_wifi)[puntos_cerca[1], 1]),"] a {}".format(listadistancias[puntos_cerca[1]]*1000), "metros , tiene en promedio {}".format(int(np.array(zonas_wifi)[puntos_cerca[1], 2])), "usuarios")
                wifi_ordenado.append(np.array(zonas_wifi)[puntos_cerca[1], :])

            #punto con mayor promedio de usuarios
            if np.array(zonas_wifi)[puntos_cerca[0], 2] > np.array(zonas_wifi)[puntos_cerca[1], 2]:
                print("La zona wifi {}".format(puntos_cerca[0]+1), ": ubicada en ['{}'".format(np.array(zonas_wifi)[puntos_cerca[0], 0]),", '{}'".format(np.array(zonas_wifi)[puntos_cerca[0], 1]),"] a {}".format(listadistancias[puntos_cerca[0]]*1000), "metros , tiene en promedio {}".format(int(np.array(zonas_wifi)[puntos_cerca[0], 2])), "usuarios")
                wifi_ordenado.append(np.array(zonas_wifi)[puntos_cerca[0], :])
            else:
                print("La zona wifi {}".format(puntos_cerca[1]+1), ": ubicada en ['{}'".format(np.array(zonas_wifi)[puntos_cerca[1], 0]),", '{}'".format(np.array(zonas_wifi)[puntos_cerca[1], 1]),"] a {}".format(listadistancias[puntos_cerca[1]]*1000), "metros , tiene en promedio {}".format(int(np.array(zonas_wifi)[puntos_cerca[1], 2])), "usuarios")
                wifi_ordenado.append(np.array(zonas_wifi)[puntos_cerca[1], :])

            #RF03: El programa indica al usuario en qué dirección está ubicada la coordenada el punto de acceso wifi elegido y cuál es el tiempo promedio para llegar hasta ese lugar.
            indicaciones_llegada(wifi_ordenado, ubicacion_usuario)
            print("Hasta pronto")
            opcion_menu = imprimir_menu()
            validar_opcion_menu(opcion_menu)
        else:
            print("Error ubicación")
            exit
    else:
        print("Error sin registro de coordenadas")
        exit

#calcula las distancias de las coordenadas de acuerdo al punto actual elegido por el usuario
def calcular_distancia(zona_actual, zona_wifi):
    delta_lat=zona_actual[0]-zona_wifi[0]
    delta_lon=zona_actual[1]-zona_wifi[1]

    ecuacion_pat1=(sin(delta_lat/2)**2) + cos(zona_actual[0]) * cos(zona_wifi[0]) * (sin(delta_lon/2)**2)
    distancia = 2 * radio_tierra * asin(ecuacion_pat1)
    return distancia

#elige los dos puntos mas cercanos al usuario
def puntos_cercanos(distancias):
    distanciasduplicadas=list(distancias)
    min1=distanciasduplicadas.index(min(distanciasduplicadas)) 
    distanciasduplicadas.pop(min1)
    min2=distancias.index(min(distanciasduplicadas))
    cercanos=[min1, min2]
    return cercanos


#imprime las indicaciones al usuario para llegar a los puntos wifi
def indicaciones_llegada(zona_wifi, zona_usuario):
    global zonawifi_usuario
    global recorrido_usuario
    indicacion=int(input("Elija 1 o 2 para recibir indicaciones de llegada "))
    if indicacion==1 or indicacion==2:
        #comparo latitudes para saber si las indicaciones son hacia el norte o hacia el sur
        y=""
        zonawifi_usuario=np.array(zona_wifi)[indicacion-1]
        if np.array(zona_wifi)[indicacion-1, 0] > zona_usuario[0]:
            y="norte"
        else:
            y="sur"

        #comparo longitudes para saber si las indicaciones son hacia el oriente o hacia el occidente
        x=""
        if np.array(zona_wifi)[indicacion-1, 1] > zona_usuario[1]:
            x="oriente"
        else:
            x="occidente"

        print("Para llegar a la zona wifi dirigirse primero al {}".format(x),"y luego hacia el {}".format(y))
        
        #Calcular tiempo según va a pie o en auto
        distancia_punto_elegido=calcular_distancia(zona_usuario, np.array(zona_wifi)[indicacion-1, :])*1000
        tiempo_a_pie=distancia_punto_elegido/0.483
        print("- Tiempo a pie: {}".format(tiempo_a_pie/60), " minutos aproximadamente")

        tiempo_en_auto=distancia_punto_elegido/20.83
        print("- Tiempo en auto: {}".format(tiempo_en_auto/60), " minutos aproximadamente")

        recorrido_usuario=[distancia_punto_elegido, 'A pie', tiempo_a_pie/60, 'En auto', tiempo_en_auto/60]
        
    else:
        print("Error zona wifi")
        exit

#RF01: El programa prepara los resultados de las zonas de conexión wifi más cercanas en un diccionario de datos para ser exportado a un archivo.
def guardar_informacion():
    os.system("cls")
    global coordenadas
    global ubicacion_usuario
    global zonawifi_usuario
    global recorrido_usuario
    global informacion
    if np.all((coordenadas != 0)):
        if not len(ubicacion_usuario):
            print("Error de alistamiento")
            exit
        else:
            informacion = { 'actual': ubicacion_usuario,
                'zonawifi1': zonawifi_usuario,
                'recorrido': recorrido_usuario}
            print(informacion)
            guardar=int(input("¿Está de acuerdo con la información a exportar? Presione 1 para confirmar, 0 para regresar al menú principal "))
            if guardar==1:
                guardar_archivo("wifi_cercano.txt",informacion)
            elif guardar==0:
                opcion_menu = imprimir_menu()
                validar_opcion_menu(opcion_menu)
            else:
                exit
    else:
        print("Error de alistamiento")
        exit

#RF02: El programa utiliza un archivo externo para actualizar la información de las 4 zonas conexión wifi en el municipio.
def actualizar_wifi_archivo():
    global zonas_wifi
    zonas_wifi=np.array(zonas_wifi)
    try:
        zonas_wifi = np.loadtxt('wifi_municipio.txt', usecols=range(3))
        regresar=int(input("Datos de coordenadas para zonas wifi actualizados, presione 0 para regresar al menú principal "))
        if regresar==0:
            opcion_menu = imprimir_menu()
            validar_opcion_menu(opcion_menu)
        else:
            print("Opción incorrecta")
            exit
    except IOError:
        fmt = '%.3f', '%.3f', '%d'
        np.savetxt("wifi_municipio.txt", zonas_wifi, fmt=fmt)
        opcion_menu = imprimir_menu()
        validar_opcion_menu(opcion_menu)
    except FileNotFoundError:
        fmt = '%.3f', '%.3f', '%d'
        np.savetxt("wifi_municipio.txt", zonas_wifi, fmt=fmt)
        opcion_menu = imprimir_menu()
        validar_opcion_menu(opcion_menu)

def guardar_archivo(nombre,datos=""):
    try:
        # Primero crear y abrir un archivo de texto
        archivo = open(nombre, "w", encoding="utf-8")
        # Recorrer los elementos del diccionario, dividir la clave y el valor de cada elemento en una cadena, agregar separadores y saltos de línea
        for k,v in datos.items():
	        archivo.write(str(k)+' '+str(v)+'\n')
        # Nota para cerrar el archivo
        archivo.close()
        print("Exportando archivo")
        exit
    except IOError:
        print("Error con el archivo:", nombre)
        exit
    except FileNotFoundError:
        archivo = open(nombre, "w", encoding="utf-8")
        archivo.close()
        opcion_menu = imprimir_menu()
        validar_opcion_menu(opcion_menu)

#Easter egg
def promedio_latitudes():
    cantidad=int(input("¿Cuántas latitudes vas a ingresar? "))
    suma=0
    for i in range(0, cantidad):
        latitud = float(input(f"Ingresa latitud {i+1}: "))
        suma=suma+latitud
    promedio=suma/cantidad
    print("El promedio es:", promedio)

#inicio del programa
usuario =input("Escribe tu nombre de usuario ")

if usuario==default_usuario:
    #usuario correcto
    password = input("Escribe tu contraseña ")
    if password==default_password:
        #contraseña correcta
        #solicitud de captcha
        captcha_usuario=int(input("Ingresa el resultado de la siguiente operacion: "+str(codigo_grupo)+" + "+str(operacion)+" = "))
        if captcha_usuario==captcha:
            print("Sesión iniciada")
            #Desarrollo de Reto 2
            #RF02: El programa permite elegir una opción del menú como favorito
            opcion=imprimir_menu()
            validar_opcion_menu(opcion)
        else:
            print("Error")
            exit
    elif password=="m1s10nt1c":
        promedio_latitudes()
    else:
        #contraseña incorrecta
        print("Error")
        exit
elif usuario=="Tripulante2022":
    print("Este fue mi primer programa y vamos por más")
    exit
else:
    #usuario incorrecto
    print("Error")
    exit

