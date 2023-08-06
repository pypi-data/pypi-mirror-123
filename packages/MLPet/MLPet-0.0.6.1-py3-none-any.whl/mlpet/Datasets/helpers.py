import random
import warnings
import numpy as np
import pandas as pd
import importlib

def _standardize_group_formation_name(name):
    if 'INTRA' in name or 'NO ' in name:
        name=' '.join(name.split(' ')[:2])
        name=' '.join(name.split('_')[:2])
    else:
        name=name.split(' ')[0]
        name=name.split('_')[0]
        name=name.upper()
        name=name.replace('AA','A')
        name=name.replace('Å','A')
        name=name.replace('AE','A')
        name=name.replace('Æ','A')
        name=name.replace('OE','O')
        name=name.replace('Ø','O')
    return name

def generate_log_settings(settings, lognames, badlognames, log_curves=None):
    all_settings = dict()
    for i, logname in enumerate(lognames):
        all_settings[logname] = settings
        all_settings[logname]['label_column'] = badlognames[i]
        if log_curves is not None:
            all_settings[logname]['curves'] = log_curves
    return all_settings

def _standardize_names(names, mapper):
    """
    Standardize curve names in a list based on the curve_mappings dictionary. 
    Any columns not in the dictionary are ignored.

    Args:
        names (list): list with curves names
        mapper (dictionary): dictionary with mappings. Defaults to curve_mappings.

    Returns:
        list: list of strings with standardized curve names
    """
    standardized_names = []
    for name in names:
        if mapper.get(name):
            standardized_names.append(mapper.get(name))
        else:
            standardized_names.append(name)
    return standardized_names

def _standardize_curve_names(df, mapper):
    """
    Standardize curve names in a dataframe based on the curve_mappings dictionary. 
    Any columns not in the dictionary are ignored. 

    Args:
        df (pd.DataFrame): dataframe to which apply standardization of columns names
        mapper (dictionary): dictionary with mappings. Defaults to curve_mappings.

    Returns:
        pd.DataFrame: dataframe with columns names standardized
    """
    return df.rename(columns=mapper)

def _make_col_dtype_lists(df):
    """
    Returns lists of numerical and categorical columns

    Args:
        df (pd.DataFrame): dataframe with columns to classify

    Returns:
        tuple: lists of numerical and categorical columns
    """
    num_cols = set(df._get_numeric_data().columns)
    cat_cols = list(set(df.columns) - set(num_cols))
    return list(num_cols), cat_cols

def generate_sequential_dataset(df, time_steps):
    """
    Returns the x (training) data in the format required by Keras LSTM/GRU models for LSTM networks

    Args:
        df (pd.DataFrame): data for input in LSTM networks (keras)
        time_steps (int): number of time steps

    Returns:
        np.array: samples with time steps included
    """
    samples = df.values
    if df.columns.size%(time_steps+1)==0: 
        n_original_cols = df.columns.size//(time_steps+1)
        samples         = samples.reshape((len(samples), time_steps+1, n_original_cols))
        return samples
    raise ValueError ('Number of columns not divisible by number of time steps.')

def shuffle_dfs(x, y):
    """
    Returns dataframes shuffled equally in indices. Both dataframes should have same indices values.
    Useful for neural networks training for example.

    Args:
        x (pd.DataFrame): dataframe 1
        y (pd.DataFrame): dataframe 2

    Returns:
        tuple: both dataframes equally shuffled in indices
    """
    idx = np.random.permutation(x.index)
    return x.reindex(idx), y.reindex(idx)

def oversample_targets(df, label_column, method="RandomOverSampler"):
    """
    Oversamples dataset

    Args:
        df (pd.DataFrame): dataframe to oversample
        method (str, optional): method used for oversampling. Defaults to "RandomOverSampler".

    Returns:
        pd.DataFrame: oversampled dataframe
    """
    features                    = df.loc[:, df.columns != label_column]
    targets                     = df.loc[:, label_column]
    module_name                 = "imblearn.over_sampling"
    cls_name                    = method
    cls                         = getattr(importlib.import_module(module_name), cls_name)
    oversampler                 = cls()
    features, targets           = oversampler.fit_resample(features, targets)
    features[label_column] = targets
    return features

def _apply_metadata(df, **kwargs):
    """
    Applies specified metadata to data

    Args:
        df (pd.DataFrame): dataframe to apply metadata to

    Returns:
        tuple: pd.Dataframe after applying metadata, list of numerical columns and list of categorical columns
    """
    num_cols, cat_cols = _make_col_dtype_lists(df)
    imputed            = kwargs.get('imputed', False)
    if imputed:
        print('Applying metadata....')
        if 'num_filler' in kwargs.keys():
            num_filler = kwargs['num_filler']
            if imputed:
                df.loc[:, num_cols] = df[num_cols].replace(to_replace=num_filler, value=np.nan)
        if 'cat_filler' in kwargs.keys():
            cat_filler = kwargs['cat_filler']
            if imputed:
                df.loc[:, cat_cols] = df[cat_cols].replace(to_replace=cat_filler, value=np.nan)
    return df, num_cols, cat_cols 

