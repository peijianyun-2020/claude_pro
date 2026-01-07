# 故障排查指南

## 常见问题及解决方案

### 一、数据处理相关

#### Q1. 提示"未找到数据文件"

**症状:**
```
❌ 未找到数据文件: D:\AI\Trae项目工作区\南方区域电力现货市场价格跟踪\每日日前数据表\20251231日前.xlsx
```

**排查步骤:**
1. 确认文件位置是否正确:
   ```bash
   dir "D:\AI\Trae项目工作区\南方区域电力现货市场价格跟踪\每日日前数据表"
   ```

2. 检查文件命名格式:
   - 正确: `20251231日前.xlsx` 或 `20251231实时.xlsx`
   - 错误: `12月31日.xlsx`、`2025-12-31.xlsx`

3. 确认文件扩展名:
   - 必须是 `.xlsx` 或 `.xls`
   - 检查是否隐藏了扩展名

**解决方案:**
- 重命名文件为正确格式
- 移动文件到指定目录
- 使用 `--batch` 参数批量处理目录下所有文件

---

#### Q2. 数据读取失败或为空

**症状:**
```
❌ 数据读取失败或为空
```

**排查步骤:**
1. 检查Excel文件是否损坏:
   - 尝试用Excel打开文件
   - 检查是否有受保护视图

2. 检查数据格式:
   - 必须包含时间列(时间、时段、小时等)
   - 必须包含区域列(广东、广西、云南、贵州、海南、全区域)
   - 价格必须是数值型

3. 查看原始数据形状:
   ```python
   import pandas as pd
   df = pd.read_excel('20251231日前.xlsx')
   print(df.shape)
   print(df.columns)
   print(df.head())
   ```

**解决方案:**
- 确保Excel包含必要的列
- 转换数据类型为数值型
- 删除空行和无效数据

---

#### Q3. 中文显示为方框

**症状:**
图表中的中文文字显示为方框 `□□□`

**原因:**
系统缺少中文字体

**解决方案:**

