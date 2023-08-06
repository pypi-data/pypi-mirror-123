# compare-qrels
Qualitatively compare the qrels results of two IR systems.

## Why use this?
Determining whether one has progressed in IR is often done based on improvement on mean metrics - the mean of certain
metrics across queries - such as MRR, micro-recall or micro-precision. If a new model slightly significantly
outperforms an old model on these mean metrics, it is often concluded that the new model is better. 
Statistical significance is insufficient to prove that one system outperforms another in offline 
evaluation, because the characteristics of your query set may not perfectly reflect queries from "real" users. 
If the new model fails at queries that the old model could handle very well and if those types of queries 
are overrepresented in queries  of "real" users, your system may have significantly outperform in an 
offline setting, but fails to transfer those results into an online setting.
Researchers should take this possibility into account by **qualitatively assessing the strengths and weaknesses** between different methods and models.

Mean metrics can obscure the following characteristics on systems: 

- **Specialisation**: in the figure the models perform well on different types of queries, i.e.  specialisation. Comparing these models
  is difficult or nonsensical, because they could serve different goals/domains/queries. Specialisation can be quickly
  observed when plotting, for instance,
  the ∆recall in a histogram.  If most queries have a high positive or negative ∆recall, then
  the models are specialised on different queries.
  
  ![Specialisation](images/diff.png)
- **Distributed performance**: the figure shows a situation in which model A performs well on all queries whereas 
  model  B  performs  perfect  on  some  queries,  but  fails  at  others.   Concluding  that  model  B  is 
  better than model A could be premature.  When Conversational Passage Ranking (CPR) is being used
  in  a  ConvQA  system  to  fulfil  a  user’s  information  need,  a  few  documents  might  be  enough  to  provide
  an  answer  for  each  query.   Then  it  is  preferred  that  a  Conversational  Passage  Ranking  (CPR)  system
  performs well on a wide range of queries instead of specialising on a few.  An example of such a system is asearch engine like Google.  As a user, it is preferred to have some relevant documents for all your queries.Distributed performance can be quickly observed when plotting, for instance, the recall in a histogramlike in figure 4c.  If most queries have a medium recall score instead of either a high or a low score, themodel performs distributively overall.
  
  ![Distributed performance](images/average.png)
- **Search space overlap**:  the recall scores of two systems hide the information about which documents
are retrieved. This information can be gained by computing the overlap of retrieved documents of two
models. The figure illustrates the case in which the recall scores as the same, but the overlap is different.  In
the left case, the models find roughly the same documents, but model A finds more relevant documents
than model B, i.e.  the results of A are a super set of the results of B. Then it is fair to conclude that
model A is better than model B. However, if the overlap is low as illustrated in the right case, both models
find different relevant documents, i.e.  the models are complementary.  When the goal of a system is total
recall, for instance in legal IR, not one model but both models should be used.

![Overlap](images/overlap.png)

## How to use

See [sample_compare_qrels.py](sample_compare_qrels.py).

## Example output
The example output is the output of comparing two Conversational Passage Retrieval systems.


### Figures
![](output/delta.png)
![](output/delta_metric_hist.png)
![](output/metric_hist.png)
![](output/overlap.png)

### Terminal output

