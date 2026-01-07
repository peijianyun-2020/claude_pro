# 数据处理脚本说明

## process_data.py

### 功能描述
整合数据读取、汇总、图表生成和文案生成的核心脚本。

### 依赖项
- Python 3.10+
- pandas
- numpy
- matplotlib
- openpyxl (Excel读取)
- 市场处理模块: `market_processor.py`

### 使用方法

#### 1. 处理指定日期
```bash
python process_data.py --type dayahead --date 20251231
```

**参数说明:**
- `--type`: 数据类型,可选 `dayahead`(日前) 或 `realtime`(实时)
- `--date`: 日期,格式 `YYYYMMDD` 或 `today`

#### 2. 批量处理
```bash
python process_data.py --type dayahead --batch
```

处理 `每日日前数据表/` 目录下所有Excel文件。

#### 3. 处理今天的数据
```bash
python process_data.py
```
默认处理今天的日前数据。

### 处理流程

1. **数据读取**
   - 从Excel文件读取价格数据
   - 自动识别时间列和价格列
   - 支持宽格式(多区域列)和长格式(区域列+数值列)

2. **数据汇总**
   - 追加到汇总CSV文件
   - 自动去重(基于日期+时间)
   - 按日期/时间排序

3. **图表生成**
   - 生成PNG(300 DPI,高质量)
   - 生成SVG(矢量图)
   - 生成JPG(压缩图)
   - 中文显示优化

4. **文案生成**
   - 标题:南方电力现货｜MM/DD 日前电价速报 ⚡️
   - 概览:均价、峰谷值
   - 各区域分析(含奖牌标记)
   - 市场情绪判断

### 输出文件结构

```
YYYYMMDD日前/
├── 图_日前_YYYYMMDD.jpg     # 小红书发布用
├── 图_日前_YYYYMMDD.svg     # 矢量图
├── 图表_日前_YYYYMMDD.png   # 高清图
└── 文案_日前_YYYYMMDD.txt   # 发布文案
```

### 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 未找到数据文件 | 文件名不符或路径错误 | 检查文件命名和位置 |
| 数据读取失败 | Excel格式异常 | 检查Excel列名和数据格式 |
| 中文显示为方框 | 缺少中文字体 | 安装SimHei或Microsoft YaHei |
| 文案生成失败 | 缺少全区域数据 | 确保Excel包含全区域列 |

### 注意事项

1. Excel文件命名必须严格按照 `YYYYMMDD日前.xlsx` 或 `YYYYMMDD实时.xlsx`
2. 时间列支持格式: `HH:MM`、`HH:MM:SS` 或纯数字小时
3. 区域列名称必须是: 全区域、广东、广西、云南、贵州、海南
4. 汇总CSV文件使用UTF-8-BOM编码,确保Excel正确打开
