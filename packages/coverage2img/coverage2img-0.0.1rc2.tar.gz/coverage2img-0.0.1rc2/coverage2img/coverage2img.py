import json
import os
from typing import Tuple

import pandas as pd
import plotly.express as px

from .coverage_model import CoverageModel


def coverage_to_img(input_path: str = 'coverage.json', output_path: str = 'coverage.png'):
    df, depth = load_data(input_path)
    figure = create_figure(df, depth)
    figure.write_image(output_path)


def load_data(input_path: str) -> Tuple[pd.DataFrame, int]:
    data = json.loads(open(input_path).read())
    coverage_model = CoverageModel(**data)

    each_summary_data = {k: v.summary.to_dict() for k, v in coverage_model.files.coverage_of_files.items()}
    df = pd.DataFrame(each_summary_data.values(), index=each_summary_data.keys())
    depth_df = pd.DataFrame([k.split('/') for k in each_summary_data.keys()], index=each_summary_data.keys())
    depth = len(depth_df.columns)

    df = depth_df.join(df, how='left')
    return df, depth


def create_figure(df: pd.DataFrame, depth: int):
    path = df.columns[:depth]
    df = df[df['percent_covered'] != 0]
    treemap = px.treemap(
        df,
        path=path,
        values='percent_covered',
        color_continuous_scale=px.colors.diverging.RdYlGn,
        color="percent_covered",
    )
    return treemap


if __name__ == '__main__':
    pd.set_option('max_column', None)
    coverage_to_img('../coverage.json')

    # import matplotlib.pyplot as plt
    #
    # plt.axes()
    # rectangle = plt.Rectangle((0, 0), 20, 20, fc='blue', ec="red")
    # plt.gca().add_patch(rectangle)
    # plt.axis('scaled')
    # plt.show()
