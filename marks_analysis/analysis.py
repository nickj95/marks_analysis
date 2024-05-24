import pandas as pd
from scipy.stats import ks_2samp
import seaborn as sns
import matplotlib.pyplot as plt
import os


class MarkBreakdown:
    def __init__(self, data, by, mark, board=False):
        self._by = by
        self._mark = mark
        self._board = board
        self.data = data.loc[data['Exam Board'] == board] if board else data
        self.df = self.get_breakdown_table(self.data, by, mark, board)
        self.__print__ = print(self.df.to_string())

    def get_breakdown_table(self, data, by_, mark_, board):
        breakdown = data.groupby([by_])[mark_].apply(get_stats)
        breakdown.index = breakdown.index.droplevel(1)
        breakdown = pd.concat([
            get_stats(
                data.loc[
                    data['Exam Board'] == board if board else [True] * len(data),
                    'Agreed Mark'].rename('Total - Agreed')), breakdown])  # Hardcoded

        markers = data[by_].unique().tolist()
        markers.sort()

        breakdown = pd.concat([
            breakdown,
            pd.Series(
                name='KS P',
                index=markers,
                data=["{:.3f}".format(get_ks_pval(data, by_, marker, mark_)) for marker in markers])
        ], axis=1)

        breakdown['P**'] = breakdown['KS P'].astype(float).apply(
            lambda x: '**' if x < 0.01 else '*' if x < 0.05 else '`' if x < 0.1 else '')
        return breakdown

    def generate_figure(self, counts=False):
        # Preparing the figure data
        plot_data = self.data.copy()

        p_dict = self.df['KS P'].astype(float).to_dict()
        plot_data['p'] = plot_data[self._by].apply(
            lambda x: p_dict[x]).apply(
            lambda x: '<0.01' if x < 0.01 else '<0.05' if x < 0.05 else '<0.1' if x < 0.1 else '>=0.1')

        marker_order = self.df.iloc[1:, ]['Mean'].astype(float).sort_values().index.values
        hue_order = ['<0.01', '<0.05', '<0.1', '>=0.1']
        # You need to fix the variable names
        count_dict = self.data.groupby([self._by])[self._mark].count().to_dict()

        # Figure
        g = sns.catplot(
            data=plot_data,
            x=self._mark,
            hue='p',
            y=self._by,
            kind='box',
            dodge=False,
            height=10,
            aspect=1.25,
            order=marker_order,
            hue_order=hue_order,
            palette='RdBu',
            legend=False)

        if counts:
            for i, item in enumerate(marker_order[::1]):
                g.ax.text(x=82, y=i, s=f'N={count_dict[item]}', va='center')

        g.fig.suptitle(
            f"Marks Distribution by {self._by} for {self._board if self._board else ''} 2022, whiskers 1.5xIQR", y=1.01)
        g.ax.yaxis.tick_right()
        g.ax.yaxis.set_label_position('right')
        sns.despine(g.fig, left=True, right=False)
        g.ax.set_xlim(40, 85)
        g.ax.xaxis.set_ticks(range(40, 90, 10))
        g.ax.legend(loc='center left', title='p KS 2samp')
        g.ax.grid(which='both', axis='both', ls='-', color='k', alpha=0.1)
        g.fig.savefig(f"figures/marks_distribution_{self._by}_{self._mark}_{self._board if self._board else 'TOTAL'}.png",
                      bbox_inches='tight')

    def save_breakdown(self):
        filename_base = f"marks_by_{self._by}_{self._mark}_{self._board if self._board else 'TOTAL'}"
        self.df.to_csv(f"files/{filename_base}.csv")
        self.df.to_html(f"files/{filename_base}.html")
        self.df.to_latex(f"files/{filename_base}.tex")


def get_ks_pval(data, col, val, mark):
    samp_X = data.loc[data[col] == val, mark]
    pop_X = data.loc[data[col] != val, mark]
    p_val = ks_2samp(samp_X, pop_X)[1]
    return p_val


def get_stats(s):
    s = s.aggregate({
        "Cands": len,
        ">=70": lambda x: "{:.3g}%".format(100 * (sum(x >= 70) / len(x))),
        ">=60": lambda x: "{:.3g}%".format(100 * (sum((x >= 60) & (x < 70)) / len(x))),
        ">=50": lambda x: "{:.3g}%".format(100 * (sum((x >= 50) & (x < 60)) / len(x))),
        ">=40": lambda x: "{:.3g}%".format(100 * (sum((x >= 40) & (x < 50)) / len(x))),
        ">=30": lambda x: "{:.3g}%".format(100 * (sum((x >= 30) & (x < 40)) / len(x))),
        "<30": lambda x: "{:.3g}%".format(100 * (sum((x < 30)) / len(x))),
        "Q1": lambda x: "{:.3g}".format(pd.Series.quantile(x, 0.25)),
        "Median": lambda x: "{:.3g}".format(pd.Series.median(x)),
        "Q3": lambda x: "{:.3g}".format(pd.Series.quantile(x, 0.75)),
        "Mean": lambda x: "{:.3g}".format(pd.Series.mean(x)),
        "St. Dev.": lambda x: "{:.3g}".format(pd.Series.std(x)),
        "Max": lambda x: "{:.3g}".format(pd.Series.max(x)),
        "Min": lambda x: "{:.3g}".format(pd.Series.min(x))
    })
    df = pd.DataFrame(s).T
    return df


