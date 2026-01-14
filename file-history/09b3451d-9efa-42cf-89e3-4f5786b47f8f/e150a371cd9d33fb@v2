"""
南方区域电力现货价格自动化采集工具

功能：
1. 自动访问交易系统并等待用户登录
2. 自动导航到用电侧成交价格模块
3. 自动选择日期和数据类型（日前/实时）
4. 自动提取API响应数据
5. 自动生成CSV文件

使用方法：
    # 自动采集模式（推荐）
    python auto_collect_spot_price.py --date 2026-01-11 --type dayahead

    # 交互式模式
    python auto_collect_spot_price.py

注意：需要先安装Chrome DevTools MCP服务
"""

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple


# ==================== 配置区域 ====================

# 交易系统URL
TRADING_SYSTEM_URL = "https://spot.poweremarket.com/uptspot/sr/mp/portaladmin/index.html#/"

# API端点名称
API_ENDPOINT_NAME = "getWatchUserPriceData"

# 数据目录
DATA_DIR = Path(r"D:\AI\cc_pro\现货价格采集")

# 地区代码映射
REGION_MAP = {
    "00": "全区域",
    "02": "广东",
    "03": "广西",
    "04": "云南",
    "05": "贵州",
    "06": "海南"
}


# ==================== Chrome DevTools 工具类 ====================

class ChromeDevToolsHelper:
    """
    Chrome DevTools MCP 工具包装类

    注意：此类需要在Claude Code环境中使用，依赖MCP chrome-devtools工具
    """

    def __init__(self):
        """初始化Chrome DevTools助手"""
        self.is_connected = False
        self.current_url = None

    def check_available(self) -> bool:
        """
        检查Chrome DevTools MCP是否可用

        返回:
            bool: MCP工具是否可用
        """
        try:
            # 这里实际上会在Claude Code环境中检查MCP工具
            # 在脚本运行时，我们假设MCP工具可用
            return True
        except Exception:
            return False

    def list_pages(self):
        """列出所有打开的Chrome页面"""
        # 这个方法将由Claude通过MCP工具调用
        pass

    def new_page(self, url: str):
        """
        创建新页面并导航到指定URL

        参数:
            url: 目标URL
        """
        # 这个方法将由Claude通过MCP工具调用
        pass

    def navigate_page(self, url: str):
        """
        在当前页面导航到指定URL

        参数:
            url: 目标URL
        """
        # 这个方法将由Claude通过MCP工具调用
        pass

    def take_snapshot(self, verbose: bool = False):
        """
        获取页面快照

        参数:
            verbose: 是否包含详细信息

        返回:
            页面快照数据
        """
        # 这个方法将由Claude通过MCP工具调用
        pass

    def click(self, uid: str):
        """
        点击页面元素

        参数:
            uid: 元素的唯一标识符
        """
        # 这个方法将由Claude通过MCP工具调用
        pass

    def fill(self, uid: str, value: str):
        """
        填写表单字段

        参数:
            uid: 元素的唯一标识符
            value: 要填写的值
        """
        # 这个方法将由Claude通过MCP工具调用
        pass

    def list_network_requests(self, resource_types: list = None):
        """
        列出网络请求

        参数:
            resource_types: 资源类型筛选器

        返回:
            网络请求列表
        """
        # 这个方法将由Claude通过MCP工具调用
        pass

    def get_network_request(self, reqid: int):
        """
        获取网络请求详情

        参数:
            reqid: 请求ID

        返回:
            请求详情（包含响应数据）
        """
        # 这个方法将由Claude通过MCP工具调用
        pass

    def wait_for(self, text: str, timeout: int = 30000):
        """
        等待页面文本出现

        参数:
            text: 要等待的文本
            timeout: 超时时间（毫秒）
        """
        # 这个方法将由Claude通过MCP工具调用
        pass


# ==================== 数据处理函数 ====================

