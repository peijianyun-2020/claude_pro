#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ邮箱读取工具 - 用户级SKILL入口
从项目目录读取配置并执行邮件读取
"""

import sys
import os
from pathlib import Path

# 添加项目skills目录到路径
project_root = Path.cwd()
skills_dir = project_root / ".claude" / "skills"
sys.path.insert(0, str(skills_dir))

# 导入并执行主脚本
if __name__ == "__main__":
    # 导入qqmail_reader模块
    import qqmail_reader

    # 解析参数
    count = 10
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            print("⚠️  无效的邮件数量，使用默认值10")

    # 从.env加载配置并执行
    qqmail_reader.load_env_file()

    email = os.getenv("QQMAIL_EMAIL")
    auth_code = os.getenv("QQMAIL_AUTH_CODE")

    if not email or not auth_code:
        print("❌ 错误: 未找到邮箱配置")
        print("请确保.env文件中配置了QQMAIL_EMAIL和QQMAIL_AUTH_CODE")
        sys.exit(1)

    # 读取并显示邮件
    emails = qqmail_reader.read_qq_mails(email, auth_code, count)
    if emails:
        qqmail_reader.display_emails(emails)

    print(f"\n{'=' * 80}")
    print("✅ 完成！")
    print(f"{'=' * 80}\n")
