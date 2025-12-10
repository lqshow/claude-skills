# Tech Manga Explainer

> 🎨 生成技术科普漫画 - AI 驱动的技术概念可视化学习工具

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](../../LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)


## ✨ 特性

- 🎨 **AI 驱动的图像生成** - 使用 Google Gemini 生成高质量漫画图像
- 🎭 **多角色组合** - 支持火影师徒（卡卡西 & 鸣人）、程序员搭档（码叔 & 小新）等角色组
- 🖌️ **多种画风** - 日式漫画、简约线条、赛博朋克、手绘涂鸦四种风格
- 📚 **结构化学习** - 通过对话形式将复杂技术概念拆解为易懂知识点
- 🔧 **数据驱动** - 内置多个技术主题模板，易于扩展新主题
- 🌐 **交互式输出** - 生成可浏览的 HTML 漫画教程

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
ln -s $(pwd)/tech-manga-explainer ~/.claude/skills/tech-manga-explainer

# 或者直接复制
cp -r tech-manga-explainer ~/.claude/skills/
```

### 方法 2: 只下载这个 skill

```bash
# 下载 skill
git clone --depth 1 --filter=blob:none --sparse https://github.com/lqshow/claude-skills.git
cd claude-skills
git sparse-checkout set tech-manga-explainer

# 安装到 Claude
ln -s $(pwd)/tech-manga-explainer ~/.claude/skills/
```

### 验证安装

```bash
# 检查 skill 是否安装成功
ls ~/.claude/skills/tech-manga-explainer

# 列出支持的画风
python3 ~/.claude/skills/tech-manga-explainer/scripts/generate_tech_manga.py --list-styles

# 列出支持的角色组
python3 ~/.claude/skills/tech-manga-explainer/scripts/generate_tech_manga.py --list-presets
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
python3 scripts/generate_tech_manga.py --prompt "训练场场景" --dialogue "鸣人:这是什么？|卡卡西:这是技术漫画" --show-prompt
```

## 🎯 使用方法

### 在 Claude 中使用（推荐）

直接在 Claude 对话中请求：

```
用漫画解释一下 Kubernetes Pod 是什么
```

或者：

```
用火影忍者的漫画风格讲解 Docker 容器
```

Claude 会自动调用这个 skill 并生成图像。

### 命令行使用

```bash
cd ~/.claude/skills/tech-manga-explainer

# 列出所有可用画风
python3 scripts/generate_tech_manga.py --list-styles

# 列出所有可用角色组
python3 scripts/generate_tech_manga.py --list-presets

# 生成技术漫画（默认使用卡卡西和鸣人）
python3 scripts/generate_tech_manga.py \
  --prompt "木叶村训练场，卡卡西在白板前讲解" \
  --dialogue "鸣人:这个 Docker 到底是什么啊！|卡卡西:嘛嘛，你想想忍者出任务时为什么要带卷轴？" \
  --tech-diagram "Docker 容器结构示意图" \
  --output page_01.png

# 使用程序员角色组
python3 scripts/generate_tech_manga.py \
  --preset coder \
  --style manga \
  --prompt "办公室场景，码叔在白板前" \
  --dialogue "小新:Pod是什么？|码叔:就像一个集装箱..." \
  --output page_01.png

# 赛博朋克风格讲 AI
python3 scripts/generate_tech_manga.py \
  --style cyberpunk \
  --prompt "未来城市背景，全息投影" \
  --dialogue "鸣人:AI Agent 和普通聊天机器人有什么区别？|卡卡西:就像上忍和下忍的区别" \
  --output agent_01.png

# 只显示提示词，不生成图像
python3 scripts/generate_tech_manga.py --prompt "场景" --dialogue "对话" --show-prompt

