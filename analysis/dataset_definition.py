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
# TODO age_kids, agebandCIS
# https://github.com/opensafely/CIS-pop-validation/blob/889723139089e4ab146862d6fba1f410cf35b8c4/analysis/study_definition.py#L94-L112
# TODO has_died
# https://github.com/opensafely/CIS-pop-validation/blob/889723139089e4ab146862d6fba1f410cf35b8c4/analysis/study_definition.py#L59-L62
# TODO care_home_tpp, care_home_code
# https://github.com/opensafely/CIS-pop-validation/blob/889723139089e4ab146862d6fba1f410cf35b8c4/analysis/study_definition.py#L64-L83
# TODO msoa
# https://github.com/opensafely/CIS-pop-validation/blob/889723139089e4ab146862d6fba1f410cf35b8c4/analysis/study_definition.py#L213-L223
# TODO region
# https://github.com/opensafely/CIS-pop-validation/blob/889723139089e4ab146862d6fba1f410cf35b8c4/analysis/study_definition.py#L248-L270

# Single-day events (Did any event occur on this day?) ----
# https://github.com/opensafely/CIS-pop-validation/blob/889723139089e4ab146862d6fba1f410cf35b8c4/analysis/study_definition.py#L300-L369
# TODO positive covid test: postest_01
# TODO positive case identification: primary_care_covid_case_01
# TODO emergency attendance for covid: covidemergency_01
# TODO covid admission: covidadmitted_01
# TODO composite measure: any_infection_or_disease_01

# 14-day events (Did any event occur within the last 14 days?) ----
# https://github.com/opensafely/CIS-pop-validation/blob/889723139089e4ab146862d6fba1f410cf35b8c4/analysis/study_definition.py#L372-L443
# TODO positive covid test: postest_14
# TODO positive case identification: primary_care_covid_case_14
# TODO emergency attendance for covid: covidemergency_14
# TODO covid admission: covidadmitted_14
# TODO composite measure: any_infection_or_disease_14

# Ever-day events (Did any event occur any time up to and including this day?) ----
# https://github.com/opensafely/CIS-pop-validation/blob/889723139089e4ab146862d6fba1f410cf35b8c4/analysis/study_definition.py#L445-L517
# TODO positive covid test: postest_ever
# TODO positive case identification: primary_care_covid_case_ever
# TODO emergency attendance for covid: covidemergency_ever
# TODO covid admission: covidadmitted_ever
# TODO composite measure: any_infection_or_disease_ever

# Define dataset restrictions ----
set_registered = practice_registrations.exists_for_patient()
set_sex_not_null = dataset.sex.is_not_null()
set_sex_fm = (dataset.sex == "F") | (dataset.sex == "M")
set_age_ge2_le120 = (dataset.age >= 2) & (dataset.age <= 120)

# Set dataset population ----
dataset.set_population(
    set_registered & set_sex_not_null & set_sex_fm & set_age_ge2_le120
)
