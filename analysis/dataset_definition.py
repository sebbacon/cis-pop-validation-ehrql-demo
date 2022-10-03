from databuilder.ehrql import Dataset, case, codelist_from_csv, when
from databuilder.tables.beta.tpp import patients, practice_registrations

dataset = Dataset()


dataset.set_population(practice_registrations.exists_for_patient())
