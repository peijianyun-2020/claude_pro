# 飞书多维表格 MCP 服务器实现方案

## 需求概述

创建一个飞书多维表格 MCP 服务器，用于将 Claude Code 中获取的数据（社交媒体数据、监控数据等）自动写入飞书多维表格。

**核心需求：**
- 数据类型：小红书/抖音社交媒体数据 + 监控/爬虫数据
- 操作模式：追加或更新（根据关键字段判断是否存在）
- 凭证方式：个人飞书账号

## 实现方案

### 架构设计

```
Claude Code → MCP Server → 飞书开放平台 API → 飞书多维表格
                ↑
           Python MCP Server
```

### 核心功能

1. **认证管理**
   - 支持个人应用凭证（App ID + App Secret）
   - 自动刷新访问令牌

2. **数据写入工具**
   - `write_record`: 写入单条记录
   - `batch_write_records`: 批量写入记录
   - `upsert_record`: 追加或更新记录（根据指定字段查找）

3. **数据查询工具**
   - `find_record`: 根据条件查找记录
   - `get_table_schema`: 获取表格字段结构

### 文件结构

```
D:\AI\cc_pro\program\202601 CLAUDE CODE链接飞书\
├── feishu-bitable-mcp/    # MCP 服务器主目录
│   ├── server.py          # MCP 服务器主文件
│   ├── feishu_client.py   # 飞书 API 客户端
│   ├── config.json        # 配置文件模板
│   ├── requirements.txt   # Python 依赖
│   └── README.md          # 使用说明
├── docs/                  # 项目文档
│   ├── 飞书应用创建指南.md
│   ├── 使用说明.md
│   └── 故障排查.md
└── install.cmd            # Windows 安装脚本
```

## 实现步骤

### 步骤 1: 创建飞书应用（用户手动操作）

1. 访问飞书开放平台：https://open.feishu.cn/app
2. 创建企业自建应用（个人账号也可以创建）
3. 获取 App ID 和 App Secret
4. 申请权限：
   - `bitable:app` - 读写多维表格
   - `bitable:app:readonly` - 读取表格（用于查重）
5. 发布应用（个人应用直接发布即可）

### 步骤 2: 获取多维表格信息

从飞书表格 URL 中提取：
- `app_token`: 表格应用 token
- `table_id`: 数据表 ID

URL 格式：`https://feishu.cn/base/app_token?table=table_id`

### 步骤 3: 开发 MCP 服务器

**关键文件：`feishu-bitable-mcp/server.py`**

功能：
- 实现 MCP 工具接口
- 提供 `upsert_record` 工具（核心功能）
- 支持字段映射和类型转换

**关键文件：`feishu-bitable-mcp/feishu_client.py`**

功能：
- 封装飞书 API 调用
- 处理认证令牌获取和刷新
- 实现记录查找、创建、更新逻辑

**关键文件：`docs/飞书应用创建指南.md`**

功能：
- 详细的飞书应用创建步骤
- 权限申请指南
- 如何获取 app_token 和 table_id

**关键文件：`docs/使用说明.md`**

功能：
- MCP 服务器安装和配置步骤
- 使用示例和最佳实践
- 常见问题解答

### 步骤 4: MCP 服务器配置

在 Claude Code 中配置服务器：

**方式 1: 命令行安装**
```bash
claude mcp add feishu-bitable python "D:/AI/cc_pro/program/202601 CLAUDE CODE链接飞书/feishu-bitable-mcp/server.py"
```

**方式 2: 配置文件**
在 Claude 配置中添加：
```json
{
  "mcpServers": {
    "feishu-bitable": {
      "command": "python",
      "args": ["D:/AI/cc_pro/program/202601 CLAUDE CODE链接飞书/feishu-bitable-mcp/server.py"],
      "env": {
        "FEISHU_APP_ID": "cli_xxx",
        "FEISHU_APP_SECRET": "xxx",
        "FEISHU_APP_TOKEN": "xxx",
        "FEISHU_TABLE_ID": "xxx"
      }
    }
  }
}
```

### 步骤 5: 使用示例

在对话中调用：

