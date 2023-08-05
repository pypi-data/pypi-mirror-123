import json
from venv import logger
import pandas as pd
from datetime import datetime

# # # # -------------------------------------------------------------------------------- # # # #
import cloudscraper
scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# # # # -------------------------------------------------------------------------------- # # # #


class PublicAPI:
    """
    This is the official python library for Ramzinex.com Cryptocurrency Exchange
    Author: Mohammadreza Mirzaei
    Email: mirzaeimohammadreza98@gmail.com
    LinkedIn: https://www.linkedin.com/in/mohammad-reza-mirzaei/
    """

    def __init__(self):
        # self.api_ramzinex = api_ramzinex
        pass

    def get_prices(self):
        response_ramzinex = None
        try:
            url = "https://publicapi.ramzinex.com/exchange/api/exchange/prices"
            response_ramzinex = scraper.get(url)
            check_response_ramzinex = json.loads(response_ramzinex.text)
            return check_response_ramzinex
        except Exception as e:
            logger.exception(str(e))
            err = "#error #get_prices"
            if response_ramzinex is not None:
                err += "\nstatus_code:\n" + str(response_ramzinex.status_code) + \
                       "\nreason:\n" + str(response_ramzinex.reason)
            err += "\n" + str(e)
            result = {"status": -1, "error": err, "data": None}
            return result

    def get_markets(self, pair_id=None):
        response_ramzinex = None
        try:
            url = "https://publicapi.ramzinex.com/exchange/api/v1.0/exchange/pairs"
            if pair_id is not None:
                url += "/" + str(pair_id)
            response_ramzinex = scraper.get(url)
            check_response_ramzinex = json.loads(response_ramzinex.text)
            return check_response_ramzinex
        except Exception as e:
            logger.exception(str(e))
            err = "#error #get_markets"
            if response_ramzinex is not None:
                err += "\nstatus_code:\n" + str(response_ramzinex.status_code) + \
                       "\nreason:\n" + str(response_ramzinex.reason)
            err += "\n" + str(e)
            result = {"status": -1, "error": err, "data": None}
            return result

    def get_markets_turnover(self, data):
        if data is not None:
            try:
                pairs_volume, usdt_pairs_volume, irr_pairs_volume = [], [], []
                for market in data:
                    try:
                        pair_dict = {"pair": market['tv_symbol']['ramzinex'],
                                     "quote_volume": str(market["financial"]["last24h"]['quote_volume']),
                                     "base_volume": str(market["financial"]["last24h"]['base_volume']),
                                     "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        pairs_volume.append(pair_dict)
                        if market['tv_symbol']['ramzinex'][-3:] == "irr":
                            irr_pairs_volume.append(pair_dict)
                        elif market['tv_symbol']['ramzinex'][-4:] == "usdt":
                            usdt_pairs_volume.append(pair_dict)
                    except Exception as e:
                        logger.exception(str(e))

                df = pd.DataFrame(pairs_volume)
                df_irr = pd.DataFrame(irr_pairs_volume)
                irr_markets_turnover = df_irr[['quote_volume']].astype(float).sum()['quote_volume']
                df_usdt = pd.DataFrame(usdt_pairs_volume)
                usdt_markets_turnover = df_usdt[['quote_volume']].astype(float).sum()['quote_volume']
                return [irr_markets_turnover, usdt_markets_turnover, df, df_irr, df_usdt]
            except Exception as e:
                err = str(e)
                logger.exception(err)
                result = {"status": -1, "error": err, "data": None}
                return result
