---
name: xianhuoprice
description: 南方区域电力现货价格数据采集工具。从南方区域现货电能量交易系统自动提取日前和实时用电侧成交价格数据。当用户需要采集电价数据、提取现货价格或获取电力市场数据时使用此技能。
---

# 南方区域电力现货价格采集助手

## 概述

本 Skill 提供从南方区域现货电能量交易系统自动提取用电侧成交价格数据的能力，包括：
1. 日前价格数据提取 (dateType="0")
2. 实时价格数据提取 (dateType="1")
3. 数据格式转换 (JSON → CSV)
4. 批量日期数据处理

适用场景：
- 日常电价数据采集
- 历史数据批量提取
- 价格趋势分析数据准备
- 市场交易数据归档

## 快速开始

### 场景一：采集指定日期的实时价格

当用户说："采集20260101的实时现货价格" 或 "提取2026-01-01的实时数据"

执行步骤：
1. 确认目标日期和数据类型（实时/日前）
2. 检查是否已登录系统
3. 使用Chrome DevTools访问API接口
4. 复制API响应数据
5. 调用数据处理脚本生成CSV文件
6. 验证生成的CSV文件

### 场景二：批量采集多日数据

当用户说："采集最近7天的日前数据" 或 "批量提取2025年12月的数据"

执行步骤：
1. 确定日期范围和数据类型
2. 为每个日期依次执行API请求
3. 收集所有响应数据
4. 批量处理生成多个CSV文件
5. 汇总处理结果

### 场景三：重新采集失败数据

当用户说："重新采集20251231的数据" 或 "上次采集失败了，再试一次"

执行步骤：
1. 检查是否已有该日期的CSV文件
2. 如有，询问是否覆盖
3. 重新执行采集流程
4. 验证数据完整性

## 系统访问信息

### 交易平台地址
```
https://spot.poweremarket.com/uptspot/sr/mp/portaladmin/index.html#/
```

### 核心API接口
```
POST https://spot.poweremarket.com/uptspot/ma/spot/spottrade/scptp/sr/mp/spottrade/baseinfo/TranOver/getWatchUserPriceData
```

### 请求参数
```json
{
  "operateDate": "2026-01-01",  // 目标日期 YYYY-MM-DD
  "dateType": "1"                // "0"=日前, "1"=实时
}
```

## 数据采集流程

### 标准采集步骤（推荐方式）

#### 方式1: 使用JSON文件（推荐）

**步骤1: 提取API数据并保存为JSON文件**
- 打开Chrome浏览器访问交易系统
- 按F12打开开发者工具，切换到Network标签
- 在系统中选择"用电侧成交价格"模块
- 切换数据类型（日前/实时）并选择目标日期
- 在Network中搜索：`getWatchUserPriceData`
- 点击请求 → 切换到Response标签
- 复制完整JSON数据并保存为 `.json` 文件（例如 `api_data.json`）

**步骤2: 运行处理脚本**
```bash
cd D:\AI\cc_pro\.claude\skills\southern-spot-price-collector\scripts
python process_spot_price.py --date 2025-01-01 --type realtime --input api_data.json
```

#### 方式2: 使用命令行参数

**步骤1: 提取API数据**
- 同上，复制完整JSON数据

**步骤2: 编辑脚本并运行**
- 打开 `scripts/process_spot_price.py`
- 将JSON数据粘贴到 `DEFAULT_API_DATA` 变量的 `data` 字段中
- 保存文件并运行：
```bash
python process_spot_price.py --date 2025-01-01 --type realtime
```

#### 方式3: 交互式模式

直接运行脚本，按提示输入参数：
```bash
python process_spot_price.py
```

然后按提示输入：
- 目标日期（YYYY-MM-DD 或 YYYYMMDD）
- 数据类型（1=实时，2=日前）
- JSON文件路径（可选，不输入则使用脚本中的数据）

### 使用自动化脚本（推荐）

#### 完整处理脚本
```python
import csv
import json
from pathlib import Path
from datetime import datetime

# 数据目录配置
DATA_DIR = Path(r"D:\AI\cc_pro\现货价格采集")

def save_price_data(api_data, target_date, data_type="realtime"):
    """
    保存价格数据为CSV

    参数:
        api_data: API返回的完整JSON数据
        target_date: 目标日期 (YYYY-MM-DD 或 YYYYMMDD)
        data_type: 数据类型 ("dayahead" 或 "realtime")
    """
    # 地区代码映射
    region_map = {
        "00": "全区域",
        "02": "广东",
        "03": "广西",
        "04": "云南",
        "05": "贵州",
        "06": "海南"
    }

    # 创建CSV数据
    csv_data = []
    headers = ["时间", "全区域", "广东", "广西", "云南", "贵州", "海南"]
    csv_data.append(headers)

    # 生成24个小时的数据
    for hour in range(24):
        time_str = f"{hour:02d}:00"
        row = [time_str]

        for exchange_code in ["00", "02", "03", "04", "05", "06"]:
            region_data = next(
                (item for item in api_data["data"]
                 if item["exchange"] == exchange_code),
                None
            )

            if region_data:
                price_key = f"price{hour:02d}00"
                price = region_data.get(price_key, "0")
                row.append(price)
            else:
                row.append("0")

        csv_data.append(row)

    # 生成文件名
    date_formatted = target_date.replace("-", "")
    type_label = "实时价格" if data_type == "realtime" else "日前价格"
    csv_filename = f"{type_label}_{date_formatted}.csv"
    csv_path = DATA_DIR / csv_filename

    # 保存文件
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)

    print(f"✅ 数据已保存: {csv_path}")
    print(f"📊 记录数: {len(csv_data)-1} 行")
    print(f"📅 日期: {target_date}")
    print(f"🏷️  类型: {type_label}")

    return csv_path

# 使用示例
if __name__ == "__main__":
    # 从API复制的JSON数据
    api_response = {
        "code": 0,
        "msg": "success",
        "data": [
            # 粘贴API返回的data数组
        ]
    }

    # 调用保存函数
    save_price_data(
        api_data=api_response,
        target_date="2026-01-01",
        data_type="realtime"
    )
```

