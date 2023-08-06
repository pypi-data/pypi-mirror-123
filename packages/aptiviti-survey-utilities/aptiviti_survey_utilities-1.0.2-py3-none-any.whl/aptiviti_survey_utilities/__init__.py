import pandas as pd 
import numpy as np
from aptiviti_odbc import aptiviti_odbc_connection

class survey_utilities:
    def __init__(self, sql_host, sql_username, sql_password, database='Incite'):

        self.frequency_period_map = {
            'quarterly': 'Q',
            'annual': 'Y'
        }

        self.frequency_seasonal_map = {
            'quarterly': 4,
            'annual': 1
        }


        self.size_list = [
            'Fortune100', 
            'Fortune500', 
            'Fortune1000', 
            'SP500', 
            'Global1000', 
            'Global2000', 
            'Private225', 
            'GiantPrivate', 
            'FederalGovernment', 
            'BIG72', 
            'TopTierTelco'
        ]

        self.survey_month_map = {
            'JAN': 1,
            'FEB': 2,
            'MAR': 3,
            'APR': 4,
            'MAY': 5,
            'JUN': 6,
            'JUL': 7,
            'AUG': 8,
            'SEP': 9,
            'OCT': 10,
            'NOV': 11,
            'DEC': 12
        }


        self.survey_quarter_map = {
            1: 1,
            2: 1,
            3: 1,
            4: 2,
            5: 2,
            6: 2,
            7: 3,
            8: 3, 
            9: 3,
            10: 4,
            11: 4,
            12: 4
        }

        self.reverse_survey_quarter_map = {
            1: 1,
            2: 4,
            3: 7,
            4: 10
        }

        self.database_connection = aptiviti_odbc_connection(sql_host, sql_username, sql_password, database)

    def get_tsis_fundamentals(self, vendors = None, industries = None, metrics = ['ADOPTION', 'REPLACING', 'INCREASE', 'DECREASE', 'FLAT'], limit=None):

        if vendors == None:
            vendor_query = ''
        else:
            vendor_list = "', '".join(vendors)
            vendor_query = f"vu.[Vendor_Overall] in ('{vendor_list}') AND "

        if industries == None:
            industries_query = ''
        else:
            industry_list = "', '".join(industries)
            industries_query = f"[Industry] in ('{industry_list}') AND "

        if limit == None:
            limit_query = ''
        else:
            limit_query = f"TOP {str(limit)}"

        metric_list = "', '".join(metrics)

        survey_data_sql = f"""
        SELECT {limit_query}
            rw.[Survey], rw.[Survey Date], dw.[Industry], dw.[Region], rw.[Sector], rw.[Vendor], rw.[Metric], dw.[Enterprise_Size], dw.[Public_Private], dw.[Fortune100], dw.[Fortune500],dw.[Fortune1000],dw.[SP500],dw.[Global1000],dw.[Global2000],dw.[Private225],dw.[GiantPrivate],dw.[FederalGovernment],dw.[BIG72],dw.[TopTierTelco], COUNT(rw.[Metric]) as Citations 
        FROM
            [Survey].[dbo].[TSIS_Response_Warehouse] rw WITH (NOLOCK)
        INNER JOIN
            [Survey].[dbo].[TSIS_Demographics_Warehouse] dw
            ON rw.[First] = dw.[First] AND rw.[Last] = dw.[Last]
        INNER JOIN
            [Classification].[dbo].[Vendor_Universe] vu
            ON rw.[Vendor] = vu.[Vendor]
        WHERE {vendor_query} {industries_query} rw.[Metric] in ('{metric_list}')
        GROUP BY 
            rw.[Survey], dw.[Industry], dw.[Region], rw.[Sector], rw.[Survey Date], rw.[Vendor], rw.[Metric], dw.[Enterprise_Size], dw.[Public_Private], dw.[Fortune100], dw.[Fortune500],dw.[Fortune1000],dw.[SP500],dw.[Global1000],dw.[Global2000],dw.[Private225],dw.[GiantPrivate],dw.[FederalGovernment],dw.[BIG72],dw.[TopTierTelco]
        ORDER BY 
            rw.[Survey]
        """
        survey_data = self.database_connection.query(survey_data_sql)
        survey_data['Month'] = survey_data['Survey Date'].str[:3]
        survey_data['Month'] = survey_data['Month'].map(self.survey_month_map)
        survey_data['Year'] = "20" + survey_data['Survey Date'].str[-2:]
        survey_data['Year'] = survey_data['Year'].astype(int)
        
        for size in self.size_list:
            survey_data.loc[~survey_data[size].isnull(), size] = 1
            survey_data.loc[survey_data[size].isnull(), size] = 0

        survey_data = pd.get_dummies(survey_data, columns=['Enterprise_Size'], drop_first=True)
        return survey_data

    def calculate_fundamental_metrics(self, survey_data, pivot_index=['period'], pivot_columns=['Metric'], percent_change=False, frequency='quarterly'):
        total_citations = survey_data.groupby(['Survey','Survey Date','Month', 'Year'])['Citations'].sum()
        survey_data = pd.concat([survey_data, pd.get_dummies(survey_data[['Industry', 'Region', 'Sector']])], axis='columns')
        survey_data.drop(['Industry', 'Region', 'Sector'], axis='columns', inplace=True)
        merged_data = survey_data.merge(total_citations, how='inner', on='Survey')        
        merged_data.loc[:,'Citations_x'] = merged_data.loc[:,'Citations_x'] / merged_data.loc[:,'Citations_y']
        merged_data.drop('Citations_y', axis='columns', inplace=True)
        merged_data['period'] = merged_data['Month'].astype(str) + '/1/' + merged_data['Year'].astype(str)
        merged_data['period'] = pd.to_datetime(merged_data['period'])
        merged_data['period'] = merged_data['period'].dt.to_period(self.frequency_period_map[frequency])
        merged_data.drop(['Vendor', 'Survey', 'Survey Date', 'Month', 'Year'], axis='columns', inplace=True)
        merged_data[self.size_list] = merged_data[self.size_list].astype(int)
        pivoted = merged_data.pivot_table(index=pivot_index, columns=pivot_columns, aggfunc=np.sum)
        pivoted.columns = [' '.join(col).strip().replace('Citations_x ', '') for col in pivoted.columns.values]
        pivoted.fillna(0,inplace=True)
        if percent_change:
            for column in pivoted.columns:
                pivoted.loc[:,column] = pivoted.loc[:,column].pct_change()
        pivoted.replace([np.inf, -np.inf], np.nan, inplace=True)
        pivoted.fillna(0,inplace=True)
        return [pivoted, total_citations]