"""
This is a boilerplate pipeline 'data_cleaning'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import clean_sales

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=clean_sales,
                inputs="sales",
                outputs="cleaned_sales",
                name="clean_sales_node",
            )
        ]
    )