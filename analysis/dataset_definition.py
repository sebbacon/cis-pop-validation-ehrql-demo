from databuilder.ehrql import Dataset, case, codelist_from_csv, when
from databuilder.tables.beta.tpp import (
    patients,
    practice_registrations,
    sgss_covid_all_tests,
)
from datetime import date

dataset = Dataset()

# Define and extract dataset variables ----
# Demographic variables
dataset.sex = patients.sex
dataset.age = patients.date_of_birth.difference_in_years(date.today())

# Covid tests
covid_tests = sgss_covid_all_tests
prior_tests = covid_tests.take(
    covid_tests.specimen_taken_date.is_on_or_before("2022-01-01")
)
dataset.covid_test_0_date = prior_tests.specimen_taken_date.maximum_for_patient()

# Define dataset restrictions ----
set_registered = practice_registrations.exists_for_patient()
set_sex_not_null = dataset.sex.is_not_null()
set_sex_fm = (dataset.sex == "F") | (dataset.sex == "M")
set_age_ge2_le120 = (dataset.age >= 2) & (dataset.age <= 120)

# Set dataset population ----
dataset.set_population(
    set_registered & set_sex_not_null & set_sex_fm & set_age_ge2_le120
)
