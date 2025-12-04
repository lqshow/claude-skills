# Food Diorama Skill

> 🎨 生成中国城市 3D 美食盲盒图像 - AI 驱动的文化美食场景创作工具


[![License](https://img.shields.io/badge/license-MIT-blue.svg)](../../LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)


## ✨ 特性

- 🎨 **AI 驱动的图像生成** - 使用 Google Gemini 生成高质量图像
- 🏙️ **多城市支持** - 支持中国特色城市
- 🎭 **Pop Mart 风格** - 可爱的盲盒风格，四宫格布局
- 📖 **文化融合** - 融合历史人物、文化符号和地域特色
- 🔧 **数据驱动** - 数据与代码分离，易于扩展新城市

## 📦 前置依赖

### 必需依赖

1. **Python 3.7+**
   ```bash
   python3 --version
   ```

2. **nanobanana-skill** （图像生成引擎）
   
   这个 skill 依赖 `nanobanana-skill` 来调用 AI 图像生成服务。

   **安装方法**：
   
   打开 Claude Code，运行以下命令：
   ```bash
   /plugin marketplace add feiskyer/claude-code-settings
   /plugin install claude-code-settings
   ```

   > ℹ️ `nanobanana-skill` 提供了统一的 AI 图像生成接口

3. **API Keys**
   - Google Gemini API Key

### 可选依赖

```bash
pip3 install python-dotenv requests --break-system-packages
```

## 🚀 安装

### 方法 1: 克隆整个仓库（推荐）

```bash
# 克隆仓库
git clone https://github.com/lqshow/claude-skills.git
cd claude-skills

# 创建符号链接到 Claude skills 目录
ln -s $(pwd)/food-diorama-skill ~/.claude/skills/food-diorama-skill

# 或者直接复制
cp -r food-diorama-skill ~/.claude/skills/
```

### 方法 2: 只下载这个 skill

```bash
# 下载 skill
git clone --depth 1 --filter=blob:none --sparse https://github.com/lqshow/claude-skills.git
cd claude-skills
git sparse-checkout set food-diorama-skill

# 安装到 Claude
ln -s $(pwd)/food-diorama-skill ~/.claude/skills/
```

### 验证安装

```bash
# 检查 skill 是否安装成功
ls ~/.claude/skills/food-diorama-skill

# 列出支持的城市
python3 ~/.claude/skills/food-diorama-skill/scripts/generate_food_diorama.py --list-cities
```

## ⚙️ 配置

### 1. 安装 nanobanana-skill

**重要**：这个 skill 依赖 `nanobanana-skill`，必须先安装。

```bash
/plugin marketplace add feiskyer/claude-code-settings
/plugin install claude-code-settings
```

### 2. 配置 API Key


```bash
# 在用户主目录创建配置文件
cat > ~/.nanobanana.env << 'EOF'
GEMINI_API_KEY=your_gemini_api_key_here
EOF

# 设置权限
chmod 600 ~/.nanobanana.env
```

### 3. 验证配置

```bash
# 测试生成（会显示提示词但不实际生成）
python3 scripts/generate_food_diorama.py 温州 --show-prompt
```

## 🎯 使用方法

### 在 Claude 中使用（推荐）

直接在 Claude 对话中请求：

```
生成一个天津的美食盲盒
```

或者：

```
Generate a food diorama for 南京
```

Claude 会自动调用这个 skill 并生成图像。

### 命令行使用

```bash
cd ~/.claude/skills/food-diorama-skill

# 列出所有支持的城市
python3 scripts/generate_food_diorama.py --list-cities

# 生成指定城市的美食盲盒
python3 scripts/generate_food_diorama.py 温州

# 只显示提示词，不生成图像
python3 scripts/generate_food_diorama.py 温州 --show-prompt

# 查看帮助
python3 scripts/generate_food_diorama.py --help
```

## 🎨 效果预览

### 温州美食盲盒
![温州预览](./assets/温州-diorama.png)

### 南京美食盲盒
![南京预览](./assets/南京-diorama.png)

### 拉萨美食盲盒
![拉萨预览](./assets/拉萨-diorama.png)

### 新疆美食盲盒
![新疆预览](./assets/新疆-diorama.png)

## 🏙️ 支持的城市

目前已支持以下城市：

- ✅ **南京** (Nanjing) - 盐水鸭、鸭血粉丝汤
- ✅ **拉萨** (Lhasa) - 酥油茶、糌粑、牦牛肉
- ✅ **新疆** (Xinjiang) - 大盘鸡、羊肉串、馕
- ✅ **温州** (Wenzhou) - 鱼丸、灯盏糕

想要添加更多城市？查看 [如何添加新城市](#添加新城市)

## 查看新城市


```bash
python3 scripts/generate_food_diorama.py 温州 --show-prompt
```

### 详细指南

查看 [references/city-database-guide.md](./references/city-database-guide.md) 获取详细的数据格式说明和最佳实践。

## 📖 数据格式说明

每个城市的数据结构包含：

- **base**: 代表城市的基础食物
- **base_desc**: 基础食物的详细描述
- **history_text**: 历史铭文或城市格言
- **city_material**: 城市特色材质（如青砖、木质等）
- **city_decoration**: 城市地标或特色装饰
- **q1-q4**: 四个象限的食物配置
  - **name**: 食物名称
  - **desc**: 外观描述
  - **texture**: 质感描述
  - **action**: 小人物的动作
  - **costume**: 人物服饰（可选）
  - **historical_figure**: 历史人物（可选）
  - **historical_scene**: 历史场景（可选）
  - **cultural_symbol**: 文化符号（可选）

完整的数据格式和示例，请参考 [city-database-guide.md](./references/city-database-guide.md)

## 🔧 故障排查

### 问题 1: nanobanana-skill 找不到

**错误信息**：
```
Cannot find nanobanana.py in any of the expected locations
```

**解决方案**：
```bash
# 安装 nanobanana-skill
/plugin marketplace add feiskyer/claude-code-settings
/plugin install claude-code-settings

# 验证安装
ls ~/.claude/skills/nanobanana-skill/
```

### 问题 2: 城市不存在

**错误信息**：
```
City '杭州' not found in database
```

**解决方案**：
```bash
# 查看支持的城市列表
python3 scripts/generate_food_diorama.py --list-cities

# 添加新城市到 data/cities.json
vim data/cities.json
```

### 问题 3: 图像生成失败

**可能原因**：
- API 配额不足
- 网络连接问题
- 提示词违反 AI 服务的内容政策

**解决方案**：
```bash
# 先查看生成的提示词
python3 scripts/generate_food_diorama.py 城市名 --show-prompt

# 检查 API 状态
curl https://generativelanguage.googleapis.com/v1/models?key=YOUR_API_KEY
```

## 📊 技术架构

```
food-diorama-skill/
├── data/
│   └── cities.json          # 城市数据库（数据与代码分离）
├── scripts/
│   └── generate_food_diorama.py  # 主脚本
├── references/
│   └── city-database-guide.md    # 数据格式指南
├── assets/                  # 预览图
└── SKILL.md                 # Claude 可读文档
```

**工作流程**：
1. 从 `cities.json` 加载城市数据
2. 根据数据生成结构化的 AI 提示词
3. 调用 `nanobanana-skill` 生成图像
4. 返回生成的图像 URL


## 🙏 致谢

- [nanobanana-skill](https://github.com/feiskyer/claude-code-settings) - 图像生成引擎
- [Claude](https://claude.ai) by Anthropic - AI 助手平台
