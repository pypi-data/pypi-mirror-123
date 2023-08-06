"""
Title: 
Author: Julio Rodriguez
Organization: SENER
"""

# BLK: Imports

# Standard Libraries
from datetime import datetime

# 3rd Party
import numpy as np
import pandas as pd
from tqdm import tqdm
import openpyxl as opx

# Local Libraries
from . import solar_general as _gn


# Global class
class Cstruct:
    pass


# Global variables


# Code


def inicializa_deltas(DLT, datos_tmpt, kks_loops, n_locs=4):
    # FuncBLK: inicializa_deltas
    DLT.datos_tmpt_ordenados = np.zeros([datos_tmpt.shape[1], kks_loops.size, n_locs], dtype=float)     # Temperaturas de cada LOC en cada muestra ordenadas por lazo y en orden de 1-4 LOCs
    DLT.deltas = np.zeros([datos_tmpt.shape[1], kks_loops.size, n_locs], dtype=float)   # Incremento de temperatura de un LOC a otro (primer delta es de Tin a LOC1)
    DLT.dtns = np.zeros([datos_tmpt.shape[1], kks_loops.size, n_locs], dtype=float)     # Incremento de temperatura estimado desde el principio del panel hasta su LOC (en el medio)
    DLT.paneles = np.zeros([datos_tmpt.shape[1], kks_loops.size, n_locs], dtype=float)  # Estimación de lo que calienta un panel utilizando dtns. Inestable cuando una PT100 no mide bien.
    DLT.delta_tot = np.empty([datos_tmpt.shape[1], kks_loops.size], dtype=float)        # Incremento de temperatura total estimado
    DLT.delta_prom = np.empty([datos_tmpt.shape[1], kks_loops.size], dtype=float)       # Incremento medio estimado de temperatura (dtns prom.)
    DLT.delta_desv = np.empty([datos_tmpt.shape[1], kks_loops.size], dtype=float)       # Desviación típica de el incremento de temperatura estimado(std dtns)
    DLT.t_out_est = np.empty([datos_tmpt.shape[1], kks_loops.size], dtype=float)        # Temperatura de salida estimada
    DLT.t_in = np.empty([datos_tmpt.shape[1], kks_loops.size], dtype=float)             # Temperatura de entrada (dato)
    DLT.t_out = np.empty([datos_tmpt.shape[1], kks_loops.size], dtype=float)            # Temperatura de salida (dato)
    return DLT


def genera_deltas(kks_loops, index_kks_loops, pos_loc, datos_tmpt, datos_general, med, DLT, sect_div, pt100_est, pt100_d, is_pt_sum, ct_pos, ht_pos, n_locs=4):   # Si noche es True no hay que pasar la pt100_noche
    sec = 0
    # Si la variable is_pt_sum es cierta, entonces se hace que pt100_d sea 0 para no sumar la diferencia estimada de arreglo de PT100
    if is_pt_sum:
        pt100_d = np.zeros(pt100_d.shape, dtype=float)
    for k in np.arange(kks_loops.size):  # Loop de cada loop(kksloop)
        if sect_div[sec + 1] < k:  # Comprobar en que sector estamos (plantilla ordenada por sectores)
            sec += 1

        # Ordenar por nº de LOC
        pos = np.argwhere(index_kks_loops == k).squeeze()  # Posiciones de lás máquinas del loop actual
        pre_pos_ordenado = np.argsort(pos_loc[pos] - 1)  # Sacar las posiciones del array ordenado de las posiciones de cada LOC (mejor mirarlo en debugging)
        pos_ordenado = pos[pre_pos_ordenado]  # Posiciones de los LOCs ordenados por numero de LOC
        DLT.datos_tmpt_ordenados[med, k, 0] = datos_tmpt[pos_ordenado[0], med] - pt100_d[k, 0]

        # Primer LOC
        DLT.deltas[med, k, 0] = DLT.datos_tmpt_ordenados[med, k, 0] - datos_general[ct_pos + sec, med]  # Diferencia (en temperatura) entre el primer LOC y la temperatura de entrada
        DLT.dtns[med, k, 0] = DLT.datos_tmpt_ordenados[med, k, 0] - datos_general[ct_pos + sec, med]
        DLT.paneles[med, k, 0] = 2 * DLT.dtns[med, k, 0]

        # Resto de LOCs
        for i in np.arange(n_locs - 1) + 1:
            DLT.datos_tmpt_ordenados[med, k, i] = datos_tmpt[pos_ordenado[i], med] - pt100_d[k, i]
            DLT.deltas[med, k, i] = DLT.datos_tmpt_ordenados[med, k, i] - DLT.datos_tmpt_ordenados[med, k, i - 1] # Diferencia del LOC i y el i - 1
            DLT.dtns[med, k, i] = DLT.deltas[med, k, i] - DLT.dtns[med, k, i - 1]
            DLT.paneles[med, k, i] = 2 * DLT.dtns[med, k, i]

        # Calculos
        DLT.delta_tot[med, k] = DLT.datos_tmpt_ordenados[med, k, -1] - datos_general[ct_pos + sec, med]  # Diferencia entre el último LOC y la temperatura de entrada
        DLT.delta_prom[med, k] = (DLT.delta_tot[med, k]) / 7  # Delta total entre 7 nos da la media de cuanto vale un dtn aprox.
        DLT.delta_desv[med, k] = np.std(DLT.dtns[med, k, :])  # Desviación típica de la delta estimada
        DLT.t_out_est[med, k] = DLT.datos_tmpt_ordenados[med, k, 3] + DLT.dtns[med, k, 3]   # Temperatura de salida estimada
        DLT.t_in[med, k] = datos_general[ct_pos + sec, med]   # T entrada sector
        DLT.t_out[med, k] = datos_general[ht_pos + sec, med]  # T salida sector

    return DLT


