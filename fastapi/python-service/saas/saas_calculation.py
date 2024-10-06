import json
import pandas as pd
import numpy as np
import os

def load_excel_data(file_path):
    """
    Load Excel data into a pandas DataFrame.
    """
    df = pd.read_excel(
        file_path,
        sheet_name='Sheet1',
        header=None,
        skiprows=1,
    )
    return df

def extract_income_statement(df):
    """
    Extract data from the income statement section.
    """
    income_statement = df.iloc[40:47].fillna(0)
    total_company_revenue = sum(list(income_statement[2][1:]))
    total_subscription_revenue = sum(list(income_statement[3][1:]))
    total_implementation_revenue = sum(list(income_statement[4][1:]))
    return {
        "total_company_revenue": total_company_revenue,
        "total_subscription_revenue": total_subscription_revenue,
        "total_implementation_revenue": total_implementation_revenue,
    }

def extract_cogs_statement(df):
    """
    Extract data from the cost of goods sold (COGS) section.
    """
    cogs_statement = df.iloc[50:58].fillna(0)
    total_company_cogs = sum(list(cogs_statement[2][0:4]))
    total_subscription_cogs = sum(list(cogs_statement[3][0:4]))
    total_implementation_cogs = sum(list(cogs_statement[4][0:4]))
    return {
        "total_company_cogs": total_company_cogs,
        "total_subscription_cogs": total_subscription_cogs,
        "total_implementation_cogs": total_implementation_cogs,
    }

def calculate_gross_profit(revenue_dict, cogs_dict):
    """
    Calculate gross profit based on revenue and COGS.
    """
    total_company_gross_profit = revenue_dict["total_company_revenue"] - cogs_dict["total_company_cogs"]
    subscription_gross_profit = revenue_dict["total_subscription_revenue"] - cogs_dict["total_subscription_cogs"]
    implementation_gross_profit = revenue_dict["total_implementation_revenue"] - cogs_dict["total_implementation_cogs"]
    return {
        "total_company_gross_profit": total_company_gross_profit,
        "subscription_gross_profit": subscription_gross_profit,
        "implementation_gross_profit": implementation_gross_profit,
    }

def calculate_gross_profit_percentage(revenue_dict, gross_profit_dict):
    """
    Calculate gross profit percentage.
    """
    total_company_gross_profit_percentage = (gross_profit_dict["total_company_gross_profit"] / revenue_dict["total_company_revenue"]) * 100
    subscription_gross_profit_percentage = (gross_profit_dict["subscription_gross_profit"] / revenue_dict["total_subscription_revenue"]) * 100
    implementation_gross_profit_percentage = (gross_profit_dict["implementation_gross_profit"] / revenue_dict["total_implementation_revenue"]) * 100
    return {
        "total_company_gross_profit_percentage": total_company_gross_profit_percentage,
        "subscription_gross_profit_percentage": subscription_gross_profit_percentage,
        "implementation_gross_profit_percentage": implementation_gross_profit_percentage,
    }

def extract_customer_data(df):
    """
    Extract customer-related data.
    """
    customer = df.iloc[59:63].fillna(0)
    new_customer = customer.iloc[2][2]
    total_customer = customer.iloc[3][2]
    return {
        "new_customer": new_customer,
        "total_customer": total_customer,
    }

def calculate_revenue_per_customer(revenue_dict, customer_dict):
    """
    Calculate revenue per customer.
    """
    implementation_revenue_per_customer = revenue_dict["total_implementation_revenue"] / customer_dict["new_customer"]
    subscription_revenue_per_customer = revenue_dict["total_subscription_revenue"] / customer_dict["total_customer"]
    return {
        "implementation_revenue_per_customer": implementation_revenue_per_customer,
        "subscription_revenue_per_customer": subscription_revenue_per_customer,
    }

def calculate_gross_profit_per_customer(gross_profit_dict, customer_dict):
    """
    Calculate gross profit per customer.
    """
    implementation_gross_profit_per_customer = gross_profit_dict["implementation_gross_profit"] / customer_dict["new_customer"]
    subscription_gross_profit_per_customer = gross_profit_dict["subscription_gross_profit"] / customer_dict["total_customer"]
    return {
        "implementation_gross_profit_per_customer": implementation_gross_profit_per_customer,
        "subscription_gross_profit_per_customer": subscription_gross_profit_per_customer,
    }

