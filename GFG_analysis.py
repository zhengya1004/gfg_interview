import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from typing import *


def plot_revenue_cr_abs(df: pd.DataFrame) -> None:
    """Plot revenue vs. conversion rate.

    :param df: with columns:
     - Channel_Type
     - Spend
     - Revenue
    :return:
    """

    fig = plt.figure(figsize=(8, 6))
    ax = plt.axes()
    fig.suptitle('Analysis by Channel Type')
    colors = {'App install network': 'red', 'Web channel': 'green', 'Newsletters': 'blue', 'PR': 'yellow'}

    grouped = df.groupby('Channel_Type')
    for key, group in grouped:
        group.plot(ax=ax, kind='scatter', x='Spend', y='Revenue', label=key, color=colors[str(key)])

    ax.set_ylabel("Revenue")
    ax.set_xlabel("Spend")

    plt.savefig("plots/analysis_Revenue_Spend.png")


def preform_hypothesis_test(df: pd.DataFrame) -> None:
    """Perform the hypothesis testing

    :param df: with columns:
     - Channel_Type
     - Paid_Free
     - Spend
     - Revenue
    :return:
    """
    df_app = df[df['Channel_Type'] == 'App install network'].copy()
    df_web = df[df['Channel_Type'] == 'Web channel'].copy()
    df_newsletter = df[df['Channel_Type'] == 'Newsletters'].copy()
    df_pr = df[df['Channel_Type'] == 'PR'].copy()
    df_paid = df[df['Paid_Free'] == 'Paid'].copy()
    df_free = df[df['Paid_Free'] == 'Free'].copy()
    corr_app, p_app = pearsonr(df_app['Spend'], df_app['Revenue'])
    corr_web, p_web = pearsonr(df_web['Spend'], df_web['Revenue'])
    corr_newsletter, p_newsletter = pearsonr(df_newsletter['Spend'], df_newsletter['Revenue'])
    corr_pr, p_pr = pearsonr(df_pr['Spend'], df_pr['Revenue'])
    corr_paid, p_paid = pearsonr(df_paid['Spend'], df_paid['Revenue'])
    corr_free, p_free = pearsonr(df_free['Spend'], df_free['Revenue'])
    correlation = [[corr_app, p_app], [corr_web, p_web],
                   [corr_newsletter, p_newsletter], [corr_pr, p_pr],
                   [corr_paid, p_paid], [corr_free, p_free]]
    df_correlation = pd.DataFrame(data=correlation, columns=['Correlation_Coefficient', 'p_value'],
                                  index=['app_install_network', 'web_channel', 'newsletters', 'PR', 'paid',
                                         'free']).reset_index(drop=False).rename(columns={'index': 'type'})
    df_correlation.to_csv("output/df_correlation.csv", index=False)


def plot_data_channel_type(df: pd.DataFrame) -> None:
    """Plot the some metrics for each channel type.

    This function will plot the following metrics for each channel type:
     - average CR per week per channel
     - average ABS per week per channel
     - average CIR per week per channel
    :param df: with columns:
     - Channel_Type
     - CR
     - ABS
     - CIR
    :return:
    """
    fig, axs = plt.subplots(1, 3, figsize=(12, 7))
    fig.suptitle('Analysis by Channel Type')
    fig.text(0.5, 0.04, 'Channel Type', ha='center')
    df_cr = df.sort_values(by='CR', ascending=False)
    df_abs = df.sort_values(by='ABS', ascending=False)
    df_cir = df.sort_values(by='CIR', ascending=False)
    axs[0].bar(df_cr['Channel_Type'], df_cr['CR'], width=0.5)
    axs[1].bar(df_abs['Channel_Type'], df_abs['ABS'], width=0.5)
    axs[2].bar(df_cir['Channel_Type'], df_cir['CIR'], width=0.5)

    axs[0].set_ylabel("Avg Conversion Rate per week per channel", fontsize=10)
    for x, y in zip(df_cr['Channel_Type'], df_cr['CR']):
        label = "{:.5f}".format(y)
        axs[0].annotate(label, (x, y), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=7)
        axs[0].tick_params(axis='y', labelsize=9)
        axs[0].tick_params(axis='x', labelsize=9, rotation=90)

    axs[1].set_ylabel("Avg ABS per week per channel", fontsize=10)
    for x, y in zip(df_abs['Channel_Type'], df_abs['ABS']):
        label = "{:.5f}".format(y)
        axs[1].annotate(label, (x, y), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=7)
        axs[1].tick_params(axis='y', labelsize=9)
        axs[1].tick_params(axis='x', labelsize=9, rotation=90)

    axs[2].set_ylabel("Avg Cost to Income Ratio per week per channel", fontsize=10)
    for x, y in zip(df_cir['Channel_Type'], df_cir['CIR']):
        label = "{:.5f}".format(y)
        axs[2].annotate(label, (x, y), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=7)
        axs[2].tick_params(axis='y', labelsize=9)
        axs[2].tick_params(axis='x', labelsize=9, rotation=90)

    plt.subplots_adjust(wspace=0.3, bottom=0.2)

    plt.savefig("plots/analysis_channel_type.png")


