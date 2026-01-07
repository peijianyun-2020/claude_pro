# 快速开始指南

## 5分钟快速上手

### 前置准备

1. **Python环境**
   ```bash
   python --version  # 需要 Python 3.10+
   ```

2. **安装依赖**
   ```bash
   cd D:\AI\Trae项目工作区\南方区域电力现货市场价格跟踪
   pip install -r requirements.txt
   ```

3. **小红书MCP服务**
   - 确保Claude Code已安装小红书MCP服务
   - 完成登录认证

---

## 三种使用方式

### 方式一: 完整工作流(推荐)

**场景:** 从数据处理到自动发布

```bash
# Step 1: 处理数据并生成内容
cd xiaohongshu-market-skill\scripts
python process_data.py --type dayahead --date 20251231

# Step 2: 审阅生成的内容
# 查看文件: D:\AI\Trae项目工作区\南方区域电力现货市场价格跟踪\20251231日前\

# Step 3: 发布到小红书
python publish_xiaohongshu.py --date 20251231 --category dayahead
```

**或者让Claude自动完成:**
```
处理2025年12月31日的日前电价数据并发布到小红书
```

---

### 方式二: 仅生成内容

**场景:** 数据分析和内容创作,手动控制发布

```bash
# 处理数据
python scripts/process_data.py --type dayahead --date 20251231

# 输出文件位置:
# - 20251231日前/图_日前_20251231.jpg
# - 20251231日前/文案_日前_20251231.txt
```

---

### 方式三: 发布已有内容

**场景:** 内容已生成,仅需发布

```bash
# 直接发布
python scripts/publish_xiaohongshu.py --date 20251231 --category dayahead

# 或交互式选择
python scripts/publish_xiaohongshu.py --interactive
```

---

## 常用命令速查

### 数据处理

```bash
# 处理今天的数据
python scripts/process_data.py

# 处理指定日期
python scripts/process_data.py --date 20251231

# 批量处理所有文件
python scripts/process_data.py --batch

# 处理实时数据
python scripts/process_data.py --type realtime --date 20251231
```

### 小红书发布

```bash
# 发布指定日期
python scripts/publish_xiaohongshu.py --date 20251231

# 查看可发布内容
python scripts/publish_xiaohongshu.py --interactive

# 检查登录状态
python scripts/publish_xiaohongshu.py --check-login
```

---

## 文件结构

```
xiaohongshu-market-skill/
├── SKILL.md                    # Skill主配置文件
├── README.md                   # 本文件
├── TROUBLESHOOTING.md          # 故障排查指南
└── scripts/
    ├── process_data.py         # 数据处理脚本
    ├── publish_xiaohongshu.py  # 小红书发布脚本
    ├── data_processor.md       # 数据处理文档
    └── xiaohongshu_publisher.md # 发布文档
```

---

## 典型工作流程

### 每日发布流程

**时间:** 每个工作日 09:00-10:00

**步骤:**

1. **获取数据** (手动)
   - 从交易平台下载最新Excel
   - 命名为 `YYYYMMDD日前.xlsx`
   - 放入 `每日日前数据表/` 目录

2. **处理数据** (自动)
   ```bash
   python scripts/process_data.py --type dayahead --date today
   ```

3. **审阅内容** (手动)
   - 查看生成的图表
   - 检查文案准确性
   - 确认无误

4. **发布内容** (自动)
   ```bash
   python scripts/publish_xiaohongshu.py --date today --category dayahead
   ```

5. **记录反馈** (手动)
   - 查看发布后的阅读/点赞/收藏数据
   - 记录在Excel日志中

---

## 与Claude配合使用

### 自然语言命令示例

**数据处理:**
- "处理今天的日前电价数据"
- "生成2025年12月31日的图表和文案"
- "批量处理所有待处理的实时数据"

**内容生成:**
- "为昨天的数据生成小红书文案"
- "创建价格曲线图,要包含所有区域"

**小红书发布:**
- "把20251228的内容发布到小红书"
- "检查小红书登录状态"
- "列出所有可以发布的内容"

**完整工作流:**
- "处理今天的数据并发布到小红书"
- "完成从数据到发布的全流程"

---

## 配置说明

### 修改项目路径

如果你的项目路径不是默认路径,修改脚本中的路径:

```python
# scripts/process_data.py
PROJECT_ROOT = Path(r"你的项目路径")

# scripts/publish_xiaohongshu.py
PROJECT_ROOT = Path(r"你的项目路径")
```

### 自定义标签

编辑 `scripts/publish_xiaohongshu.py`:

```python
# 修改默认标签
default_tags = ["你的标签1", "你的标签2", ...]
```

### 调整图表样式

编辑项目中的 `market_processor.py`:

```python
# 修改图表尺寸
plt.figure(figsize=(12, 8))  # (宽, 高)

# 修改颜色
colors = ['#1f77b4', '#ff7f0e', ...]

# 修改字体
matplotlib.rcParams['font.sans-serif'] = ['你的字体']
```

---

## 下一步

1. **阅读完整文档:**
   - [SKILL.md](SKILL.md) - 完整功能说明
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 故障排查

2. **测试流程:**
   - 使用历史数据测试
   - 确认每个环节正常

3. **优化效率:**
   - 创建批处理脚本
   - 设置定时任务

4. **数据分析:**
   - 跟踪发布效果
   - 优化内容策略

---

## 获取帮助

遇到问题?

1. 查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. 检查脚本文档 (scripts/*.md)
3. 向Claude描述问题,获取针对性建议

---

## 示例: 完整对话

```
用户: 处理今天的日前电价数据并发布到小红书

Claude: 好的,我来帮你完成这个任务。

📖 正在处理数据...
✅ 数据已读取
✅ 汇总数据库已更新
✅ 图表已生成: 20251231日前/图_日前_20251231.jpg
✅ 文案已生成: 20251231日前/文案_日前_20251231.txt

📝 生成的内容预览:
标题: 南方电力现货｜12/31 日前电价速报 ⚡️
概览: 全区域均价约285.3元/兆瓦时；峰值420.5出现在09时...

🔍 检查小红书登录状态...
✅ 已登录

🚀 发布到小红书...
✅ 发布成功!

📊 内容链接: [小红书笔记URL]
```