def datos_loop_a_loc(kks_loops_full, kks_loops, *args):
    out = np.empty(0)
    args = list(args)
    try:
        temp = args[0].shape[1]
    except IndexError:
        args[0] = args[0][:, np.newaxis]
    for data in args:
        try:
            temp = np.empty([kks_loops_full.size, data.shape[1]], dtype=data.dtype)
        except IndexError:
            data = data[:, np.newaxis]
            temp = np.empty([kks_loops_full.size, data.shape[1]], dtype=data.dtype)
        for k in np.arange(kks_loops.size):
            if data.shape[1] == 4:
                pos_locs = np.argwhere(kks_loops_full == kks_loops[k])
                for i in np.arange(pos_locs.size):
                    temp[pos_locs[i]] = data[k]
            else:
                pos_locs = np.argwhere(kks_loops_full == kks_loops[k])
                for i in np.arange(pos_locs.size):
                    temp[pos_locs[i, 0]] = data[k]
        if np.array_equal(data, args[0]):
            out = temp
        else:
            out = np.append(out, temp, axis=1)
    return out


def data_loc4_to_loc(data, index_kks_loops, pos_loc):
    data_out = np.empty(0)
    for k in np.arange(index_kks_loops.size):
        # Conseguir que se sincronice el 4loc a loc
        data_out = np.append(data_out, data[index_kks_loops[k], pos_loc[k] - 1])
    return data_out


def array_division(datos):
    comp_arr = np.zeros(datos.size, dtype=int)  # Crea un array de ceros del tipo integer del mismo tamaño que fechas
    k1 = 0
    div_arr = np.empty(0, dtype=int)  # Crea un array vacio del tipo integer sin nada dentro
    while comp_arr[-1] != (datos.size - 1):  # Con este loop se busca conseguir un array con las posiciones de la última alarma de cada día para poder dividir la lista de alarmas que está ordenada cronológicamente
        comp = datos[k1]  # Se le da el valor de la fecha a comparar en cada vuelta de loop
        comp_arr = np.argwhere(datos == comp)  # Esta función nos devuelve un array con los índices donde el array de fechas coincide con la fecha actual del loop
        k1 = comp_arr[-1] + 1  # Se actualiza k1 con el último índice del array de los índices
        div_arr = np.append(div_arr, comp_arr[-1], axis=0)  # Se guarda el último valor del índice para tener de referencia hasta donde dura cada día
    return div_arr


def corregir_texto_alarmas(origin):
    inst = np.array(origin, dtype='U140')
    inst = np.char.replace(inst, 'Loc ', '')
    inst = np.core.defchararray.rstrip(inst)  # Quita los espacios al final
    return inst


