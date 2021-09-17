import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import os
from app import app
from matplotlib.ticker import MaxNLocator

def coerce_pattern(value_hist):
    try:
        value_hist.index = value_hist.index.astype('int')
        if value_hist.index.max() <= 10:
            value_hist = value_hist.sort_index()
    except:
        pass 
    return value_hist

def image_to_utf2(col):
    figfile = BytesIO()
    
    values_histogram = col.value_counts()
    values_histogram = coerce_pattern(values_histogram)

    if len(values_histogram) > 20:
        n_truncated = values_histogram.shape[0] - 20
        values_histogram = values_histogram.iloc[:10]\
                .append(pd.Series([0], index=['']))\
                .append(values_histogram.iloc[-10:])
        
    if len(values_histogram) > 0:
        ax = plt.figure(figsize=(5, 5)).gca()
        _ = values_histogram.plot.barh(figsize=(5, 5), color="#2c457a")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        if len(values_histogram) > 20:
            plt.text(0.05, 9.75, f'({n_truncated} truncated {col.name} values....)', style='italic')
        
        # plt.xticks(rotation = 0)
        # plt.ylabel(col.name)
        # plt.xlabel("counts")        

    else:
        plt.bar([], [])
        plt.xticks([])
        plt.yticks([])
        
    plt.ylabel(col.name)
    plt.xlabel('counts')
    plt.tight_layout()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    figdata_png = base64.b64encode(figfile.getvalue())
    img_str = str(figdata_png, "utf-8")

    plt.close()
    return img_str

def generate_statistics(filename):
    if filename.endswith('.csv'):
        df = pd.read_csv(os.path.join(app.config['UPLOAD_PATH'], filename), dtype=str) # read POST-ed file
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        df = pd.read_excel(os.path.join(app.config['UPLOAD_PATH'], filename), dtype=str) # read POST-ed file
    else:
        raise ValueError('File is not supported')

    column_stats = []
    for col in df.columns:
        column_stats.append({
            'col_name': df[col].name,
            'n_nulls': df[col].isna().sum(),
            'n_uniques': df[col].nunique(),
            'b64_graph': image_to_utf2(df[col])
        })

    return column_stats