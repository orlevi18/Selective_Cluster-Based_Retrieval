# Selective Cluster-Based Document Retrieval
CIKM '16 Proceedings of the 25th ACM International Conference on Information and Knowledge Management

Or Levi	      Technion - Israel Institute of Technology, Haifa, Israel
Fiana Raiber	Technion - Israel Institute of Technology, Haifa, Israel
Oren Kurland	Technion - Israel Institute of Technology, Haifa, Israel
Ido Guy       Yahoo Research & Ben-Gurion University of the Negev, Haifa, Israel

# Abstract
We address the long standing challenge of selective cluster-based retrieval; namely, deciding on a per-query basis whether to apply cluster-based document retrieval or standard document retrieval. To address this classification task, we propose a few sets of features based on those utilized by the cluster-based ranker, query-performance predictors, and properties of the clustering structure. Empirical evaluation shows that our method outperforms state-of-the-art retrieval approaches, including cluster-based, query expansion, and term proximity methods.

# Implementation
We use Indri for Information Retrieval in the Language Modeling framework; Python for feature engineering, feature selection and result processing;  and Weka machine learning toolkit for SVM regression
