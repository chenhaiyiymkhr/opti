# GitHub 上传与 IDE 运行指南

本文说明如何把本项目上传到 GitHub，以及如何在 VS Code / PyCharm 这类 IDE 中运行。

## 1. 推荐上传到 GitHub 的文件结构

上传时请保持下面的目录结构，不要把 `src` 里的文件拆出来单独放到根目录。

```text
optical_link_budget_sim/
├─ README.md
├─ GITHUB_UPLOAD_GUIDE.md
├─ requirements.txt
├─ .gitignore
├─ run_demo.py
├─ configs/
│  └─ default.json
├─ src/
│  ├─ __init__.py
│  ├─ units.py
│  ├─ link_budget.py
│  ├─ osnr.py
│  ├─ ook_sim.py
│  ├─ metrics.py
│  └─ plots.py
└─ results/
   ├─ eye_diagram_nominal.png
   ├─ eye_diagram_low_osnr.png
   ├─ distance_sweep.png
   └─ ber_q_curve.png
```

## 2. 为什么 `src` 必须原样上传

`run_demo.py` 中通过下面这种方式调用核心模块：

```python
from src.link_budget import calculate_link_budget
from src.metrics import calculate_q_ber
from src.ook_sim import add_awgn, generate_bits, raised_edge_nrz, sample_waveform
from src.osnr import estimate_osnr
from src.plots import plot_ber_q_curve, plot_distance_sweep, plot_eye_diagram
```

因此 GitHub 仓库中必须存在：

```text
src/
├─ __init__.py
├─ units.py
├─ link_budget.py
├─ osnr.py
├─ ook_sim.py
├─ metrics.py
└─ plots.py
```

其中 `src/__init__.py` 用来告诉 Python：`src` 是一个可以导入的包。  
如果你把 `src` 里的文件直接拖到根目录，或者漏掉 `__init__.py`，`run_demo.py` 可能会出现 `ModuleNotFoundError`。

## 3. 哪些文件不需要上传

不要上传下面这些文件：

```text
.venv/
__pycache__/
*.pyc
results/*.csv
results/*.json
```

原因：

| 文件/目录 | 不上传原因 |
|---|---|
| `.venv/` | 虚拟环境体积大，别人应使用 `requirements.txt` 自己安装依赖 |
| `__pycache__/` | Python 自动生成的缓存 |
| `*.pyc` | Python 编译缓存 |
| `results/*.csv` | 运行后可重新生成 |
| `results/*.json` | 运行后可重新生成 |

结果图 `results/*.png` 可以上传，因为它们能让 GitHub 页面直接展示项目效果。

## 4. 用 GitHub 网页上传

适合第一次上传、不会 Git 命令的情况。

1. 打开 GitHub，创建新仓库，例如：

```text
optical-link-budget-sim
```

2. 进入新仓库，点击：

```text
Add file -> Upload files
```

3. 从本地项目目录中拖拽上传这些文件和文件夹：

```text
README.md
GITHUB_UPLOAD_GUIDE.md
requirements.txt
.gitignore
run_demo.py
configs/
src/
results/
```

4. 注意 `results/` 中只建议上传 `.png` 图片：

```text
eye_diagram_nominal.png
eye_diagram_low_osnr.png
distance_sweep.png
ber_q_curve.png
```

5. 在页面底部填写提交信息：

```text
Initial commit: optical link budget simulation
```

6. 点击 `Commit changes`。

## 5. 用 Git 命令上传

在 PowerShell 中进入项目目录：

```powershell
Set-Location 'D:\工作\optical_link_budget_sim'
```

初始化仓库：

```powershell
git init
git add README.md GITHUB_UPLOAD_GUIDE.md requirements.txt .gitignore run_demo.py configs src results/*.png
git commit -m "Initial commit: optical link budget simulation"
```

连接 GitHub 远程仓库：

```powershell
git branch -M main
git remote add origin https://github.com/<你的用户名>/optical-link-budget-sim.git
git push -u origin main
```

