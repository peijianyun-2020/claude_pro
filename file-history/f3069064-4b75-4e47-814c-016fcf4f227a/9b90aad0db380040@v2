# 微信公众号采集工具实施计划

## 需求概述

开发一个微信公众号文章采集工具，支持两种使用方式：
1. **给定公众号名称**：采集近期（如近3个月）的文章并保存到本地
2. **给定文章链接**：保存单篇文章到本地

**保存格式**：Markdown格式 + 纯文本结构化数据 + 图片下载

**技术方案**：使用Chrome DevTools MCP工具，通过浏览器访问采集（简单可靠，无需API）

---

## 技术架构

### 1. Chrome DevTools MCP集成
- 使用 `mcp__chrome-devtools__` 工具集访问微信文章
- 核心工具：
  - `navigate_page`：导航到文章URL
  - `take_snapshot`：获取页面快照（基于a11y树）
  - `evaluate_script`：执行JavaScript提取HTML内容
  - `take_screenshot`：截图（可选）

### 2. 单篇文章采集流程
1. 使用 `navigate_page` 打开文章链接
2. 使用 `take_snapshot` 获取页面结构，提取：
   - 标题、作者、公众号名称、发布时间
   - 正文内容（通过 `evaluate_script` 获取HTML）
   - 所有图片URL
3. 使用 `markdownify` 将HTML转为Markdown
4. 使用 `requests` 下载图片到本地
5. 替换Markdown中的图片URL为本地路径
6. 保存Markdown文件和JSON元数据

### 3. 公众号历史文章采集流程
**方案A：从文章页面获取"相关文章"链接**
- 从任意一篇文章页面提取"相关文章"列表
- 逐个访问采集
- 适合获取同一公众号的多篇文章

**方案B：手动提供文章链接列表**
- 用户提供一个包含多个文章链接的文本文件
- 程序逐个读取链接并采集
- 简单可靠，适合小规模采集

### 4. 数据存储
- 按公众号名称创建目录
- Markdown文件命名：`YYYY-MM-DD_标题.md`
- JSON文件存储结构化数据：标题、链接、发布时间、作者等

---

## 文件结构

```
wechat_collector/
├── config.py                 # 配置文件（存储路径等）
├── chrome_collector.py      # Chrome DevTools MCP采集器
├── article_parser.py        # 文章解析器（提取HTML内容）
├── markdown_generator.py    # Markdown生成器
├── image_downloader.py      # 图片下载器
├── wechat_collector.py      # 主程序（命令行接口）
├── utils.py                 # 工具函数
├── requirements.txt         # 依赖包
└── README.md                # 使用说明
```

---

## 核心功能实现

### 功能1：单篇文章采集
**输入**：文章链接（如 `https://mp.weixin.qq.com/s/5cuBvvdfHuunxzW825fNHA`）

**流程**：
```python
# 1. 打开文章页面
chrome_devtools.navigate_page(url=article_url)

# 2. 获取页面快照，提取元数据
snapshot = chrome_devtools.take_snapshot()
# 从快照中提取：标题、作者、公众号名称、发布时间

# 3. 使用JavaScript获取HTML内容
html_content = chrome_devtools.evaluate_script(
    function="() => { return document.body.innerHTML; }"
)

# 4. 解析HTML，提取正文和图片
soup = BeautifulSoup(html_content, 'lxml')
content_div = soup.select_one('#js_content')
images = soup.select('img')

# 5. 转换为Markdown
markdown_text = markdownify(str(content_div))

# 6. 下载图片
for img_url in image_urls:
    download_image(img_url, save_path)

# 7. 保存文件
save_markdown(markdown_text, metadata)
```

**输出**：
- `2026-01-04_《电力中长期市场基本规则》解读：总则和总体要求.md`
- `2026-01-04_《电力中长期市场基本规则》解读_metadata.json`
- `images/` 目录（包含所有图片）

### 功能2：从"相关文章"采集多篇
**输入**：一篇公众号文章链接

**流程**：
1. 打开文章页面
2. 从页面快照中提取"相关文章"链接（uid=1_236到uid=1_253之间的链接）
3. 逐个访问这些链接并调用"功能1"
4. 可选择采集深度（只采集直接相关，还是递归采集）

**输出**：
- 多篇Markdown文件
- `index.json`（包含所有文章的元数据）

### 功能3：批量采集（从文件读取链接）
**输入**：包含文章链接的文本文件（`links.txt`）

**流程**：
1. 读取 `links.txt`，每行一个链接
2. 逐个调用"功能1"采集
3. 显示进度和错误日志

**输出**：
- 所有文章的Markdown文件
- `collection_metadata.json`（整体元数据）

---

## 关键技术点

### 1. Chrome DevTools MCP调用示例
```python
# 打开页面
mcp__chrome-devtools__navigate_page(url="https://mp.weixin.qq.com/s/...")

# 获取快照
snapshot = mcp__chrome-devtools__take_snapshot()
# 返回结构化文本，包含uid和元素内容

# 执行JavaScript提取HTML
html = mcp__chrome-devtools__evaluate_script(
    function="""
    () => {
        return {
            title: document.querySelector('h1')?.innerText,
            author: document.querySelector('#js_author_name')?.innerText,
            content: document.querySelector('#js_content')?.innerHTML,
            images: Array.from(document.querySelectorAll('img'))
                .map(img => img.src)
        };
    }
    """
)
```

