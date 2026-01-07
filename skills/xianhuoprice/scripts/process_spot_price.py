"""
南方区域电力现货价格数据处理脚本（通用版本）
支持通过命令行参数指定日期和数据类型

使用方法:
    # 方式1: 从JSON文件读取数据
    python process_spot_price.py --date 2025-01-01 --type realtime --input data.json

    # 方式2: 在脚本中直接粘贴API数据
    python process_spot_price.py --date 2025-01-01 --type dayahead

    # 方式3: 使用交互式提示
    python process_spot_price.py
"""

import csv
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List


# ==================== 配置区域 ====================

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

# 默认API数据（当没有输入文件时使用）
DEFAULT_API_DATA = {
    "code": 0,
    "msg": "success",
    "data": [
        # TODO: 将API复制的JSON数据粘贴到这里
    ]
}


# ==================== 核心函数 ====================

def validate_api_data(data: Dict) -> tuple[bool, str]:
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
        return False, "'data'列表为空"

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


def generate_summary_report(csv_path: Path) -> None:
    """
    生成数据统计摘要

    参数:
        csv_path: CSV文件路径
    """
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            print("[WARNING] CSV file is empty, cannot generate summary")
            return

        print("\n[STATISTICS] Data Summary:")
        print("-"*60)

        for region in ["全区域", "广东", "广西", "云南", "贵州", "海南"]:
            prices = []
            for row in rows:
                try:
                    price = float(row[region])
                    if price > 0:  # 忽略0值
                        prices.append(price)
                except (ValueError, KeyError):
                    pass

            if prices:
                avg_price = sum(prices) / len(prices)
                max_price = max(prices)
                min_price = min(prices)

                # 找到最高价和最低价的时段
                max_hour = next(row["时间"] for row in rows if float(row.get(region, 0)) == max_price)
                min_hour = next(row["时间"] for row in rows if float(row.get(region, 0)) == min_price)

                print(f"\n{region}:")
                print(f"  - Average price: {avg_price:.2f} CNY/MWh")
                print(f"  - Highest price: {max_price:.2f} (at {max_hour})")
                print(f"  - Lowest price: {min_price:.2f} (at {min_hour})")
                print(f"  - Price range: {max_price - min_price:.2f} CNY/MWh")

        print("\n" + "="*60)

    except Exception as e:
        print(f"[WARNING] Error generating summary: {e}")


def load_api_data_from_file(file_path: str) -> Dict:
    """
    从JSON文件加载API数据

    参数:
        file_path: JSON文件路径

    返回:
        Dict: API数据
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"[INFO] Successfully loaded API data from: {file_path}")
        return data
    except Exception as e:
        raise IOError(f"Failed to load JSON file: {e}")


def parse_arguments():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        description='Process Southern Regional Electric Spot Price Data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process with date and data type
  python process_spot_price.py --date 2025-01-01 --type realtime

  # Load data from JSON file
  python process_spot_price.py --date 2025-01-01 --type dayahead --input api_data.json

  # Interactive mode (will prompt for inputs)
  python process_spot_price.py

  # Using short aliases
  python process_spot_price.py -d 20250101 -t realtime
        """
    )

    parser.add_argument(
        '-d', '--date',
        type=str,
        help='Target date (YYYY-MM-DD or YYYYMMDD)'
    )

    parser.add_argument(
        '-t', '--type',
        type=str,
        choices=['realtime', 'dayahead', 'rt', 'da'],
        help='Data type: realtime (rt) or dayahead (da)'
    )

    parser.add_argument(
        '-i', '--input',
        type=str,
        help='Input JSON file path containing API data'
    )

    parser.add_argument(
        '--no-summary',
        action='store_true',
        help='Skip generating statistical summary'
    )

    return parser.parse_args()