把 `<你的用户名>` 替换成你的 GitHub 用户名。

## 6. 在 VS Code 中运行

### 6.1 打开项目文件夹

打开 VS Code，选择：

```text
File -> Open Folder
```

选择：

```text
D:\工作\optical_link_budget_sim
```

注意：要打开整个 `optical_link_budget_sim` 文件夹，不要只打开 `src` 文件夹。

### 6.2 创建虚拟环境

打开 VS Code 终端：

```text
Terminal -> New Terminal
```

执行：

```powershell
python -m venv .venv
```

激活虚拟环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

如果提示脚本执行策略限制，执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 6.3 安装依赖

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6.4 选择 Python 解释器

按 `Ctrl + Shift + P`，搜索：

```text
Python: Select Interpreter
```

选择项目里的解释器：

```text
.\.venv\Scripts\python.exe
```

### 6.5 运行项目

推荐在终端中运行：

```powershell
python run_demo.py
```

不要直接运行 `src/link_budget.py`、`src/osnr.py` 等文件。  
这些文件是模块文件，负责被 `run_demo.py` 调用，不是项目入口。

运行成功后，查看：

```text
results/
```

会生成：

```text
single_case_summary.json
distance_sweep.csv
eye_diagram_nominal.png
eye_diagram_low_osnr.png
distance_sweep.png
ber_q_curve.png
```

## 7. 在 PyCharm 中运行

### 7.1 打开项目

选择：

```text
File -> Open
```

打开：

```text
D:\工作\optical_link_budget_sim
```

### 7.2 配置解释器

进入：

```text
Settings -> Project -> Python Interpreter
```

选择或新建虚拟环境：

```text
D:\工作\optical_link_budget_sim\.venv\Scripts\python.exe
```

### 7.3 安装依赖

PyCharm 终端中执行：

```powershell
pip install -r requirements.txt
```

### 7.4 配置运行入口

右键点击：

```text
run_demo.py
```

选择：

```text
Run 'run_demo'
```

或者在运行配置中设置：

```text
Script path: D:\工作\optical_link_budget_sim\run_demo.py
Working directory: D:\工作\optical_link_budget_sim
```

关键点：`Working directory` 必须是项目根目录，否则可能找不到 `configs/default.json` 或 `src` 模块。

## 8. 上传结果图的建议

建议上传这 4 张图：

```text
results/eye_diagram_nominal.png
results/eye_diagram_low_osnr.png
results/distance_sweep.png
results/ber_q_curve.png
```

不建议上传：

```text
results/distance_sweep.csv
results/single_case_summary.json
```

因为 CSV 和 JSON 每次运行都会重新生成，放进 GitHub 容易造成无意义变更。

## 9. README 中展示结果图

可以在 `README.md` 中加入：

```markdown
## 仿真结果示例

### 距离扫描

![distance sweep](results/distance_sweep.png)

### 默认链路眼图

![nominal eye diagram](results/eye_diagram_nominal.png)

### 低 OSNR 眼图

![low OSNR eye diagram](results/eye_diagram_low_osnr.png)

### BER-Q 曲线

![BER-Q curve](results/ber_q_curve.png)
```

这样别人打开 GitHub 仓库首页时，可以直接看到仿真效果。

## 10. 常见错误

| 报错 | 原因 | 解决 |
|---|---|---|
| `ModuleNotFoundError: No module named 'src'` | 没有从项目根目录运行，或 `src` 目录没上传 | 打开整个项目，运行 `python run_demo.py` |
| `No module named 'matplotlib'` | 没安装依赖 | 执行 `pip install -r requirements.txt` |
| 找不到 `configs/default.json` | 工作目录不对 | 在项目根目录运行，或检查 PyCharm 的 Working directory |
| GitHub 没显示图片 | 没上传 `results/*.png`，或 README 路径写错 | 确认图片路径是 `results/xxx.png` |

