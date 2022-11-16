"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import create_model,create_predications,reverse_ohc

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=create_model,
                inputs=["engineered_sales","parameters"],
                outputs=["ridge_model","ridge_model_fitted_scaler"],
                name="create_model",
            ),
            node(
                func=create_predications,
                inputs=["ridge_model","ridge_model_fitted_scaler","boxcox_hyper","engineered_sales"],
                outputs="engineered_sales_with_predictions",
                name="create_predications"
            ),        
            node(
                func=reverse_ohc,
                inputs=["engineered_sales_with_predictions","ohc_columns"],
                outputs="predictions",
                name="reverse_ohc"
            )         
        ]
    )