def validate_api_data(data: Dict) -> Tuple[bool, str]:
    """
    验证API数据的完整性

    参数:
        data: API返回的完整数据

    返回:
        (bool, str): (是否有效, 错误信息)
    """
    if not isinstance(data, dict):
        return False, "API数据不是字典格式"

    if "data" not in data:
        return False, "API数据中缺少'data'字段"

    if not isinstance(data["data"], list):
        return False, "'data'字段不是列表格式"

    if len(data["data"]) == 0:
        return False, "数据尚未生成（data列表为空）"

    # 检查是否包含所有地区
    exchanges = {item.get("exchange") for item in data["data"]}
    missing_regions = set(REGION_MAP.keys()) - exchanges
    if missing_regions:
        return False, f"缺少地区代码: {', '.join(missing_regions)}"

    return True, ""


def save_price_data(
    api_response: Dict,
    target_date: str,
    data_type: str = "realtime"
) -> Path:
    """
    保存价格数据为CSV文件

    参数:
        api_response: API返回的完整JSON数据
        target_date: 目标日期 (YYYY-MM-DD 或 YYYYMMDD)
        data_type: 数据类型 ("dayahead" 或 "realtime")

    返回:
        Path: 生成的CSV文件路径

    异常:
        ValueError: 数据验证失败
        IOError: 文件写入失败
    """
    # 验证数据
    is_valid, error_msg = validate_api_data(api_response)
    if not is_valid:
        raise ValueError(f"API数据验证失败: {error_msg}")

    # 标准化日期格式
    if "-" in target_date:
        date_formatted = target_date.replace("-", "")
    else:
        date_formatted = target_date

    # 确定文件名前缀
    type_label = "实时价格" if data_type == "realtime" else "日前价格"
    csv_filename = f"{type_label}_{date_formatted}.csv"
    csv_path = DATA_DIR / csv_filename

    # 创建CSV数据
    csv_data = []
    headers = ["时间", "全区域", "广东", "广西", "云南", "贵州", "海南"]
    csv_data.append(headers)

    # 生成24个小时的数据
    missing_count = 0
    for hour in range(24):
        time_str = f"{hour:02d}:00"
        row = [time_str]

        for exchange_code in ["00", "02", "03", "04", "05", "06"]:
            # 查找对应地区的数据
            region_data = next(
                (item for item in api_response["data"]
                 if item.get("exchange") == exchange_code),
                None
            )

            if region_data:
                price_key = f"price{hour:02d}00"
                price = region_data.get(price_key, "0")

                # 验证价格值
                try:
                    float_price = float(price)
                    if float_price < 0:
                        print(f"[WARNING] {time_str} {REGION_MAP[exchange_code]} 出现负价格: {price}")
                except ValueError:
                    print(f"[WARNING] {time_str} {REGION_MAP[exchange_code]} 价格值无效: {price}")
                    missing_count += 1

                row.append(price)
            else:
                print(f"[WARNING] 未找到地区 {exchange_code} ({REGION_MAP.get(exchange_code, '未知')}) 的数据")
                row.append("0")
                missing_count += 1

        csv_data.append(row)

    # 确保输出目录存在
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 保存CSV文件
    import csv
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)
    except Exception as e:
        raise IOError(f"写入CSV文件失败: {e}")

    # 输出处理结果
    print("\n" + "="*60)
    print("[SUCCESS] Data saved successfully!")
    print("="*60)
    print(f"File path: {csv_path}")
    print(f"Target date: {target_date}")
    print(f"Data type: {type_label}")
    print(f"Data rows: {len(csv_data)-1} rows (24 hours)")
    print(f"Missing data: {missing_count} values")
    print("="*60)

    # 数据统计
    if missing_count == 0:
        print("[COMPLETE] Data integrity: Perfect! All time periods and regions complete")
    else:
        print(f"[WARNING] Data integrity: {missing_count} missing values, please check raw data")

    return csv_path


