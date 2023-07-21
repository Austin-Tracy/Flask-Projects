import os
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def get_product_rules() -> tuple:
    """
    Reads in a cleaned dataset of telecommunication market basket data, 
    calculates frequent itemsets using the Apriori algorithm, and generates 
    association rules based on the frequent itemsets. Removes rules where the 
    antecedent and consequent are the same product, as well as rules where the 
    antecedent is "Dust-Off Compressed Gas 2 pack". Returns the resulting 
    product rules and a list of all products in the dataset.
    """
    df_cleaned = pd.read_csv(os.path.join('ml_app', 'data', 'teleco_market_basket_cleaned.csv'))
    frequent_itemsets = apriori(df_cleaned, min_support=0.01, use_colnames=True)
    product_rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    # remove product rules where the antecedent and consequent are the same product
    product_rules = product_rules[~(product_rules['antecedents'] == product_rules['consequents'])]
    # remove product rules where antecedent is "Dust-Off Compressed Gas 2 pack"
    product_list = df_cleaned.columns.tolist()
    return product_rules, product_list