**Windows:**
1. 安装 SimHei (黑体) 或 Microsoft YaHei (微软雅黑)
2. 或下载 [DejaVu Sans](https://dejavu-fonts.github.io/)

**Linux:**
```bash
sudo apt-get install fonts-wqy-microhei
```

**macOS:**
系统自带中文字体,无需额外安装

**验证:**
```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']
# 应输出: ['SimHei', 'Microsoft YaHei', ...]
```

---

#### Q4. 文案生成失败

**症状:**
```
❌ 缺少全区域价格数据：日前 2025-12-31
```

**原因:**
Excel数据中缺少"全区域"列

**解决方案:**
1. 确保Excel包含"全区域"列
2. 或修改代码使用其他区域(如"广东")
3. 检查列名是否完全匹配(全区域 ≠ 全省)

---

### 二、小红书发布相关

#### Q5. 小红书登录失效

**症状:**
```
❌ 未登录或登录已过期
```

**解决方案:**

**方法一: 通过Claude MCP**
1. 请求Claude检查登录状态:
   ```
   检查小红书登录状态
   ```
2. 如未登录,请求获取二维码:
   ```
   获取小红书登录二维码
   ```
3. 使用小红书APP扫码登录

**方法二: 重新认证**
```bash
python scripts/publish_xiaohongshu.py --check-login
```

---

#### Q6. 图片上传失败

**症状:**
```
❌ 图片上传失败: 格式不支持或文件过大
```

**排查步骤:**
1. 检查图片格式:
   ```bash
   # 查看图片信息
   magick identify 图_日前_20251231.jpg
   ```

2. 检查文件大小:
   ```bash
   dir 图_日前_20251231.jpg
   ```
   应小于10MB

3. 检查图片分辨率:
   - 建议宽度 ≥1080px
   - 建议高度 ≥1080px

**解决方案:**
```python
from PIL import Image

# 打开并调整图片
img = Image.open('图_日前_20251231.jpg')

# 调整大小(保持比例)
if img.width < 1080 or img.height < 1080:
    ratio = max(1080/img.width, 1080/img.height)
    new_size = (int(img.width*ratio), int(img.height*ratio))
    img = img.resize(new_size, Image.LANCZOS)

# 保存为JPG(质量85%)
img.save('图_日前_20251231_opt.jpg', 'JPEG', quality=85, optimize=True)
```

---

#### Q7. 内容审核失败

**症状:**
```
❌ 内容审核未通过: 包含敏感词汇
```

**常见敏感词:**
- 极端价格描述(避免过度强调"负电价")
- 绝对化用语("最好"、"第一")
- 营销推广词汇("立即购买"、"限时优惠")

**解决方案:**
1. 审阅文案,移除敏感词
2. 使用中性、客观的表达
3. 避免营销类语言

**修改示例:**
- ❌ "负电价来袭,千万别错过!"
- ✅ "部分时段出现负价格,请理性分析"

---

#### Q8. MCP调用失败

**症状:**
```
❌ MCP服务异常: 无法连接到小红书服务
```

**排查步骤:**
1. 检查MCP服务状态:
   ```bash
   claude mcp list
   ```

2. 查看小红书MCP是否已安装:
   ```bash
   claude mcp list | grep xiaohongshu
   ```

**解决方案:**
1. 重启Claude Code
2. 重新安装小红书MCP服务
3. 检查网络连接
4. 查看MCP日志文件

---

### 三、系统集成相关

#### Q9. Python环境问题

**症状:**
```
ModuleNotFoundError: No module named 'pandas'
```

**解决方案:**
```bash
# 进入项目目录
cd D:\AI\Trae项目工作区\南方区域电力现货市场价格跟踪

# 安装依赖
pip install -r requirements.txt
```

**如遇到网络问题:**
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

#### Q10. 路径错误

**症状:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'D:\\AI\\...'
```

**原因:**
路径中包含中文或特殊字符

**解决方案:**
1. 使用原始字符串:
   ```python
   path = r"D:\AI\Trae项目工作区\..."
   ```

2. 使用双反斜杠:
   ```python
   path = "D:\\AI\\Trae项目工作区\\..."
   ```

3. 使用正斜杠:
   ```python
   path = "D:/AI/Trae项目工作区/..."
   ```

---

### 四、数据质量问题

#### Q11. Excel数据格式异常

**症状:**
```
警告：未找到时间列，使用第一列
警告：未找到价格列，使用第二列
```

**原因:**
列名不符合预期

**解决方案:**
1. 标准化列名:
   - 时间列: "时间"、"时段"、"小时"、"时刻"
   - 价格列: "价格"、"电价"
   - 区域列: "广东"、"广西"、"云南"、"贵州"、"海南"、"全区域"

2. 或修改代码中的候选列表:
   ```python
   # 在 market_processor.py 中
   TIME_COL_CANDIDATES = ['时间', '时段', '你的时间列名']
   ```

---

#### Q12. 时间格式解析失败

**症状:**
```
ValueError: time data '1' does not match format '%H:%M'
```

**原因:**
时间格式不一致

**支持的格式:**
- `HH:MM` (如 "09:30")
- `HH:MM:SS` (如 "09:30:00")
- 纯数字 (如 "9", "14")

**解决方案:**
统一时间格式为 `HH:MM`:
```python
# 在Excel中设置单元格格式为"时间"
# 或使用Python转换
df['时间'] = df['时间'].apply(lambda x: f'{int(x):02d}:00')
```

---

## 获取帮助

如果以上方案无法解决问题:

1. **查看日志:**
   ```bash
   # 查看详细错误日志
   python process_data.py --type dayahead --date 20251231 --verbose
   ```

2. **检查示例数据:**
   参考 `20251231日前/` 目录下的正确示例

3. **联系支持:**
   - 提供完整的错误信息
   - 说明操作步骤
   - 附加相关文件截图

## 预防措施

1. **定期备份数据:**
   ```bash
   # 每日备份汇总CSV
   copy 汇总_日前.csv 备份_汇总_日前_%date:~0,4%%date:~5,2%%date:~8,2%.csv
   ```

2. **测试环境验证:**
   - 新流程先用测试数据验证
   - 确认无误后再处理正式数据

3. **定期检查:**
   - 每周检查一次汇总CSV完整性
   - 验证生成的图表和文案准确性