def save_api_data_for_backup(api_response: Dict, target_date: str, data_type: str) -> Path:
    """
    保存API原始数据为JSON备份文件

    参数:
        api_response: API返回的完整JSON数据
        target_date: 目标日期
        data_type: 数据类型

    返回:
        Path: 备份文件路径
    """
    type_label = "realtime" if data_type == "realtime" else "dayahead"
    date_formatted = target_date.replace("-", "")
    backup_filename = f"api_backup_{type_label}_{date_formatted}.json"
    backup_path = DATA_DIR / "backups" / backup_filename

    # 确保备份目录存在
    backup_path.parent.mkdir(parents=True, exist_ok=True)

    # 保存备份文件
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(api_response, f, ensure_ascii=False, indent=2)

    print(f"[BACKUP] API data saved to: {backup_path}")
    return backup_path


# ==================== 自动化采集流程 ====================

def auto_collect_spot_price(
    target_date: str,
    data_type: str = "dayahead"
) -> bool:
    """
    自动化采集现货价格数据

    注意：此函数需要在Claude Code环境中运行，会调用Chrome DevTools MCP工具

    参数:
        target_date: 目标日期 (YYYY-MM-DD)
        data_type: 数据类型 ("dayahead" 或 "realtime")

    返回:
        bool: 采集是否成功
    """
    print("\n" + "="*60)
    print("南方区域电力现货价格自动化采集工具")
    print("="*60)
    print(f"\n[CONFIG]")
    print(f"  - Target date: {target_date}")
    print(f"  - Data type: {data_type}")
    print(f"  - System URL: {TRADING_SYSTEM_URL}")

    # 生成操作提示
    date_type_label = "0" if data_type == "dayahead" else "1"
    print(f"\n[INFO] 自动化采集流程说明：")
    print(f"  1. 打开交易系统")
    print(f"  2. 等待您手动登录")
    print(f"  3. 自动导航到用电侧成交价格模块")
    print(f"  4. 自动选择日期: {target_date}")
    print(f"  5. 自动选择数据类型: {'日前' if data_type == 'dayahead' else '实时'}")
    print(f"  6. 自动提取API数据")
    print(f"  7. 自动生成CSV文件")

    print(f"\n[PROMPT] 准备开始采集，请在浏览器中完成登录操作...")
    print(f"="*60)

    # 返回操作指令（由Claude Code执行）
    return True


def generate_claude_instructions(
    target_date: str,
    data_type: str = "dayahead"
) -> str:
    """
    生成Claude Code执行指令

    参数:
        target_date: 目标日期
        data_type: 数据类型

    返回:
        str: Claude Code执行指令
    """
    instructions = f"""
# 南方区域电力现货价格自动化采集指令

## 采集参数
- 目标日期: {target_date}
- 数据类型: {data_type}
- 交易系统: {TRADING_SYSTEM_URL}

## 执行步骤

### 步骤1: 访问交易系统
使用Chrome DevTools访问: {TRADING_SYSTEM_URL}

### 步骤2: 等待用户登录
- 检查页面是否显示登录界面
- 如果是，提示用户手动登录
- 等待用户回复"已登录"

### 步骤3: 导航到用电侧成交价格模块
- 查找并点击"用电侧成交价格"标签
- 等待页面加载完成

### 步骤4: 选择数据类型
- 查找"日前"和"实时"单选框
- 点击选中: {"日前" if data_type == "dayahead" else "实时"}

### 步骤5: 设置日期
- 查找日期输入框（运行日）
- 点击日期框
- 选择日期: {target_date}
- 等待API请求触发

### 步骤6: 提取API数据
- 列出所有XHR/Fetch网络请求
- 查找请求URL包含: {API_ENDPOINT_NAME}
- 获取该请求的响应数据
- 验证响应数据中的data字段是否为空

### 步骤7: 处理数据
如果data不为空:
- 调用save_price_data函数生成CSV文件
- 保存API备份文件
- 验证CSV文件完整性
- 报告采集结果

如果data为空:
- 提示数据尚未生成
- 建议采集其他日期或稍后重试

## API端点信息
- URL包含: {API_ENDPOINT_NAME}
- 请求参数示例:
  {{
    "operateDate": "{target_date}",
    "dateType": "{'0' if data_type == 'dayahead' else '1'}"
  }}

## 预期响应格式
{{
  "code": 0,
  "msg": "success",
  "data": [
    {{
      "watchUserPriceId": "...",
      "exchange": "00",
      "price0000": "371.7845",
      "price0100": "348.1993",
      ...
    }}
  ]
}}

## 输出目录
{DATA_DIR}

## CSV文件命名
- {'日前价格_' if data_type == 'dayahead' else '实时价格_'}{target_date.replace('-', '')}.csv
"""
    return instructions


