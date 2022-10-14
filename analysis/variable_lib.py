from databuilder.ehrql import case, when
from databuilder.tables.beta import tpp as schema


def age_as_of(date):
    return schema.patients.date_of_birth.difference_in_years(date)