def corregir_texto_alarmas_V2(origin):
    inst = np.char.replace(origin, 'Loc ', '')
    inst = np.char.replace(inst, '/', '-')
    inst = np.char.replace(inst, 'HE', 'GX')
    inst = np.core.defchararray.rstrip(inst)
    return inst


def convertir_df_numerico_GENERAL(df, nombres_columnas_general, planta):    # FIXME: NO GLOBAL
    if planta == "Ilanga":
        df = _gn.convertir_df_numerico(df, [nombres_columnas_general[0], nombres_columnas_general[3], nombres_columnas_general[4], nombres_columnas_general[5]])
    elif planta == "Kathu":
        df = _gn.convertir_df_numerico(df, [nombres_columnas_general[0], nombres_columnas_general[4], nombres_columnas_general[5], nombres_columnas_general[9], nombres_columnas_general[12]])
    elif planta == "NoorII":
        df = _gn.convertir_df_numerico(df, ["ID", "Latitude (º)", "Longitude (º)", "RING / SUBFIELD", "LOC POSITION IN THE LOOP"])
    elif planta == "NoorIII":
        df = _gn.convertir_df_numerico(df, [nombres_columnas_general[0], nombres_columnas_general[3], nombres_columnas_general[4], nombres_columnas_general[12]])
    return df


def generar_excel_planta(Data, planta, datos, col_datos, cols_numeric=[], fich_nom=None, hora_select=None):
    # BLK: Generar fichero Excel

    if hora_select is None:
        hora_selected = Data.fecha_archivo
    else:
        hora_selected = hora_select.replace(":", "-")

    if fich_nom is None:
        fich_nom = Data.ruta_defecto + f"/{planta}" + "/Conclusiones " + Data.fecha_archivo + f"/Conclusiones_{hora_selected}.xlsx"

    print("Generando fichero Excel...")
    colgen_tam = Data.nombres_columna_general.size
    # sBLK: Creación del fichero
    writer = pd.ExcelWriter(fich_nom, engine='xlsxwriter')
    # Generar dataframes de pandas con los arrays de numpy para el volcado a excel
    df_temp = pd.DataFrame(datos, columns=col_datos)
    # Convertir celdas de excel al formato numérico (sin formato por defecto)
    df_temp = convertir_df_numerico_GENERAL(df_temp, Data.nombres_columna_general, planta)
    df_temp = _gn.convertir_df_numerico(df_temp, col_datos[[colgen_tam + elem for elem in cols_numeric]])  # Cal <-> DIF
    # Volcar dataframes a excel
    df_temp.to_excel(writer, index=False, header=True, sheet_name="Conclusiones")
    # Ajuste del ancho de las columnas
    _gn.ajustar_columnas_excel(writer, "Conclusiones", len(col_datos), df_temp.columns, normal=True)

    # Activar autofilter
    worksheet = writer.sheets["Conclusiones"]
    worksheet.autofilter(0, 0, Data.kks_loops_full.size, col_datos.size)

    # Guardar Excel
    writer.save()

    # sBLK: Modificar características del Excel
    # Inmovilizar primera fila
    excel_planta = opx.load_workbook(fich_nom)
    nom_hojas = excel_planta.sheetnames
    hoja_conclusiones = excel_planta["Conclusiones"]
    hoja_conclusiones.freeze_panes = "A2"
    excel_planta.save(fich_nom)


def ordenar_locs(datos_tmpt, kks_loops, index_kks_loops, pos_loc, n_locs=4):
    datos_tmpt_ordenados = np.zeros([datos_tmpt.shape[1], kks_loops.size, n_locs], dtype=float)  # Temperaturas de cada LOC en cada muestra ordenadas por lazo y en orden de 1-4 LOCs
    for med in np.arange(datos_tmpt.shape[1]):  # Loop de cada medición horaria
        # Ordenar por nº de LOC
        for k in np.arange(kks_loops.size):  # Loop de cada loop(kksloop)
            pos = np.argwhere(index_kks_loops == k).squeeze()  # Posiciones de lás máquinas del loop actual
            pre_pos_ordenado = np.argsort(pos_loc[pos] - 1)  # Sacar las posiciones del array ordenado de las posiciones de cada LOC (mejor mirarlo en debugging)
            pos_ordenado = pos[pre_pos_ordenado]  # Posiciones de los LOCs ordenados por numero de LOC
            datos_tmpt_ordenados[med, k, 0] = datos_tmpt[pos_ordenado[0], med]
            for i in np.arange(n_locs - 1) + 1:
                datos_tmpt_ordenados[med, k, i] = datos_tmpt[pos_ordenado[i], med]
    return datos_tmpt_ordenados