## 数据格式说明

### API响应结构
```json
{
  "code": 0,
  "msg": "success",
  "data": [
    {
      "watchUserPriceId": "唯一ID",
      "exchange": "00",          // 地区代码
      "price0000": "371.7845",  // 00:00价格
      "price0100": "348.1993",  // 01:00价格
      ...
      "price2300": "450.1234"   // 23:00价格
    }
  ]
}
```

### 地区代码映射
| 代码 | 地区 |
|------|------|
| 00 | 全区域 |
| 02 | 广东 |
| 03 | 广西 |
| 04 | 云南 |
| 05 | 贵州 |
| 06 | 海南 |

### CSV输出格式
```csv
时间,全区域,广东,广西,云南,贵州,海南
00:00,371.7845,387.849,373.3411,249.8317,438.4059,449.9766
01:00,348.1993,361.7443,331.3694,204.2519,425.8183,500.0455
...
23:00,450.1234,470.2341,445.3456,320.1234,520.3456,530.4567
```

## 数据类型区分

### 日前数据 (Day-Ahead)
- **dateType**: "0"
- **用途**: 次日价格预测、交易计划制定
- **更新**: 每日发布未来24小时预测
- **文件命名**: 日前价格_YYYYMMDD.csv

### 实时数据 (Real-Time)
- **dateType**: "1"
- **用途**: 实时结算、实际用电成本分析
- **更新**: 实时更新（15分钟间隔）
- **文件命名**: 实时价格_YYYYMMDD.csv

**重要**: 两种数据提取方法完全相同，仅需切换页面上的"日前/实时"按钮。

## 项目路径配置

### 工作目录
```
D:\AI\cc_pro\现货价格采集\
```

### 输出文件
```
实时价格_20260101.csv    # 实时数据
日前价格_20260101.csv    # 日前数据
```

### 参考文档
- `提取方法说明.md` - 详细提取指南
- `快速操作指南.md` - 5分钟快速上手
- `实时数据与日前数据区别说明.md` - 数据类型对比

## 常见问题处理

### Q1: 找不到 getWatchUserPriceData 接口？
**解决方案**:
- 确保已点击"用电侧成交价格"标签
- 检查Network筛选器是否设置为"XHR"
- 确认已勾选"Preserve log"
- 刷新页面重新触发请求

### Q2: API返回空数据？
**解决方案**:
- 检查登录状态是否有效
- 确认日期参数格式正确（YYYY-MM-DD）
- 验证目标日期是否有数据
- 检查dateType参数（"0"或"1"）

### Q3: CSV文件乱码？
**解决方案**:
- 使用Excel打开时选择UTF-8编码
- 或用记事本/VSCode直接查看
- 脚本已使用utf-8-sig编码确保兼容性

### Q4: 数据不完整（缺少某些时段）？
**解决方案**:
- 实时数据：部分时段可能尚未发生
- 日前数据：可能在00:00后才完全生成
- 检查原始JSON数据是否包含所有时段
- 验证所有地区代码都存在

## 完整工作流示例

### 单日数据采集
```bash
# 1. 登录系统并提取API数据（手动操作）
#    - 访问交易平台
#    - 打开DevTools
#    - 选择日期和数据类型
#    - 复制JSON响应

# 2. 运行处理脚本
cd D:\AI\cc_pro\现货价格采集
python process_spot_price.py

# 3. 验证输出
#    - 检查CSV文件
#    - 确认数据完整性
#    - 查看统计信息
```

### 批量采集示例
```python
dates = ["2026-01-01", "2026-01-02", "2026-01-03"]

for date in dates:
    print(f"正在采集 {date} 的实时数据...")
    # 1. 手动切换日期并复制API数据
    # 2. 处理并保存
    save_price_data(api_data, date, "realtime")
```

## 数据验证检查清单

采集完成后验证：
- [ ] CSV文件包含24行数据（不含标题）
- [ ] 所有6个地区都有数据
- [ ] 价格值合理（非负、非异常大）
- [ ] 文件命名正确（日期、类型匹配）
- [ ] 文件保存在正确目录
- [ ] 数据可被Excel/Pandas正确读取

## 最佳实践

1. **命名规范**: 严格遵循 `类型_YYYYMMDD.csv` 格式
2. **备份策略**: 采集后立即备份原始JSON数据
3. **数据验证**: 每次采集后检查数据完整性
4. **批量处理**: 使用脚本自动化重复性工作
5. **错误处理**: 采集失败时记录详细错误信息
6. **版本控制**: 为不同批次数据添加版本标识

## 技术支持

如遇到问题：
1. 查阅 `现货价格采集` 目录下的参考文档
2. 检查系统登录状态和网络连接
3. 验证日期格式和数据类型参数
4. 对比已成功采集的数据格式

## 更新日志

- v1.0 (2025-01-03): 初始版本，支持日前/实时价格数据采集
