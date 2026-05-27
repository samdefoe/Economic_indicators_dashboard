import numpy as np
from llm_summarizer import _create_all_snapshots
from data_retrieval import convert_data_to_dfs

def _generate_score(zone):
    zone_scores = {
        "red_low": 25,
        "yellow_low": 65,
        "green": 100,
        "yellow_high":65,
        "red_high": 25
    }

    score = zone_scores[zone]
    return score


def generate_economy_health_score(snapshots):
    weights = {
    "real_gdp": 0.18,
    "unemployment_rate": 0.18,
    "inflation_rate": 0.16,
    "consumer_price_index": 0.10,
    "producer_price_index": 0.08,
    "personal_consumption_expenditures": 0.10,
    "consumer_sentiment": 0.09,
    "federal_funds_rate": 0.06,
    "retail_sales": 0.05,
    }

    scores = []
    for i in range(len(snapshots)):
        scores.append(_generate_score(snapshots[i]['current_zone']))

    scores_array = np.array(scores)
    weights_array = np.array(list(weights.values()))

    final_score = np.sum(scores_array * weights_array)

    return final_score

    