def analyze_paper_examiner_distribution(data, mark='Initial Mark'):
    row_order = data.groupby(['Paper'])['Examiner'].count().sort_values(ascending=False).index.values

    g = sns.catplot(
        data=data,
        x=mark,
        col='Paper',
        y='Examiner',
        kind='swarm',
        col_wrap=3,
        sharey=False,
        aspect=1.25,
        col_order=row_order,
        palette='tab10'
    )
    g.fig.suptitle('Marks Distribution by Paper and Examiner 2022', y=1.01)
    plt.savefig("figures/Marks_distribution_by_Paper_and_Examiner.png")
    plt.show()


# Some utilities I've had to use in the past are included here.
# You may use call them inside analyze_all_examiners if needed.


def get_other_mark(row, df_marker):
    other = df_marker.loc[
        (df_marker['CandNo'] == row['CandNo']) &
        (df_marker['Paper'] == row['Paper']) &
        (df_marker['Examiner'] != row['Examiner']), :]
    return other['Initial Mark'].values[0] if not other.empty else None


def plot_agreed_marks(df_marker):
    if 'Agreed Mark' in df_marker.columns:
        melted_data = df_marker.melt(value_vars=['Agreed Mark'], var_name='Mark Type', value_name='Mark')
        g = sns.displot(
            data=melted_data,
            x='Mark',
            hue='Mark Type',
            kind='kde',
            fill=True,
            rug=True
        ).set(title="Aggregate: Agreed Mark Distribution")
        plt.savefig("figures/Aggregate_Agreed_Marks.png")
        plt.show()


def check_agreed_marks(df_marker):
    df_agreed_mark = (df_marker.groupby(['CandNo', 'Paper'])
                      .nunique()
                      .gt(1)
                      .replace({True: 'Differ', False: 'Agree'})
                      .reset_index()
                      )
    return df_agreed_mark["Agreed Mark"].value_counts()


def plot_mark_differences(df_marker):
    if 'Agreed Mark' in df_marker.columns:
        df_difference = df_marker.copy()
        df_difference["Mark Difference Absolute"] = abs(df_marker["Initial Mark"] - df_marker["Agreed Mark"])
        df_difference["Mark Difference"] = df_marker["Initial Mark"] - df_marker["Agreed Mark"]
        sns.displot(df_difference, x="Mark Difference")
        plt.savefig("figures/Difference_between_Initial_and_Agreed_Marks.png")
        plt.show()
        return df_difference
    return None


def plot_absolute_mark_differences(df_difference):
    if df_difference is not None:
        df = pd.DataFrame(df_difference.groupby('Examiner')["Mark Difference Absolute"].sum().sort_values(ascending=False))
        df["Examiner"] = df.index
        plt.figure(num=None, figsize=(24, 22), dpi=90, facecolor='w', edgecolor='r')
        sns.barplot(
            data=df,
            y="Examiner",
            x="Mark Difference Absolute",
            orient="h",
            dodge=False,
            palette='RdBu',
        )
        plt.savefig("figures/Absolute_Mark_Difference.png")
        plt.show()
        return df
    return None

# Analyze


def analyze_data(data, by, mark, boards=[False]):
    # Ensure directories exist before analysis
    os.makedirs("files", exist_ok=True)
    os.makedirs("figures", exist_ok=True)

    for board in boards:
        mb = MarkBreakdown(data, by, mark, board=board)
        mb.generate_figure(counts=True)
        mb.save_breakdown()


# There is probably a more efficient way to do this like by calling an index or a random marker.
# However, this does the job and is more dynamic.
# Call the utility functions within this function to add more versatility.


def analyze_all_examiners(df_marker):
    # Ensure directories exist before analysis
    os.makedirs("files", exist_ok=True)
    os.makedirs("figures", exist_ok=True)

    # Plot agreed marks aggregated
    plot_agreed_marks(df_marker)

    # Check if agreed marks differ
    if 'Agreed Mark' in df_marker.columns:
        agreed_mark_counts = check_agreed_marks(df_marker)
        print(agreed_mark_counts)

        # Plot mark differences and get the updated DataFrame
        df_difference = plot_mark_differences(df_marker)

        # Plot absolute mark differences using the updated DataFrame
        df_absolute_diff = plot_absolute_mark_differences(df_difference)
        print(df_absolute_diff)

    # Save the processed marker data to a CSV file
    df_absolute_diff.to_csv("files/Marks by Examiner (Initial vs Agreed Difference).csv")