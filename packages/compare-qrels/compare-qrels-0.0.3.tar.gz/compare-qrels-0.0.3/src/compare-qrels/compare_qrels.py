from collections import defaultdict
from typing import List, Optional
from dataclasses import dataclass, field
import json, pandas, pytrec_eval, logging, os
import matplotlib.pyplot as plt
from pathlib import Path

__all__ = ['CompareData', 'compute_qrels_df']

logger = logging.getLogger(__name__)
DELTA = u'Δ'

# Make sure it prints the entire dataframe contents
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', 1000)

one = lambda x: f"{x}_1"
two = lambda x: f"{x}_2"
combined = lambda x: f"{x}_combined"


@dataclass
class CompareData:
    run_a: dict
    run_b: dict
    metric_labels: list
    data: pandas.DataFrame
    name_run_a: str = field(default_factory=lambda:"Run A")
    name_run_b: str = field(default_factory=lambda:"Run B")
    bins: List = field(default_factory=lambda:[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

    def print_overlap_hist(self, save_file: Optional[str] = "output/overlap.png"):
        percentages = []
        n_queries = len(self.run_a.keys())
        for qid in self.run_a.keys():
            set_a = set(self.run_a[qid].keys())
            set_b = set(self.run_b[qid].keys())
            overlap = list(set_a & set_b)
            percentages.append(len(overlap) / len(set_a) * 100)

        plt.title(f"Results overlap (n_queries={n_queries})")
        plt.xlabel("% Percentage of overlap")
        plt.ylabel("# Queries")
        plt.hist(percentages, bins=self.bins, histtype='bar', rwidth=0.8)
        plt.xticks(self.bins)
        if save_file:
            plt.savefig(save_file)
        plt.show()

    def __check_path(self, path: str):
        if os.path.isfile(path):
            os.remove(path)
            logging.info(f"Removed file {path}")
        dir = Path(path).parent.name

        if dir:
            if not os.path.exists(dir):
                logging.info(f"Created dir {dir}")
            os.makedirs(dir, exist_ok=True)

    def __validate_metric(self, metric: str):
        if metric not in self.metric_labels:
            raise KeyError(f'The metrics {metric} is invalid. Please choose one of the metrics: {self.metric_labels}')

    def print_analysis(self,
                       metric: str,
                       limit_hard: float = 0.2,
                       limit_outperforms: float = 0.3,
                       limit_easy: float = 0.8,
                       limit_low_overlap: float = 0.4,
                       limit_high_overlap: float = 0.6,
                       ):
        """

        :param metric:
        :param limit_hard:
        :param limit_outperforms:
        :param limit_easy:
        :return:
        """
        d = f"{DELTA}{metric}"
        self.__validate_metric(metric)
        hard_queries = self.data[(self.data[one(metric)] < limit_hard) & (self.data[two(metric)] < limit_hard)]
        easy_queries = self.data[(self.data[one(metric)] > limit_easy) & (self.data[two(metric)] > limit_easy)]
        overlap_queries = self.data[
            (self.data[combined(metric)] > self.data[one(metric)])
            & (self.data[combined(metric)] > self.data[two(metric)])
        ]

        run_b_outperforms = self.data[(self.data[d] > limit_outperforms)]
        run_a_outperforms = self.data[(self.data[d] < -1*limit_outperforms)]

        both = ['qid', 'percentage', 'topic', one(metric), two(metric)]
        print(f"{len(easy_queries)} easy queries ({metric} > {limit_easy}) for both methods:\n"
              f"{self.__low_high_overlap(easy_queries, limit_low_overlap, limit_high_overlap)}\n"
              f"{easy_queries[both]}\n")
        print(f"{len(hard_queries)} hard queries ({metric} < {limit_hard}) for both methods:\n"
              f"{self.__low_high_overlap(hard_queries, limit_low_overlap, limit_high_overlap)}\n"
              f"{hard_queries[both]}\n")
        print(f"{len(run_b_outperforms)} queries where {self.name_run_b} outperforms {self.name_run_a} ({DELTA}{metric} > {limit_outperforms}):\n"
              f"{self.__low_high_overlap(run_b_outperforms, limit_low_overlap, limit_high_overlap)}\n"
              f"{run_b_outperforms[both]}\n")
        print(f"{len(run_a_outperforms)} queries where {self.name_run_a} outperforms {self.name_run_b} ({DELTA}{metric} > {limit_outperforms}):\n"
              f"{self.__low_high_overlap(run_a_outperforms, limit_low_overlap, limit_high_overlap)}\n"
              f"{run_a_outperforms[both]}\n")
        print(f"{len(overlap_queries)} complementary queries:\n"
              f"{self.__low_high_overlap(overlap_queries, limit_low_overlap, limit_high_overlap)}\n"
              f"{overlap_queries[both + [combined(metric)]]}\n")

    def __low_high_overlap(self, data, limit_low_overlap: float, limit_high_overlap: float):
        l = limit_low_overlap * 100
        h = limit_high_overlap * 100

        low = data[data['percentage'] < l]
        high = data[data['percentage'] >= h]
        between = data[(data['percentage'] < h) & (data['percentage'] >= l)]

        return f"{len(low)} with low overlap (<{l}%), " \
               f"{len(high)} with high overlap (>={h}%) and " \
               f"{len(between)} with medium overlap (>={l}% and <{h}%)"

    def print_table(self, save_file: Optional[str] = "output/table.html"):
        self.__check_path(save_file)
        html_file = open(save_file, "w")
        html_file.write(self.data.style.to_html(encoding="UTF-8"))
        html_file.close()

    def print_delta_metric_hist(self, metric: str, save_file: Optional[str] ="output/delta_metric_hist.png"):
        self.__validate_metric(metric)
        from pylab import show, savefig, xlim, \
            axes, xlabel, title, ylabel

        bin_values = []
        larger_than_zero = [-1 * v for v in self.bins][1:]
        larger_than_zero.reverse()
        double_bins = larger_than_zero + self.bins
        double_bins = [v/100 for v in double_bins]
        for b in range(len(double_bins) - 1):
            is_last_bound = double_bins[b + 1] == double_bins[-1]
            right_bound = double_bins[b + 1] + 1 if is_last_bound else double_bins[b + 1]
            l = double_bins[b]
            r = right_bound
            bin_df1 = self.data[(self.data[f"{DELTA}{metric}"] >= l) & (self.data[f"{DELTA}{metric}"] < r)]
            bin_values += bin_df1[f"{DELTA}{metric}"].tolist()

        # set axes limits and labels
        title(f"Delta {metric}: {self.name_run_a} vs {self.name_run_b}")
        ylabel(f"# queries")
        xlabel("Score")
        xlim(-1, 1)
        plt.hist(bin_values, bins=double_bins, rwidth=0.9)
        # hB.set_visible(False)
        # hR.set_visible(False)

        if save_file:
            self.__check_path(save_file)
            savefig(save_file)

        show()

    def print_metric_hist(self, metric: str, save_file: Optional[str] = "output/metric_hist.png"):
        self.__validate_metric(metric)
        from pylab import show, savefig, xlim, \
            axes, xlabel, title, ylabel

        bin_values = [
            [],
            []
        ]
        for b in range(len(self.bins) - 1):
            is_last_bound = self.bins[b + 1] == self.bins[-1]
            right_bound = self.bins[b + 1] + 1 if is_last_bound else self.bins[b + 1]
            l = self.bins[b] / 100
            r = right_bound / 100
            bin_df1 = self.data[(self.data[one(metric)] >= l) & (self.data[one(metric)] < r)]
            bin_df2 = self.data[(self.data[two(metric)] >= l) & (self.data[two(metric)] < r)]
            bin_values[0] += bin_df1[one(metric)].tolist()
            bin_values[1] += bin_df2[two(metric)].tolist()

        ax = axes()
        n_bins = len(bin_values)

        # set axes limits and labels
        title(f"{metric} ")
        ylabel(f"# queries")
        xlabel("Recall sore")
        xlim(0, 1)
        plt.hist(bin_values, rwidth=0.9)
        plt.legend((self.name_run_a, self.name_run_b))
        # hB.set_visible(False)
        # hR.set_visible(False)

        if save_file:
            self.__check_path(save_file)
            savefig(save_file)

        show()

    def print_delta_metric_box_plots(self, metric: str, save_file: Optional[str] = 'output/delta.png'):
        self.__validate_metric(metric)
        metric = DELTA + metric
        from pylab import plot, show, savefig, xlim, figure, \
            ylim, legend, boxplot, setp, axes, xlabel, title, ylabel

        # function for setting the colors of the box plots pairs
        def setBoxColors(bp):
            setp(bp['boxes'][0], color='blue')
            setp(bp['caps'][0], color='blue')
            setp(bp['caps'][1], color='blue')
            setp(bp['whiskers'][0], color='blue')
            setp(bp['whiskers'][1], color='blue')
            # setp(bp['fliers'][0], color='blue')
            # setp(bp['fliers'][1], color='blue')
            setp(bp['medians'][0], color='blue')

        bin_values = []
        for b in range(len(self.bins) - 1):
            is_last_bound = self.bins[b+1] == self.bins[-1]
            # Include the edge for the last bin as well
            right_bound = self.bins[b+1] + 1 if is_last_bound else self.bins[b+1]
            bin_df = self.data[(self.data['percentage'] >= self.bins[b]) & (self.data['percentage'] < right_bound)]
            bin_values.append([
                bin_df[f"{metric}"].tolist(),
            ])

        fig = figure()
        ax = axes()
        n_bins = len(bin_values)
        xticks, xticklabels = [], []
        for i in range(n_bins):
            l, r = (i*3)+1, (i*3)+2
            middle = (r + l) / 2
            xticks.append(middle)
            xticklabels.append(f"{self.bins[i]}-{self.bins[i+1]}")
            bp = boxplot(bin_values[i],
                         positions=[middle],
                         widths=1.0,
                         showfliers=False, showcaps=True
                         )
            setBoxColors(bp)

        # set axes limits and labels
        title(f"{metric} ")
        ylabel(f"{metric} score")
        xlabel("% Percentage of overlap")
        xlim(0, n_bins * 3)
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels)
        if save_file:
            self.__check_path(save_file)
            savefig(save_file)
        show()


def compute_qrels_df(qrels: dict, topics: dict, file_a: str, file_b: str, metrics, name_a: str, name_b: str):
    with open(file_a, "r", encoding='utf-8') as f1:
        run_a = json.load(f1)
    with open(file_b, "r", encoding='utf-8') as f2:
        run_b = json.load(f2)

    if len(run_a.keys()) != len(run_b.keys()):
        raise ValueError(f'Both lists should have the same length: {len(run_a.keys())} vs  {len(run_b.keys())} ')

    qrels_keys = list(qrels.keys())
    missing_keys_in_qrels_a = [k for k in run_a.keys() if k not in qrels_keys]
    if len(missing_keys_in_qrels_a) > 0:
        logger.warning(f"Keys in run_a that are missing qrels: {missing_keys_in_qrels_a}")

    evaluator = pytrec_eval.RelevanceEvaluator(qrels, metrics)

    # The run should have the format {query_id: {doc_id: rank_score}}
    run_combined = defaultdict(str)
    for qid in run_a.keys():
        run_combined[qid] = {**run_a[qid], ** run_b[qid]}

    # The run should have the format {query_id: {doc_id: rank_score}}
    res_combined = evaluator.evaluate(run_combined)
    res_a = evaluator.evaluate(run_a)
    res_b = evaluator.evaluate(run_b)

    labels = ['Query ID', 'Percentage']
    qids = list(res_a.keys())[0]
    metric_labels = res_a[qids].keys()
    for metric_label in metric_labels:
        labels += [one(metric_label), two(metric_label), f"{DELTA}{metric_label}"]

    cols_per_qid = {}
    for qid in run_a.keys():
        if qid in missing_keys_in_qrels_a:
            continue
        set_a = set(run_a[qid].keys())
        set_b = set(run_b[qid].keys())
        overlap = list(set_a & set_b)
        percentage = len(overlap) / len(set_a) * 100

        cols_per_qid[qid] = {
            'qid': qid,
            'topic': topics[qid],
            'percentage': percentage,
        }
        for metric_label in metric_labels:
            cols_per_qid[qid][one(metric_label)] = res_a[qid][metric_label]
            cols_per_qid[qid][two(metric_label)] = res_b[qid][metric_label]
            cols_per_qid[qid][combined(metric_label)] = res_combined[qid][metric_label]
            cols_per_qid[qid][f"{DELTA}{metric_label}"] = res_b[qid][metric_label] - res_a[qid][metric_label]
    pandas.options.display.float_format = "{:,.3f}".format
    df = pandas.DataFrame.from_dict(cols_per_qid.values())

    sum_scores_a = defaultdict(float)
    for qid in res_a.keys():
        for metric in res_a[qid].keys():
            sum_scores_a[metric] += res_a[qid][metric]
    N = len(res_a.keys())
    print(f"Mean scores {name_a}", {k: v / N for k, v in sum_scores_a.items()})

    sum_scores_b = defaultdict(float)
    for qid in res_b.keys():
        for metric in res_b[qid].keys():
            sum_scores_b[metric] += res_b[qid][metric]
    print(f"Mean scores {name_b}", {k: v / N for k, v in sum_scores_b.items()})

    return CompareData(data=df,
                       run_a=run_a,
                       run_b=run_b,
                       name_run_a=name_a,
                       name_run_b=name_b,
                       metric_labels=metric_labels)