def crea_carpetas_conclusiones(Data, planta):
    _gn.crear_directorio_v2(Data.ruta_defecto, f"{planta}")
    return _gn.crear_directorio_v2(Data.ruta_defecto, f"{planta}/Conclusiones {Data.fecha_archivo}")


def eliminar_alarmas(alarmas, tipos_alarma, fechas_alarmas, alarmas_deseadas):
    index_particion = np.ones(alarmas.size, dtype=bool)     # Array de unos con el tamaño de las alarmas originales
    for i in tqdm(np.arange(alarmas_deseadas.size)):
        comp = np.argwhere(alarmas == alarmas_deseadas[i])  # Obtener indices de las posiciones de las alarmas que nos interesan
        if comp.any():
            np.put(index_particion, comp, False)    # Poner False en dichas posiciones de las alarmas originales
    index_particion = np.argwhere(index_particion)  # Obtener las posiciones donde todavía hay True en las alarmas originales, es decir, las que no nos interesan
    alarmas_new = np.delete(alarmas, index_particion, None)     # Eliminar dichas alarmas (inst)
    tipos_alarma_new = np.delete(tipos_alarma, index_particion, None)   # Eliminar los tipos de alarmas (desc)
    fechas_alarmas_new = np.delete(fechas_alarmas, index_particion, None)   # Eliminar las fechas (fechas)
    return alarmas_new, tipos_alarma_new, fechas_alarmas_new


def array_division_dias_csvalarm(fechas, planta):
    fecha = np.empty(fechas.size, datetime)                             # Crea un array vacío de tipo datetime del mismo tamaño que fechas
    for k in np.arange(fechas.size):                                    # Transformamos las fechas de tipo string a tipo datetime (para poder quitar la parte de la hora y poder así filtrar por día las alarmas)
        if planta != "NoorIII":
            fecha[k] = datetime.strptime(fechas[k], '%d/%m/%Y %H:%M:%S')    # Se le indica a la función que formato de fecha y hora tenemos en nuestro archivo
        else:
            fecha[k] = datetime.strptime(fechas[k], '%d/%m/%Y %H:%M')    # Es necesario hacer este if ya que el csv de NoorIII sale con la hora en diferente formato
        fecha[k] = np.datetime64(fecha[k], 'D')                         # Nos quedamos con la parte de fecha solo (AAAA-MM-DD)

    comp_arr = np.zeros(fechas.size, dtype=int)                         # Crea un array de ceros del tipo integer del mismo tamaño que fechas
    k1 = 0
    div_arr = np.empty(0, dtype=int)                                    # Crea un array vacio del tipo integer sin nada dentro
    while comp_arr[-1] != (fechas.size - 1):                            # Con este loop se busca conseguir un array con las posiciones de la última alarma de cada día para poder dividir la lista de alarmas que está ordenada cronológicamente
        comp = fecha[k1]                                                # Se le da el valor de la fecha a comparar en cada vuelta de loop
        comp_arr = np.argwhere(fecha == comp)                           # Esta función nos devuelve un array con los índices donde el array de fechas coincide con la fecha actual del loop
        k1 = comp_arr[-1] + 1                                           # Se actualiza k1 con el último índice del array de los índices
        div_arr = np.append(div_arr, comp_arr[-1], axis=0)              # Se guarda el último valor del índice para tener de referencia hasta donde dura cada día
    return div_arr, fecha                                                      # Este loop se repite hasta que en la última posición del array de los indices aparezca el último indice de la lista de alarmas


def init_dir(ruta_defecto, plant, fecha_archivo):
    # Directorios mínimos
    _gn.crear_directorio_v2(ruta_defecto, plant)
    _gn.crear_directorio_v2(ruta_defecto, plant + "/Conclusiones " + fecha_archivo)

