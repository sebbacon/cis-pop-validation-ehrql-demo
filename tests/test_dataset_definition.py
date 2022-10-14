# To test dataset definition run the following command in the terminal:
# pytest tests/test_dataset_definition.py
import os
import pandas as pd
import pytest


def test_dataset_definition():
    # arrange
    cwd = os.getcwd()
    df_output = pd.read_csv(f"{cwd}/output/dataset.csv")

    # act
    pt2 = df_output.iloc[0].to_dict()
    pt3 = df_output.iloc[1].to_dict()
    pt7 = df_output.iloc[2].to_dict()
    
    # assert
    assert pt2 == {'patient_id': 2, 'sex': 'F', 'age': 72, 'has_died': 'F'}
    assert pt3 == {'patient_id': 3, 'sex': 'F', 'age': 62, 'has_died': 'F'}
    assert pt7 == {'patient_id': 7, 'sex': 'M', 'age': 22, 'has_died': 'F'}
