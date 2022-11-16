"""
This is a boilerplate pipeline 'feature_engineering'
generated using Kedro 0.18.3
"""
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import boxcox

def normalized_price(sales: pd.DataFrame) -> tuple:
    """ use boxcox to normalise sales price """

    bc_result = boxcox(sales["price"])
    bc_y = pd.Series(bc_result[0])
    lam = bc_result[1]

    boxcox_hyper = {}
    boxcox_hyper['lamdba'] = lam

    logging.info(f"lambda {lam}")
    bc_y.hist()

    sales["normalizedPrice"] = bc_y
    #sales.to_csv('sales_normalizedPrice.csv',index=False)
    return sales, boxcox_hyper

def ohc(sales: pd.DataFrame) -> tuple:
    """ OHC sales """
    categorical_features = sales.dtypes[sales.dtypes == object].index.tolist()
    categorical_features.append('tax')
    categorical_features.append('engineSize')
    logging.info(f"categorical_features {categorical_features}")
    sales = pd.get_dummies(sales, columns=categorical_features, prefix_sep='_x_')
    # sales.to_csv('sales_normalizedPrice_ohc.csv',index=False)
    return sales, categorical_features







