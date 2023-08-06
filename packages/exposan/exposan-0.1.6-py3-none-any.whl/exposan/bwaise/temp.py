#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 08:32:03 2021

@author: Yalin Li
"""

from matplotlib import pyplot as plt

fig = plt.figure(figsize=(4, 3))
fig.add_subplot(1, 2, 1)



#%%

import pandas as pd, seaborn as sns

combineds = table_dct['morris_combined']

mu_star, mu_sigma = (i.copy() for i in combineds.values())

dct = {'mu_star': combineds['mu_star'].copy(),
       'sigma': combineds['sigma'].copy()}
for k, df in dct.items():
    columns = [f'{i[0]}-{i[1]}' for i in df.columns]
    columns[0] = 'parameter'
    df.columns = columns
    df.index = df.parameter
    df = df.drop('parameter', axis=1)
    # df = df.stack(dropna=False).to_frame().reset_index()
    # dct[k] = df.rename(columns={0: k})
    dct[k] = df.stack(dropna=False).to_frame().rename(columns={0: k})

# mu_star, mu_sigma = dct.values()

plot_df = pd.concat(dct.values(), axis=1).reset_index()
plot_df.rename(columns={'level_1': 'metric'}, inplace=True)

g = sns.relplot(
    data=plot_df,
    x="metric", y="parameter", hue="sigma", size="mu_star",
    # palette="vlag",
    hue_norm=(0, 1),
    edgecolor=".7",
    height=10, sizes=(50, 250), size_norm=(-.2, .8),
)

for label in g.ax.get_xticklabels():
    label.set_rotation(90)


#%%
import os, pandas as pd
results_path = '/Users/yalinli_cabbi/OneDrive/Coding/es/exposan/bwaise/results'

origin_dct = dict(mu_star={}, sigma={})
norm_dct = dict(mu_star={}, sigma={})
for model in (modelA, modelB, modelC):
    ID = model.system.ID[-1]

    # inputs = s.define_inputs(model)
    # # Want to use a larger N (maybe 100)
    # morris_samples = s.generate_samples(inputs, kind='Morris', N=N_morris, seed=seed)

    # evaluate(model, morris_samples)

    # # These are the unprocessed data
    # morris_dct = s.morris_analysis(model, inputs, seed=seed,
    #                                nan_policy='fill_mean',
    #                                file=os.path.join(results_path, f'Morris{ID}.xlsx'))

    # table_dct['morris'][ID] = model.table.copy()
    # table_dct['morris_dct'][ID] = morris_dct.copy()

    morris_dct = table_dct['morris_dct'][ID]

    origins = dict(mu_star=[], sigma=[])
    filtereds = dict(mu_star=[], sigma=[])

    for i in model.metrics:
        df = morris_dct[i.name]
        df.sort_values(by=['mu_star'], ascending=False, inplace=True)
        origins['mu_star'].append(df.mu_star)
        origins['sigma'].append(df.sigma)

        df_filtered = df.iloc[0:5] # select the top five
        filtereds['mu_star'].append(df_filtered.mu_star)
        filtereds['sigma'].append(df_filtered.sigma)

    mu_star_origin = pd.concat([df.parameter, *origins['mu_star']], axis=1)
    sigma_origin = pd.concat([df.parameter, *origins['sigma']], axis=1)
    mu_star_filtered = pd.concat(filtereds['mu_star'], axis=1)
    sigma_filtered = pd.concat(filtereds['sigma'], axis=1)

    # Won't be able to divde if having different column names
    sigma_filtered.columns = mu_star_filtered.columns = [i.name for i in model.metrics]

    # Normalize
    sigma_norm = sigma_filtered/mu_star_filtered.max()
    mu_star_norm = mu_star_filtered/mu_star_filtered.max()

    for i in (mu_star_filtered, mu_star_norm, sigma_filtered, sigma_norm):
        i.insert(0, 'parameter', mu_star_origin.parameter)

    columns = ['parameter'] + [i.name for i in model.metrics]
    for df in (mu_star_origin, mu_star_filtered, mu_star_norm,
               sigma_origin, sigma_filtered, sigma_origin):
        df.columns = columns

    origin_dct['mu_star'][f'{model.system.ID}'] = mu_star_origin
    origin_dct['sigma'][f'{model.system.ID}'] = sigma_origin
    norm_dct['mu_star'][f'{model.system.ID}'] = mu_star_norm
    norm_dct['sigma'][f'{model.system.ID}'] = sigma_norm


# Process data

combineds = {}
writer = pd.ExcelWriter(os.path.join(results_path, 'Morris_combined2.xlsx'))

for k in ('mu_star', 'sigma'):
    columns = []
    data = []
    for i in model.metrics:
    # for i in key_metrics:
        for ID, df in norm_dct[k].items():
            df.index = df.parameter
            columns.append(f'{i.name}-{ID}')
            data.append(df[i.name])

    combined = pd.concat(data, axis=1)
    columns_mi = pd.MultiIndex.from_tuples([i.split('-') for i in columns])
    combined.columns = columns_mi
    combined.reset_index(inplace=True)
    combineds[k] = combined

    combined.to_excel(writer, sheet_name=f'{k}_combined')
    for ID, df in origin_dct[k].items():
        df.to_excel(writer, sheet_name=f'{k}_all_sys{ID}')

writer.save()

table_dct['morris_combined'] = combineds
# pickle_path = os.path.join(results_path, 'table_dct.pckl')
# save_pickle(table_dct, pickle_path)


#%%
mu_star_origin_dct = {}
mu_star_norm_dct = {}
for model in (modelA, modelB, modelC):
    ID = model.system.ID[-1]
    # inputs = s.define_inputs(model)
    # # Want to use a larger N (maybe 100)
    # morris_samples = s.generate_samples(inputs, kind='Morris', N=N_morris, seed=seed)

    # evaluate(model, morris_samples)

    # # These are the unprocessed data
    # morris_dct = s.morris_analysis(model, inputs, seed=seed,
    #                                nan_policy='fill_mean',
    #                                file=os.path.join(results_path, f'Morris{ID}.xlsx'))

    # morris_dct =
    # table_dct['morris'][ID] = model.table.copy()
    # table_dct['morris_dct'][ID] = morris_dct.copy()

    morris_dct = table_dct['morris_dct'][ID]
    origin = []
    filtered = []

    for i in model.metrics:
        df = morris_dct[i.name]
        df.sort_values(by=['mu_star'], ascending=False, inplace=True)
        origin.append(df.mu_star)
        df_filtered = df.mu_star.iloc[0:5] # select the top five
        filtered.append(df_filtered)

    mu_star_filtered = pd.concat(filtered, axis=1)
    mu_star_norm = mu_star_filtered/mu_star_filtered.max() # normalize

    mu_star_origin = pd.concat([df.parameter, *origin], axis=1)
    for i in (mu_star_filtered, mu_star_norm):
        i.insert(0, 'parameter', mu_star_origin.parameter)

    mu_star_origin.columns = mu_star_filtered.columns = mu_star_norm.columns = \
        ['parameter'] + [i.name for i in model.metrics]

    mu_star_origin_dct[f'{model.system.ID}'] = mu_star_origin
    mu_star_norm_dct[f'{model.system.ID}'] = mu_star_norm


    columns = []
    data = []
    for i in model.metrics:
        for ID, df in mu_star_norm_dct.items():
            df.index = df.parameter
            columns.append(f'{i.name}-{ID}')
            data.append(df[i.name])

    combined = pd.concat(data, axis=1)
    columns_mi = pd.MultiIndex.from_tuples([i.split('-') for i in columns])
    combined.columns = columns_mi
    combined.reset_index(inplace=True)
    table_dct['morris_combined'] = combined

    writer = pd.ExcelWriter(os.path.join(results_path, 'Morris_mu_star.xlsx'))
    combined.to_excel(writer, sheet_name='Top five')
    for ID, df in mu_star_origin_dct.items():
        df.to_excel(writer, sheet_name=ID)
    writer.save()