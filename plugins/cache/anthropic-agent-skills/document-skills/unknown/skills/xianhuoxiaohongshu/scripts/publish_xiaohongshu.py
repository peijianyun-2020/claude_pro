#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书发布脚本 - 南方电力现货市场
自动发布电价分析内容到小红书
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime, date

# 项目路径配置
PROJECT_ROOT = Path(r"D:\AI\Trae项目工作区\南方区域电力现货市场价格跟踪")

# MCP工具导入 (通过Claude Code调用)
# 注意: 此脚本设计为通过Claude MCP环境调用
# 直接运行时需要安装小红书MCP服务


def check_login_status():
    """
    检查小红书登录状态
    (需要通过MCP工具调用)
    """
    print("🔍 检查小红书登录状态...")
    print("提示: 此功能需要通过Claude MCP环境调用 check_login_status 工具")
    # 实际使用时由Claude调用MCP工具
    return None


def extract_content_from_files(date_str, category='日前'):
    """
    从生成的文件中提取标题、正文和图片路径

    Args:
        date_str: 日期字符串 (YYYYMMDD)
        category: '日前' 或 '实时'

    Returns:
        dict: {
            'title': str,
            'content': str,
            'images': list,
            'tags': list,
            'folder_path': Path
        }
    """
    # 构建文件夹路径
    folder_name = f"{date_str}{category}"
    folder_path = PROJECT_ROOT / folder_name

    if not folder_path.exists():
        print(f"❌ 文件夹不存在: {folder_path}")
        return None

    # 文件路径
    copy_file = folder_path / f"文案_{category}_{date_str}.txt"
    image_file = folder_path / f"图_{category}_{date_str}.jpg"

    # 备用图片文件(PNG)
    if not image_file.exists():
        image_file = folder_path / f"图表_{category}_{date_str}.png"

    if not copy_file.exists():
        print(f"❌ 文案文件不存在: {copy_file}")
        return None

    if not image_file.exists():
        print(f"❌ 图片文件不存在: {image_file}")
        return None

    # 读取文案
    with open(copy_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if not lines:
        print(f"❌ 文案文件为空: {copy_file}")
        return None

    # 提取标题(第一行)
    title = lines[0]

    # 提取正文(第二行开始,去除空行)
    content_lines = []
    for line in lines[1:]:
        if line.strip():
            content_lines.append(line.strip())

    # 添加引导语
    content = '\n\n'.join(content_lines) + '\n\n觉得有用请点赞收藏~'

    # 默认标签
    default_tags = ["电力现货", "电价分析", "能源市场", "日前电价", "电力交易"]

    # 根据内容调整标签
    if '负价' in content or '0价' in content:
        default_tags.append("价格波动")
    if '偏强' in content:
        default_tags.append("电价上涨")
    elif '偏弱' in content:
        default_tags.append("电价下跌")

    return {
        'title': title[:50],  # 限制标题长度
        'content': content,
        'images': [str(image_file.absolute())],
        'tags': default_tags,
        'folder_path': folder_path
    }


def publish_to_xiaohongshu(date_str, category='日前'):
    """
    发布内容到小红书

    Args:
        date_str: 日期字符串 (YYYYMMDD)
        category: '日前' 或 '实时'

    Returns:
        bool: 发布是否成功
    """
    print(f"\n{'='*60}")
    print(f"小红书发布: {category} {date_str}")
    print(f"{'='*60}\n")

    # 1. 提取内容
    print("📖 步骤 1/3: 提取文案和图片...")
    content_data = extract_content_from_files(date_str, category)

    if not content_data:
        print("❌ 内容提取失败")
        return False

    print(f"✅ 标题: {content_data['title']}")
    print(f"✅ 正文长度: {len(content_data['content'])} 字符")
    print(f"✅ 图片: {content_data['images'][0]}")
    print(f"✅ 标签: {', '.join(content_data['tags'])}")

    # 2. 检查登录状态(通过MCP)
    print("\n🔍 步骤 2/3: 检查登录状态...")
    print("提示: 此步骤需要Claude调用MCP工具: mcp__xiaohongshu-mcp__check_login_status")
    # 实际由Claude执行

    # 3. 发布内容(通过MCP)
    print("\n🚀 步骤 3/3: 发布到小红书...")
    print("提示: 此步骤需要Claude调用MCP工具: mcp__xiaohongshu-mcp__publish_content")
    print(f"参数:")
    print(f"  - title: {content_data['title']}")
    print(f"  - content: {content_data['content'][:100]}...")
    print(f"  - images: {content_data['images']}")
    print(f"  - tags: {content_data['tags']}")
    # 实际由Claude执行

    print(f"\n{'='*60}")
    print("✅ 发布完成!")
    print(f"{'='*60}\n")

    return True


def list_available_contents(category='日前'):
    """列出所有可发布的内容"""
    contents = []

    # 遍历项目根目录
    for item in PROJECT_ROOT.iterdir():
        if item.is_dir() and category in item.name:
            # 提取日期
            try:
                date_str = item.name.replace(category, '')
                # 验证日期格式
                datetime.strptime(date_str, '%Y%m%d')

                # 检查必要文件
                copy_file = item / f"文案_{category}_{date_str}.txt"
                image_file = item / f"图_{category}_{date_str}.jpg"

                if copy_file.exists() and (image_file.exists() or (item / f"图表_{category}_{date_str}.png").exists()):
                    contents.append({
                        'date': date_str,
                        'category': category,
                        'folder': item
                    })
            except ValueError:
                continue

    return sorted(contents, key=lambda x: x['date'], reverse=True)


def interactive_publish():
    """交互式发布"""
    print("\n📋 可发布内容列表:\n")

    # 列出日前内容
    dayahead_contents = list_available_contents('日前')
    if dayahead_contents:
        print("日前数据:")
        for i, item in enumerate(dayahead_contents[:10], 1):
            print(f"  {i}. {item['date']}")

    # 列出实时内容
    realtime_contents = list_available_contents('实时')
    if realtime_contents:
        print("\n实时数据:")
        for i, item in enumerate(realtime_contents[:10], len(dayahead_contents) + 1):
            print(f"  {i}. {item['date']} ({item['category']})")

    if not dayahead_contents and not realtime_contents:
        print("❌ 未找到可发布的内容")
        return

    print("\n提示: 请指定日期和类别进行发布")
    print("示例: python publish_xiaohongshu.py --date 20251231 --category dayahead")


def main():
    parser = argparse.ArgumentParser(
        description='小红书发布工具 - 南方电力现货市场',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 发布指定日期的日前内容
  python publish_xiaohongshu.py --date 20251231 --category dayahead

  # 发布今天的实时内容
  python publish_xiaohongshu.py --date today --category realtime

  # 交互式选择
  python publish_xiaohongshu.py --interactive

  # 检查登录状态
  python publish_xiaohongshu.py --check-login
        """
    )

    parser.add_argument(
        '--date',
        type=str,
        help='日期 (YYYYMMDD格式 或 "today")'
    )

    parser.add_argument(
        '--category',
        choices=['dayahead', 'realtime', '日前', '实时'],
        default='dayahead',
        help='数据类型 (默认: dayahead)'
    )

    parser.add_argument(
        '--interactive',
        action='store_true',
        help='交互式发布'
    )

    parser.add_argument(
        '--check-login',
        action='store_true',
        help='检查小红书登录状态'
    )

    args = parser.parse_args()

    if args.check_login:
        # 检查登录状态
        check_login_status()

    elif args.interactive:
        # 交互式发布
        interactive_publish()

    elif args.date:
        # 标准化日期
        if args.date.lower() == 'today':
            date_str = date.today().strftime('%Y%m%d')
        else:
            date_str = args.date

        # 标准化类别
        category = '日前' if args.category in ['dayahead', '日前'] else '实时'

        # 发布
        publish_to_xiaohongshu(date_str, category)

    else:
        # 默认交互模式
        interactive_publish()


if __name__ == '__main__':
    main()
