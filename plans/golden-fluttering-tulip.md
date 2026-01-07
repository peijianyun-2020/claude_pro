# Anthropic 官方 Skills 安装计划

## 目标
将 Anthropic 官方 skills 从 GitHub 仓库安装到 Claude Code 用户级别，使其在所有项目中可用。

## 背景
- **GitHub 仓库**: https://github.com/anthropics/skills
- **目标系统**: Windows (用户目录: C:\Users\55315)
- **配置级别**: 全局（用户级别）

## 可用技能列表

### 文档处理技能 (document-skills)
- **pdf**: PDF 文档处理（提取文本、表单字段等）
- **docx**: Word 文档处理
- **xlsx**: Excel 电子表格处理
- **pptx**: PowerPoint 演示文稿处理

### 示例技能 (example-skills)
- **algorithmic-art**: 使用 p5.js 创建算法艺术
- **skill-creator**: 创建新技能的元技能
- **mcp-builder**: MCP 服务器生成器
- **webapp-testing**: Web 应用测试
- **brand-guidelines**: 品牌指南
- **canvas-design**: Canvas 设计
- **doc-coauthoring**: 文档协作
- **frontend-design**: 前端设计
- **internal-comms**: 内部沟通
- **slack-gif-creator**: Slack GIF 创建器
- **theme-factory**: 主题工厂
- **web-artifacts-builder**: Web 工件构建器

## 用户确认
- **技能包选择**: document-skills（仅文档处理技能）
- **包含技能**: pdf, docx, xlsx, pptx
- **依赖环境**: 已安装 Python 3.8+ 和 Node.js 18+

## 实施方案

### 使用 Claude Code 内置命令（推荐方案）

#### 步骤 1: 注册市场仓库
```
/plugin marketplace add anthropics/skills
```
这会从 GitHub 克隆仓库到本地并注册市场。

#### 步骤 2: 安装技能包
```
/plugin install document-skills@anthropic-agent-skills
```
这会安装四个文档处理技能：pdf, docx, xlsx, pptx

#### 步骤 3: 验证安装
```
/plugin list
```

#### 步骤 4: 测试技能
```
使用 PDF 技能从 document.pdf 提取文本
使用 DOCX 技能创建一个 Word 文档
```

## 关键文件

### 需要修改的文件
1. **C:\Users\55315\.claude\plugins\known_marketplaces.json**
   - 添加 anthropic-agent-skills 市场注册

2. **C:\Users\55315\.claude\settings.json**
   - 启用已安装的技能插件

3. **C:\Users\55315\.claude\plugins\installed_plugins.json**
   - 自动记录插件安装信息

### 需要创建的目录结构
```
C:\Users\55315\.claude\plugins\
├── marketplaces\
│   └── anthropic-agent-skills\      # GitHub 仓库克隆
│       └── .claude-plugin\
│           └── marketplace.json
└── cache\
    └── anthropic-agent-skills\
        └── document-skills\
            └── 1.0.0\
                ├── .claude-plugin\
                │   └── plugin.json
                └── skills\
                    ├── pdf\
                    ├── docx\
                    ├── xlsx\
                    └── pptx\
```

## 验证步骤

### 1. 检查市场注册
```
/plugin marketplace list
```
应显示: `anthropic-agent-skills`

### 2. 检查插件安装
```
/plugin list
```
应显示:
- `document-skills@anthropic-agent-skills` ✓

### 3. 检查文件系统
```bash
ls "C:\Users\55315\.claude\plugins\cache\anthropic-agent-skills\document-skills\1.0.0\skills"
```
应显示: pdf, docx, xlsx, pptx

### 4. 功能测试
- 测试 PDF 技能（提取文本）
- 测试 DOCX 技能（创建文档）
- 测试 XLSX 技能（处理电子表格）
- 测试 PPTX 技能（创建演示文稿）

## 潜在问题和解决方案

### 问题 1: Git 仓库克隆失败
**解决**: 手动克隆并配置

### 问题 2: 权限错误
**解决**: 以管理员身份运行或检查目录权限

### 问题 3: 技能未加载
**解决**: 检查 settings.json 并重启 Claude Code

### 问题 4: 依赖缺失
**解决**: 安装 Python 3.8+ 和 Node.js 18+

### 问题 5: Windows 路径问题
**解决**: 在 JSON 中使用双反斜杠 `\\`

## 使用示例

### PDF 处理
```
使用 PDF 技能从 report.pdf 提取所有表格
使用 PDF 技能合并 file1.pdf 和 file2.pdf
使用 PDF 技能从 invoice.pdf 提取表单字段
```

### Word 文档处理
```
使用 DOCX 技能创建一个包含标题和段落的 Word 文档
使用 DOCX 技能从 template.docx 生成报告
```

### Excel 电子表格处理
```
使用 XLSX 技能从 data.xlsx 提取销售数据
使用 XLSX 技能创建包含图表的电子表格
```

### PowerPoint 演示文稿
```
使用 PPTX 技能创建一个包含 5 张幻灯片的演示文稿
使用 PPTX 技能从 template.pptx 生成月度报告
```

## 更新和维护

### 更新技能
```
/plugin update document-skills@anthropic-agent-skills
```

### 卸载技能
```
/plugin uninstall document-skills@anthropic-agent-skills
```

### 删除市场
```
/plugin marketplace remove anthropic-agent-skills
```

## 注意事项

1. **许可证**: pdf, docx, xlsx, pptx 是 source-available，非开源
2. **依赖**: 某些技能需要 Python、Node.js 等运行时
3. **版本**: 定期更新以获取最新功能
4. **备份**: 定期备份配置文件

## 下一步

1. 执行安装步骤（3个命令）
2. 验证功能
3. 测试文档处理技能
