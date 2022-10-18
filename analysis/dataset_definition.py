from analysis.variable_lib import age_as_of, has_died, address_as_of
from databuilder.ehrql import Dataset, case, codelist_from_csv, when
from databuilder.tables.beta.tpp import (
    patients,
    practice_registrations,
    sgss_covid_all_tests,
    clinical_events,
    addresses,
    hospital_admissions,
    emergency_care_attendances,
)
from datetime import date
import codelists


def has_prior_event(codelist, where=True):
    return (
        prior_events.take(where)
        .take(prior_events.snomedct_code.is_in(codelist))
        .exists_for_patient()
    )


# Set index date
# TODO this is just an example for testing
index_date = date(2022, 6, 1)


dataset = Dataset()
address = address_as_of(index_date)
prior_events = clinical_events.take(clinical_events
                                    .date.is_on_or_before(index_date))

# Define and extract dataset variables ----
# Demographic variables
dataset.sex = patients.sex
dataset.age = age_as_of(index_date)
dataset.has_died = has_died(index_date)

# TPP care home flag
dataset.care_home_tpp = case(
    when(address.care_home_is_potential_match).then(True), default=False
)

# Patients in long-stay nursing and residential care
dataset.care_home_code = has_prior_event(codelists.carehome)


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
set_sex_fm = (dataset.sex == "F") | (dataset.sex == "M")
set_age_ge2_le120 = (dataset.age >= 2) & (dataset.age <= 120)
set_has_not_died = ~dataset.has_died

# Set dataset population ----
dataset.set_population(
    set_registered & set_sex_fm & set_age_ge2_le120 & set_has_not_died
)