def calculate_average_customer_lifetime(df):
    """
    Calculate average customer lifetime.
    """
    churn_rate = df.iloc[72:73].fillna(0).iloc[0][2]
    average_customer_lifetime = 1 / churn_rate
    return {
        "average_customer_lifetime": average_customer_lifetime,
    }

def calculate_total_lifetime_value_subscription(revenue_per_customer_dict, gross_profit_per_customer_dict, average_lifetime_dict):
    """
    Calculate total lifetime value from subscription.
    """
    
    total_lifetime_value_subscription = average_lifetime_dict["average_customer_lifetime"] * gross_profit_per_customer_dict["subscription_gross_profit_per_customer"]
    return {
        "total_lifetime_value_subscription": total_lifetime_value_subscription,
    }

def calculate_customer_lifetime_value(total_lifetime_value_dict, gross_profit_per_customer_dict):
    """
    Calculate customer lifetime value.
    """
    customer_lifetime_value = total_lifetime_value_dict["total_lifetime_value_subscription"] + gross_profit_per_customer_dict["implementation_gross_profit_per_customer"]
    return {
        "customer_lifetime_value": customer_lifetime_value,
    }

def calculate_customer_acquisition_cost(df, customer_dict):
    """
    Calculate customer acquisition cost.
    """
    total_snm_expense = sum(df.iloc[84:90].fillna(0)[2][:])
    customer_acquisition_cost = total_snm_expense / customer_dict["new_customer"]
    return {
        "customer_acquisition_cost": customer_acquisition_cost,
    }

def calculate_ltv_cac_ratio(customer_lifetime_value_dict, acquisition_cost_dict):
    """
    Calculate LTV to CAC ratio.
    """
    ltv_cac_ratio = customer_lifetime_value_dict["customer_lifetime_value"] / acquisition_cost_dict["customer_acquisition_cost"]
    return {
        "ltv_cac_ratio" : ltv_cac_ratio,
    }

def final_result():
    """
    Main function to orchestrate the data processing and JSON generation.
    """
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'public', 'files'))
    arr = []
    for a, b, c in os.walk(path):
        arr = c

    arr.sort(reverse=True)
    file_path = os.path.join(path, arr[0])

    df = load_excel_data(file_path)

    income_statement = extract_income_statement(df)
    cogs_statement = extract_cogs_statement(df)
    gross_profit = calculate_gross_profit(income_statement, cogs_statement)
    gross_profit_percentage = calculate_gross_profit_percentage(income_statement, gross_profit)
    customer_data = extract_customer_data(df)
    revenue_per_customer = calculate_revenue_per_customer(income_statement, customer_data)
    gross_profit_per_customer = calculate_gross_profit_per_customer(gross_profit, customer_data)
    average_customer_lifetime = calculate_average_customer_lifetime(df)
    total_lifetime_value_subscription = calculate_total_lifetime_value_subscription(revenue_per_customer, gross_profit_per_customer, average_customer_lifetime)
    customer_lifetime_value = calculate_customer_lifetime_value(total_lifetime_value_subscription, gross_profit_per_customer)
    acquisition_cost = calculate_customer_acquisition_cost(df, customer_data)
    ltv_cac_ratio = calculate_ltv_cac_ratio(customer_lifetime_value, acquisition_cost)

    # Combine all results into a single dictionary
    results_dict = {
        **income_statement,
        **cogs_statement,
        **gross_profit,
        **gross_profit_percentage,
        **customer_data,
        **revenue_per_customer,
        **gross_profit_per_customer,
        **average_customer_lifetime,
        **total_lifetime_value_subscription,
        **customer_lifetime_value,
        **acquisition_cost,
        **ltv_cac_ratio,
    }

    
    return results_dict

    # If you want to write the JSON data to a file:
    # with open('results.json', 'w') as f:
    #     json.dump(results_dict, f, indent=2)

if __name__ == "__main__":
    final_result()
