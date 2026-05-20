from datetime import date

# 🇧🇬 Bulgarian official holidays
BG_HOLIDAYS = {
    "2026-01-01",  # New Year
    "2026-03-03",  # Liberation Day
    "2026-05-01",  # Labour Day
    "2026-05-06",  # St. George Day
    "2026-09-06",  # Unification Day
    "2026-09-22",  # Independence Day
    "2026-12-24",
    "2026-12-25",
    "2026-12-26",
}

# 🏢 Company-specific holidays (edit freely)
COMPANY_HOLIDAYS = {
    # "2026-04-10",
}

# 🏖 Personal vacation days (you control this)
PERSONAL_VACATION = {
    # "2026-02-15",
}


def is_non_working_day(today: date) -> bool:
    day_str = today.strftime("%Y-%m-%d")

    # Weekend check
    if today.weekday() >= 5:
        return True

    # Holiday checks
    if day_str in BG_HOLIDAYS:
        return True

    if day_str in COMPANY_HOLIDAYS:
        return True

    if day_str in PERSONAL_VACATION:
        return True

    return False