"""
This is a boilerplate pipeline 'feature_engineering'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import normalized_price, ohc

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=normalized_price,
                inputs="cleaned_sales",
                outputs=["normalized_price","boxcox_hyper"],
                name="normalized_price",
            ),            
            node(
                func=ohc,
                inputs="normalized_price",
                outputs=["engineered_sales","ohc_columns"],
                name="one_hot_encoding",
            ),

        ]
    )