```
# 写入小红书笔记数据
将这个小红书笔记写入飞书表格：
- 标题：xxx
- 作者：xxx
- 点赞数：xxx

# 批量写入监控数据
将以下监控数据写入飞书表格：
[数据列表]
```

## 关键文件路径

**需要创建的文件：**
- `D:\AI\cc_pro\program\202601 CLAUDE CODE链接飞书\feishu-bitable-mcp\server.py`
- `D:\AI\cc_pro\program\202601 CLAUDE CODE链接飞书\feishu-bitable-mcp\feishu_client.py`
- `D:\AI\cc_pro\program\202601 CLAUDE CODE链接飞书\feishu-bitable-mcp\requirements.txt`
- `D:\AI\cc_pro\program\202601 CLAUDE CODE链接飞书\feishu-bitable-mcp\config.json.template`
- `D:\AI\cc_pro\program\202601 CLAUDE CODE链接飞书\docs\飞书应用创建指南.md`
- `D:\AI\cc_pro\program\202601 CLAUDE CODE链接飞书\docs\使用说明.md`
- `D:\AI\cc_pro\program\202601 CLAUDE CODE链接飞书\docs\故障排查.md`
- `D:\AI\cc_pro\program\202601 CLAUDE CODE链接飞书\install.cmd`

**需要修改的配置：**
- Claude MCP 配置文件（位置待定）

**项目输出：**
- 完整的 MCP 服务器代码
- 飞书应用配置文档
- 使用示例和测试脚本
- 项目总结文档（记录开发过程和遇到的问题）

## 数据流程

### 追加或更新逻辑

```
1. 接收数据
   ↓
2. 检查唯一字段（如笔记ID、链接等）
   ↓
3. 调用 find_record 查找是否存在
   ↓
4a. 存在 → 调用 update_record 更新
4b. 不存在 → 调用 create_record 创建
   ↓
5. 返回操作结果
```

### 示例数据结构

**小红书笔记数据：**
```json
{
  "title": "笔记标题",
  "author": "作者昵称",
  "likes": 1234,
  "collects": 567,
  "comments": 89,
  "url": "https://xiaohongshu.com/...",
  "note_id": "唯一ID",
  "publish_time": "2026-01-12",
  "tags": ["标签1", "标签2"]
}
```

**监控数据：**
```json
{
  "timestamp": "2026-01-12 10:30:00",
  "metric_name": "价格",
  "value": 123.45,
  "source": "数据来源",
  "region": "地区"
}
```

## 验证步骤

1. **安装验证**
   - 运行安装脚本
   - 检查 Python 依赖安装成功
   - 验证 MCP 服务器可被 Claude Code 调用

2. **连接验证**
   - 测试飞书 API 认证
   - 验证可访问指定的多维表格
   - 检查权限配置正确

3. **功能验证**
   - 测试追加新记录
   - 测试更新已有记录
   - 测试批量写入
   - 验证字段类型转换正确

4. **集成验证**
   - 在对话中调用 MCP 工具
   - 验证从小红书 skill 获取的数据可写入
   - 验证从抖音 skill 获取的数据可写入
   - 验证监控数据可写入

## 飞书 API 参考

- **认证**: `POST /auth/v3/tenant_access_token/internal`
- **查找记录**: `GET /bitable/v1/apps/{app_token}/tables/{table_id}/records`
- **创建记录**: `POST /bitable/v1/apps/{app_token}/tables/{table_id}/records`
- **更新记录**: `PUT /bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}`
- **批量操作**: `POST /bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create`

## 注意事项

1. **权限申请**：确保应用有足够的权限访问多维表格
2. **频率限制**：飞书 API 有频率限制，大量数据需分批处理
3. **字段类型**：飞书多维表格字段类型需与数据匹配
4. **唯一标识**：建议为每类数据定义唯一字段用于查重
5. **安全性**：不要将 App Secret 提交到代码仓库

## 扩展功能（可选）

1. 支持多个表格配置
2. 自动创建数据表
3. 数据验证和错误处理
4. 数据格式转换（如日期格式）
5. 支持附件上传（如图片）
