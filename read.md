# 汉诺塔搜索：中文运行说明

这是一个独立项目，GitHub 仓库建议命名为 `tower-of-hanoi-search`。
`README.md` 是英文项目介绍，本文件是中文使用说明。

## 如何运行

需要 Python 3.10 或更新版本。核心程序和测试只使用标准库，无须安装 NumPy。
在这个文件所在的项目目录打开终端，运行：

```bash
python hanoi.py --disks 4 --pegs 3 --algorithm ida --heuristic 3b
python hanoi.py --disks 4 --pegs 4 --algorithm ida --heuristic 4a
python -m unittest discover -s tests -v
```

前两条分别求三根柱和四根柱的汉诺塔，打印完整移动步骤和展开状态数。
第三条运行自动化测试。

## 全部实验

```bash
python experiments.py --quick
python experiments.py
```

第一条是快速演示；第二条是完整实验，包括 h3b 六盘、k(6)、h4a 七盘。
完整实验可能需要几分钟，取决于电脑速度。`results/results.json` 保存完整结果。
`report.ipynb` 已经保存所有实验的实际输出和关系式解释，可以直接用 VS Code 打开查看。

如果希望在 JupyterLab 里运行：

```bash
python -m pip install -r requirements-notebook.txt
python -m jupyterlab report.ipynb
```

## 核心内容

- IDS：逐步增加深度上限。
- IDA*：逐步增加 g+h 的代价上限。
- h3a、h3b：三根柱的两个可采纳启发式。
- h4a：四根柱启发式，使用 k(d) 作为下界。
- 只检查当前路径上的重复状态，不维护跨迭代的全局访问集合。
- 生成后继时才计一次展开，单纯检查目标不计数。

`f(d,4)=2k(d-1)+1` 对 d≥1 成立。完整理由写在 Notebook 的 1.3(c)。
四柱的 k 表支持最多七个盘，不同状态的解题调用应依次进行。

## 上传 GitHub

1. 新建一个空仓库，例如 `tower-of-hanoi-search`。
2. 解压压缩包后，进入里面的 `tower-of-hanoi` 文件夹。
3. 把这个文件夹内部的文件和子文件夹上传，让 `README.md` 出现在仓库首页。
4. 不要把客户流失项目混入这个仓库。
5. 如使用 Git，依次运行 `git init`、`git add .`、`git commit -m "Add complete Hanoi search project"`，再按 GitHub 空仓库页面显示的地址连接远程仓库并推送。

项目保留课程起始代码的来源说明，详见 `NOTICE.md`。