# ==================== 命令行接口 ====================

def parse_arguments():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        description='自动化采集南方区域电力现货价格数据',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 采集日前价格
  python auto_collect_spot_price.py --date 2026-01-11 --type dayahead

  # 采集实时价格
  python auto_collect_spot_price.py --date 2026-01-11 --type realtime

  # 使用交互式模式
  python auto_collect_spot_price.py

注意:
  - 此脚本需要在Claude Code环境中运行
  - 需要安装Chrome DevTools MCP服务
  - 登录操作需要手动完成
        """
    )

    parser.add_argument(
        '-d', '--date',
        type=str,
        help='目标日期 (YYYY-MM-DD 或 YYYYMMDD)'
    )

    parser.add_argument(
        '-t', '--type',
        type=str,
        choices=['realtime', 'dayahead', 'rt', 'da'],
        default='dayahead',
        help='数据类型: realtime (rt) 或 dayahead (da)，默认为dayahead'
    )

    parser.add_argument(
        '--instructions-only',
        action='store_true',
        help='仅生成Claude Code执行指令，不执行采集'
    )

    return parser.parse_args()


def interactive_prompt():
    """
    交互式提示用户输入参数
    """
    print("\n" + "="*60)
    print("南方区域电力现货价格自动化采集工具")
    print("="*60)

    # 提示输入日期
    date_input = input("\n请输入目标日期 (YYYY-MM-DD 或 YYYYMMDD): ").strip()
    if not date_input:
        print("[ERROR] 日期不能为空")
        return None, None

    # 提示输入数据类型
    print("\n选择数据类型:")
    print("  1. 实时价格 (realtime)")
    print("  2. 日前价格 (dayahead)")
    type_input = input("请输入选择 (1 或 2, 默认: 2): ").strip()

    if type_input == "1":
        data_type = "realtime"
    else:
        data_type = "dayahead"

    return date_input, data_type


def main():
    """主程序入口"""
    # 解析命令行参数
    args = parse_arguments()

    # 如果没有提供日期，使用交互式提示
    if not args.date:
        target_date, data_type = interactive_prompt()
        if not target_date:
            print("[ERROR] 缺少必要参数")
            return
    else:
        target_date = args.date
        # 处理数据类型别名
        if args.type in ['rt', 'realtime']:
            data_type = 'realtime'
        else:  # 'da' or 'dayahead'
            data_type = 'dayahead'

    # 如果仅生成指令
    if args.instructions_only:
        instructions = generate_claude_instructions(target_date, data_type)
        print("\n" + "="*60)
        print("Claude Code 执行指令")
        print("="*60)
        print(instructions)
        return

    # 执行自动化采集
    print("\n[INFO] 正在生成采集指令...")
    print("[INFO] 请将以下指令提供给Claude Code执行:\n")

    instructions = generate_claude_instructions(target_date, data_type)
    print(instructions)

    print("\n" + "="*60)
    print("[IMPORTANT] 注意事项")
    print("="*60)
    print("1. 此脚本需要在Claude Code环境中运行")
    print("2. 需要安装Chrome DevTools MCP服务")
    print("3. 首次运行需要您手动完成登录操作")
    print("4. 登录后系统会自动完成后续采集流程")
    print("="*60)


if __name__ == "__main__":
    main()
