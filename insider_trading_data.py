from get_trading_data import get_data  # get data from NSE insider trading api
import numpy as np
import pandas as pd
from datetime import datetime
import yfinance as yf
import os
import logging

logging.basicConfig(filename="data_update.log", format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Fields to track
columns = ['ticker', 'company_name', 'regulation', 'person_name', 'person_category',
           'type_of_security_prior', 'no_of_security_prior', 'pct_shareholding_prior',
           'type_of_security_acquired', 'no_of_securities_acquired', 'value_of_securities_acquired',
           'transaction_type', 'type_of_security_post', 'no_of_security_post', 'pct_post',
           'date_of_allotment_acquisition_from', 'date_of_allotment_acquisition_to',
           'date_of_intimation_to_company', 'mode_of_acquisition', 'derivative_type_security',
           'derivative_contract_specification', 'notional_value_buy', 'units_contract_lot_size_buy',
           'notional_value_sell', 'units_contract_lot_size_sell', 'exchange', 'remark',
           'broadcast_date_and_time', 'xbrl_link']

insider_df = pd.read_csv('insider.csv', index_col=0, parse_dates=['date'])  # load csv file

insider_df['person_name'] = insider_df['person_name'].str.lower()
insider_df['person_category'] = insider_df['person_category'].str.lower()

data = get_data()  # fetch data obtained from API

if type(data) == str:
    # there was some error and we couldn't fetch data from the API
    logger.info('error fetching data')
else:
    logger.info('data fetched')
    # Fill the dataframe with the insider trades from the day
    insider_data = data['data']
    # we will fill this dataframe every day
    day_df = pd.DataFrame(columns=columns)

    for i in range(len(insider_data)):
        trade_data = insider_data[i]
        date = datetime.strptime(trade_data['date'], '%d-%b-%Y %H:%M')

        company_name = trade_data['company']
        ticker = trade_data['symbol']
        person_name = trade_data['acqName'].lower()
        regulation = trade_data['anex'].lower()

        if 'personCategory' in trade_data:
            person_category = trade_data['personCategory'].lower()
        else:
            person_category = '-'

        if type(trade_data['secAcq']) == str:
            number_of_securities = int(trade_data['secAcq'])
        else:
            number_of_securities = 0

        if type(trade_data['secVal']) == str and trade_data['secVal'].replace('.', '', 1).isdigit():
            value_of_securities = int(float(trade_data['secVal']))
        else:
            value_of_securities = 0

        transaction_type = trade_data['tdpTransactionType']

        if (trade_data['befAcqSharesNo']) == 'Nil' or (trade_data['befAcqSharesNo']) == '-':
            shares_before_acq = 0
        else:
            shares_before_acq = int(trade_data['befAcqSharesNo'])

        if (trade_data['afterAcqSharesNo'] == 'Nil') or (trade_data['afterAcqSharesNo'] == '-'):
            shares_after_acq = 0
        else:
            shares_after_acq = int(trade_data['afterAcqSharesNo'])

        if (trade_data['befAcqSharesPer'] == 'Nil') or (trade_data['befAcqSharesPer'] == '-'):
            pct_before_acq = 0
        else:
            pct_before_acq = float(trade_data['befAcqSharesPer'])

        if (trade_data['afterAcqSharesPer'] == 'Nil') or (trade_data['afterAcqSharesPer'] == '-'):
            pct_after_acq = 0
        else:
            pct_after_acq = float(trade_data['afterAcqSharesPer'])

        acq_mode = trade_data['acqMode']
        type_of_security_prior = trade_data['secType']
        security_type = trade_data['secType']
        date_of_allotment_acquisition_from = trade_data['acqfromDt']
        date_of_allotment_acquisition_to = trade_data['acqtoDt']
        date_of_intimation_to_company = trade_data['intimDt']
        exchange = trade_data['exchange']
        derivative_type_security = trade_data['derivativeType']
        derivative_contract_specification = trade_data['derivativeType']
        notional_value_buy = trade_data['derivativeType']
        units_contract_lot_size_buy = trade_data['derivativeType']
        notional_value_sell = trade_data['derivativeType']
        units_contract_lot_size_sell = trade_data['derivativeType']
        no_of_security_prior = trade_data['befAcqSharesNo']
        pct_shareholding_prior = trade_data['befAcqSharesPer']
        type_of_security_acquired = trade_data['secType']
        no_of_securities_acquired = trade_data['secAcq']
        value_of_securities_acquired = trade_data['secVal']
        type_of_security_post = trade_data['securitiesTypePost']
        no_of_security_post = trade_data['afterAcqSharesNo']
        pct_post = trade_data['afterAcqSharesPer']
        mode_of_acquisition= trade_data['acqMode']
        broadcast_date_and_time = trade_data['date']
        remark = trade_data['derivativeType']
        xbrl_link = trade_data['xbrl']

        # Add missing columns with default values or adjust the number of elements in the row
        row = [
            ticker, company_name, regulation, person_name, person_category,
            type_of_security_prior, no_of_security_prior, pct_shareholding_prior,
            type_of_security_acquired, no_of_securities_acquired, value_of_securities_acquired,
            transaction_type, type_of_security_post, no_of_security_post, pct_post,
            date_of_allotment_acquisition_from, date_of_allotment_acquisition_to,
            date_of_intimation_to_company, mode_of_acquisition, derivative_type_security,
            derivative_contract_specification, notional_value_buy, units_contract_lot_size_buy,
            notional_value_sell, units_contract_lot_size_sell, exchange, remark,
            broadcast_date_and_time, xbrl_link
        ]

        # Make sure the length of the row matches the length of the columns
        day_df.loc[len(day_df.index)] = row

        # Print trade information for debugging
        print(f"Processed trade {i+1}/{len(insider_data)}: {ticker} - {company_name}")

    # Post-processing of the dataframe
    logger.info(f'entries added: {len(day_df)}')
    insider_df = pd.concat([day_df, insider_df], ignore_index=True)
    insider_df.to_csv('insider.csv')