### 2. 从页面快照提取元数据
基于实际测试，页面快照包含：
- uid=1_1: 标题（heading level 1）
- uid=1_3: 作者
- uid=1_5: 公众号名称
- uid=1_6: 发布时间
- uid=1_14及以后: 正文内容

### 3. Markdown转换和图片处理
```python
from markdownify import markdownify as md
import requests
from pathlib import Path

# 转换HTML为Markdown
markdown_text = md(str(content_div))

# 下载图片
def download_image(url, save_dir):
    response = requests.get(url)
    filename = Path(url).name
    filepath = Path(save_dir) / filename
    filepath.write_bytes(response.content)
    return filepath

# 替换图片URL为本地路径
def replace_image_urls(markdown_text, image_dir):
    # 使用正则或字符串替换
    ...
```

### 4. 使用Chrome DevTools MCP的优势
- **无需处理反爬**：使用真实浏览器访问
- **JavaScript渲染**：自动加载动态内容
- **简单可靠**：直接访问，无需复杂的cookie/headers处理
- **支持交互**：可以模拟点击、滚动等操作

---

## 依赖包

```
requests>=2.31.0
beautifulsoup4>=4.12.0
markdownify>=0.11.6
lxml>=4.9.0
Pillow>=10.0.0
python-dotenv>=1.0.0
```

**注意**：Chrome DevTools MCP是预装的MCP工具，无需额外安装依赖包。

---

## 使用示例

### 命令行接口
```bash
# 采集单篇文章
python wechat_collector.py article "https://mp.weixin.qq.com/s/5cuBvvdfHuunxzW825fNHA"

# 从"相关文章"采集多篇
python wechat_collector.py related "https://mp.weixin.qq.com/s/5cuBvvdfHuunxzW825fNHA" --depth 1

# 批量采集（从文件读取链接）
python wechat_collector.py batch links.txt

# 采集并下载图片
python wechat_collector.py article "https://..." --download-images
```

### 配置文件（config.py）
```python
# 存储配置
OUTPUT_DIR = "./wechat_articles"
IMAGE_DIR = "images"
DOWNLOAD_IMAGES = True

# 文件命名
FILE_FORMAT = "{date}_{title}.md"  # 2026-01-04_标题.md

# Chrome DevTools配置
PAGE_LOAD_TIMEOUT = 30000  # 页面加载超时（毫秒）
```

---

## 实施步骤

1. **阶段1：基础框架搭建**
   - 创建项目结构
   - 实现配置管理（config.py）
   - 实现Chrome DevTools MCP封装（chrome_collector.py）

2. **阶段2：单篇文章采集**
   - 实现文章解析器（article_parser.py）
   - 实现Markdown生成器（markdown_generator.py）
   - 实现图片下载器（image_downloader.py）
   - 测试单篇文章采集

3. **阶段3：批量采集功能**
   - 实现"相关文章"链接提取
   - 实现批量采集逻辑
   - 实现进度显示和错误处理

4. **阶段4：优化和完善**
   - 添加命令行参数解析
   - 添加日志记录
   - 优化图片下载性能
   - 编写使用文档（README.md）

---

## 测试验证

### 测试用例1：单篇文章采集
```bash
python wechat_collector.py article "https://mp.weixin.qq.com/s/5cuBvvdfHuunxzW825fNHA"
```
**验证点**：
- Chrome DevTools成功打开页面
- Markdown文件生成成功
- 标题、作者、时间正确
- 正文内容完整
- 图片下载成功（如启用）
- JSON元数据正确

### 测试用例2：从"相关文章"采集
```bash
python wechat_collector.py related "https://mp.weixin.qq.com/s/5cuBvvdfHuunxzW825fNHA" --depth 1
```
**验证点**：
- 成功提取"相关文章"链接
- 逐个访问并采集成功
- 生成索引文件

### 测试用例3：批量采集
```bash
python wechat_collector.py batch links.txt
```
**验证点**：
- 所有链接都处理完成
- 错误处理和重试机制正常
- 进度显示正确

---

## 注意事项

1. **Chrome DevTools MCP限制**：
   - 需要确保Chrome浏览器可用
   - 页面加载可能需要等待时间
   - 一次只能访问一个页面（单线程）

2. **采集速度**：
   - 单篇文章采集约需10-30秒（包括页面加载、解析、图片下载）
   - 批量采集建议添加延时，避免请求过快
   - 可以添加进度显示，让用户了解采集状态

3. **图片下载**：
   - 微信图片可能需要referer才能访问
   - 下载的图片仅供个人学习使用，注意版权
   - 可以选择不下载图片，只保留URL

4. **错误处理**：
   - 网络错误：自动重试
   - 页面加载失败：跳过并记录日志
   - 解析失败：保存原始HTML供调试

5. **数据备份**：
   - 定期备份采集的文章数据
   - 建议使用Git进行版本控制

---

## 后续扩展

- 支持并发采集（多个Chrome标签页）
- 支持导出为PDF格式
- 支持数据库存储（SQLite/MySQL）
- 支持搜索和过滤功能
- 添加Web界面
