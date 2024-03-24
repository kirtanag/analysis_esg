from Green_Bonds_Analysis.climate_bond_analysis.company_esg_news_flow_analysis import get_all_news


# Let's get news flow around ESG for Barclays
barclays_esg_news = get_all_news('Barclays')
print(f'Got {len(barclays_esg_news)} news references')
print(barclays_esg_news)