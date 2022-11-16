"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.3
"""
import numpy as np
import pandas as pd
import json
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV
from scipy.special import inv_boxcox

from kedro.extras.datasets.pickle import PickleDataSet

def create_model(sales: pd.DataFrame, params: dict) -> tuple:
    """ Create Ridge Regression model and return it """
    y=sales["normalizedPrice"]
    X=sales.drop(["price","normalizedPrice"],axis=1)


    # 25% split and same randon seed as simple linear regression
    train_test_split_params = params.get("train_test_split",{})
    X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                        test_size=train_test_split_params.get("test_size",.25),
                                                        random_state=train_test_split_params.get("random_state",101))
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train_s = scaler.transform(X_train)
    X_test_s = scaler.transform(X_test)

    # model parameters
    model_params = params.get("model_params",{})
    alphas = model_params.get("alphas",[10])
    cv = model_params.get("cv",3)

    ridgeCV = RidgeCV(alphas=alphas, 
                      cv=3).fit(X_train_s, y_train)

    #y_pred=ridgeCV.predict(X_test_s)
    return ridgeCV, scaler

# inputs=["ridge_model","ridge_model_fitted_scaler","boxcox_hyper","engineered_sales"],
def create_predications(ridge_model: PickleDataSet, 
                        ridge_model_fitted_scaler: PickleDataSet,
                        boxcox_hyper: dict, 
                        engineered_sales: pd.DataFrame) -> pd.DataFrame:
    """ 
        Returns engineered_sale with a predicted price as an added column
            
    """

    
    price = engineered_sales["price"]
    sales_X = engineered_sales.drop(["price","normalizedPrice"],axis=1)

    print(f"ridge_model_fitted_scaler {ridge_model_fitted_scaler}")

    sales_X_s = ridge_model_fitted_scaler.transform(sales_X)
    predicted_price = ridge_model.predict(sales_X_s)
    # boxcox lambda - saved when normalising price
    lambda_ = boxcox_hyper.get("lamdba")
    print(lambda_)  

    #engineered_sales["predicted_price_normalised"] = predicted_price
    engineered_sales["predicted_price"] = inv_boxcox(predicted_price,lambda_).astype(int)
    return engineered_sales.drop(["normalizedPrice"], axis=1)
    

def _reverse_ohc(sales: pd.DataFrame, ohc_column: str, cols: list) -> pd.DataFrame:
    """ 
        creates a DataFrame[ohc_column] where
            ohc_column: name of column before ohc, eg. model
            ohc_column will be set to the ohc column name where value = 1 
            column name will be extracted by removing the column prefix_sep, e.g.
                model_x_B-MAX -> B-MAX
            cols: list of columns created by ohc, e.g. [model_x_B-MAX , model_x_C-MAX, ....]

    """
    df = sales[cols].copy()
    for c in cols:
        c_name = c.split(f'{ohc_column}_x_')[1]
        print(c_name)
        mask = df[c] == 1
        df.loc[mask,ohc_column] = c_name
    return df

# ["engineered_sales_with_predictions","ohc_columns"],    
def _reverse_ohc(df_ohc: pd.DataFrame, ohc_column: str, cols: list) -> pd.DataFrame:
    """ 
        creates a DataFrame[ohc_column] where
            ohc_column: name of column before ohc, eg. model
            ohc_column will be set to the ohc column name where value = 1 
            column name will be extracted by removing the column prefix_sep, e.g.
                model_x_B-MAX -> B-MAX
            cols: list of columns created by ohc, e.g. [model_x_B-MAX , model_x_C-MAX, ....]

    """
    df = df_ohc[cols].copy()
    for c in cols:
        c_name = c.split(f'{ohc_column}_x_')[1]
        #print(c_name)
        mask = df[c] == 1
        df.loc[mask,ohc_column] = c_name
    return df.drop(cols, axis = 1)

def reverse_ohc(df_ohc: pd.DataFrame, ohc_columns: dict) -> pd.DataFrame:
    """ reverse the ohc to restore original columns 
        ohc columns are dropped 

        ohc was carried out using prefix_sep='_x_'
    """

    #ohc_columns = ['model', 'transmission', 'fuelType', 'tax', 'engineSize']
    for ohc_column in ohc_columns:
        cols = [ x for x in df_ohc.columns if x.startswith(f"{ohc_column}_x_") ]
        # cols -> [model_x_B-MAX , model_x_C-MAX, model_x_EcoSport, model_x_Edge, ....]
        non_ohc_col = _reverse_ohc(df_ohc   , ohc_column, cols)
        #print(non_ohc_col)
        df_ohc[ohc_column] = non_ohc_col
        df_ohc.drop(cols, axis = 1, inplace=True)
    return df_ohc