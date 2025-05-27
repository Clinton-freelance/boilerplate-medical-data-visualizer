import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def draw_cat_plot():
    # Load data
    df = pd.read_csv('medical_examination.csv')

    # Add 'overweight' column
    df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25).astype(int)

    # Normalize data
    df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
    df['gluc'] = (df['gluc'] > 1).astype(int)

    # Melt dataframe
    df_cat = pd.melt(df, id_vars=['cardio'],
                     value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])

    # Group and reformat the data
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).size()

    # Draw the catplot
    cat_plot = sns.catplot(data=df_cat, kind='bar',
                           x='variable', y='size', hue='value', col='cardio')
    fig = cat_plot.fig
    fig.savefig('catplot.png')
    return fig


def draw_heat_map():
    # Load data
    df = pd.read_csv('medical_examination.csv')

    # Add 'overweight' column
    df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25).astype(int)

    # Normalize data
    df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
    df['gluc'] = (df['gluc'] > 1).astype(int)

    # Filter data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
                 (df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate correlation matrix
    corr = df_heat.corr()

    # Create mask
    mask = pd.np.triu(pd.np.ones_like(corr, dtype=bool))

    # Set up plot
    fig, ax = plt.subplots(figsize=(12, 10))

    # Draw heatmap
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f",
                center=0, square=True, cbar_kws={'shrink': .5})
    fig.savefig('heatmap.png')
    return fig
