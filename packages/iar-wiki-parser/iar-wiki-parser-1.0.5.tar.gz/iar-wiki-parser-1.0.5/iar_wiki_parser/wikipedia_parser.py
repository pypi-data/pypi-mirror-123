#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Proporciona la clase ParseadorWikipedia, que descarga, trocea y limpia la Wikipedia en español y crea un
corpus con ellla.
"""

from iar_wiki_parser.wikipedia_parser_consts import MARCA_FIN_ARTICULO
from iar_tokenizer.tokenizer import Tokenizer
from os.path import isfile, join, exists, dirname, getsize, realpath
from os import listdir, makedirs
from itertools import groupby
from time import time, strftime, localtime
import xml.etree.ElementTree as ElementTree
import urllib
import re
import codecs
import bz2file
import sys
import pickle
import html.entities as htmlentitydefs


barra = '\\' if sys.platform == 'win32' else '/'
directorio_base = dirname(realpath(__file__)) + barra


class ParseadorWikipedia:
    """Esta clase se utiliza para extraer un corpus de texto extraído de la Wikipedia en español.

    No contiene atributos, con lo que todos sus métodos son estáticos.
    """
    def __init__(self):
        pass

    @staticmethod
    def extrae_articulos_refinados(actualiza_archivo_raw=False, articulos_por_fasciculo=1000,
                                   articulos_rechazados_guardados='cpahtwmRDS0'):
        """Se descarga el archivo con toda la Wikipedia española, se trocea en artículos, se seleccionan y
         refinan.

        Se descarga https://dumps.wikimedia.org/eswiki/latest/eswiki-latest-pages-articles-multistream.xml.bz2
        si es necesario (no existe o se pide que se actualice el archivo utilizado -hay versiones nuevas cada
        dos semanas-).

        Posteriormente, se descomprime dicho archivo y se lee, troceándolo en artículos y seleccionando los
        artículos con contenido, que se refinan eliminando etiquetas y cualquier formato de Wikipedia y se
        empaquetan en "fascículos" que contienen 1.000 por defecto de estos artículos refinados. Un fascículo
        es simplemente un archivo de texto que contiene varios artículos separados por la marca
        '~~~~ Fin artículo ~~~~\n'

        Los artículos rechazados debido a que son redirecciones, páginas de categoría... pueden guardarse
        aparte, o simplemente se ignoran, según el parametro.

        :type actualiza_archivo_raw: bool
        :param actualiza_archivo_raw: Si está a True se descarga de la Wikipedia la última versión del archivo
            grande que contiene todo el contenido de la Wikipedia en español aunque dicho archivo esté ya
            descargado. Si está a False, solo se descarga si no lo tenemos.
        :type articulos_por_fasciculo: int
        :param articulos_por_fasciculo: Cantidad de artículos que se incluye dentro de cada fascículo.
        :type articulos_rechazados_guardados: unicode
        :param articulos_rechazados_guardados: Es una cadena de caracteres que indica cuáles de los archivos
            rechazados deben ser guardados en el directorio de archivos rechazados. Cada uno de los siguientes
            caracteres identifica un motivo por el que el artículo puede rechazarse:
            - c: es un artículo que recoge los artículos de una cierta Categoría.
            - p: es un artículo que recoge una Plantilla.
            - a: es un artículo de Anexo.
            - h: es un artículo de Ayuda.
            - t: es un artículo de un Portal de la Wikipedia.
            - w: es un (meta)artículo de Wikipedia o Wikiproyecto.
            - m: es un artículo de Mediawiki.
            - R: el artículo contiene una Redirección.
            - D: el artículo es una Desambiguación.
            - 0: el artículo está vacío.
            - S: el artículo tiene erroes de formato y se sospecha que su contenido puede no ser solo texto.
        """
        # La tarea de procesar de inicio a fin el archivo raw lleva mucho tiempo. Es por ello por lo que se
        # requiere un mecanismo para poder procesarlo parcialmente y continuar más adelante. Esto es
        # especialmente importante si decidimos guardar los artículos rechazados, lo cual retrasa mucho el
        # procesado y además puede crear varios millones de ficheros (los artículos rechazados se guardan en
        # un archivo cada uno, mientras que los refinados se agregan en fascículos), algo que puede hacer
        # impracticable su utilización salvo que se organicen debidamente en subdirectorios.
        # Se tiene un directorio propio para los artículos refinados, en los que se guardan los archivos de
        # fascículos, así como un archivo de índice que contiene los títulos de todos los artículos refinados,
        # asi como su posición dentro de uno de los fascículos, su numeración y su posición en el fichero
        # grande de Wikipedia.
        # Los artículos rechazados se meten en su propio directorio, que a su vez está dividido en
        # subdirectorios según el motivo para su rechazado. Además, se tiene un subdirectorio por cada
        # fascículo (si bien cada artículo tiene su propio archivo), donde hay tantos archivos como artículos
        # rechazados por este motivo haya entre el primer artículo refinado de este subdirectorio (fascículo)
        # y el primero del siguiente fascículo.
        # Dichos subdirectorios están nombrados con el patrón AAAAAAA@PPPPPPPPPPP donde los 7 primeros
        # caracteres son dígitos que indican el nº del primer artículo que se incluye en dicho subdirectorio
        # (hay más de 3 millones), @ separadora y otros 11 dígitos que indican el byte del archivo raw en el
        # que comienza dicho artículo (ocupa unos 11GB).
        # Este código AAAAAAA@PPPPPPPPPPP se utiliza también para dar nombre a los archivos con los
        # fascículos, y también se ponen al inicio de los nombres de los archivos que contienen artículos
        # rechazados. También aparecen en el archivo de índice, precediendo al nombre del artículo refinado.

        # Inicializamos algunas variables de recuentos y demás.
        hora_inicio_total = time()
        nombre_fasciculo_actual = ''
        nombre_ultimo_archivo_indexado = ''
        posicion_lectura_inicial = 0
        n_articulos_refinados = 0
        n_articulos_refinados_inicial = 0
        n_articulos_procesados = 0
        n_articulos_procesados_inicial = 0

        # Creamos las variables con los nombres de (algunos de) los directorios que utilizaremos.
        directorio_trabajo = directorio_base + 'archivos_de_datos' + barra
        directorio_archivo_raw = directorio_trabajo + 'archivo_xml_raw' + barra
        directorio_articulos_rechazados = directorio_trabajo + 'articulos_rechazados' + barra
        directorio_articulos_redirect = directorio_articulos_rechazados + 'redirect' + barra
        directorio_articulos_desambiguacion = directorio_articulos_rechazados + 'desambiguacion' + barra
        directorio_articulos_sospechosos = directorio_articulos_rechazados + 'sospechosos' + barra
        directorio_articulos_vacios = directorio_articulos_rechazados + 'vacios' + barra
        directorio_articulos_refinados = directorio_trabajo + 'articulos_refinados' + barra

        # Primero vemos si es necesario bajar el archivo xml gigante, o si ya está bajado.
        if not exists(directorio_archivo_raw):
            makedirs(directorio_archivo_raw)
        nombre_archivo_raw = 'eswiki-latest-pages-articles-multistream.xml'
        path_archivo_raw = directorio_archivo_raw + nombre_archivo_raw
        if actualiza_archivo_raw or not isfile(path_archivo_raw):
            # Si queremos actualizar el archivo raw, lo bajamos de Wikipedia (actualmente, 2,73GB comprimido).
            # También deberemos bajarlo cuando nos falte la versión descomprimida (que ocupa unos 11,5 GB) y
            # no tengamos la comprimida. En cualquier caso, el archivo que tenemos que bajar es:
            # https://dumps.wikimedia.org/eswiki/latest/eswiki-latest-pages-articles-multistream.xml.bz2
            # Este archivo tarda 24 minutos en bajar.
            if actualiza_archivo_raw or not isfile(path_archivo_raw + '.bz2'):
                # No tenemos la versión comprimida o la queremos actualizar, así que la descargamos.
                url_archivo_raw_bz2 =\
                    'https://dumps.wikimedia.org/eswiki/latest/' + nombre_archivo_raw + '.bz2'
                # url_archivo_raw_bz2 = url_archivo_raw_bz2.replace('latest', '20170820')
                print('Descargando de', url_archivo_raw_bz2 + '...', end=' ')
                hora_inicio_descarga = time()
                urllib.urlretrieve(url_archivo_raw_bz2, path_archivo_raw + '.bz2')
                tiempo_descarga = time() - hora_inicio_descarga
                print('descargado en', str(int(tiempo_descarga) / 3600).zfill(2) + ':' +
                      str((int(tiempo_descarga) / 60) % 60).zfill(2) + ':' +
                      str(tiempo_descarga % 60).zfill(2))
            # Como nos faltaba el archivo descomprimido (o queríamos actualizarlo), lo descomprimimos.
            # Tarda 9 minutos.
            print('Descomprimiendo', nombre_archivo_raw + '.bz2...', end=' ')
            hora_inicio_descompresion = time()
            # Es necesario usar bz2file.open porque el archivo es multistream, y bz2.BZ2File no lo soporta
            with bz2file.open(path_archivo_raw + '.bz2', 'rt', encoding="utf-8") as archivo_raw_bz2:
                with codecs.open(path_archivo_raw, "w", encoding='utf-8') as archivo_raw:
                    while True:
                        texto = archivo_raw_bz2.read(16 * 1024)
                        if not texto:
                            # Hemos acabado de trocear el archivo.
                            break
                        archivo_raw.write(texto)
            tiempo_descompresion = int(time() - hora_inicio_descompresion)
            print('descomprimido en {:02d}:{:02d}:{:02d}'.format(int(tiempo_descompresion / 3600),
                                                                 int(tiempo_descompresion / 60) % 60,
                                                                 int(tiempo_descompresion % 60)))
        elif exists(directorio_articulos_refinados):
            # No estamos procesando el archivo raw desde el principio, sino que ya lo teníamos y quizá lo
            # hayamos procesado parcialmente (el proceso completo de selección y refinado de artículos dura
            # unas 20 horas).
            # Debemos sacar la posición (byte) por el que hay que continuar el procesado del archivo raw.
            path_archivo_indice = directorio_articulos_refinados + 'index.txt'
            if isfile(path_archivo_indice):
                # Tenemos un archivo de índice que lista todos los archivos con sus contenidos.
                with codecs.open(path_archivo_indice, encoding='utf-8') as archivo_indice:
                    texto_indice = archivo_indice.read()
                if texto_indice:  # Podría estar vacío
                    # Con el contenido de index.txt, sabemos los artículos procesados y revisados, y los bytes
                    # ya consumidos del archivo gigante. También sabemos qué fascículo estábamos procesando.
                    ultimo_articulo_indexado = texto_indice[texto_indice.rfind('\n- ') + 3:]
                    n_articulos_procesados_inicial = int(ultimo_articulo_indexado[:7]) + 1
                    n_articulos_procesados = n_articulos_procesados_inicial
                    posicion_lectura_inicial = int(ultimo_articulo_indexado[8:19])
                    nombre_ultimo_archivo_indexado = ultimo_articulo_indexado[20:]
                    n_articulos_refinados_inicial = texto_indice.count('\n- ')
                    n_articulos_refinados = n_articulos_refinados_inicial
                    posicion_nombre_ultimo_fasciculo = texto_indice.rfind('En fascículo ') + 13
                    nombre_fasciculo_actual = texto_indice[posicion_nombre_ultimo_fasciculo:
                                                           posicion_nombre_ultimo_fasciculo + 19]

        print('-' * 100)
        print('| Leyenda: motivos por los que un artículo se rechaza o se acepta')
        print('| Artículos aceptados:')
        print('| +: Artículo válido y refinado')
        print('| Artículos rechazados: d: Módulo')
        print('| c: Categoría, p: Plantilla, a: Anexo, h: Ayuda, t: Portal, w: Wikipedia, Wikiproyecto, '
              'm: Mediawiki')
        print('| R: Redirección, D: Desambiguación, S: Sospechoso, 0: Vacío')
        print('-' * 100)
        print('0123456789' * 10)
        # Imprimimos blancos si ya hemos procesado artículos, para que el artículo que haga 100 quede justo a
        # la derecha
        if n_articulos_procesados:
            sys.stdout.write((n_articulos_procesados % 100) * ' ')

        # Leemos el archivo raw de la Wikipedia y lo separamos en artículos. Como el archivo es xml, el texto
        # de cada artículo aparece entre las etiquetas <page>...</page>, así que identificamos estas etiquetas
        # en el texto y nos quedamos con lo intermedio. De cada artículo obtendremos un string con toda la
        # información.
        # Por algún motivo, seek/tell no funcionan bien con codec.open, ya que parece que seek cuenta bytes
        # pero tell da información de caracteres (y los caracteres fuera del ASCII ocupan más de un byte). De
        # ahí que haya que abrir el archivo raw de texto como binario, leer por líneas y luego decodificar
        # como utf-8.
        longitud_archivo_raw = getsize(path_archivo_raw)
        archivo_raw = open(path_archivo_raw, "rb")
        if not exists(directorio_articulos_refinados):
            makedirs(directorio_articulos_refinados)

        if posicion_lectura_inicial:
            archivo_raw.seek(posicion_lectura_inicial)
            # Saltamos la primera línea, la que tiene el <page> para no volver a procesar/copiar el mismo
            # artículo.
            archivo_raw.readline()

            # Para tener un sistema con mayor tolerancia a los fallos, no damos por hecho que el fichero de
            # index y los fascículos estén "sincronizados": hemos podido borrar parte del index para que se
            # vuelva a reprocesar, con lo que tendríamos que volver a reescribir parte del fascículo. Lo que
            # hacemos es borrar aquello que esté en el fascículo que sea posterior al último artículo
            # "oficialmente" procesado.
            # Leemos al completo el último fascículo:
            with codecs.open(directorio_articulos_refinados + nombre_fasciculo_actual + '.txt',
                             encoding='utf-8') as archivo_fasciculo_actual:
                texto_fasciculo_actual = archivo_fasciculo_actual.read()
            # Buscamos el inicio de ese último artículo procesado. Recuerda que el nombre del último archivo
            # indexado ya incluye un salto de carro al final (es importante que el \n\n solo aparece tras un
            # título de artículo, y de ahí que encuentre sin error el inicio del artículo y no cualquier otro
            # texto que pueda incluir el nombre del artículo).
            inicio_ultimo_articulo_indexado =\
                texto_fasciculo_actual.find(nombre_ultimo_archivo_indexado + '\n')
            # A partir de ahí, buscamos el final del último artículo
            fin_ultimo_archivo_indexado = inicio_ultimo_articulo_indexado +\
                texto_fasciculo_actual[inicio_ultimo_articulo_indexado:].find(MARCA_FIN_ARTICULO) + 23
            # Recortamos lo que pudiera haber tras el fin de este último artículo (si no hemos modificado nada
            # a propósito, normalmente no habrá nada después, ya que el index.txt y el fascículo estarán
            # "sincronizados").
            texto_fasciculo_actual = texto_fasciculo_actual[:fin_ultimo_archivo_indexado]
            # Hay problemas para usar el truncate() en textos utf8, así que lo más sencillo es machacar el
            # archivo con el "nuevo" texto (que quizá sea el mismo que ya había). En cualquier caso se hace
            # una sola vez.
            with codecs.open(directorio_articulos_refinados + nombre_fasciculo_actual + '.txt', "w",
                             encoding='utf-8') as archivo_fasciculo_actual:
                archivo_fasciculo_actual.write(texto_fasciculo_actual)
            # Abrimos en modo append el fascículo y el archivo index para seguir escribiendo a partir del
            # final.
            archivo_fasciculo_actual = codecs.open(directorio_articulos_refinados + nombre_fasciculo_actual +
                                                   '.txt', "a", encoding='utf-8')
            archivo_indice = codecs.open(directorio_articulos_refinados + 'index.txt', "a", encoding='utf-8')
        else:
            # Tendríamos que crear el fichero del primer fascículo, pero todavía no sabemos qué título tendrá
            # porque no sabemos las posiciones de lectura que son las que le dan nombre. Lo ponemos a None más
            # que nada porque no podemos crear un fichero "genérico" sin abrir nada. Con el None este el
            # editor no se nos queja.
            archivo_fasciculo_actual = None
            # Creamos el archivo index.txt
            archivo_indice = codecs.open(directorio_articulos_refinados + 'index.txt', "w", encoding='utf-8')

        hora_inicio_refinado = time()
        texto_articulo_xml = ''
        posicion_lectura_actual = posicion_lectura_inicial
        hora_fin_fasciculo = hora_inicio_refinado
        bytes_fin_fasciculo = posicion_lectura_inicial
        while True:
            texto = archivo_raw.readline()
            try:
                texto = texto.decode("utf-8")
            except UnicodeDecodeError as error:
                # Muy raramente, hay algún texto que, por lo que sea, da error. He visto esto una vez en una
                # página de discusión, que incluía códigos raros. Para que no se pare todo, simplemente se
                # elimina desde el punto en el que da el error en adelante. En el fondo, el artículo no va a
                # interesar porque no es de contenido, así que da igual.
                texto = texto[:error.start].decode('utf-8')
            if not texto:
                # Hemos acabado de procesar el pedazo de archivo.
                break
            # Aún no ha acabado el archivo.
            if '<page>' in texto or texto_articulo_xml:
                # Comenzamos nuevo artículo o continuamos un artículo que llevábamos a medias.
                if '<page>' in texto:
                    # Comenzaba nuevo artículo. Actualizamos la posición de inicio del artículo.
                    posicion_lectura_actual = archivo_raw.tell() - len(texto)
                # En cualquier caso, añadimos la línea leída al texto del artículo (estará vacío si es nuevo).
                texto_articulo_xml += texto
                if '</page>' in texto:
                    # Hemos llegado al final del artículo, así que lo procesamos.
                    articulo = ElementTree.fromstring(texto_articulo_xml.encode('utf-8'))
                    texto_articulo_xml = ''
                    titulo_articulo = articulo.find('title').text.strip()
                    # En realidad, el nombre del archivo solo se usa si el artículo se rechaza y debemos
                    # guardarlo.
                    # No obstante, nos vale principalmente para guardar el código tipo AAAAAAA@PPPPPPPPPPP,
                    # que sí se usa para nombrar archivos de fascículos o en el índice.
                    nombre_archivo_articulo = '{:07d}@{:011d}#{}.txt'.format(n_articulos_procesados,
                                                                             posicion_lectura_actual,
                                                                             titulo_articulo)
                    if n_articulos_procesados % 100 == 0 and n_articulos_procesados:
                        # Vamos imprimiendo los motivos y estamos en la columna 100. Salto de carro.
                        print('')

                    n_articulos_procesados += 1
                    if not nombre_fasciculo_actual:
                        # Con el anterior artículo refinado, llegamos a la cantidad de artículos por fascículo
                        # y cerramos el archivo. Ahora creamos el siguiente archivo de fascículo.
                        nombre_fasciculo_actual = nombre_archivo_articulo[:19]
                    # Extraemos el propio texto (Wiki) del artículo xml parseado.
                    texto_articulo = articulo.find('revision').find('text').text
                    if not texto_articulo:
                        # Hay casos raros de artículos sin texto (MediaWiki:Excontent), y en esos casos la
                        # variable texto_articulo vale None (y no '') lo que crea problemas.
                        texto_articulo = ''
                    else:
                        texto_articulo = texto_articulo.strip()

                    # Hacemos una purga inicial de artículos:
                    # - Si el nombre del artículo comienza por: Ayuda:, Categoría:, Plantilla:, Anexo:,
                    #   Portal:, Mediawiki:, Wikipedia:, Wikiproyecto:, se aparta a especiales
                    # - Si el artículo contiene #REDIRECT o #REDIRECCIÓN (también minúsculas) se pone en
                    #   redirigidos
                    # - Si el artículo es una DESAMBIGUACIÓN, va al directorio de desambiguaciones.
                    marca_articulo_especial = titulo_articulo.find(':')
                    if marca_articulo_especial != -1:
                        marca = titulo_articulo[:marca_articulo_especial].lower()
                        if marca in ['anexo', 'ayuda', 'categoría', 'plantilla', 'portal',
                                     'mediawiki', 'módulo', 'wikipedia', 'wikiproyecto']:
                            motivo = 't' if marca == 'portal' else 'h' if marca == 'ayuda' else\
                                'd' if marca == 'módulo' else marca[:1].lower()
                            if motivo in articulos_rechazados_guardados:
                                # No lo refinamos. Lo metemos en el directorio de artículos
                                # rechazados/especiales.
                                ParseadorWikipedia.\
                                    guarda_articulo(directorio_articulos_rechazados + marca + barra,
                                                    nombre_fasciculo_actual, nombre_archivo_articulo,
                                                    titulo_articulo + '\n\n' + texto_articulo)
                            sys.stdout.write(motivo)
                            continue

                    if '#redirec' in texto_articulo.lower():
                        if 'R' in articulos_rechazados_guardados:
                            # No lo refinamos. Lo metemos en el directorio de rechazados/redirect
                            ParseadorWikipedia.guarda_articulo(directorio_articulos_redirect,
                                                               nombre_fasciculo_actual,
                                                               nombre_archivo_articulo,
                                                               titulo_articulo + '\n\n' + texto_articulo)
                        sys.stdout.write('R')
                        continue

                    if re.findall('\{\{desambiguación\}\}', texto_articulo, re.IGNORECASE):
                        if 'D' in articulos_rechazados_guardados:
                            # No lo refinamos. Lo metemos en el directorio de desambiguaciones
                            ParseadorWikipedia.guarda_articulo(directorio_articulos_desambiguacion,
                                                               nombre_fasciculo_actual,
                                                               nombre_archivo_articulo,
                                                               titulo_articulo + '\n\n' + texto_articulo)
                        sys.stdout.write('D')
                        continue

                    # EXTRACCIÓN DE CATEGORÍAS
                    # La idea inicial era extraer las categorías para enlazar semánticamente unos artículos
                    # con otros.
                    # Así que de momento desactivamos la identificación de las categorías.
                    # categorias = re.findall('\[\[categoría:[^\[]+?\]\]', texto_articulo, re.IGNORECASE)

                    # ELIMINACIÓN DE ETIQUETAS WIKI Y ELEMENTOS HIPERTEXTUALES
                    # Se refina el artículo, eliminando etiquetas (a veces también el contenido entre apertura
                    # y cierre)
                    texto_articulo_refinado = ParseadorWikipedia.refina_texto_articulo(texto_articulo)

                    # - Si tras eliminar etiquetas, tablas y demás, nos ha quedado un artículo vacío, lo
                    #   guardamos (sin refinar) en el directorio de rechazados/vacíos.
                    if texto_articulo_refinado == '':
                        if '0' in articulos_rechazados_guardados:
                            ParseadorWikipedia.guarda_articulo(directorio_articulos_vacios,
                                                               nombre_fasciculo_actual,
                                                               nombre_archivo_articulo,
                                                               titulo_articulo + '\n\n' + texto_articulo)
                        sys.stdout.write('0')
                        continue

                    # - Si tras el refinado queda alguna etiqueta (buscamos algo como </), se aparta a
                    #   sospechosos.
                    #   Esto son errores, y como tal, se tratan un poco como se puede.
                    texto_sospechoso = ''
                    if '</' in texto_articulo_refinado:
                        inicio = texto_articulo_refinado.find('</')
                        texto_sospechoso = texto_articulo_refinado[max(0, inicio - 30):
                                                                   min(len(texto_articulo_refinado),
                                                                       inicio + 30)]
                    if texto_sospechoso:
                        if 'S' in articulos_rechazados_guardados:
                            # Lo metemos (refinado) en el directorio de rechazados/sospechosos
                            ParseadorWikipedia.\
                                guarda_articulo(directorio_articulos_sospechosos, nombre_fasciculo_actual,
                                                nombre_archivo_articulo,
                                                titulo_articulo + '\n\n' + texto_articulo_refinado)
                        sys.stdout.write('S')
                        continue

                    # Guardamos el artículo en el fascículo. La estructura interna del artículo es:
                    # - Comienza con el título del artículo tal y como aparece en Wikipedia.
                    # - Separado con un doble salto de carro \n\n (el único en el texto) se encuentra el texto
                    #   del artículo, libre de etiquetas y demás. Los párrafos están separados por un único
                    #   salto de carro \n, y las secciones y subsecciones se distinguen de la forma
                    #   == Sección ==, === Subsección ===, siendo que los espacios entre los caracteres y el =
                    #   pueden no aparecer, además de que pueden usarse de 1 a 6 signos = (equivalentes a <h1>
                    #   a <h6>).
                    # - Al acabar el texto del artículo (el artículo se corta antes de llegar a las
                    #   referencias y bibliografía y demás), se añade, tras el último carácter
                    #   (presumiblemente un punto) el separador \n~~~~ Fin artículo ~~~~\n
                    if n_articulos_refinados % articulos_por_fasciculo == 0:
                        # Empezamos un nuevo fascículo. Lo marcamos en el archivo de índice.
                        nombre_fasciculo_actual = nombre_archivo_articulo[:19]
                        archivo_indice.write('En fascículo ' + nombre_fasciculo_actual + ':\n')
                        # Creamos el nuevo archivo de fascículo (cerramos primero el anterior).
                        if archivo_fasciculo_actual:
                            archivo_fasciculo_actual.close()
                        archivo_fasciculo_actual = codecs.open(directorio_articulos_refinados +
                                                               nombre_fasciculo_actual + '.txt', "w",
                                                               encoding='utf-8')
                    # Añadimos este artículo al fascículo y marcamos su final.
                    archivo_fasciculo_actual.write(titulo_articulo + '\n\n' + texto_articulo_refinado + '\n' +
                                                   MARCA_FIN_ARTICULO)
                    # Damos cuenta en el índice de la posición de este artículo.
                    archivo_indice.write('- ' + nombre_archivo_articulo[:-4] + '\n')
                    # Obligamos a que la escritura sea efectiva, por si paramos la ejecución, para que no se
                    # pierda información.
                    archivo_fasciculo_actual.flush()
                    archivo_indice.flush()
                    sys.stdout.write('+')
                    n_articulos_refinados += 1
                    if n_articulos_refinados % articulos_por_fasciculo == 0 and n_articulos_refinados:
                        # Hemos refinado 1000 artículos y acabamos de terminar un fascículo.
                        # Vamos a hacer cálculos de velocidad y tiempos remanentes de procesado.
                        # Primero estadísticas aplicadas al total de los bytes procesados
                        ahora = time()
                        posicion_actual = archivo_raw.tell()
                        tiempo_de_refinado = ahora - hora_inicio_refinado
                        bytes_procesados = posicion_actual - posicion_lectura_inicial
                        bytes_restantes = longitud_archivo_raw - posicion_actual
                        velocidad = bytes_procesados / tiempo_de_refinado
                        tiempo_restante = bytes_restantes / velocidad
                        hora_fin_estimada = int(ahora + tiempo_restante)
                        # Luego los valores del último fascículo (valores "instantáneos")
                        velocidad_instantanea = (posicion_actual - bytes_fin_fasciculo) /\
                            (ahora - hora_fin_fasciculo)
                        tiempo_restante_instantaneo = bytes_restantes / velocidad_instantanea
                        hora_fin_estimada_instantanea = int(ahora + tiempo_restante_instantaneo)
                        # Actualizamos los valores de inicio de fascículo
                        hora_fin_fasciculo = ahora
                        bytes_fin_fasciculo = posicion_actual
                        tiempo_de_refinado = int(tiempo_de_refinado)
                        velocidad = int(velocidad)
                        velocidad_instantanea = int(velocidad_instantanea)
                        tiempo_restante = int(tiempo_restante)
                        # Imprimimos las estadísticas
                        print('\n\n- Artículos Procesados:', '{:7d}'.format(n_articulos_procesados),
                              '  - Bytes Procesados:', ' {:11d}'.format(bytes_procesados),
                              '  - Tiempo de Procesado: ',
                              '{:02d}:{:02d}:{:02d}'.format(int(tiempo_de_refinado / 3600),
                                                            int(tiempo_de_refinado / 60) % 60,
                                                            int(tiempo_de_refinado % 60)))
                        print('- Artículos Refinados:', '{:8d}'.format(n_articulos_refinados),
                              '  - Bytes Restantes:  ', '{:11d}'.format(bytes_restantes),
                              '  - Tiempo Restante:     ',
                              '{:02d}:{:02d}:{:02d}'.format(int(tiempo_restante / 3600),
                                                            int(tiempo_restante / 60) % 60,
                                                            int(tiempo_restante % 60)))
                        print(' ' * 34 + '- Velocidad (bytes/seg):', '{:7d}'.format(velocidad),
                              '  - Hora de finalización:', strftime('%H:%M:%S', localtime(hora_fin_estimada)))
                        print(' ' * 58 + '(' + '{:7d}'.format(velocidad_instantanea) + ')' +
                              ' ' * 25 + '(' + strftime('%H:%M:%S', localtime(hora_fin_estimada_instantanea))
                              + ')')
                        print('')
                        sys.stdout.write((n_articulos_procesados % 100) * ' ')
                        pass

        # Hemos llegado al final del archivo raw. Lo cerramos, junto al archivo de índice.
        archivo_raw.close()
        archivo_indice.close()
        # Es posible que no hayamos llegado a abrir ningún fascículo (posibilidad enrevesada pero existe).
        if archivo_fasciculo_actual:
            archivo_fasciculo_actual.close()
        # Calculamos el tiempo total de ejecución.
        tiempo_total = int(time() - hora_inicio_total)
        print('\n\n' + str(n_articulos_refinados - n_articulos_refinados_inicial), 'artículos refinados (' +
              str(n_articulos_procesados - n_articulos_procesados_inicial) + ' procesados) en',
              '{:02d}:{:02d}:{:02d}'.format(int(tiempo_total / 3600),
                                            int(tiempo_total / 60) % 60,
                                            int(tiempo_total % 60)))

    @staticmethod
    def guarda_articulo(directorio_salida, subdirectorio_salida, nombre_archivo_salida, texto_articulo):
        """Crea un archivo de texto en el path directorio/subdirectorio/nombre, recortando el nombre si es muy
        largo.

        Como el nombre del archivo puede incluir todo tipo de caracteres (ya que se usa el título del
        artículo), antes de nada se modifica el nombre del archivo, eliminando y modificando caracteres
        prohibidos, y recortándolo para que no sobrepase el tamaño máximo del path.

        :type directorio_salida: unicode
        :param directorio_salida: Path del directorio donde se guardará el archivo de texto (acabado en '/').
        :type subdirectorio_salida: unicode
        :param subdirectorio_salida: Nombre del subdirectorio donde se guardará el archivo de texto (acabado
            en '/').
        :type nombre_archivo_salida: unicode
        :param nombre_archivo_salida: Nombre del archivo de salida donde se guardará el texto (acabado en
            '.txt').
        :type texto_articulo: unicode
        :param texto_articulo: El contenido de texto que se guardará en el archivo.

        """
        # Eliminamos y reemplazamos los caracteres prohibidos en los nombres de archivos.
        titulo_retocado = re.sub(r'[\\/?*|<>]', '', nombre_archivo_salida).replace(':', '_').replace('"', "'")

        if not exists(join(directorio_salida, subdirectorio_salida)):
            # Si no existe el subdirectorio, se crea (incluyendo también los directorios previos).
            makedirs(join(directorio_salida, subdirectorio_salida))
        path_archivo_salida = directorio_salida + subdirectorio_salida + barra + titulo_retocado
        if len(path_archivo_salida) >= 260:
            # El path es demasiado grande. Recortamos el nombre del archivo
            extension = path_archivo_salida.split('.')[-1]
            path_archivo_salida = path_archivo_salida[:258 - len(extension)] + '.' + extension
        try:
            # Abrimos, guardamos y cerramos.
            archivo_salida = codecs.open(path_archivo_salida, "w", encoding='utf-8')
            archivo_salida.write(texto_articulo)
            archivo_salida.close()
        except Exception as excepcion:
            print('\n#### Error escribiendo', path_archivo_salida)
            print(str(excepcion))

    @staticmethod
    def refina_texto_articulo(texto_articulo):
        """Se eliminan las etiquetas wiki, tablas, plantillas, enlaces... del texto, y se devuelve.

        Es importante que no elimina los marcadores de (sub)sección (tipo ^(={1,6}).+\1$), ya que se
        utilizarán para estructurar el texto en palabras, frases, párrafos, secciones y artículos.

        Además, todos los saltos de carro son de una única línea, y se trunca el artículo antes de la
        bibliografía, referencias, notas...

        :type texto_articulo: unicode
        :param texto_articulo: El texto tal y como aparece en la Wikipedia.
        :rtype: unicode
        :return: El texto del artículo, refinado y sin etiquetas ni símbolos de formato.
        """
        # NOS QUEDAMOS HASTA LA SECCIÓN DE REFERENCIAS/ENLACES EXTERNOS
        # Usualmente el texto que aparece aquí son URLs, nombres de libros (en inglés) y "basurilla".
        # Regex optimizado
        regex =\
            '\n(={1,6})\s*(Referencias?|Bibliografía|Notas|Enlaces externos|Véase también)\s*\\1\n[\w\W]*'
        texto_articulo = re.sub(regex, '', texto_articulo)

        # ELIMINAMOS LA SECCIÓN DE ALGUNAS PUBLICACIONES Y LIBROS
        # Aparecen habitualmente en artículos sobre científicos que han publicado cosas, y está lleno de
        # referencias bibliográficas, casi siempre en inglés.
        regex = '\n(={1,6})\s*(Algunas publicaciones|Libros)\s*\\1\n[\w\W]*(?:\n=)'
        texto_articulo = re.sub(regex, '', texto_articulo)

        # COMENTARIOS: <!---...--->
        # Regex optimizado
        regex = '<!--(?:[^>]*>)*?(?<=-->)'
        texto_articulo = re.sub(regex, '', texto_articulo)

        # FUNCIONES DE PARSEADO: {{#función: ... | ... }} y {{plantilla|param1|param2|...}}
        # Las funciones son como {{#if: ... }} https://www.mediawiki.org/wiki/Help:Extension:ParserFunctions
        # y eliminamos todo su contenido.
        # Es interesante eliminar estas antes que las tablas ({|...|}) porque pueden llevar en su interior
        # parámetros separados por | (y en las funciones de parseado, además este símbolo sirve, pospuesto,
        # para chequear la existencia de una variable), que si van al final, se junta con el } de cierre y
        # da la sensación de que es el cierre de tabla.
        #
        # PLANTILLAS DE WIKIPEDIA: {{Plantilla|param1|param2...}}
        # Las eliminamos por completo salvo unas cuantas, para las que solo eliminamos la etiqueta.
        # Nos quedamos con el texto que se muestra y descartamos los parámetros previos.
        # Pueden estar anidadas (de ahí el bucle de bucklers sin alcohol).
        # Algunas de estas plantillas tienen parámetros que podrían ser utilizables (como texto de enlaces):
        # - {{AP|Período de las Autonomías Provinciales (Argentina)}} -> Artículo principal
        # - {{VT|Constitución de la Nación Argentina}} -> Véase también
        # Sin embargo, los parámetros pueden ser categorías también, y habría que hacerlo "bien". Este texto
        # que se podría aprovechar, en la mayoría o (total) de los artículos, aparecerá inmediatamente después
        # o como parte del título de la sección.
        # En realidad hay cientos de plantillas, aunque la mayor parte de ellas se usan para incluir
        # información que no es textual en español. En cualquier caso, hemos escogido un reducidísimo número,
        # las más usadas, sacadas de
        # https://es.wikipedia.org/wiki/Categor%C3%ADa:Wikipedia:Plantillas_de_formato_de_texto
        #
        # Es interesante eliminar estas antes que las tablas ({|...|}) porque pueden llevar en su interior
        # parámetros separados por | (y en las funciones de parseado, además este símbolo sirve, pospuesto,
        # para chequear la existencia de una variable), que si van al final, se junta con el } de cierre y
        # da la sensación de que es el cierre de tabla.
        plantillas_respetables = ['esd', 'nowrap', 'small', 'grande', 'tamaño', 'abreviatura',
                                  'versalita', 'sobrerrayado', 'sin negrita', 'sin cursiva']
        inicio = 0
        while True:
            # Pueden aparecer etiquetas del tipo {{...}} anidadas. Así que nos aseguramos de que cortamos por
            # el }} que esté al mayor nivel, permitiendo que se incluyan etiquetas del mismo tipo dentro de la
            # propia etiqueta.
            inicio = texto_articulo.find('{{', inicio)
            if inicio == -1:
                # Hemos llegado al final. Salimos del bucle.
                break
            fin = inicio + 2
            contenido = ''
            while not contenido or contenido.count('{') - contenido.count('}') != 0:
                # No hay la misma cantidad de cierres que de aperturas. Esto es debido a que aún no hemos
                # buscado el cierre (primera iteración) o a que hemos llegado a un cierre anidado.
                # Forzosamente, el que cierra la apertura está más adelante.
                # Buscamos un cierre o un cambio de sección (que "resetea" todo y vale como cierre).
                # Se resta a fin -1 ya que a veces se pueden tener cosas como {{{...}}} y el
                # algoritmo encuentra los dos primeros {{ y los dos primeros }}, de forma que no puede
                # cuadrar, porque si avanzamos 2 es incapaz de encontrar los dos segundos }}
                cierre = re.search('(?:\}\})|(?:\n=+[^\n]+=+\s*?\n)', texto_articulo[fin - 1:])
                if cierre:
                    # Hemos encontrado un cierre (o cambio de sección)
                    fin += cierre.start() - 1
                    if texto_articulo[fin:fin + 2] == '}}':
                        # Es un auténtico cierre. Actualizamos el contenido y volvemos a verificar.
                        fin += 2
                        contenido = texto_articulo[inicio + 2:fin - 2]
                        continue
                    else:
                        # Hemos llegado a un cambio de sección sin encontrar el cierre.
                        # Eliminamos desde el principio del párrafo donde estaba la apertura, hasta el inicio
                        # de la sección.
                        inicio = texto_articulo[:inicio].rfind('\n') + 1
                else:
                    # No hemos encontrado ni un cierre ni un cambio de sección.
                    fin = len(texto_articulo)
                texto_articulo = texto_articulo[:inicio] + texto_articulo[fin:]
                break
            else:
                # Hemos conseguido cuadrar correctamente aperturas con cierres.
                if re.findall('^(' + '|'.join(plantillas_respetables) + ')',
                              contenido, flags=re.IGNORECASE):
                    # Hemos encontrado una de las plantillas de las que sólo eliminamos la etiqueta.
                    # Nos quedamos con el último parámetro.
                    contenido = contenido.split('|')[-1]
                else:
                    # Es una plantilla de las que hay que eliminar completamente.
                    contenido = ''
                texto_articulo = texto_articulo[:inicio] + contenido + texto_articulo[fin:]

        # TABLAS: {|....|}
        # Se borran por completo. Es el mismo modelo que para plantillas o funciones de parseado, con la
        # diferencia de que las tablas puede incluir secciones dentro.
        inicio = 0
        while True:
            # Pueden aparecer etiquetas del tipo {|...|} anidadas. Así que nos aseguramos de que cortamos por
            # el |} que esté al mayor nivel, permitiendo que se incluyan etiquetas del mismo tipo dentro de la
            # propia etiqueta.
            inicio = texto_articulo.find('{|', inicio)
            if inicio == -1:
                # Hemos llegado al final. Salimos del bucle.
                break
            fin = inicio + 2
            contenido = ''
            while not contenido or contenido.count('{|') - contenido.count('|}') != 0:
                # No hay la misma cantidad de cierres que de aperturas. Esto es debido a que aún no hemos
                # buscado el cierre (primera iteración) o a que hemos llegado a un cierre anidado.
                # Forzosamente, el que cierra la apertura está más adelante. Buscamos un cierre.
                fin = texto_articulo.find('|}', fin)
                if fin != -1:
                    # Hemos encontrado un cierre.
                    fin += 2
                    contenido = texto_articulo[inicio + 2:fin - 2]
                    continue
                # Al no encontrar el cierre, preferimos no arriesgar y cortar el archivo hasta este párrafo.
                inicio = texto_articulo[:inicio].rfind('\n') + 1
                texto_articulo = texto_articulo[:inicio]
                break
            else:
                contenido = ''
                texto_articulo = texto_articulo[:inicio] + contenido + texto_articulo[fin:]
        # Existen algunas plantillas como Colort, que por algún motivo, a veces tienen un cierre |} que no
        # hace ninguna falta. Como ya hemos procesado las tablas, eliminamos estos cierres extra.
        texto_articulo = texto_articulo.replace('|}', '')

        # ENLACES: [[rey (ajedrez)|rey]] blanco
        # [[Archivo:Pucará.jpg|izquierda|miniaturadeimagen|Yacimiento arqueológico [[Pucará de Tilcara]].]]
        # Nos quedamos con el texto que se muestra y descartamos los parámetros previos.
        inicio = 0
        while True:
            # Pueden aparecer etiquetas del tipo [[...]] anidadas. Así que nos aseguramos de que cortamos por
            # el ]] que esté al mayor nivel, permitiendo que se incluyan etiquetas del mismo tipo dentro de la
            # propia etiqueta.
            inicio = texto_articulo.find('[[', inicio)
            if inicio == -1:
                # Hemos llegado al final. Salimos del bucle.
                break
            fin = inicio + 2
            contenido = ''
            while not contenido or contenido.count('[') - contenido.count(']') != 0:
                # No hay la misma cantidad de cierres que de aperturas. Esto es debido a que aún no hemos
                # buscado el cierre (primera iteración) o a que hemos llegado a un cierre anidado.
                # Forzosamente, el que cierra la apertura está más adelante.
                # Buscamos un cierre o un cambio de sección (que "resetea" todo y vale como cierre).
                # Se resta a fin -1 ya que a veces se pueden tener cosas como [[...[...]]] y el
                # algoritmo encuentra los dos primeros [[ y los dos primeros ]], de forma que no puede
                # cuadrar, porque si avanzamos 2 es incapaz de encontrar los dos segundos ]]
                cierre = re.search('(?:\]\])|(?:\n=+[^\n]+=+\s*?\n)', texto_articulo[fin - 1:])
                if cierre:
                    # Hemos encontrado un cierre (o cambio de sección)
                    fin += cierre.start() - 1
                    if texto_articulo[fin:fin + 2] == ']]':
                        # Es un auténtico cierre. Actualizamos el contenido y volvemos a verificar.
                        fin += 2
                        contenido = texto_articulo[inicio + 2:fin - 2]
                        continue
                    else:
                        # Hemos llegado a un cambio de sección sin encontrar el cierre.
                        # Eliminamos desde el principio del párrafo donde estaba la apertura, hasta el inicio
                        # de la sección.
                        inicio = texto_articulo[:inicio].rfind('\n') + 1
                else:
                    # No hemos encontrado ni un cierre ni un cambio de sección.
                    fin = len(texto_articulo)
                texto_articulo = texto_articulo[:inicio] + texto_articulo[fin:]
                break
            else:
                # Hemos conseguido cuadrar correctamente aperturas con cierres.
                if ':' not in contenido or contenido.split(':')[0].lower()\
                        not in ['categoría', 'archivo', 'file', 'image', 'imagen', 'als']:
                    # Los enlaces son del tipo [[nombre artículo|texto]]. Nos quedamos con el texto, con el
                    # pequeño problema de que puede no haber texto (cuando se quiere que aparezca el mismo
                    # texto que el título del artículo al que se enlaza) o el texto puede incluir a su vez más
                    # estructuras que hagan uso de |.
                    # De ahí que nos quedemos el contenido al completo si no hallamos un |, y si no, nos
                    # quedamos con lo que queda a la derecha de dicho primer | (muy probablemente último).
                    contenido = contenido[(contenido.find('|') + 1) if '|' in contenido else 0:]
                else:
                    # Es un enlace de los que hay que eliminar completamente.
                    contenido = ''
                texto_articulo = texto_articulo[:inicio] + contenido + texto_articulo[fin:]

        # PARÁMETROS TIPO HTML: <ref ...>...</ref>, <ref ... />
        # Se elimina tanto la etiqueta como el contenido. Se tienen en Cuenca los anidamientos.
        # Conviene eliminar estas etiquetas después de las de tablas, plantillas y enlaces ({|, {{, [[) porque
        # ocurre a veces que el último parámetro de una plantilla es algo en html, y al eliminarlo nos queda
        # el separador de parámetro | junto al marcador de fin de plantilla }}, y eso parece un fin de tabla.
        tags = ['cite', 'code', 'del', 'font', 'gallery', 'includeonly', 'kbd', 'math', 'nowiki',
                'onlyinclude', 'pre', 'ref', 'r[bpt]', 'ruby', 's(trike)?', 'samp', 'source',
                'syntaxhighlight', 'table', 't[dhr]', 'time(line)?', 'mapframe', 'graph', 'hr',
                'imagemap']
        regex_apertura = '(?:< ?(' + '|'.join(tags) + ')[^>]*?>)'
        inicio = 0
        while True:
            # Primero buscamos una etiqueta de apertura (quizá también con el cierre incluido)
            extremos_apertura = re.search(regex_apertura, texto_articulo[inicio:], flags=re.IGNORECASE)
            if not extremos_apertura:
                # No hemos encontrado etiquetas de apertura, así que hemos terminado el procesado
                break

            # Extraemos el contenido de la etiqueta de apertura
            fin = inicio + extremos_apertura.end()
            inicio += extremos_apertura.start()
            apertura = texto_articulo[inicio:fin]
            # Vemos si la etiqueta tiene "autocierre"
            if apertura[-2:] == '/>':
                # Lo tiene. Simplemente borramos la etiqueta.
                texto_articulo = texto_articulo[:inicio] + texto_articulo[fin:]
            else:
                # Tenemos que buscar el cierre, para lo cual primero extraemos cuál es la etiqueta.
                etiqueta = re.search('[a-z]+', apertura, flags=re.IGNORECASE).group().lower()
                # Buscamos la primera etiqueta de cierre (de este tipo de etiqueta) que sigue a esta etiqueta.
                regex_cierre = '(?:<\/ ?' + etiqueta + ' ?>)'
                extremos_cierre = re.search(regex_cierre, texto_articulo[inicio:], flags=re.IGNORECASE)
                if not extremos_cierre:
                    # Pues hay un problema con las aperturas y cierres, que están mal. Para cortar por lo sano
                    # borramos desde el principio del párrafo hasta la siguiente sección.
                    inicio_parrafo = texto_articulo[:inicio].rfind('\n') + 1
                    extremos_seccion = re.search('(?:\n=+[^\n]+=+\s*?\n)', texto_articulo[inicio:])
                    if extremos_seccion:
                        fin = inicio + extremos_seccion.start()
                    else:
                        fin = len(texto_articulo)
                    inicio = inicio_parrafo
                    texto_articulo = texto_articulo[:inicio] + texto_articulo[fin:]
                    continue
                # Se ha encontrado el siguiente cierre a la apertura que vimos, pero eso no significa que
                # ambas etiquetas estén emparejadas. Podemos tener algo como <div>...<div>...</div>...</div>,
                # y en ese caso habríamos encontrado la primera y la tercera etiqueta, que no están
                # relacionadas.
                # Por ello, lo que hacemos es buscar la etiqueta de apertura concreta que hemos encontrado,
                # pero en el texto que hay entre el inicio de la apertura y el inicio del cierre y nos
                # quedamos con la última aparición. Esa aparición será habitualmente la que ya hemos
                # encontrado, pero asi evitamos emparejar mal las aperturas con los cierres.
                regex_reapertura = '(?:< ?' + etiqueta + '[^>]*?>)'
                extremos_reapertura =\
                    [f for f in re.finditer(regex_reapertura,
                                            texto_articulo[inicio:inicio + extremos_cierre.end()],
                                            flags=re.IGNORECASE)][-1]
                # A la fuerza se encuentra algo, normalmente lo mismo que con el regex_apertura. Borramos el
                # par de etiquetas y lo que queda entre medias, salvo en los <cite>.
                texto_articulo = texto_articulo[:inicio + extremos_reapertura.start()] + \
                    ('' if apertura != '<cite>'
                     else texto_articulo[inicio + extremos_reapertura.end():
                                         inicio + extremos_cierre.start()]) + \
                    texto_articulo[inicio + extremos_cierre.end():]
        # También hay etiquetas que no necesitan tener cierre, como <br> o <hr>.
        texto_articulo = re.sub('< ?[bh]r[^/>]*?>(?=/>)', '\n', texto_articulo, flags=re.IGNORECASE)

        # FILAS DE PLANTILLAS DE TABLAS: |...
        # Es muy difícil de identificar, pero hay plantillas que abren y cierran las llaves, y luego ponen
        # líneas de separación así, fuera de área de llaves y de todo. Así que lo hacemos a pelo.
        regex = '(?:\|[^\n]+)'
        texto_articulo = re.sub(regex, '', texto_articulo, flags=re.IGNORECASE)

        # FORMATO: ''...'', '''...'''
        # Quitamos las marcas estas. De momento dejamos los ' simples, pero más adelante los eliminaremos.
        texto_articulo = texto_articulo.replace("'''", '').replace("''", '')

        # ENLACES EXTERNOS: [https://....]
        regex = '\[(?:https?:)?\/\/[^\[]+?\]'
        texto_articulo = re.sub(regex, '', texto_articulo, flags=re.IGNORECASE)

        # ENLACES EXTERNOS DIRECTOS
        # A veces aparecen sin más en el texto.
        regex = '(?:https?:)?\/\/[^ \t\n]+'
        texto_articulo = re.sub(regex, '', texto_articulo, flags=re.IGNORECASE)

        # ETIQUETAS FORMATO: <tag>...</tag>, <tag />
        # https://es.wikipedia.org/wiki/Ayuda:HTML_en_el_wikitexto
        # Eliminamos sólo las etiquetas. Como solo se quita la etiqueta, y es bastante frecuente que estén
        # descabaladas no nos fijamos en los emparejamientos de aperturas y cierres, sino que las quitamos
        # todas a capón.
        tags_formato = ['abbr', 'b', 'bd[io]', 'big', 'blockquote', 'caption', 'center', 'data',
                        'd[dlt]',
                        'dfn', 'div', 'em', 'font', 'i', 'ins', 'li', 'mark', 'noinclude',
                        '[ou]l',
                        'p', 'poem', 'q', 'small', 'span', 'strong', 'su[bp]', 'tt', 'u', 'var',
                        'wbr']
        regex = '(?:<\/? ?(' + '|'.join(tags_formato) + ')[^>]*?>)'
        texto_articulo = re.sub(regex, '', texto_articulo, flags=re.IGNORECASE)

        # ENCABEZADOS DE SECCIONES: <h1>...</h1>
        regex = '(?:<\/?h[1-6]>)'
        inicio = 0
        while True:
            # Buscamos la apertura o el cierre de la etiqueta de encabezado
            extremos_apertura = re.search(regex, texto_articulo[inicio:], flags=re.IGNORECASE)
            if not extremos_apertura:
                # No hemos encontrado etiquetas de este tipo, así que salimos
                break
            # Extraemos el contenido de la etiqueta
            fin = inicio + extremos_apertura.end()
            inicio += extremos_apertura.start()
            etiqueta = texto_articulo[inicio:fin]
            # Miramos qué nivel de encabezado es (el número tras la h)
            nivel = int(etiqueta[-2])
            texto_articulo = texto_articulo[:inicio] + ('=' * nivel) + texto_articulo[fin:]

        # ENTIDADES HTML
        texto_articulo = ParseadorWikipedia.unescape(texto_articulo)

        # CÓDIGOS DE LISTAS: ##, **, ::, ;...
        # Se pueden poner varios # o * al inicio de la línea
        texto_articulo = re.sub('(?:(?<=^)|(?<=\n))[#*:;]+\s*', '', texto_articulo)

        # LÍNEAS DIVISORIAS: ----
        texto_articulo = re.sub('(?:(?:(?<=^)|(?<=\n))----\n?)', '\n', texto_articulo)

        # PALABRAS RESERVADAS DE WIKIPEDIA: __NOMBRE__
        texto_articulo = re.sub('__[A-Z]+__', '', texto_articulo, flags=re.IGNORECASE)

        # BLANCOS AL INICIO Y AL FINAL DE PÁRRAFO
        texto_articulo = re.sub('(?:(?:(?<=^)|(?<=\n))[\t ]+)|(?:[\t ]+(?:(?=$)|(?=\n)))',
                                '', texto_articulo)

        # PARÉNTESIS VACÍOS
        # Es bastante común que entre paréntesis haya una plantilla estándar, y al borrarla, queda vacío
        texto_articulo = re.sub('\(\s*\)', '', texto_articulo)

        # ESPACIOS SUPERFLUOS
        # Al quitar etiquetas, suelen estar rodeadas de espacios, con lo que queda más de un espacio junto.
        texto_articulo = re.sub(' {2,}', ' ', texto_articulo)
        # Por el mismo motivo, a veces quedan espacios seguidos de signo de puntuación.
        texto_articulo = re.sub('\s+([,.;:])', '\\1', texto_articulo)

        # SALTOS DE LÍNEA SUPERFLUOS
        texto_articulo = re.sub('\n\s*\n+', '\n', texto_articulo).strip()

        # ELIMINAMOS SECCIONES QUE CONTENGAN ISBN
        # Hay muchas secciones que tienen nombres variados y que contienen obras de diverso tipo, en diversas
        # lenguas, y que en ocasiones podemos descubrir porque tienen un ISBN/ISSN. Quitamos toda la sección.
        regex = '(?:\n=(?:(?:\n(?!=))|.)*?IS[BS]N +[0-9](?:\n|.)*?(?:$|(?=\n(?:=|~))))'
        texto_articulo = re.sub(regex, '', texto_articulo, flags=re.IGNORECASE)

        claves = ['colspan', 'align', 'background', 'style', 'width', 'height', 'latitude', 'bgcolor',
                  'svg', 'ngc', 'circle', 'jesc', 'jpg']
        if sum([1 if key in texto_articulo else 0
                for key in claves]) > 1:
            for clave in claves:
                texto_articulo = re.sub('^(?:(?:\||!)[^\n]*?' + clave + '[^\n]*(?:\n|$))', '',
                                        texto_articulo, flags=re.IGNORECASE | re.MULTILINE)
                texto_articulo = re.sub('\n\s*\n+', '\n', texto_articulo).strip()

        return texto_articulo

    @staticmethod
    def unescape(texto):
        """Convierte las entidades XML/HTML, tipo &oacute; o lo que es lo mismo, &#243; en sus caracteres
        unicode.

        :type texto: unicode
        :param texto: El texto en el que se tienen que convertir las entidades en caracteres.
        :rtype: unicode
        :return: El texto de entrada con las entidades convertidas en caracteres unicode.
        """
        def fixup(m):
            """Se convierte el texto que representa a una entidad, en el carácter unicode al que equivale.

            :type m: SRE_Match
            :param m: Un objeto match de la expresión regular que captura entidades HTML.
            :rtype: unicode
            :return: El texto unicode que equivale a la entidad HTML.
            """
            texto_con_entidades_html = m.group(0)
            if texto_con_entidades_html[:2] == '&#':
                # character reference
                try:
                    if texto_con_entidades_html[:3] == '&#x':
                        return chr(int(texto_con_entidades_html[3:-1], 16))
                    else:
                        return chr(int(texto_con_entidades_html[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    texto_con_entidades_html =\
                        chr(htmlentitydefs.name2codepoint[texto_con_entidades_html[1:-1]])
                except KeyError:
                    pass
            return texto_con_entidades_html  # leave as is

        # Llamamos a re.sub con el parámetro de reemplazo tipo callable en vez de string. re.sub le pasará el
        # argumento del match que haya podido encontrar.
        return re.sub('&#?\w+;', fixup, texto)

    @staticmethod
    def divide_en_snippets(texto_articulo, palabras_por_snippet=200,
                           caracteres_invalidos='0123456789\-_/$%&*+<>=@#^'):
        """Dividimos un texto de un artículo de la Wikipedia en snippets.

        Cada artículo se divide en trozos (snippets) que intentan tener alrededor del número de palabras que
        se indica en el parámetro. No dividimos los párrafos, y juntamos los nombres de las secciones con los
        párrafos siguientes. Este método se utiliza para crear representaciones semánticas vectoriales.

        :type texto_articulo: unicode
        :param texto_articulo: El texto del artículo que queremos dividir en snippets. Tiene que incluir las
            marcas de seccion (tipo "^(={1,6})[^\n]+\1$"), o si no, todo el texto se tratará como una misma
            sección.
        :type palabras_por_snippet: int
        :param palabras_por_snippet: El número "ideal" de palabras que tendría que tener cada snippet. Como no
            se dividen los párrafos, este número es indicativo, y normalmente los snippets no tendrán casi
            nunca el número exacto de palabras, sino que tendrán un número de palabras cercano a este ideal.
            Si este número es 0, significa que queremos crear un snippet con todo el texto del artículo, sin
            importar los headers, párrafos ni nada.
        :type caracteres_invalidos: unicode
        :param caracteres_invalidos: Caracteres que invalidan una palabra. Al segmentar el texto, toda aquella
            "palabra" que incluya alguno de estos caracteres será considerada como inválida (y se descartará).
        :rtype: [{unicode}]
        :return: Una lista de snippets, cada uno de ellos conteniendo un conjunto de palabras (que son cadenas
            unicode).
        """
        # Dividimos en párrafos, teniendo en cuenta las secciones.
        regex_seccion = '(?:={1,6})[^=].*?(?<!=)(?:={1,6})$'
        # Primero quitamos el título, que está al inicio y separado del cuerpo del artículo por un doble \n
        # (que es el único doble \n que hay en el texto del artículo).
        titulo, texto_articulo = texto_articulo.split('\n\n')
        parrafos = [par.strip() for par in texto_articulo.split('\n') if par.strip()]
        snippets = []
        # Comenzamos el primer snippet con el título
        snippet_actual = Tokenizer.segmenta_por_palabras([titulo], elimina_separadores=True,
                                                         segmenta_por_guiones_internos=False,
                                                         segmenta_por_guiones_externos=True,
                                                         adjunta_separadores=False,
                                                         agrupa_separadores=False)
        # Consideramos el título como el header a mayor nivel posible, nivel 0 (a menor número, mayor
        # importancia).
        nivel_header_actual = 0
        for texto_parrafo in parrafos:
            # El texto del artículo se ha refinado, pero se han dejado las marcas de (sub)secciones para poder
            # dividir el texto en sus componentes. Las secciones habitualmente se marcan con (== ?)...( ?==),
            # con el título de la sección entre medias, y las subsecciones habitualmente se marcan con tres
            # signos ===.
            # No obstante, se admiten entre uno y seis signos de =, para imitar los <h1> - <h6>
            if re.match(regex_seccion, texto_parrafo):
                # Tenemos un título de sección. Vemos qué nivel de encabezado es.
                nivel_header = len(texto_parrafo) - len(texto_parrafo.lstrip('='))
                # Eliminamos las marcas.
                texto_parrafo = re.sub('(^(?:={1,6}\s*))|((?:\s*={1,6})$)', '', texto_parrafo)
            else:
                nivel_header = 7
            # Dividimos el texto en frases y palabras
            frases = Tokenizer.segmenta_por_frases(texto_parrafo, elimina_separadores=True,
                                                   elimina_separadores_blancos=True)
            palabras_parrafo = [pal for pal in
                                Tokenizer.segmenta_por_palabras(frases, elimina_separadores=True,
                                                                segmenta_por_guiones_internos=False,
                                                                segmenta_por_guiones_externos=True,
                                                                adjunta_separadores=False,
                                                                agrupa_separadores=False)
                                if not re.findall('[' + caracteres_invalidos + ']', pal)]
            if not palabras_parrafo:
                # Puede ocurrir cuando entra un párrafo con números o símbolos que queda reducido a 0
                # palabras.
                continue
            if palabras_por_snippet == 0:
                # Esto quiere decir que debemos siempre añadir todo el texto para crear un único snippet por
                # artículo. Así que no necesitamos calcular nada y simplemente añadimos las palabras al
                # snippet.
                comienza_nuevo_snippet = False
            elif nivel_header == nivel_header_actual:
                # Lo que entra está al mismo nivel de heading que lo que había (probablemente sea texto
                # "simple").
                # En estas condiciones se adjunta este párrafo al snippet en curso si al hacerlo estamos más
                # cerca de nuestro objetivo de palabras por snippet, y si ocurre el caso contrario, comenzamos
                # un nuevo snippet. Decretamos que el párrafo nos acerca a nuestro objetivo cuando para
                # alcanzar el tamaño requerido en palabras deberíamos aumentar la cantidad de palabras hasta
                # ahora por un porcentaje mayor, que el porcentaje de reducción necesario para alcanzar dicho
                # objetivo una vez que le añadiéramos este párrafo. Es decir, si hasta ahora llevamos 75
                # palabras y entra un párrafo de 50, se tiene que necesitamos un aumento del 33% para alcanzar
                # las 100, mientras que después nos estaría sobrando el 20%, con lo que consideramos que 125
                # palabras se acerca más a nuestro objetivo de 100 que 75, con lo que añadimos este párrafo al
                # snippet en curso.
                # Este algoritmo también funciona cuando la suma del número de palabras del snippet actual más
                # las palabras que vienen es menor que el valor requerido (siempre añadimos) y también cuando
                # el snippet actual ya tiene más palabras de las requeridas (siempre creamos nuevo snippet).
                n_palabras_snippet_actual = len(snippet_actual)
                n_palabras_parrafo = len(palabras_parrafo)
                comienza_nuevo_snippet = float(palabras_por_snippet) / n_palabras_snippet_actual < \
                    float(n_palabras_snippet_actual + n_palabras_parrafo) / palabras_por_snippet
            else:
                # Caben dos posibilidades:
                # - Está entrando un header, y el párrafo anterior era texto simple (o header pero a nivel
                #   inferior). Debemos comenzar un snippet nuevo porque cambia de sección (y no es
                #   subsección).
                # - Está entrando texto simple o un header a nivel inferior que lo que teníamos hasta ahora.
                #   Independientemente del tamaño, aunque nos pasemos, no dejamos un título "huérfano" sin al
                #   menos el primer párrafo de "texto de verdad". Unimos este párrafo al snippet que estamos
                #   creando.
                comienza_nuevo_snippet = nivel_header < nivel_header_actual
            if comienza_nuevo_snippet:
                snippets.append(set(snippet_actual))
                snippet_actual = palabras_parrafo
            else:
                snippet_actual += palabras_parrafo
            nivel_header_actual = nivel_header
            pass
        # El último de los snippets que hemos creado nunca llegó a añadirse a la lista.
        snippets.append(set(snippet_actual))
        return snippets

    @staticmethod
    def estructura_texto_articulo(texto_articulo, elimina_separadores=True, adjunta_separadores=False,
                                  agrupa_separadores=False, elimina_titulos=False):
        """Dividimos los artículos en secciones, párrafos, frases y palabras.

        :type texto_articulo: unicode
        :param texto_articulo: El texto del artículo que queremos estructurar. Tiene que incluir las marcas de
            seccion (tipo "^(={1,6})[^\n]+\1$"), o si no, todo el texto se tratará como una misma sección.
        :type elimina_separadores: bool
        :param elimina_separadores: Si está a True, los separadores se eliminan del resultado.
            Si está a False, se actúa con dichos separadores según el parámetro siguiente..
        :type adjunta_separadores: bool
        :param adjunta_separadores: Si está a False, los signos ortográficos se colocan como tokens
            independientes. Si está a True los signos ortográficos no se colocan como tokens independientes
            sino que se adjuntan al siguiente/anterior token según corresponda: los signos de apertura se
            añaden al siguiente y los de cierre y pausa se adjuntan al anterior.
        :type agrupa_separadores: bool
        :param agrupa_separadores: Solo afecta si adjunta_separadores es True. En dicho caso,
            si este parámetro está a True, cada frase no es un simple unicode, sino que es una lista de
            unicodes: signos de apertura, texto y signos de cierre de frase. Si este parámetro está a
            False, entonces se devuelve un listado de unicodes, que pueden ser el texto de la frase o de
            los signos de apertura/cierre.
        :type elimina_titulos: bool
        :param elimina_titulos: Si está a True, los títulos de artículos/(sub)secciones se eliminan.
        :rtype: [[[[unicode]]]]
        :return: Una lista de secciones, que son listas de párrafos, que son listas de frases, que son listas
            de palabras (que son cadenas unicode).
        """
        regex_seccion = '(?:={1,6})[^=].*?(?<!=)(?:={1,6})$'
        # Primero quitamos el título, que está al inicio y separado del cuerpo del artículo por un doble \n
        # (que es el único doble \n que hay en el texto del artículo).
        titulo, texto_articulo = texto_articulo.split('\n\n')
        parrafos = [par.strip() for par in texto_articulo.split('\n') if par.strip()]
        # Los títulos de sección son también párrafos.
        # Dividimos el texto en secciones, cada uno de los cuales es una lista de párrafos,
        # formados por listas de frases, que son listas de palabras.
        secciones = [[[Tokenizer.segmenta_por_palabras([titulo],
                                                       elimina_separadores=elimina_separadores,
                                                       segmenta_por_guiones_internos=False,
                                                       segmenta_por_guiones_externos=True,
                                                       adjunta_separadores=adjunta_separadores,
                                                       agrupa_separadores=False)]]]
        nivel_header_actual = 0
        for texto_parrafo in parrafos:  # Son párrafos pero también títulos de (sub)sección.
            # El texto del artículo se ha refinado, pero se han dejado las marcas de (sub)secciones para poder
            # dividir el texto en sus componentes. Las secciones habitualmente se marcan con
            # (== ?)...( ?==), con el título de la sección entre medias, y las subsecciones habitualmente se
            # marcan con tres signos ===.
            # No obstante, se admiten entre uno y seis signos de =, para imitar los <h1> - <h6>
            if re.match(regex_seccion, texto_parrafo):
                # Tenemos un título de sección. Vemos qué nivel de encabezado es.
                nivel_header = len(texto_parrafo) - len(texto_parrafo.lstrip('='))
                # Eliminamos las marcas.
                texto_parrafo = re.sub('(^(?:={1,6}\s*))|((?:\s*={1,6})$)', '', texto_parrafo)
                if not texto_parrafo.strip():
                    # Puede ocurrir, que haya títulos de sección que sean una directiva (una bandera,
                    # por ejemplo), y que al eliminarlo el título quede en nada.
                    continue
            else:
                nivel_header = 7
            frases = []
            if nivel_header < nivel_header_actual:
                # La sección es de mayor o igual nivel, luego es una nueva sección u otro párrafo del mismo
                # nivel que el anterior. En cualquier caso, este texto es el inicio de una nueva sección.
                # Si tenemos una sección de menor nivel que la anterior, lo pegamos, para no dejar títulos de
                # (sub)sección sueltos.
                secciones.append([])
            elif nivel_header > nivel_header_actual:
                # Se decide meter como frases del mismo párrafo, todos aquellos títulos de (sub)sección
                # inmediatamente precedentes al primer párrafo de la (sub)sección. Cuando van varios títulos
                # seguidos (cada uno de un nivel inferior), se meten todos esos títulos.
                if (not elimina_titulos) and secciones[-1]:
                    # Puede ser que el título de la sección sea una palabra descartable o que los eliminemos.
                    frases = secciones[-1][0]
                secciones[-1] = []
            nivel_header_actual = nivel_header

            # Dividimos el párrafo en frases.
            if not elimina_separadores:
                texto_estructurado = \
                    Tokenizer.segmenta_estructurado(texto_parrafo,
                                                    elimina_separadores=elimina_separadores,
                                                    elimina_separadores_blancos=True,
                                                    parentesis_segmentan_frases=False,
                                                    segmenta_por_guiones_internos=False,
                                                    segmenta_por_guiones_externos=True,
                                                    adjunta_separadores=adjunta_separadores,
                                                    agrupa_separadores=agrupa_separadores)
                frases += texto_estructurado[0]
            else:
                for frase in Tokenizer.segmenta_por_frases(texto_parrafo,
                                                           elimina_separadores=elimina_separadores,
                                                           elimina_separadores_blancos=True,
                                                           adjunta_separadores=adjunta_separadores,
                                                           agrupa_separadores=agrupa_separadores):
                    palabras = [pal for pal in Tokenizer.
                                segmenta_por_palabras([frase],
                                                      elimina_separadores=elimina_separadores,
                                                      segmenta_por_guiones_internos=False,
                                                      segmenta_por_guiones_externos=True,
                                                      adjunta_separadores=adjunta_separadores,
                                                      agrupa_separadores=False)]
                    # Puede ocurrir cuando entra un párrafo con números o símbolos que queda reducido
                    # a 0 palabras.
                    if palabras:
                        frases.append(palabras)
            if frases:
                secciones[-1].append(frases)
        return secciones

    @staticmethod
    def recuenta_formas(incluye_signos=False, separa_inicio_frase=True):
        """Toma el contenido del corpus y hace un recuento del número de apariciones de cada forma.

        :type incluye_signos: bool
        :param incluye_signos: Si está a True, también se recuentan los signos de puntuación.
        :type separa_inicio_frase: bool
        :param separa_inicio_frase: Si está a True, se eliminan todos los tokens previos a la primera palabra
            de cada frase. Esto nos vale para poder poner en minúsculas aquellas palabras que únicamente están
            con mayúscula inicial al comenzar la frase. Esto ayuda para identificar nombres propios de los que
            no lo son.
        """
        hora_inicio_total = time()
        directorio_trabajo = directorio_base
        directorio_fasciculos =\
            directorio_trabajo + barra + 'archivos_de_datos' + barra + 'articulos_refinados' + barra
        nombres_fasciculos = [f for f in listdir(directorio_fasciculos) if '@' in f]
        uno_por_ciento = float(len(nombres_fasciculos)) / 100.0
        recuento_formas = {}
        recuento_formas_minuscula = {}
        recuento_formas_inicio = {}
        print('\nRecontando formas de fascículos en .../' + '/'.join(directorio_fasciculos.split(barra)[-5:]))
        print('_' * 102)
        print('|1       10        20        30        40        50'
              '        60        70        80        90       100|')
        sys.stdout.write('|')
        for orden_fasciculo_actual, nombre_fasciculo_actual in enumerate(nombres_fasciculos):
            # Leemos el fascículo completo, que incluye 1000 artículos.
            with codecs.open(directorio_fasciculos + nombre_fasciculo_actual, encoding="utf-8")\
                    as archivo_fasciculo:
                texto_fasciculo = archivo_fasciculo.read()
            # Primero dividimos en artículos. Al dividir según la marca, el último artículo estará vacío
            # (es lo que queda -nada- tras la última marca).
            articulos = [art for art in texto_fasciculo.split(MARCA_FIN_ARTICULO)][:-1]
            for orden_articulo, texto_articulo in enumerate(articulos):
                texto_estructurado = ParseadorWikipedia.\
                    estructura_texto_articulo(texto_articulo,
                                              elimina_separadores=not incluye_signos,
                                              adjunta_separadores=True,
                                              agrupa_separadores=True,
                                              elimina_titulos=False)

                formas = [forma for seccion in texto_estructurado for parrafo in seccion
                          for frase in parrafo for forma in frase]
                for forma, grupo_apariciones in groupby(sorted(formas)):
                    n_apariciones = len(list(grupo_apariciones))
                    recuento_formas[forma] = recuento_formas.setdefault(forma, 0) + n_apariciones
                    forma = forma.lower()
                    recuento_formas_minuscula[forma] =\
                        recuento_formas_minuscula.setdefault(forma, 0) + n_apariciones
                if separa_inicio_frase:
                    # Volvemos a estructurar porque nos interesa quitar los separadores para que la
                    # primera palabra de la frase sea el primer token.
                    if incluye_signos:
                        texto_estructurado = ParseadorWikipedia. \
                            estructura_texto_articulo(texto_articulo,
                                                      elimina_separadores=True,
                                                      adjunta_separadores=True,
                                                      agrupa_separadores=True,
                                                      elimina_titulos=False)
                    formas = [forma for seccion in texto_estructurado for parrafo in seccion
                              for frase in parrafo for forma in frase[:1]]
                    for forma, grupo_apariciones in groupby(sorted(formas)):
                        n_apariciones = len(list(grupo_apariciones))
                        recuento_formas_inicio[forma] = \
                            recuento_formas_inicio.setdefault(forma, 0) + n_apariciones

            if int(orden_fasciculo_actual / uno_por_ciento) <\
                    int((orden_fasciculo_actual + 1) / uno_por_ciento):
                sys.stdout.write('.')
        print('|')
        print('_' * 102)
        directorio_recuento =\
            directorio_trabajo + barra + 'archivos_de_datos' + barra + 'datos_estructurados' + barra
        if not exists(directorio_recuento):
            makedirs(directorio_recuento)
        path_archivo_recuento = directorio_recuento + 'recuentos_formas' +\
            ('+signos' if incluye_signos else '') + '.pickle'
        print('Guardando recuento .../' + '/'.join(path_archivo_recuento.split(barra)[-5:]))
        with open(path_archivo_recuento, 'wb') as archivo_recuento:
            pickle.dump(recuento_formas, archivo_recuento, pickle.HIGHEST_PROTOCOL)

        path_archivo_recuento_minuscula = directorio_recuento + 'recuentos_formas' +\
            ('+signos' if incluye_signos else '') + '_minuscula.pickle'
        print('Guardando recuento .../' + '/'.join(path_archivo_recuento_minuscula.split(barra)[-5:]))
        with open(path_archivo_recuento_minuscula, 'wb') as archivo_recuento_minuscula:
            pickle.dump(recuento_formas_minuscula, archivo_recuento_minuscula, pickle.HIGHEST_PROTOCOL)

        if recuento_formas_inicio:
            path_archivo_recuento_inicio = directorio_recuento + 'recuentos_formas_iniciales' + \
                                           ('+signos' if incluye_signos else '') + '.pickle'
            print('Guardando recuento .../' + '/'.join(path_archivo_recuento_inicio.split(barra)[-5:]))
            with open(path_archivo_recuento_inicio, 'wb') as archivo_recuento_inicio:
                pickle.dump(recuento_formas_inicio, archivo_recuento_inicio, pickle.HIGHEST_PROTOCOL)
            # Guardamos la versión "desmayusculizada". Esto quiere decir que cogemos las palabras que
            # aparecen en mayúscula en el recuento de formas iniciales de frase, y se las restamos del
            # recuento de total. Podríamos sumarlas además al recuento como formas minúsculas, pero la idea
            # es que solo aparezcan en mayúscula (o minúscula) las formas que sabemos fehacientemente que
            # se escriben así entre medias de una frase.
            # Haciendo esto, podemos ver más claramente qué palabras son realmente en minúscula y cuáles son
            # nombres propios. Las palabras comunes pueden convertirse tambien en nombres propios (de
            # películas, canciones) y eso confunde bastante, por lo que precisamente hacemos esto para evitar
            # en parte dicho problema.
            print('Desmayusculizando...', end=' ')
            hora_inicio_desmayusculizacion = time()
            for forma, recuento in recuento_formas_inicio.items():
                if forma != forma.lower():
                    if forma in recuento_formas:
                        recuento_formas[forma] -= recuento
                    else:
                        pass
            tiempo_de_desmayusculizado = int(time() - hora_inicio_desmayusculizacion)
            print('desmayusculizado en {:02d}:{:02d}'.format(int(tiempo_de_desmayusculizado / 60) % 60,
                                                             int(tiempo_de_desmayusculizado % 60)))
            path_archivo_recuento_desmayusculizado =\
                directorio_recuento + 'recuentos_formas_desmayusculizado' + \
                ('+signos' if incluye_signos else '') + '.pickle'
            print('Guardando recuento desmayusculizado .../' +
                  '/'.join(path_archivo_recuento_desmayusculizado.split('/')[-5:]))
            with open(path_archivo_recuento_desmayusculizado, 'wb') as archivo_recuento_desmayusculizado:
                pickle.dump(recuento_formas, archivo_recuento_desmayusculizado, pickle.HIGHEST_PROTOCOL)

        tiempo_total = int(time() - hora_inicio_total)
        print('Tiempo total de recuento: {:02d}:{:02d}:{:02d}'.format(int(tiempo_total / 3600),
                                                                      int(tiempo_total / 60) % 60,
                                                                      int(tiempo_total % 60)))

    @staticmethod
    def carga_recuentos_formas(recuentos_minuscula=False, incluye_signos=False, separa_inicio_frase=False,
                               desmayusculizado=False):
        """Se carga el archivo con el contenido de los recuentos de lemas en el corpus y se devuelve su
        contenido.

        :type recuentos_minuscula: bool
        :param recuentos_minuscula: Si está a True se cargará el recuento en el que no se hacen diferencias
            entre las letras mayúsculas o minúsculas.
        :type incluye_signos: bool
        :param incluye_signos: Si está a True, se devuelven los recuentos en los que se han incluido los
            signos de puntuación.
        :type separa_inicio_frase: bool
        :param separa_inicio_frase: Si está a True, se devuelven los recuentos en los que se han eliminado los
            signos de puntuación previos a la primera palabra de la frase.
        :type desmayusculizado: bool
        :param desmayusculizado: Si está a True, se devuelve el recuento en el que las palabras que aparecen
            con mayúscula inicial se han puesto en minúscula dependiendo de su frecuencia de aparicion en
            minúscula o mayúscula.
        :rtype: {unicode: int}
        :return: Un diccionario en el que las claves son las formas del corpus y los valores el número de
            apariciones.
        """
        hora_inicio_total = time()
        directorio_trabajo = directorio_base
        directorio_recuento =\
            directorio_trabajo + barra + 'archivos_de_datos' + barra + 'datos_estructurados' + barra
        if recuentos_minuscula:
            path_archivo_recuento = directorio_recuento + 'recuentos_formas' +\
                                    ('+signos' if incluye_signos else '') + '_minuscula.pickle'
        elif separa_inicio_frase:
            path_archivo_recuento = directorio_recuento + 'recuentos_formas_iniciales' +\
                                    ('+signos' if incluye_signos else '') + '.pickle'
        elif desmayusculizado:
            path_archivo_recuento = directorio_recuento + 'recuentos_formas_desmayusculizado' + \
                                    ('+signos' if incluye_signos else '') + '.pickle'
        else:
            path_archivo_recuento = directorio_recuento + 'recuentos_formas' +\
                                    ('+signos' if incluye_signos else '') + '.pickle'
        if not exists(path_archivo_recuento):
            print('Faltan los archivos de recuento.', path_archivo_recuento)
            ParseadorWikipedia.recuenta_formas(incluye_signos=incluye_signos,
                                               separa_inicio_frase=separa_inicio_frase)

        print('Cargando recuento .../' + '/'.join(path_archivo_recuento.split(barra)[-5:]))
        with open(path_archivo_recuento, 'rb') as archivo_recuento:
            recuento_formas = pickle.load(archivo_recuento)
        tiempo_total = int(time() - hora_inicio_total)
        print('Tiempo total de carga: {:d}:{:02d}'.format(int(tiempo_total / 60), tiempo_total % 60))
        return recuento_formas

    @staticmethod
    def test():
        u"""Este es un método que simplemente realiza un test, extrayendo, troceando y limpiando la Wikipedia.
        """
        # Primero descargamos la última versión de la Wikipedia en español, la troceamos y la limpiamos.
        ParseadorWikipedia.extrae_articulos_refinados(actualiza_archivo_raw=True,
                                                      articulos_por_fasciculo=1000,
                                                      articulos_rechazados_guardados='')
        # Hacemos llamadas a otros métodos que en realidad solo son necesarios para utilizar este corpus como
        # base para crear representaciones semánticas vectoriales.
        ParseadorWikipedia.recuenta_formas(incluye_signos=True, separa_inicio_frase=True)


if __name__ == '__main__':
    ParseadorWikipedia.test()
