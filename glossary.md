# 结构模型估计术语表

| 术语 | 英文 | 在本仓库中的含义 |
|---|---|---|
| 结构参数 | Structural parameter | 模型中描述偏好、技术、成本等机制的参数；解释取决于模型假设 |
| 原始要素 | Primitives | 模型所假定的偏好、技术、禀赋、冲击分布等基础对象 |
| 可观测量 | Observables | 数据记录中研究者能够看到的变量 |
| 不可观测量 | Unobservables | 影响行为但研究者没有直接看到的因素；不等于决策者也不知道 |
| 模型求解 | Model solution | 给定参数计算最优决策、均衡或预测 |
| 点识别 | Point identification | 模型与总体可观测信息唯一确定目标量 |
| 识别集合 | Identified set | 与总体可观测信息和模型限制相容的目标值集合 |
| 观测等价 | Observational equivalence | 不同结构在可观测信息上无法区分 |
| 局部识别 | Local identification | 在目标参数附近满足唯一性，未必在整个参数空间唯一 |
| 规范化 | Normalization | 消除计量单位或基准选择等不影响可观测结果的冗余 |
| 外生性 | Exogeneity | 具体含义取决于模型，例如解释变量与结构冲击独立或满足条件矩限制 |
| 排除限制 | Exclusion restriction | 某变量不直接进入某结构关系，只通过指定渠道产生影响 |
| 工具变量 | Instrumental variable | 在适当模型中，通过相关性和外生限制提供区分内生变量影响的信息 |
| 矩条件 | Moment condition | 模型规定的期望限制，例如 $E[zu]=0$ |
| 估计量与估计值 | Estimator and estimate | 前者是数据到结果的规则，后者是该规则在某份数据上的实现 |
| 目标函数 | Objective function | 用于评价候选参数与数据相容程度的样本准则 |
| 最大似然 | Maximum likelihood | 最大化观测数据在模型下的似然 |
| 模拟矩估计 | Simulated method of moments | 用模型模拟的统计量匹配数据统计量 |
| 校准 | Calibration | 依据外部证据、约定或匹配目标选取参数；需说明每个参数来源 |
| 反事实 | Counterfactual | 在指定环境变化和不变性假设下，计算模型预测的替代结果 |
| 不变性 | Invariance | 某些结构关系或参数在所考虑的干预下保持稳定的假设 |
| 模型误设 | Misspecification | 模型限制不能正确描述所研究的数据生成机制 |
| 外部选项 | Outside option | 不选择当前内部产品集合的备选行为；本例是不购买 A 或 B |
| 系统效用 | Systematic utility | 效用中由观测变量和参数表达的部分；与随机冲击一起决定选择 |
| 备选项常数 | Alternative-specific constant | 某选项相对基准备选项的共同吸引力参数 |
| 多项 Logit | Multinomial Logit | 在本例的独立同分布第一类极值冲击下，选择概率为效用指数的归一化值 |
| 市场规模 | Market size | 用于界定总体份额的潜在消费者数量，不一定等于已购买人数 |
| 份额反演 | Share inversion | 从选择份额恢复模型中的平均或系统效用；不自动分离价格与未观测质量 |
| 自身价格弹性 | Own-price elasticity | 某产品价格变化 1% 时，其需求的局部百分比变化 |
| 交叉价格弹性 | Cross-price elasticity | 另一产品价格变化 1% 时，本产品需求的局部百分比变化 |
| 转移比例 | Diversion ratio | 某产品失去的需求中流向某个其他选项的比例，须说明所考虑的变化 |
| 无关替代项独立性 | Independence of irrelevant alternatives, IIA | 给定两个选项系统效用时，它们的条件选择概率比不受其他选项影响 |
| 随机系数 | Random coefficients | 让特征的偏好系数随消费者变化，用来扩展异质性与替代模式 |

“弱识别”有多种正式定义。本仓库用价格变化不足导致斜率难以精确估计的例子说明信息强度，具体理论见[文献索引](classic-papers/README.md)。
