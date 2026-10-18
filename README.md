# 结构模型估计学习笔记

结构模型估计从经济主体的偏好、技术、约束和互动方式出发，推导可观测行为，再利用数据识别并估计未知参数。第一阶段的重点是分清三个问题：**模型如何产生数据，数据能区分哪些参数，有限样本如何给出估计值。**

本仓库使用中文讲解，采用“问题 → 直觉 → 数学表达 → 教学例子 → 适用边界”的顺序。先修知识是基础微观经济学、概率统计和回归分析；暂不要求掌握动态规划。

第二部分从二元选择进入多项 Logit，学习外部选项、市场份额、分组最大似然、价格弹性和替代模式。

第三部分加入未观测产品质量，学习价格内生性、工具变量、两阶段最小二乘和 GMM，并区分无效工具、弱工具与市场内相关。

## 从这里开始

第一次学习约 40 分钟：阅读[整体框架](notes/01-framework.md)，再跟随[购买决策例子](notes/03-binary-choice-example.md)，完成[自测题](exercises/01-self-check.md)第 1—5 题。

| 单元 | 核心问题 | 笔记 |
|---|---|---|
| 1 | 结构模型估计在做什么？ | [模型设定、识别与估计](notes/01-framework.md) |
| 2 | 为什么模型有解不代表参数可识别？ | [识别、数据变化与模型假设](notes/02-identification.md) |
| 3 | 如何从消费者决策走到参数估计？ | [二元购买决策的完整例子](notes/03-binary-choice-example.md) |
| 4 | 如何选择方法、检查结果和进行反事实？ | [估计方法与研究流程](notes/04-estimation-and-workflow.md) |
| 5 | 如何估计多个产品之间的选择？ | [从二元选择到多项 Logit](notes/05-multinomial-logit.md) |
| 6 | 涨价如何分流需求，Logit 有哪些限制？ | [价格弹性、替代关系与 IIA](notes/06-elasticities-and-iia.md) |
| 7 | 为什么价格内生，工具如何提供识别？ | [价格内生性、份额反演与工具变量](notes/07-endogeneity-and-iv.md) |
| 8 | 如何组合矩条件并判断结果可信度？ | [从 2SLS 到 GMM 与识别诊断](notes/08-gmm-and-diagnostics.md) |

已学完基础框架：从[第 5 单元](notes/05-multinomial-logit.md)继续，结合第 6 单元做[第二部分练习](exercises/02-self-check.md)。

已学完多项 Logit：从[第 7 单元](notes/07-endogeneity-and-iv.md)继续，结合第 8 单元做[第三部分练习](exercises/03-self-check.md)，再对照[答案](exercises/03-answers.md)与模拟输出。

配套内容：[学习路线](learning-path.md)、[术语表](glossary.md)、[基础练习](exercises/01-self-check.md)与[答案](exercises/01-answers.md)、[多项 Logit 练习](exercises/02-self-check.md)与[答案](exercises/02-answers.md)、[文献索引](classic-papers/README.md)、[论文阅读模板](templates/paper-note.md)、[可运行例子](code/README.md)。

## 三个环节的关系

| 环节 | 输入 | 核心问题 | 结果 |
|---|---|---|---|
| 模型设定 | 研究问题、制度背景、经济与统计假设 | 给定参数，产生什么行为和数据限制？ | 参数到分布或矩条件的映射 |
| 识别 | 模型限制与总体可观测信息 | 哪些参数或目标量可以被区分？ | 点识别、集合识别或未识别的结论 |
| 估计 | 有限样本、估计准则与计算方法 | 如何计算目标量并量化不确定性？ | 估计值、标准误或置信集合 |

识别取决于模型假设和数据共同提供的信息；优化器收敛、样本内拟合好，都不能单独证明结构参数已被识别或经济解释正确。

## 数值例子

安装 Python 3.10 或更新版本后，在仓库根目录运行：

```bash
python code/binary_choice_demo.py
python code/multinomial_logit_demo.py
python code/iv_gmm_demand_demo.py
```

三个脚本均仅使用 Python 标准库。二元例子展示观测等价、总体识别与样本估计；多项例子展示两种产品和外部选项的分组最大似然、价格弹性、给定价格的需求反事实以及 IIA；IV/GMM 例子比较 OLS、2SLS 与两步 GMM，展示有效、无效和弱工具，并按市场聚类计算协方差。所有随机样本均按固定种子生成；第三个脚本直接使用总体份额，其他例子另有有限消费者的抽样。

## 与其他学习材料衔接

- [充分统计量方法](https://github.com/GuoqingOu/sufficient-statistics-learning)：比较“识别整个参数向量”和“只识别政策所需目标量”。
- [国际贸易经济学](https://github.com/GuoqingOu/trade-economics-learning)：将模型、参数和政策不变性问题放入贸易反事实中。
- [网络经济学](https://github.com/GuoqingOu/network-economics-learning)：理解互动结构如何影响均衡结果与识别。

## 使用说明

第一版整理于 2026-10-13，定位为整体框架与基础学习。可以直接在 GitHub 阅读，或通过 **Code → Download ZIP** 下载。仓库中的解释与教学代码为独立编写，文献通过作者、大学、出版社或研究机构的原始入口链接提供；不分发论文全文。教学数字不是真实市场估计。

2026-10-15 更新：增加第 5—6 单元、多项 Logit 代码及 12 道配套题。

2026-10-18 更新：增加第 7—8 单元、IV/GMM 代码及 12 道配套题；目前共 8 个单元、36 道自测题和 3 个数值脚本。
