#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据处理脚本 - 南方电力现货市场
整合数据读取、汇总、图表生成和文案生成功能
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime, date

# 添加项目根目录到路径
PROJECT_ROOT = Path(r"D:\AI\Trae项目工作区\南方区域电力现货市场价格跟踪")
sys.path.insert(0, str(PROJECT_ROOT))

from market_processor import (
    read_price_file,
    append_to_csv,
    plot_for_date,
    analyze_and_write_copy,
    get_output_dir,
    DAYAHEAD_DIR,
    REALTIME_DIR
)


def process_date(target_date, category='日前'):
    """
    处理指定日期的数据

    Args:
        target_date: 日期对象或字符串 (YYYYMMDD)
        category: '日前' 或 '实时'

    Returns:
        tuple: (图表路径, 文案路径) 或 (None, None)
    """
    # 解析日期
    if isinstance(target_date, str):
        if target_date.lower() == 'today':
            target_date = date.today()
        else:
            target_date = datetime.strptime(target_date, '%Y%m%d').date()

    # 确定数据目录
    data_dir = DAYAHEAD_DIR if category == '日前' else REALTIME_DIR
    date_str = target_date.strftime('%Y%m%d')
    filename = f"{date_str}{category}.xlsx"
    file_path = data_dir / filename

    # 检查文件是否存在
    if not file_path.exists():
        print(f"❌ 未找到数据文件: {file_path}")
        return None, None

    print(f"\n{'='*60}")
    print(f"开始处理: {category} {date_str}")
    print(f"{'='*60}\n")

    # 1. 读取数据
    print("📖 步骤 1/4: 读取 Excel 数据...")
    df_day = read_price_file(file_path, target_date)
    if df_day is None or df_day.empty:
        print("❌ 数据读取失败或为空")
        return None, None

    # 2. 追加到汇总库
    print("\n💾 步骤 2/4: 更新汇总数据库...")
    df_all = append_to_csv(df_day, category)
    if df_all is None:
        print("❌ 数据汇总失败")
        return None, None

    # 3. 生成图表
    print("\n📊 步骤 3/4: 生成价格曲线图...")
    output_dir = get_output_dir(category, target_date)
    chart_path = plot_for_date(df_all, category, target_date, output_dir)
    if chart_path:
        print(f"✅ 图表已生成: {chart_path}")

    # 4. 生成文案
    print("\n✍️  步骤 4/4: 生成分析文案...")
    copy_path = analyze_and_write_copy(df_all, category, target_date, output_dir)
    if copy_path:
        print(f"✅ 文案已生成: {copy_path}")

    print(f"\n{'='*60}")
    print("✅ 处理完成!")
    print(f"输出目录: {output_dir}")
    print(f"{'='*60}\n")

    return chart_path, copy_path


def process_batch(category='日前'):
    """批量处理所有待处理文件"""
    data_dir = DAYAHEAD_DIR if category == '日前' else REALTIME_DIR

    if not data_dir.exists():
        print(f"❌ 数据目录不存在: {data_dir}")
        return

    # 列出所有Excel文件
    excel_files = list(data_dir.glob('*.xlsx')) + list(data_dir.glob('*.xls'))

    if not excel_files:
        print(f"❌ 未找到Excel文件: {data_dir}")
        return

    print(f"找到 {len(excel_files)} 个文件，开始批量处理...\n")

    success_count = 0
    failed_files = []

    for file_path in excel_files:
        # 从文件名解析日期
        date_match = None
        import re
        match = re.search(r'(\d{8})', file_path.name)
        if match:
            date_str = match.group(1)
            try:
                target_date = datetime.strptime(date_str, '%Y%m%d').date()

                # 处理文件
                chart_path, copy_path = process_date(target_date, category)

                if chart_path and copy_path:
                    success_count += 1
                else:
                    failed_files.append(file_path.name)

            except ValueError as e:
                print(f"❌ 无法解析日期: {file_path.name} - {e}")
                failed_files.append(file_path.name)
        else:
            print(f"⚠️  跳过文件(无法解析日期): {file_path.name}")

    # 输出汇总
    print(f"\n{'='*60}")
    print(f"批量处理完成!")
    print(f"成功: {success_count}/{len(excel_files)}")
    if failed_files:
        print(f"失败: {len(failed_files)}")
        for f in failed_files:
            print(f"  - {f}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='南方电力现货市场数据处理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 处理指定日期的日前数据
  python process_data.py --type dayahead --date 20251231

  # 处理今天的实时数据
  python process_data.py --type realtime --date today

  # 批量处理所有日前数据
  python process_data.py --type dayahead --batch
        """
    )

    parser.add_argument(
        '--type',
        choices=['dayahead', 'realtime', '日前', '实时'],
        default='dayahead',
        help='数据类型 (默认: dayahead)'
    )

    parser.add_argument(
        '--date',
        type=str,
        help='日期 (YYYYMMDD格式 或 "today")'
    )

    parser.add_argument(
        '--batch',
        action='store_true',
        help='批量处理所有文件'
    )

    args = parser.parse_args()

    # 标准化类别名称
    category = '日前' if args.type in ['dayahead', '日前'] else '实时'

    if args.batch:
        # 批量模式
        process_batch(category)
    elif args.date:
        # 单日期模式
        process_date(args.date, category)
    else:
        # 默认处理今天
        process_date('today', category)


if __name__ == '__main__':
    main()