def plot_data_week(df: pd.DataFrame) -> None:
    """Plot the some metrics for each week.

    This function will plot the following metrics for each week:
     - average CR over all channels
     - average ABS over all channels
     - average CIR overall channels
    :param df: with columns:
     - Week
     - CR
     - ABS
     - CIR
    :return:
    """
    fig, axs = plt.subplots(1, 3, figsize=(10, 7))

    fig.suptitle('Analysis by Week')
    fig.text(0.5, 0.04, 'Week', ha='center')
    axs[0].bar(df['Week'], df['CR'], width=0.5)
    axs[1].bar(df['Week'], df['ABS'], width=0.5)
    axs[2].bar(df['Week'], df['CIR'], width=0.5)

    axs[0].set_ylabel("Avg Conversion Rate per channel", fontsize=10)
    for x, y in zip(df['Week'], df['CR']):
        label = "{:.5f}".format(y)
        axs[0].annotate(label, (x, y), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=7)
        axs[0].tick_params(axis='y', labelsize=9)
        axs[0].tick_params(axis='x', labelsize=9)

    axs[1].set_ylabel("Avg ABS per channel", fontsize=10)
    for x, y in zip(df['Week'], df['ABS']):
        label = "{:.5f}".format(y)
        axs[1].annotate(label, (x, y), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=7)
        axs[1].tick_params(axis='y', labelsize=9)
        axs[1].tick_params(axis='x', labelsize=9)

    axs[2].set_ylabel("Avg Cost to Income Ratio per channel", fontsize=10)
    for x, y in zip(df['Week'], df['CIR']):
        label = "{:.5f}".format(y)
        axs[2].annotate(label, (x, y), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=7)
        axs[2].tick_params(axis='y', labelsize=9)
        axs[2].tick_params(axis='x', labelsize=9)

    plt.subplots_adjust(wspace=0.4, bottom=0.2)

    plt.savefig("plots/analysis_week.png")


def plot_data_paid_free(df: pd.DataFrame) -> None:
    """Plot the some metrics for paid/free channels.

    This function will plot the following metrics for paid and free channels:
     - average CR for all paid channels
     - average CR for all free channels
     - average ABS for all paid channels
     - average ABS for all free channels
     - average CIR for all paid channels
     - average CIR for all free channels
    :param df: with columns:
     - Paid_Free
     - CR
     - ABS
     - CIR
    :return:
    """
    fig, axs = plt.subplots(1, 3, figsize=(10, 7))
    fig.suptitle('Analysis by Paid/Free Channels')
    fig.text(0.5, 0.04, 'Paid Channel/Free Channel', ha='center')
    axs[0].bar(df['Paid_Free'], df['CR'], width=0.5)
    axs[1].bar(df['Paid_Free'], df['ABS'], width=0.5)
    axs[2].bar(df['Paid_Free'], df['CIR'], width=0.5)

    axs[0].set_ylabel("Avg Conversion Rate per week per channel", fontsize=10)
    for x, y in zip(df['Paid_Free'], df['CR']):
        label = "{:.5f}".format(y)
        axs[0].annotate(label, (x, y), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=7)
        axs[0].tick_params(axis='y', labelsize=9)
        axs[0].tick_params(axis='x', labelsize=9)

    axs[1].set_ylabel("Avg ABS per week per channel", fontsize=10)
    for x, y in zip(df['Paid_Free'], df['ABS']):
        label = "{:.5f}".format(y)
        axs[1].annotate(label, (x, y), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=7)
        axs[1].tick_params(axis='y', labelsize=9)
        axs[1].tick_params(axis='x', labelsize=9)

    axs[2].set_ylabel("Avg Cost to Income Ratio per week per channel", fontsize=10)
    for x, y in zip(df['Paid_Free'], df['CIR']):
        label = "{:.5f}".format(y)
        axs[2].annotate(label, (x, y), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=7)
        axs[2].tick_params(axis='y', labelsize=9)
        axs[2].tick_params(axis='x', labelsize=9)

    plt.subplots_adjust(wspace=0.4, bottom=0.2)

    plt.savefig("plots/analysis_paid_free.png")


def compute_metrics(raw_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Calculate a few metrics for each channel each week.

    This function will calculate the following metrics:
    - CR: conversion rate, which is orders/visits
    - ABS: average basket size, which is revenue/orders
    - CIR: Cost to Income Ratio, which is spend/revenue

    :param raw_df:
    :return:
    """

    # We only read row 2 (inclusive) to row 20 (exclusive) to remove the data description
    data = raw_df.iloc[2:20, :].reset_index(drop=True)

    columns = ['Channel', 'Paid_Free', 'Spend', 'Visits', 'Orders', 'Revenue', 'Week']
    data.columns = columns
    data['Spend'] = data['Spend'].astype('int64')
    data['Visits'] = data['Visits'].str.replace(',', '').astype('int64')
    data['Orders'] = data['Orders'].str.replace(',', '').astype('int64')
    data['Revenue'] = data['Revenue'].str.replace(',', '').astype('int64')

    data['CR'] = data['Orders'] / data['Visits']
    data['ABS'] = data['Revenue'] / data['Orders']
    data['CIR'] = data['Spend'] / data['Revenue']
    data['Channel_Type'] = data['Channel'].apply(lambda x: x[:-2] if len(x) > 2 else x)

    data_week = data.groupby('Week').agg(CR=('CR', 'mean'), ABS=('ABS', 'mean'), CIR=('CIR', 'mean')).reset_index(
        drop=False)
    data_channel_type = data.groupby('Channel_Type').agg(CR=('CR', 'mean'), ABS=('ABS', 'mean'), CIR=('CIR', 'mean')). \
        reset_index(
        drop=False)
    data_paid_free = data.groupby('Paid_Free').agg(CR=('CR', 'mean'), ABS=('ABS', 'mean'),
                                                   CIR=('CIR', 'mean')).reset_index(
        drop=False)

    return data, data_week, data_channel_type, data_paid_free


def main():
    raw_df = pd.read_csv("data/GFG Data Analyst test.csv")

    data, data_week, data_channel_type, data_paid_free = compute_metrics(raw_df)

    plot_data_week(data_week)
    plot_data_paid_free(data_paid_free)
    plot_data_channel_type(data_channel_type)
    plot_revenue_cr_abs(data)

    preform_hypothesis_test(data)


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    main()
