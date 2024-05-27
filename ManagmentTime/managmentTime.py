import pandas as pd
import datetime as dt
import numpy as np

def scalarHour(dt_serie):
    """Returns a list containing the hour, minutes and seconds based on datetime series"""
    return [val.strftime('%H:%M:%S') if not pd.isnull(val) else np.nan for val in dt_serie]
def scalarHxH(dt_serie, hour_serie=None):
    """
    Returns a list containing the Silao Hour where an event happened
    Args:
        dt_serie (series): Datetime series to be based on
        hour_serie (series Optional): String series containing the hour, is used to calculate the HxH, if None will be calculated
    """
    def add(val, sum_qty):
        return str(int(val)+sum_qty).rjust(2, "0")
    hour_serie = scalarHour(dt_serie) if hour_serie==None else hour_serie
    return [val[:2]+' - '+add(val[:2], 1) if val>'06:00' and val<'14:00' else \
            '14 - '+'14.5' if val>'14:00' and val<'14:30' else \
            '05.5'+' - 06' if val>'05:30' and val<'06:00' else \
            '23.5'+' - 00.5' if (val>='23:30') or (val<'00:30') else \
            (add(val[:2], -1)+'.5')+' - '+val[:2]+'.5' if val[3:5]<'30' else \
            val[:2]+'.5'+' - '+(add(val[:2], 1)+'.5') \
            for val in hour_serie]
def apply_scalars(df_, timestamp_col, month_format='str', shift_format_str=True, prefix=None, suffix=None,
                  teams_df=None, year=False, month=False, week=False, day=True, shift=True, hour=False,
                  hxh=False, weekday=False, merge=True):
    """
    Generates multiple columns containing scalar time information
    Args:
        df_ (Dataframe): Dataframe to be based on.
        timestamp_col (str): Datetime column where all the scalars will be obtained.
        month_format (str): Month format, specify 'str', 'Full' or another value to get it in number.
        shift_format_str (bool): Shift format, if False returns int values.
        prefix (str): Prefix to be added to all the column names.
        suffix (str): Suffix to be added to all the column names.
        teams_df (Dataframe): Raw dataframe obtained from SCH_TEAM_SHIFTS.
        year (bool): If true adds YEAR column.
        month (bool): If true adds MONTH column.
        week (bool): If true adds WEEK column.
        day (bool): If true adds DATE column.
        shift (bool): If true adds SHIFT column.
        hour (bool): If true adds HOUR column.
        hxh (bool): If true adds HXH column.
        weekday (bool): If true adds WEEKDAY column.
        merge (bool): If true appends all the columns to the passed Dataframe (df_), if false, returns some scalars in another dataframe.
    """
    df = df_.copy()
    #Parametros generales
    dt_serie = df[timestamp_col]
    month_fmt = '%b' if month_format in [str, 'str'] else '%B' if month_format.upper()=='FULL' else '%m'
    shift1, shift2, shift3 = ['1', '2', '3'] if shift_format_str==True else [1, 2, 3]
    prefix = '' if prefix is None else prefix
    suffix = '' if suffix is None else suffix
    #Crear series con Hora, Turno y Día
    if year or month or week or weekday or day or shift or hour or hxh or teams_df is not None:
        hour_serie = scalarHour(dt_serie)
    if shift or teams_df is not None:
        shift_serie = [np.nan if pd.isnull(val) else \
                       shift1 if val>='06:00:00' and val<'14:30:00' else \
                       shift2 if val>='14:30:00' and val<'22:30:00' else shift3 \
                       for val in hour_serie]
    if year or month or week or weekday or day or teams_df is not None:
        day_serie = [np.nan if pd.isnull(valH) else \
                     val.strftime('%d/%m/%Y') if valH>='06:00:00' else \
                     (val-dt.timedelta(days=1)).strftime('%d/%m/%Y') \
                     for val, valH in zip(dt_serie, hour_serie)]
    #Agregar columna de Hora x Hora
    if hxh:
        df.loc[:,prefix+'HXH'+suffix] = scalarHxH(dt_serie, hour_serie=hour_serie)
    #Agregar columna de Hora
    if hour:
        df.loc[:,prefix+'HOUR'+suffix] = hour_serie
    #Agregar columna de Turno
    if shift or teams_df is not None:
        df.loc[:,prefix+'SHIFT'+suffix] = shift_serie
    #Agregar columna de Día
    if year or month or week or weekday or day or teams_df is not None:
        df.loc[:,prefix+'DATE'+suffix] = day_serie
    #Agregar columna de Grupo
    if teams_df is not None:
        tmp_teams_df = pd.DataFrame({
            prefix+'DATE'+suffix: [val.strftime('%d/%m/%Y') for val in teams_df['CAL_DATE']],
            prefix+'SHIFT'+suffix: teams_df['SHF_CODE'].replace([1, 2, 3], [shift1, shift2, shift3]),
            prefix+'TEAM_CODE'+suffix: teams_df['TEAM_CODE']
        })
        if merge:
            df = df.merge(tmp_teams_df, how='left')
    #Columnas que únicamente dependen del día
    if year or month or week or weekday:
        #Crear diccionario con los valores únicos del día
        unique_day_serie = list(set(day_serie))
        unique_info_dict = {prefix+'DATE'+suffix: unique_day_serie}
        #Agregue dayfirst en este proyecto en especifico
        dt_unique_day_serie = pd.to_datetime(unique_day_serie,dayfirst=True)
        #Agregar Día de la semana a diccionario
        if weekday:
            unique_info_dict[prefix+'WEEKDAY'+suffix] = (dt_unique_day_serie.strftime('%w')).str.replace('0','7')
        #Agregar Semana a diccionario
        if week:
            unique_info_dict[prefix+'WEEK'+suffix] = dt_unique_day_serie.strftime('%V')
        #Agregar Mes a diccionario
        if month:
            unique_info_dict[prefix+'MONTH'+suffix] = dt_unique_day_serie.strftime(month_fmt)
        #Agregar Año a diccionario
        if year:
            unique_info_dict[prefix+'YEAR'+suffix] = dt_unique_day_serie.strftime('%Y')
        #Crear dataframe con Días únios y su respectiva Semana, Mes y Año
        scalars_unique_df = pd.DataFrame(unique_info_dict)
        #Mergear con dataframe
        if merge:
            df = df.merge(scalars_unique_df, how='left')
    #Eliminar columna de Día en caso de haber sido agregada y no solicitada
    if year or month or week or teams_df is not None:
        if not day:
            df = df.drop(columns=prefix+'DATE'+suffix)
    #Eliminar columna de Turno en caso de haber sido agregada y no solicitada
    if teams_df is not None:
        if not shift:
            df = df.drop(columns=prefix+'SHIFT'+suffix)
    #Retornar un dataframe si merge=False, sino, se retornan por separado los scalars que no son dependientes de la columna datetime
    if not merge:
        if (year or month or week or weekday) and (teams_df is not None):
            scalars_unique_df = scalars_unique_df.merge(tmp_teams_df, how='left')
        elif teams_df is not None:
            scalars_unique_df = tmp_teams_df
        elif year or month or week or weekday:
            pass
        else:
            scalars_unique_df = pd.DataFrame()
        return df, scalars_unique_df
    else:
        return df