from databuilder.ehrql import case, when
from databuilder.tables.beta import tpp as schema


def age_as_of(date):
    return schema.patients.date_of_birth.difference_in_years(date)


# TODO this is not exactly the same as died_from_any_cause().
# Note that this function only checks the patient table
def has_died(date):
    return (schema.patients.date_of_death.is_not_null()
            & (schema.patients.date_of_death < date))


def address_as_of(date):
    addr = schema.addresses
    active = addr.take(
        addr.start_date.is_on_or_before(date)
        & (addr.end_date.is_after(date) | addr.end_date.is_null())
    )
    # Where there are multiple active address registrations we need to pick one.
    # Logic copied from:
    # https://github.com/opensafely-core/cohort-extractor/blob/e77a0aa2/cohortextractor/tpp_backend.py#L1756-L1773
    ordered = active.sort_by(
        # Prefer the address which was registered first
        addr.start_date,
        # Prefer the address registered for longest
        addr.end_date,
        # Prefer addresses with a postcode
        case(when(addr.has_postcode).then(1), default=0),
        # Use the opaque ID as a tie-breaker for sort stability
        addr.address_id,
    )
    return ordered.first_for_patient()


def _registrations_overlapping_period(start_date, end_date):
    regs = schema.practice_registrations
    return regs.take(
        regs.start_date.is_on_or_before(start_date)
        & (regs.end_date.is_after(end_date) | regs.end_date.is_null())
    )


def practice_registration_as_of(date):
    regs = _registrations_overlapping_period(date, date)
    return regs.sort_by(regs.start_date, regs.end_date).first_for_patient()
