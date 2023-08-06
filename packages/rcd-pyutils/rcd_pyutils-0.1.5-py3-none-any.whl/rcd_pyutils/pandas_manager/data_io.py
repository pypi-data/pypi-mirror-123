import os
import json
import pandas as pd
from functools import partial
from rcd_pyutils import decorator_manager, file_manager
from concurrent.futures import ThreadPoolExecutor


@decorator_manager.timeit(program_name="Parallel Writing to json")
def pandas_to_json(df: pd.DataFrame, json_path: str) -> None:
    iter_row = zip(df.index.tolist(), df.itertuples(index=False))
    work_func = partial(file_manager.write_json, output_path=json_path)
    with ThreadPoolExecutor() as executor:
        list(executor.map(work_func, iter_row))