def interactive_prompt():
    """
    交互式提示用户输入参数
    """
    print("\n" + "="*60)
    print("Southern Regional Electric Spot Price Processor")
    print("="*60)

    # 提示输入日期
    date_input = input("\nPlease enter target date (YYYY-MM-DD or YYYYMMDD): ").strip()
    if not date_input:
        print("[ERROR] Date cannot be empty")
        return None, None

    # 提示输入数据类型
    print("\nSelect data type:")
    print("  1. Real-time (实时价格)")
    print("  2. Day-ahead (日前价格)")
    type_input = input("Please enter choice (1 or 2, default: 1): ").strip()

    if type_input == "2":
        data_type = "dayahead"
    else:
        data_type = "realtime"

    # 提示是否从文件读取
    input_file = input("\nInput JSON file path (press Enter to paste data in script): ").strip()

    return date_input, data_type, input_file


# ==================== 主程序 ====================

def main():
    """主程序入口"""
    print("\n" + "="*60)
    print("Southern Regional Electric Spot Price Data Processor")
    print("="*60)

    # 解析命令行参数
    args = parse_arguments()

    # 如果没有提供必要参数，使用交互式提示
    if not args.date or not args.type:
        date_input, type_input, input_file = interactive_prompt()
        if not date_input:
            print("[ERROR] Missing required parameters")
            return

        target_date = date_input
        data_type = type_input
        input_json = input_file if input_file else None
    else:
        target_date = args.date
        # 处理数据类型别名
        if args.type in ['rt', 'realtime']:
            data_type = 'realtime'
        else:  # 'da' or 'dayahead'
            data_type = 'dayahead'
        input_json = args.input

    # 显示配置信息
    print(f"\n[CONFIG]")
    print(f"  - Target date: {target_date}")
    print(f"  - Data type: {data_type}")
    print(f"  - Input source: {'File: ' + input_json if input_json else 'Script (paste data)'}")

    # 加载API数据
    if input_json:
        # 从文件加载
        try:
            api_data = load_api_data_from_file(input_json)
        except Exception as e:
            print(f"\n[ERROR] Failed to load input file: {e}")
            print("\n[HELP] Please ensure:")
            print("  1. File path is correct")
            print("  2. File is valid JSON format")
            print("  3. File contains 'data' field with region arrays")
            return
    else:
        # 使用脚本中的数据
        if not DEFAULT_API_DATA.get("data"):
            print("\n" + "="*60)
            print("[ERROR] No API data detected!")
            print("="*60)
            print("\n[HELP] Please use one of these methods:")
            print("")
            print("Method 1: Paste data in script")
            print("  1. Open this script in editor")
            print("  2. Find DEFAULT_API_DATA variable")
            print("  3. Paste copied JSON data into 'data' field")
            print("  4. Save and run again")
            print("")
            print("Method 2: Use JSON file")
            print("  1. Save API response to a .json file")
            print("  2. Run: python process_spot_price.py --date YYYY-MM-DD --type realtime --input your_file.json")
            print("")
            print("Method 3: Get API data from trading system")
            print("  1. Visit: https://spot.poweremarket.com/uptspot/sr/mp/portaladmin/index.html#/")
            print("  2. Open Chrome DevTools (F12) -> Network tab")
            print("  3. Find 'getWatchUserPriceData' request")
            print("  4. Copy Response data and save to JSON file")
            print("="*60 + "\n")
            return

        api_data = DEFAULT_API_DATA

    try:
        # 处理并保存数据
        csv_path = save_price_data(
            api_response=api_data,
            target_date=target_date,
            data_type=data_type
        )

        # 生成统计摘要
        if not args.no_summary:
            generate_summary_report(csv_path)

        print("\n[DONE] Processing complete! You can view data by:")
        print(f"  - Excel: Open {csv_path}")
        print(f"  - Notepad: View raw CSV")
        print(f"  - Python: pd.read_csv('{csv_path}')")
        print()

    except Exception as e:
        print(f"\n[ERROR] Processing failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