```shell script
Mean scores QuReTec (trained) {'map': 0.15798155213698378, 'recip_rank': 0.4623152325205058, 'recall_1000': 0.5586410184663372}
Mean scores Query Rewriting {'map': 0.18083664899945048, 'recip_rank': 0.47347866813888656, 'recall_1000': 0.611948585919043}

52 easy queries (recall_1000 > 0.8) for both methods:
8 with low overlap (<40.0%), 38 with high overlap (>=60.0%) and 6 with medium overlap (>=40.0% and <60.0%)
      qid  percentage                                              topic  recall_1000_1  recall_1000_2
0    31_1     100.000                             What is throat cancer?          0.933          0.933
4    31_5      87.300                       Can it spread to the throat?          0.931          0.948
11   32_3     100.000  How do they compare with tigers for being dang...          0.990          0.990
20   33_1     100.000          Tell me about the Neverending Story film.          0.870          0.870
21   33_2      28.300                                  What is it about?          1.000          1.000
22   33_3      28.100                               How was it received?          0.812          1.000
24   33_5      34.200                               Was it a book first?          1.000          1.000
28   34_1     100.000             Tell me about the Bronze Age collapse.          0.845          0.845
29   34_2     100.000                       What is the evidence for it?          0.938          0.938
30   34_3     100.000              What are some of the possible causes?          0.900          0.900
35   34_8      56.000                             What empires survived?          0.952          1.000
36   37_1     100.000                  What was the Stanford Experiment?          0.966          0.966
37   37_2     100.000                                  What did it show?          0.955          0.955
39   37_4     100.000                                    Was it ethical?          1.000          1.000
41   37_6      80.100           What happened in the Milgram experiment?          0.986          1.000
42   37_7     100.000                              Why was it important?          1.000          1.000
43   37_8      61.900  What were the similarities and differences bet...          1.000          0.966
46   40_3      71.200        What technological developments enabled it?          0.889          0.806
50   40_7     100.000                        What makes a song pop punk?          0.848          0.848
51   40_8      37.400         What is the difference between it and emo?          1.000          1.000
54   49_3      55.900         What is its relationship with Blockbuster?          0.905          0.952
55   49_4     100.000  When did Netflix shift from DVDs to a streamin...          0.913          0.913
57   49_6     100.000         How does it compare to Amazon Prime Video?          0.983          0.983
59   49_8     100.000          How has it changed the way TV is watched?          0.802          0.802
60   50_1     100.000           What was the first artificial satellite?          0.974          0.974
66   50_7     100.000                                 What are Cubesats?          1.000          1.000
70   54_3     100.000  Why is the National Air and Space Museum impor...          0.920          0.920
71   54_4     100.000                            Is the Spy Museum free?          1.000          1.000
83   56_7      45.900  Compare and contrast microevolution and macroe...          0.981          0.943
92   58_8      85.700                     How is it used in mobile apps?          1.000          0.929
93   59_1     100.000       Which weekend sports have the most injuries?          0.914          0.914
95   59_3      47.900                                   What is the ACL?          0.872          0.872
96   59_4     100.000                          What is an injury for it?          0.986          0.986
99   59_7      34.300                           What is arnica used for?          1.000          1.000
104  61_4     100.000  What is the relationship of Spider-Man to the ...          0.907          0.907
109  67_1     100.000                                  Why is blood red?          0.930          0.930
131  69_1     100.000                    How do you sleep after jet lag?          1.000          1.000
141  75_1     100.000      Why do turkey and Turkey share the same name?          0.941          0.941
143  75_3      33.800      What was their importance in native cultures?          0.895          0.842
144  75_4      63.600               When and how were they domesticated?          0.861          0.917
145  75_5      64.500                                      Can they fly?          0.960          0.960
146  75_6      22.800  Why did Ben Franklin want it to be the nationa...          1.000          1.000
147  77_1     100.000       What's the difference between soup and stew?          0.974          0.974
151  77_5     100.000                             How is cassoulet made?          1.000          1.000
154  77_8      17.200                             Tell about Bigos stew.          1.000          0.906
155  78_1     100.000                             What is the keto diet?          0.860          0.860
157  78_3      54.500                                   What is ketosis?          0.870          0.981
161  78_7     100.000                      What is intermittent fasting?          1.000          1.000
164  79_2      42.700    What is the main contribution of Auguste Comte?          0.897          0.888
165  79_3     100.000              What is the role of positivism in it?          0.830          0.830
166  79_4     100.000                 What is Herbert Spencer known for?          0.949          0.949
171  79_9     100.000       What are modern examples of conflict theory?          0.900          0.900

27 hard queries (recall_1000 < 0.2) for both methods:
10 with low overlap (<40.0%), 14 with high overlap (>=60.0%) and 3 with medium overlap (>=40.0% and <60.0%)
       qid  percentage                                              topic  recall_1000_1  recall_1000_2
1     31_2       0.000                                   Is it treatable?          0.039          0.000
10    32_2     100.000                                  What do they eat?          0.000          0.000
12    32_4     100.000      Are sharks endangered?  If so, which species?          0.000          0.000
13    32_5     100.000                   Tell me more about tiger sharks.          0.093          0.093
15    32_7     100.000                    What's the biggest ever caught?          0.125          0.125
18   32_10      30.500                        What are their adaptations?          0.188          0.125
47    40_4     100.000  When and why did people start taking pop serio...          0.061          0.061
53    49_2       0.000                        How did it originally work?          0.000          0.000
77    56_1     100.000             What is Darwin’s theory in a nutshell?          0.009          0.009
78    56_2       7.900                              How was it developed?          0.014          0.072
97    59_5      86.600                     Tell me about the RICE method.          0.125          0.167
102   61_2       0.000              Tell me about their first appearance.          0.000          0.000
110   67_2     100.000            What foods contain high levels of iron?          0.000          0.000
111   67_3      17.300                          What improves absorption?          0.000          0.000
113   67_5      61.000                              How are they created?          0.119          0.148
114   67_6      40.900                         How is oxygen transported?          0.038          0.013
117   67_9     100.000                                    Can it go away?          0.114          0.114
118  67_10      92.000                      What are its possible causes?          0.000          0.000
119  67_11      50.700                                 How is it treated?          0.094          0.075
121   68_2       7.500  What is the history of tagliatelle al ragu bol...          0.000          0.118
123   68_4       0.900         Tell me about cooking schools and classes.          0.000          0.068
124   68_5      66.100             What are famous foods from the region?          0.043          0.022
125   68_6     100.000  Describe the traditional process for making ba...          0.000          0.000
126   68_7       1.600           What is mortadella and where is it from?          0.000          0.116
127   68_8      91.500                What’s the difference with Bologna?          0.000          0.000
129  68_10       5.700       What is done with the whey after production?          0.000          0.043
150   77_4      49.900                   What are popular ones in France?          0.000          0.042

23 queries where Query Rewriting outperforms QuReTec (trained) (Δrecall_1000 > 0.3):
17 with low overlap (<40.0%), 3 with high overlap (>=60.0%) and 3 with medium overlap (>=40.0% and <60.0%)
       qid  percentage                                              topic  recall_1000_1  recall_1000_2
5     31_6      22.600                         What causes throat cancer?          0.492          0.889
6     31_7      21.300                      What is the first sign of it?          0.586          0.948
8     31_9      34.600           What's the difference in their symptoms?          0.636          1.000
26    33_7      32.700                          What are the main themes?          0.556          1.000
34    34_7      63.600                  What about environmental factors?          0.281          0.969
45    40_2      22.500                      What are its characteristics?          0.222          0.722
56    49_5      54.800                    What are its other competitors?          0.536          0.857
73    54_6      15.600  What is the best time to visit the reflecting ...          0.250          1.000
74    54_7       0.600                        Are there any famous foods?          0.000          0.333
76    54_9      47.300                         Tell me about its history.          0.000          0.444
100   59_8      21.200                What are some ways to avoid injury?          0.411          0.821
116   67_8       1.000                             What are the symptoms?          0.000          0.319
132   69_2      12.700                             How about for anxiety?          0.000          0.897
134   69_4       1.700                             How was it discovered?          0.000          0.542
137   69_7      17.400                         What are the side effects?          0.000          0.800
138   69_8      52.500      Why does it require a prescription in the UK?          0.000          0.636
140  69_10      60.600             Is it effective for treating insomnia?          0.062          0.750
153   77_7      92.900     How is it similar or different from cassoulet?          0.343          0.886
159   78_5      10.200                       What do they have in common?          0.000          0.625
160   78_6       0.000                            How are they different?          0.000          0.750
162   78_8      37.300                         How is it related to keto?          0.000          1.000
167   79_5      13.500                  How is his work related to Comte?          0.268          1.000
169   79_7       5.900                        What is its main criticism?          0.043          0.565

11 queries where QuReTec (trained) outperforms Query Rewriting (Δrecall_1000 > 0.3):
9 with low overlap (<40.0%), 0 with high overlap (>=60.0%) and 2 with medium overlap (>=40.0% and <60.0%)
      qid  percentage                                            topic  recall_1000_1  recall_1000_2
3    31_4      26.300                          What are its symptoms?           0.673          0.204
17   32_9       3.400                             Tell me about makos.          1.000          0.000
33   34_6      23.700  What other factors led to a breakdown of trade?          0.533          0.100
58   49_7      11.100       Describe it’s subscriber growth over time.          0.745          0.314
67   50_8       0.300                       What are their advantages?          1.000          0.000
98   59_6      51.100                  Is there disagreement about it?          1.000          0.000
108  61_8       0.400                   Who are the important members?          0.679          0.054
122  68_3       1.400                  What are its common variations?          0.750          0.111
142  75_2      57.800                          Where are turkeys from?          0.846          0.462
149  77_3       2.500                               How about goulash?          1.000          0.538
156  78_2       0.000                   Why was it original developed?          0.438          0.000

2 complementary queries:
1 with low overlap (<40.0%), 0 with high overlap (>=60.0%) and 1 with medium overlap (>=40.0% and <60.0%)
     qid  percentage                                              topic  recall_1000_1  recall_1000_2  recall_1000_combined
48  40_5      22.000  How has it been integrated into music education?           0.278          0.333                 0.389
49  40_6      58.500        Describe some of the influential pop bands.          0.716          0.679                 0.741
```