import pandas as pd
import plotly
import plotly.graph_objects as go
import json
from typing import List, Dict


def generate_EDA(df: pd.DataFrame, feature_vars: List[str], target_var: str) -> Dict[str, str]:
    """
    Generates exploratory data analysis plots for a given dataframe.

    Args:
    - df: A pandas dataframe containing the data to be analyzed.
    - feature_vars: A list of strings representing the names of the feature variables to be analyzed.
    - target_var: A string representing the name of the target variable to be analyzed.

    Returns:
    - A dictionary containing HTML code for each plot. The keys are the names of the feature variables.
    """
    print("Feature variables: ", feature_vars)
    print("Target variable: ", target_var)
    plots_dict = {}
    for i, feature in enumerate(feature_vars, start=1):
        fig = go.Figure()
        unique_count = df[feature].nunique()
        if unique_count <= 11: # Categorical features including binary
            if unique_count == 2:  # Binary
                df_grouped = df.groupby([feature, target_var]).size().reset_index(name='counts')
                for target_value in df_grouped[target_var].unique():
                    fig.add_trace(
                        go.Bar(
                            x=df_grouped[df_grouped[target_var]==target_value][feature],
                            y=df_grouped[df_grouped[target_var]==target_value]['counts'],
                            name=f"{target_var}={target_value}"
                        )
                    )
                fig.update_layout(barmode='stack')
            else:  # Categorical (non-binary)
                df_grouped = df.groupby([feature, target_var]).size().reset_index(name='counts')
                for target_value in df_grouped[target_var].unique():
                    fig.add_trace(
                        go.Bar(
                            x=df_grouped[df_grouped[target_var]==target_value][feature],
                            y=df_grouped[df_grouped[target_var]==target_value]['counts'],
                            name=f"{target_var}={target_value}"
                        )
                    )
                fig.update_layout(barmode='stack')

        else:  # Quantitative variables
            for target_value in df[target_var].unique():
                fig.add_trace(
                    go.Violin(
                        y=df[df[target_var]==target_value][feature],
                        name=f"{target_var}={target_value}",
                        box_visible=True,
                        meanline_visible=True,
                    )
                )

        
        fig.update_layout(title_text=f"{feature}", showlegend=True)

        # Add the div tag with unique id around the plot HTML
        plots_dict[feature] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
    return plots_dict