# 查看帮助
python3 scripts/generate_tech_manga.py --help
```

## 🎨 效果预览

### 火影师徒风格
![火影风格示例](./assets/火影风格示例.png)

### 程序员搭档风格
![程序员风格示例](./assets/程序员风格示例.png)


## 🎭 支持的角色组

### 默认角色组：火影师徒（`--preset naruto`）
- **卡卡西** 😷 - 技术导师：银白刺猬头、遮左眼的护额、深蓝色面罩、绿色马甲、慵懒眼神
- **鸣人** 🍥 - 热血学习者：金色刺猬头、蓝色眼睛、每边脸3道胡须印记、橙黑运动服

**对话风格**：热血修行、师徒传承、循序渐进
- 鸣人：冲动提问，经常犯错再理解
- 卡卡西：慵懒解答，喜欢用反问引导思考

### 备选角色组：程序员搭档（`--preset coder`）
- **码叔** 👨‍💻 - 技术导师：秃顶+两侧有发、银框眼镜、红黑格子衬衫、灰色帽衫堆在脖子后、络腮胡
- **小新** 🧑 - 技术新手：蘑菇头黑发、黑色拉链卫衣敞开、白T恤、灰背包+像素机器人挂件

**对话风格**：职场日常、轻松幽默、生活化比喻
- 小新：虚心请教，认真记笔记
- 码叔：耐心讲解，喜欢用生活化比喻

## 🖌️ 支持的画风

| 风格代码 | 风格名称 | 特点 | 适合主题 |
|---------|---------|------|---------|
| manga | 日式漫画 | 清晰线条、网点背景、动态表情、专业漫画质量 | 通用，最推荐 |
| minimal | 简约线条 | 黑白为主、极简、专业感、技术文档风格 | 架构、流程讲解 |
| cyberpunk | 赛博朋克 | 霓虹色、科技感、暗色调、全息投影效果 | AI、云原生、未来技术 |
| sketch | 手绘涂鸦 | 轻松随意、像白板画、手绘感、非正式 | 快速原型、头脑风暴 |

## 📚 内置主题模板

目前已内置以下技术主题的完整漫画教程：

- ✅ **Kubernetes Pod 入门** - 4页，集装箱比喻
- ✅ **n8n 工作流入门** - 4页，乐高积木工厂比喻
- ✅ **AI Agent 是什么** - 5页，赛博朋克风格
- ✅ **Docker 容器入门** - 4页，便当盒比喻
- ✅ **RAG 检索增强生成** - 4页，开卷考试比喻

每个主题都包含：
- 完整的页数规划
- 每页的场景、对话、技术图示
- 核心比喻设计
- 推荐画风

想要添加更多主题？查看 [如何添加新主题](#添加新主题)

## 📖 数据格式说明

每个主题的数据结构包含：

```json
{
  "topic-key": {
    "title": "教程标题",
    "pages": 4,
    "recommended_style": "manga",
    "core_analogy": "核心比喻",
    "structure": [
      {
        "page": 1,
        "scene": "场景描述",
        "dialogue": "角色:内容|角色:内容",
        "tech_diagram": "技术图示描述",
        "knowledge": "知识点"
      }
    ]
  }
}
```

### 字段说明

- **title**: 教程标题
- **pages**: 总页数
- **recommended_style**: 推荐画风
- **core_analogy**: 核心比喻（用于帮助理解）
- **structure**: 页面结构数组
  - **page**: 页码
  - **scene**: 场景描述（具体、可视化）
  - **dialogue**: 对话内容，格式：`角色:内容|角色:内容`
  - **tech_diagram**: 技术图示描述（可选）
  - **knowledge**: 本页核心知识点

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

### 问题 2: 角色外观不一致

**问题描述**：生成的图片中角色外观有变化

**解决方案**：
```bash
# 查看当前角色组的详细角色卡
python3 scripts/generate_tech_manga.py --preset naruto --show-characters

# 确保提示词中包含完整的角色卡
python3 scripts/generate_tech_manga.py --prompt "场景" --dialogue "对话" --show-prompt
```

### 问题 3: 图像生成失败

**可能原因**：
- API 配额不足
- 网络连接问题
- 提示词违反 AI 服务的内容政策

**解决方案**：
```bash
# 先查看生成的提示词
python3 scripts/generate_tech_manga.py --prompt "场景" --dialogue "对话" --show-prompt

# 检查 API 状态
curl https://generativelanguage.googleapis.com/v1/models?key=YOUR_API_KEY
```

## 📊 技术架构

```
tech-manga-explainer/
├── data/
│   └── topics.json          # 主题数据库（数据与代码分离）
├── scripts/
│   └── generate_tech_manga.py  # 主脚本
├── assets/                  # 模板文件和预览图
│   ├── manga_template.html      # 主 HTML 模板
│   ├── page_template.html       # 单页模板
│   └── dialogue_template.html   # 对话模板
└── SKILL.md                 # Claude 可读文档
```

**工作流程**：
1. 从 `topics.json` 加载主题数据（或根据用户请求动态规划）
2. 根据数据生成结构化的 AI 提示词
3. 调用 `nanobanana-skill` 生成图像
4. 使用模板生成交互式 HTML 漫画教程
5. 返回生成的图像和 HTML 文件

## 🙏 致谢

- [nanobanana-skill](https://github.com/feiskyer/claude-code-settings) - 图像生成引擎
- [Claude](https://claude.ai) by Anthropic - AI 助手平台
- 《火影忍者》 - 角色设计灵感来源