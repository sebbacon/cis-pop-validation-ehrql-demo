from databuilder.ehrql import case, when
from databuilder.tables.beta import tpp as schema


def age_as_of(date):
    return schema.patients.date_of_birth.difference_in_years(date)


# TODO this is not exactly the same as died_from_any_cause().
# Note that this function only checks the patient table
def has_died(date):
    return (schema.patients.date_of_death.is_not_null()
            & (schema.patients.date_of_death < date))