def _remove_cutoff_values(df, curves, th=0.05):
    """
    Returns the dataframe after applying the cutoff for some curves

    Args:
        df (pd.DataFrame): dataframe to remove outliers
        th (float, optional): threshold of number of samples that are outliers. 
        Used for displaying warnings of too many samples removed. Defaults to 0.05.

    Returns:
        pd.DataFrame: dataframe without outliers
    """
    len_df = len(df)

    if 'GR' in curves:
        outliers_low  = df[df.GR<0]
        outliers_high = df[df.GR>250]
        if (len(outliers_low)+len(outliers_high))/len_df>th:
            warnings.warn("Warning...........GR has more than 5% of its values lower than 0 or higher than 250")
        df.loc[df.GR<0, 'GR']   = 0
        df.loc[df.GR>250, 'GR'] = 250
    
    for resistivity in ['RSHA', 'RMED', 'RDEP']:
        if resistivity in curves:
            outliers = df[df[resistivity]>100]
            if len(outliers)/len_df>th:
                warnings.warn("Warning...........{} has more than 5% of its values higher than 100")
            df.loc[df[resistivity]>100, resistivity] = 100

    if 'NEU' in curves:
        outliers_high = df[df.NEU>1]
        outliers_low  = df[df.NEU<-0.5]
        if (len(outliers_low)+len(outliers_high))/len_df>th:
            warnings.warn("Warning...........NEU has more than 5% of its values higher than 1")
        df.loc[df.NEU>1, 'NEU']    = np.nan
        df.loc[df.NEU<-0.5, 'NEU'] = np.nan
    
    if 'PEF' in curves:
        outliers = df[df.PEF>10]
        if len(outliers)/len_df>th:
            warnings.warn("Warning...........PEF has more than 5% of its values higher than 10")
        df.loc[df.PEF>10, 'PEF'] = np.nan

    return df

def _split_df_wells(df, id_column, test_size):
    """
    Splits wells into two groups (train and val/test)

    Args:
        df (pd.DataFrame): dataframe with data of wells and well ID
        test_size (float): percentage (0-1) of wells to be in val/test data

    Returns:
        wells (list): wells IDs
        test_wells (list): wells IDs of val/test data
        training_wells (list): wells IDs of training data
    """
    wells          = df[id_column].unique()
    test_wells     = random.sample(list(wells), int(len(wells)*test_size))
    training_wells = [x for x in wells if x not in test_wells]
    return wells, test_wells, training_wells

def _df_split_train_test(df, id_column, test_size=0.2, test_wells=None):
    """
    Splits dataframe into two groups: train and val/test set.

    Args:
        df (pd.Dataframe): dataframe to split
        test_size (float, optional): size of val/test data. Defaults to 0.2.
        test_wells (list, optional): list of wells to be in val/test data. Defaults to None.

    Returns:
        tuple: dataframes for train and test sets, and list of test wells IDs
    """
    if test_wells is None:
        test_wells = _split_df_wells(df, id_column, test_size)[1]
    df_test  = df.loc[df[id_column].isin(test_wells)]
    df_train = df.loc[~df[id_column].isin(test_wells)]
    return df_train, df_test, test_wells

def _normalize(col, ref_low, ref_high, well_low, well_high):

    """
    Formula to normalize min and max values to the key well's min and max values.

    Args:
        col (pd.Series): column from dataframe to normalize (series)
        ref_low (float): min value of the column of the well of reference
        ref_high (float): max value of the column of the well of reference
        well_low (float): min value of the column of well to normalize
        well_high (float): max value of the column of well to normalize

    Returns:
        pd.Series: normalized series
    """
    diff_ref  = ref_high - ref_low
    diff_well = well_high - well_low
    return ref_low + diff_ref*(col - well_low)/diff_well

def _guess_BS_from_CALI(df, standard_BS_values=[6, 8.5, 9.875, 12.25, 17.5, 26]):
    """
    Guess bitsize from CALI, given the standard bitsizes

    Args:
        df (pd.DataFrame): dataframe to preprocess
        standard_BS_values (list): list of standardized bitsizes to consider

    Returns:
        pd.DataFrame: preprocessed dataframe
    
    """
    edges = [(a + b) / 2 for a, b in zip(standard_BS_values[::1], standard_BS_values[1::1])]
    edges.insert(0, -np.inf)
    edges.insert(len(edges), np.inf)
    df.loc[:, 'BS'] = pd.cut(df['CALI'], edges, labels=standard_BS_values)
    return df
