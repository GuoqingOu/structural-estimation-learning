# 结构模型估计文献索引

先读研究框架和识别，再读离散选择方法，最后进入具体应用。以下提供原始入口与阅读问题；不要求第一轮通读全部推导。

## Reiss 与 Wolak 2007

Peter C. Reiss and Frank A. Wolak. **Structural Econometric Modeling: Rationales and Examples from Industrial Organization.** *Handbook of Econometrics*, Volume 6A, Chapter 64, 4277–4415.

[Stanford 作者机构全文入口](https://web.stanford.edu/group/fwolak/cgi-bin/sites/default/files/files/Structural%20Econometric%20Modeling_Rationales%20and%20Examples%20From%20Industrial%20Organization_Reiss,%20Wolak.pdf)

建议先读第 2 节和第 4 节。记录经济假设、统计假设和不可观测因素分别承担什么作用。它适合建立研究框架，而不只是选择某个估计算法。

## Lewbel 2019

Arthur Lewbel. **The Identification Zoo: Meanings of Identification in Econometrics.** *Journal of Economic Literature*, 57(4), 835–903.

[AEA 期刊页面与 DOI](https://www.aeaweb.org/articles?id=10.1257/jel.20181361)

先区分点识别、集合识别、局部识别与规范化，再根据研究需要深入其他定义。阅读时追问：作者讨论的是哪个目标量，哪些信息被视为已知？全文获取取决于页面提供的访问方式。

## Train 2009

Kenneth E. Train. **Discrete Choice Methods with Simulation.** Second edition. Cambridge University Press.

[作者在 Berkeley 提供的教材页面](https://eml.berkeley.edu/books/choice2.html)

基础路线：第 2 章的选择模型性质与规范化、第 3 章的 Logit。随后阅读第 8 章数值最大化、第 10 章模拟辅助估计、第 13 章内生性；贝叶斯方法可见第 12 章。作者页面提供个人学习用电子章节，本仓库只链接，不再分发。

## Berry、Levinsohn 与 Pakes 1995

Steven Berry, James Levinsohn, and Ariel Pakes. **Automobile Prices in Market Equilibrium.** *Econometrica*, 63(4), 841–890.

[NBER 工作论文页面及正式发表信息](https://www.nber.org/papers/w4264)

该入口的工作论文版本发表于 1993 年，正式期刊版本发表于 1995 年。它将差异化产品需求、成本和市场均衡连接起来。进入这篇文献之前，先掌握 Logit、价格内生性与矩条件；阅读时区分消费者异质性、未观测产品特征、数据聚合和供给侧假设各自的作用。

## Berry 1994

Steven T. Berry. **Estimating Discrete-Choice Models of Product Differentiation.** *The RAND Journal of Economics*, 25(2), 242–262.

[论文全文的 Caltech 学术页面入口](https://www.its.caltech.edu/~mshum/gradio/papers/Berry1994.pdf)

衔接第 5—6 单元阅读。先弄清楚市场份额如何映射到平均效用，再追问价格与未观测产品特征相关时，参数如何借助额外限制识别。不要把平均效用反演和结构参数估计当成同一步。

## Nevo 2000

Aviv Nevo. **A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand.** *Journal of Economics & Management Strategy*, 9(4), 513–548.

[出版社页面与 DOI](https://onlinelibrary.wiley.com/doi/10.1111/j.1430-9134.2000.00513.x)

在掌握同质 Logit、价格内生性与矩条件后阅读，用它连接消费者异质性、需求计算和参数估计。期刊卷期年份为 2000；出版社页面另列电子发布时间，不应将两者混为一谈。本仓库当前代码只实现同质 Logit，不是随机系数或 BLP 复现。

## 第二部分的阅读顺序

先读 Train 第 3 章的概率、IIA 与弹性，再读本仓库第 5—6 单元及代码。Berry（1994）连接份额反演与内生性；Nevo（2000）和 BLP（1995）作为下一阶段入口，不要求这一轮完成全部计算细节。

## Hansen 1982

Lars Peter Hansen. **Large Sample Properties of Generalized Method of Moments Estimators.** *Econometrica*, 50(4), 1029–1054.

[作者网站论文入口](https://larspeterhansen.org/wp-content/uploads/2016/11/Hansen-econometrica-GMM.pdf)

连接总体正交限制、样本矩、权重和估计量的大样本性质。先对照第 8 单元的线性公式，理解为什么权重与效率相关，再逐步阅读一般理论；不要把效率结果用于无效矩条件或直接套用到弱识别情形。

## Staiger 与 Stock 1997

Douglas Staiger and James H. Stock. **Instrumental Variables Regression with Weak Instruments.** *Econometrica*, 65(3), 557–586.

[Stock 作者机构出版记录](https://stock.scholars.harvard.edu/publications/instrumental-variables-regression-weak-instruments)

阅读问题：当工具对内生变量的解释能力很弱时，常规大样本近似为什么可能误导？文中的具体设定、统计量和参考临界值有适用条件，不能将它们概括为任何异方差或聚类场景都适用的单一第一阶段门槛。

## Cameron 与 Miller 2015

A. Colin Cameron and Douglas L. Miller. **A Practitioner's Guide to Cluster-Robust Inference.** *Journal of Human Resources*, 50(2).

[Cameron 作者机构论文入口](https://cameron.econ.ucdavis.edu/research/Cameron_Miller_JHR_2015.pdf)

先读独立聚类与组内相关的基本框架，再看第 VII 节中 IV 和 GMM 的扩展。对应本仓库的市场矩贡献 $h_t$，辨认消费者数、产品市场观测数和独立市场数各自承担什么作用。

## 第三部分的阅读顺序

先读 [Train 第 13 章](https://eml.berkeley.edu/books/choice2nd/Ch13_p315-346.pdf)的价格内生性，再读本仓库第 7—8 单元并运行 IV/GMM 例子。随后用 Hansen（1982）理解矩估计框架，用 Staiger 与 Stock（1997）理解弱工具，用 Cameron 与 Miller（2015）理解市场内相关。随机系数需求与 BLP 留作下一部分。

## 阅读产出

每篇至少写清四项：研究目标；关键模型假设；识别所依赖的数据变化；估计准则与反事实中的不变性假设。使用[论文阅读模板](../templates/paper-note.md)记录，不要只抄写算法步骤。

本索引的入口与出版信息核对日期：2026-10-13。

第二部分新增的 Train 第 3 章入口、Berry（1994）与 Nevo（2000）于 2026-10-15 核对。

第三部分新增的 Train 第 13 章、Hansen（1982）、Staiger 与 Stock（1997）及 Cameron 与 Miller（2015）入口与出版信息于 2026-10-18 核对。
