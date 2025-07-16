def filter_leads(leads, filters):
    """
    Filters a list of leads based on a dictionary of filters.
    """
    if not filters:
        return leads

    filtered_leads = []
    for lead in leads:
        match = True
        for key, value in filters.items():
            if key in lead and lead[key] != value:
                match = False
                break
        if match:
            filtered_leads.append(lead)

    return filtered_leads

if __name__ == "__main__":
    # This is an example of how to use the filtering module.
    # The leads would be scraped from a website, and the filters
    # would be defined by the admin in the dashboard.
    sample_leads = [
        {"name": "John Doe", "company": "ABC Inc.", "industry": "Technology"},
        {"name": "Jane Smith", "company": "XYZ Corp.", "industry": "Finance"},
        {"name": "Peter Jones", "company": "123 Ltd.", "industry": "Technology"},
    ]

    # Example filter: only show leads from the "Technology" industry
    admin_defined_filters = {"industry": "Technology"}

    filtered_results = filter_leads(sample_leads, admin_defined_filters)
    print(f"Found {len(filtered_results)} matching leads:")
    for lead in filtered_results:
        print(lead)
