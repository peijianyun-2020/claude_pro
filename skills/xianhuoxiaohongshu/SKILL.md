---
name: xianhuoxiaohongshu
description: 南方区域电力现货价格数据处理、图表生成和小红书自动发布。当用户需要处理电价数据、生成价格分析图表、创建小红书文案或发布电力市场内容时使用此技能。
---

# 南方电力现货市场小红书发布助手

## 概述

本 Skill 提供南方区域电力现货市场价格数据的全流程处理能力，包括：
1. 数据读取与汇总（Excel → CSV）
2. 价格曲线图生成（PNG/SVG/JPG）
3. 小红书风格分析文案生成
4. 一键发布到小红书

适用场景：
- 日常电价数据更新与发布
- 历史数据重新分析
- 批量数据处理
- 自动化内容创作与发布

## 快速开始

### 场景一：处理新数据并发布到小红书

当用户说："处理今天的数据并发布到小红书" 或 "生成20251231的日前电价内容并发布"

执行步骤：
1. 检查数据文件是否存在（`每日日前数据表/YYYYMMDD日前.xlsx`）
2. 读取并处理数据（调用 `scripts/process_data.py`）
3. 生成图表和文案（调用 `scripts/generate_content.py`）
4. 检查小红书登录状态
5. 发布到小红书（调用 `scripts/publish_xiaohongshu.py`）

### 场景二：仅生成内容不发布

当用户说："生成今天的图表和文案" 或 "只做数据分析,不要发布"

执行步骤：
1-3. 同上（数据处理、图表生成、文案生成）
4. 输出内容文件路径供用户审阅

### 场景三：仅发布已有内容

当用户说："发布20251228的内容" 或 "把昨天的内容发到小红书"

执行步骤：
1. 定位目标日期文件夹（`YYYYMMDD日前/`）
2. 提取文案和图片
3. 检查小红书登录状态
4. 发布到小红书

## 项目路径配置

项目根目录：`D:\AI\Trae项目工作区\南方区域电力现货市场价格跟踪`

关键路径：
- 输入数据：
  - 日前：`每日日前数据表/`
  - 实时：`每日实时数据表/`
- 汇总数据库：
  - 日前：`汇总_日前.csv`
  - 实时：`汇总_实时.csv`
- 输出目录：
  - 格式：`YYYYMMDD日前/` 或 `YYYYMMDD实时/`
  - 内容：`图_类别_YYYYMMDD.jpg`、`文案_类别_YYYYMMDD.txt`

## 核心脚本使用

### 1. 数据处理与内容生成

```bash
# 处理日前数据（推荐）
python scripts/process_data.py --type dayahead --date 20251231

# 处理实时数据
python scripts/process_data.py --type realtime --date 20251231

# 批量处理所有待处理文件
python scripts/process_data.py --batch
```

### 2. 小红书发布

```bash
# 发布指定日期的内容
python scripts/publish_xiaohongshu.py --date 20251231 --category dayahead

# 交互式发布（提示用户选择日期和类别）
python scripts/publish_xiaohongshu.py --interactive
```

### 3. 仅检查登录状态

```bash
python scripts/publish_xiaohongshu.py --check-login
```

## 文案生成规则

### 标题格式
```
南方电力现货｜MM/DD 日前电价速报 ⚡️
```

### 内容结构
1. **概览**：全区域均价、峰谷值及时段
2. **极端价格提示**（如有）：0价/负价警告
3. **各区域分析**：
   - 🥇/🥈/🥉 奖牌标记（Top3区域）
   - 均价、最高价、最低价
   - 较近7日涨跌幅
   - 价差与波动（变异系数）
4. **市场情绪**：偏强/偏弱/稳

### 标签策略
默认标签：`["电力现货", "电价分析", "能源市场", "日前电价", "电力交易"]`

可根据内容调整：
- 工作日发布：添加 "电价速报"
- 周末发布：添加 "周末充电"
- 特殊情况：添加 "价格波动"、"负电价" 等

## 图表生成规范

### 输出格式
- **PNG**（300 DPI）：高质量主图，用于小红书
- **SVG**：矢量图，便于后期编辑
- **JPG**：压缩图，快速预览

### 视觉要求
- 图表尺寸：12×8 英寸
- 中文字体：SimHei / Microsoft YaHei
- 颜色方案：
  - 全区域：蓝色 (#1f77b4)
  - 广东：橙色 (#ff7f0e)
  - 广西：绿色 (#2ca02c)
  - 云南：红色 (#d62728)
  - 贵州：紫色 (#9467bd)
  - 海南：棕色 (#8c564b)

## 小红书发布注意事项

### 发布时机建议
- 最佳时间：工作日 09:00-11:00, 14:00-16:00
- 避免时段：深夜 23:00-07:00
- 频率控制：每日不超过2篇

### 内容合规
- 标题≤20字
- 数据准确，来源明确
- 避免敏感词汇
- 图表清晰可读

### 互动优化
- 文末添加引导语："觉得有用请点赞收藏~"
- 回复评论及时响应
- 定期查看数据反馈

## 常见问题处理

### Q1: 提示"未找到数据文件"
**解决方案**：
1. 检查文件命名是否正确（YYYYMMDD日前.xlsx）
2. 确认文件是否在 `每日日前数据表/` 目录
3. 尝试批量导入模式处理历史文件

### Q2: 中文显示为方框
**解决方案**：
1. Windows：安装 SimHei 或 Microsoft YaHei 字体
2. 运行字体检查脚本：`python scripts/check_fonts.py`

### Q3: 小红书发布失败
**排查步骤**：
1. 检查登录状态：`python scripts/publish_xiaohongshu.py --check-login`
2. 确认图片格式（JPG）和大小（<10MB）
3. 检查网络连接
4. 重新登录：`python scripts/publish_xiaohongshu.py --login`

### Q4: 数据分析结果为空
**排查步骤**：
1. 检查汇总CSV是否有数据：`汇总_日前.csv`
2. 确认日期在汇总库中存在
3. 运行数据重新导入：`python scripts/process_data.py --rebuild`

## 完整工作流示例

### 每日发布流程（自动化）

```bash
# 1. 更新数据（复制新Excel到指定目录后）
python scripts/process_data.py --type dayahead --date today

# 2. 审阅生成的内容
# 查看文件：YYYYMMDD日前/文案_日前_YYYYMMDD.txt
# 查看图片：YYYYMMDD日前/图_日前_YYYYMMDD.jpg

# 3. 发布到小红书
python scripts/publish_xiaohongshu.py --date today --category dayahead
```

### 批量历史数据处理

```bash
# 批量导入所有待处理文件
python scripts/process_data.py --batch

# 批量生成所有日期的内容
python scripts/generate_content.py --all-dates

# 选择性发布
python scripts/publish_xiaohongshu.py --interactive
```

## 脚本参考

详细脚本说明请参考：
- [数据处理脚本](scripts/data_processor.md)
- [小红书发布脚本](scripts/xiaohongshu_publisher.md)
- [错误排查指南](TROUBLESHOOTING.md)

## 最佳实践

1. **数据备份**：每日更新前备份汇总CSV
2. **内容审阅**：发布前检查文案准确性和图表清晰度
3. **发布时间**：选择目标用户活跃时段
4. **标签优化**：根据内容特点添加相关标签
5. **数据分析**：定期查看阅读量、点赞量、收藏量，优化内容策略

## 更新日志

- v1.0 (2025-12-31): 初始版本，支持日前/实时数据处理、图文生成、小红书发布
