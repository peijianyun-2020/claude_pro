# 南方区域电力现货价格采集 Skill

快速采集南方区域电力现货市场的日前和实时用电侧成交价格数据。

## 功能特性

- ✅ 自动采集日前和实时现货价格
- ✅ 支持24小时整点数据提取
- ✅ 覆盖6个区域（全区域、广东、广西、云南、贵州、海南）
- ✅ 自动生成CSV格式文件
- ✅ 数据验证和统计摘要

## 快速开始

### 环境要求

- Python 3.10+
- 现代浏览器（推荐Chrome）
- 南方区域现货电能量交易系统账号

### 安装

无需额外依赖，使用Python标准库即可。

```bash
cd D:\AI\cc_pro\.claude\skills\southern-spot-price-collector\scripts
```

## 使用方法

### 方法一：使用Claude对话（推荐）

直接告诉Claude你需要采集的数据：

```
采集20260101的实时现货价格
```

```
提取2026年1月1日的日前数据
```

Claude会自动完成整个采集流程。

### 方法二：手动使用脚本（支持命令行参数）

**步骤1: 获取API数据**

1. 访问交易系统并登录
2. 打开Chrome DevTools（F12）→ Network标签
3. 选择"用电侧成交价格"并切换数据类型（日前/实时）
4. 选择目标日期
5. 在Network中搜索 `getWatchUserPriceData`
6. 复制Response中的完整JSON数据

**步骤2: 运行处理脚本**

```bash
cd D:\AI\cc_pro\.claude\skills\southern-spot-price-collector\scripts
```

**方式A: 使用JSON文件（推荐）**
```bash
# 将API数据保存为JSON文件后运行
python process_spot_price.py --date 2025-01-01 --type realtime --input api_data.json
```

**方式B: 使用命令行参数**
```bash
# 先将数据粘贴到脚本的DEFAULT_API_DATA变量中
python process_spot_price.py --date 2025-01-01 --type realtime
```

**方式C: 交互式模式**
```bash
# 直接运行，按提示输入参数
python process_spot_price.py
```

**命令行参数说明:**
- `-d, --date`: 目标日期（YYYY-MM-DD 或 YYYYMMDD）
- `-t, --type`: 数据类型（realtime/rt 或 dayahead/da）
- `-i, --input`: 输入JSON文件路径
- `--no-summary`: 跳过统计摘要生成

**使用示例:**
```bash
# 实时价格数据
python process_spot_price.py -d 2025-01-01 -t realtime -i data.json

# 日前价格数据（使用简写）
python process_spot_price.py -d 20250101 -t da -i data.json

# 交互式模式
python process_spot_price.py

# 跳过统计摘要
python process_spot_price.py -d 2025-01-01 -t realtime -i data.json --no-summary
```

## 文件结构

```
southern-spot-price-collector/
├── SKILL.md                    # Skill主配置文件
├── README.md                   # 本文件
└── scripts/
    └── process_spot_price.py   # 数据处理脚本
```

## 数据格式

### 输入格式（API响应JSON）

```json
{
  "code": 0,
  "msg": "success",
  "data": [
    {
      "exchange": "00",
      "price0000": "371.7845",
      "price0100": "348.1993",
      ...
      "price2300": "450.1234"
    }
  ]
}
```

### 输出格式（CSV）

```csv
时间,全区域,广东,广西,云南,贵州,海南
00:00,371.7845,387.849,373.3411,249.8317,438.4059,449.9766
01:00,348.1993,361.7443,331.3694,204.2519,425.8183,500.0455
...
```

## 配置说明

### 修改数据目录

编辑 `scripts/process_spot_price.py`:

```python
# 修改为你的数据目录
DATA_DIR = Path(r"你的数据目录路径")
```

### 添加新的地区映射

```python
REGION_MAP = {
    "00": "全区域",
    "02": "广东",
    "03": "广西",
    "04": "云南",
    "05": "贵州",
    "06": "海南",
    # 添加新的地区代码
}
```

## 数据类型

### 日前数据 (Day-Ahead)
- **参数**: `dateType = "0"`
- **用途**: 次日价格预测、交易计划
- **文件**: `日前价格_YYYYMMDD.csv`

### 实时数据 (Real-Time)
- **参数**: `dateType = "1"`
- **用途**: 实时结算、成本分析
- **文件**: `实时价格_YYYYMMDD.csv`

## 常见问题

### Q: 找不到API接口？
**A**: 确保已点击"用电侧成交价格"标签，且Network筛选器设置为"XHR"。

### Q: 数据返回为空？
**A**: 检查登录状态、日期格式、dateType参数。

### Q: CSV文件乱码？
**A**: 使用Excel打开时选择UTF-8编码，或用记事本查看。

### Q: 缺少某些时段数据？
**A**:
- 实时数据：部分时段可能尚未发生
- 日前数据：可能在00:00后才完全生成
- 检查原始JSON数据完整性

## 数据验证

采集后检查：
- [ ] CSV包含24行数据
- [ ] 所有6个地区都有数据
- [ ] 价格值合理（非负、非异常）
- [ ] 文件命名正确
- [ ] 可被Excel正确读取

## 最佳实践

1. **备份数据**: 采集后备份原始JSON
2. **验证完整性**: 检查数据统计摘要
3. **规范命名**: 遵循 `类型_YYYYMMDD.csv` 格式
4. **批量处理**: 使用脚本自动化重复工作
5. **错误记录**: 采集失败时记录详细信息

## 技术支持

遇到问题？
1. 查看 [SKILL.md](SKILL.md) 详细文档
2. 检查 `D:\AI\cc_pro\现货价格采集` 下的参考文档
3. 验证系统登录和网络连接

## 版本历史

- **v1.0** (2025-01-03): 初始版本，支持日前/实时价格采集

## 许可

本Skill仅供学习和个人使用。
