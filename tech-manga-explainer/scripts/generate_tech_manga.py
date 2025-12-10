#!/usr/bin/env python3
"""
Tech Manga Explainer - 技术科普漫画生成器

用漫画对话形式将复杂技术概念变得通俗易懂。
支持多种角色组合：火影师徒（默认）、程序员搭档等

使用 nanobanana skill 调用 Gemini API 生成图片
"""
import sys
import argparse
import subprocess
import os
from pathlib import Path


# ============================================================
# 画风模板库
# ============================================================
STYLE_TEMPLATES = {
    "manga": {
        "name": "日式漫画",
        "prompt": """Japanese manga style illustration for technical education.
Clean black ink lines with confident strokes.
Screentone/halftone dot patterns for shading.
Dynamic expressions and reactions (sweat drops, sparkles, shock lines).
Speech bubbles with clean borders.
Panel-style composition even for single images.
Professional seinen manga quality, like technical doujinshi.
Black and white with occasional color accents for emphasis.""",
        "negative": "realistic photo, western comic, childish, blurry lines, messy"
    },
    
    "minimal": {
        "name": "简约线条",
        "prompt": """Minimal line art illustration style for technical documentation.
Clean, thin black lines on white background.
Extremely simple character designs, almost icon-like.
Focus on clarity and readability.
Technical diagrams integrated naturally.
Whiteboard sketch aesthetic but more polished.
Professional, corporate-friendly style.
Like illustrations in O'Reilly books or technical blogs.""",
        "negative": "detailed, colorful, complex shading, manga effects, busy"
    },
    
    "cyberpunk": {
        "name": "赛博朋克",
        "prompt": """Cyberpunk style illustration for tech education.
Dark background with neon accent colors (cyan, magenta, purple).
Holographic UI elements and floating displays.
Glowing edges and light bloom effects.
Futuristic tech aesthetic, like Blade Runner or Ghost in Shell.
Characters with subtle tech accessories.
High contrast, dramatic lighting.
Digital rain or circuit patterns in background.""",
        "negative": "bright, cheerful, pastoral, historical, hand-drawn sketch"
    },
    
    "sketch": {
        "name": "手绘涂鸦",
        "prompt": """Casual whiteboard sketch style illustration.
Hand-drawn look with slightly wobbly lines.
Looks like someone quickly sketched during a meeting.
Marker pen aesthetic with occasional color highlights.
Arrows, underlines, and handwritten annotations.
Informal, approachable, like a colleague explaining on paper.
Simple stick-figure-ish characters but with personality.
Graph paper or whiteboard background texture.""",
        "negative": "polished, professional, detailed, realistic, perfect lines"
    }
}


# ============================================================
# 角色组定义 - 支持多套角色
# ============================================================
CHARACTER_PRESETS = {
    # 默认：火影忍者 - 卡卡西 & 鸣人
    "naruto": {
        "name": "火影师徒",
        "description": "热血修行风，师徒传承，循序渐进，实战演练",
        "mentor": {
            "name": "卡卡西",
            "emoji": "😷",
            "css_class": "kakashi",
            "card": """【旗木卡卡西 Kakashi Hatake - 技术导师】

FACE & HEAD:
- Japanese male ninja, around 30 years old, tall and lean
- HAIR: Spiky SILVER/WHITE hair, gravity-defying style pointing up and to the left, very distinctive
- LEFT EYE: Usually covered by TILTED Konoha forehead protector (hitai-ate), showing Sharingan only in special moments
- RIGHT EYE: Relaxed, half-lidded, always looking slightly bored or lazy
- MASK: ALWAYS wearing dark navy blue FACE MASK covering nose and mouth, never removed
- Expression: calm, relaxed, slightly bored but actually very attentive, occasional eye-smile (眼笑)

BODY:
- Tall, athletic, lean muscular build
- Relaxed posture, often slouching or leaning
- Sometimes reading a small orange book (Icha Icha)

CLOTHING (NEVER CHANGES):
- HEAD: Konoha forehead protector worn TILTED to cover left eye
- TOP: Standard Konoha JONIN VEST (green/olive flak jacket) with scroll pouches
- UNDER: Dark navy blue long-sleeve shirt with built-in mask
- PANTS: Dark navy blue ninja pants
- SHOES: Standard blue ninja sandals
- GLOVES: Fingerless dark gloves with metal plate on back

ACCESSORIES:
- Small orange book (Make-Out Paradise) sometimes in hand
- Ninja tool pouch on right thigh

⚠️ CRITICAL FEATURES THAT MUST APPEAR IN EVERY IMAGE:
1. Spiky silver/white gravity-defying hair
2. Dark blue face mask ALWAYS covering nose and mouth
3. Forehead protector tilted to cover LEFT eye
4. Green jonin flak vest
5. Relaxed, half-lidded expression"""
        },
        "learner": {
            "name": "鸣人",
            "emoji": "🍥",
            "css_class": "naruto",
            "card": """【漩涡鸣人 Naruto Uzumaki - 热血学习者】

FACE & HEAD:
- Japanese male ninja, around 16 years old (Shippuden era), energetic teenager
- HAIR: Bright SPIKY BLONDE/YELLOW hair, messy and wild, sticking out in all directions
- EYES: Big bright BLUE eyes, very expressive, often wide with determination or confusion
- FACE: THREE WHISKER MARKS on each cheek (6 total), thin horizontal lines like cat whiskers
- Expression: energetic, determined, sometimes confused, often grinning widely

BODY:
- Medium height, athletic build
- Very animated body language, often pumping fists or pointing

CLOTHING (NEVER CHANGES - Shippuden outfit):
- HEAD: Konoha forehead protector worn on FOREHEAD (black cloth)
- TOP: Orange and BLACK TRACKSUIT jacket with zipper, black on shoulders and sleeves
- INSIDE: Black t-shirt visible at collar
- PANTS: Orange tracksuit pants matching the jacket
- SHOES: Black ninja sandals
- ACCESSORIES: Small green crystal necklace (Tsunade's necklace) around neck

SIGNATURE POSES:
- Thumbs up with big grin
- Fist pump shouting "Dattebayo!"
- Scratching back of head when confused
- Shadow Clone hand seal when practicing

⚠️ CRITICAL FEATURES THAT MUST APPEAR IN EVERY IMAGE:
1. Bright spiky BLONDE hair
2. THREE WHISKER MARKS on each cheek
3. Bright BLUE eyes
4. Orange and black tracksuit
5. Forehead protector on forehead (not tilted)
6. Energetic, expressive face"""
        }
    },
    
    # 备选：程序员搭档 - 码叔 & 小新
    "coder": {
        "name": "程序员搭档",
        "description": "职场日常风，老程序员带新人，轻松幽默",
        "mentor": {
            "name": "码叔",
            "emoji": "👨‍💻",
            "css_class": "mashu",
            "card": """【码叔 Ma Shu - 技术导师】

FACE & HEAD:
- Chinese male, 40 years old, round friendly face with slight double chin
- HAIR: BALDING on top (clearly visible scalp, Mediterranean pattern), dark brown fluffy hair ONLY on sides and back
- Silver rectangular metal-framed GLASSES, thin frames
- BEARD: Short scruffy salt-and-pepper beard, not neatly trimmed
- Expression: wise, patient, slightly tired but enthusiastic

BODY:
- Slightly chubby build with visible beer belly
- Height: average, stocky

CLOTHING (NEVER CHANGES):
- TOP LAYER: Red-and-black PLAID flannel shirt, sleeves ALWAYS rolled up to elbows
- UNDER LAYER: Dark gray hoodie underneath (hood bunched at back of neck)
- PANTS: Classic medium-blue denim jeans
- SHOES: Gray canvas sneakers with white rubber soles
- WATCH: Black digital Casio-style watch on LEFT wrist

ACCESSORIES:
- WHITE ceramic coffee mug with red "I ♥ DEBUG" text
- Sometimes pointing at whiteboard

⚠️ CRITICAL FEATURES THAT MUST APPEAR IN EVERY IMAGE:
1. Balding top with hair only on sides
2. Silver rectangular glasses
3. Red-black plaid shirt with rolled sleeves
4. Gray hoodie bunched at neck
5. Scruffy beard"""
        },
        "learner": {
            "name": "小新",
            "emoji": "🧑",
            "css_class": "xiaoxin",
            "card": """【小新 Xiao Xin - 技术新手】

FACE & HEAD:
- Chinese male, 25 years old, oval face, youthful
- HAIR: Black MUSHROOM CUT / BOWL CUT, straight bangs almost touching eyebrows
- Big expressive dark brown eyes
- Clean-shaven, occasional small acne spots

BODY:
- Tall and thin/slim build

CLOTHING (NEVER CHANGES):
- TOP LAYER: Black zip-up HOODIE, zipper ALWAYS open
- UNDER LAYER: Plain WHITE crew-neck t-shirt
- PANTS: Dark gray or black JOGGER pants with elastic cuffs
- SHOES: Clean WHITE sneakers

ACCESSORIES:
- Light GRAY BACKPACK with PIXEL-ART ROBOT KEYCHAIN (orange and blue)
- Often holding spiral NOTEBOOK or tablet

⚠️ CRITICAL FEATURES THAT MUST APPEAR IN EVERY IMAGE:
1. Black mushroom-cut hair with straight bangs
2. Black hoodie OPEN over white t-shirt
3. Gray backpack with pixel robot keychain
4. Tall thin build
5. Big expressive eyes"""
        }
    }
}

# 默认角色组
DEFAULT_PRESET = "naruto"


def get_character_cards(preset_name):
    """获取指定角色组的角色卡"""
    preset = CHARACTER_PRESETS.get(preset_name, CHARACTER_PRESETS[DEFAULT_PRESET])
    return preset


def parse_dialogue(dialogue_string):
    """解析对话字符串"""
    if not dialogue_string:
        return []
    
    dialogues = []
    pairs = dialogue_string.split("|")
    for pair in pairs:
        if ":" in pair:
            speaker, content = pair.split(":", 1)
            dialogues.append({
                "speaker": speaker.strip(),
                "content": content.strip()
            })
    return dialogues


def build_prompt(args):
    """构建完整的图像提示词"""
    
    style = STYLE_TEMPLATES.get(args.style, STYLE_TEMPLATES["manga"])
    preset = get_character_cards(args.preset)
    
    mentor = preset["mentor"]
    learner = preset["learner"]
    
    # 解析对话
    dialogues = parse_dialogue(args.dialogue)
    
    # 构建对话描述
    dialogue_section = ""
    if dialogues:
        dialogue_lines = ["Speech bubbles with dialogue:"]
        for d in dialogues:
            dialogue_lines.append(f'  • {d["speaker"]}: "{d["content"]}"')
        dialogue_section = "\n".join(dialogue_lines)
    
    # 构建角色描述 - 强调一致性
    character_section = f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️ CHARACTER CONSISTENCY - ABSOLUTELY CRITICAL ⚠️                ║
║  These two characters must look EXACTLY the same in EVERY page   ║
║  DO NOT change their hair, clothes, accessories, or features     ║
╚══════════════════════════════════════════════════════════════════╝

{mentor["card"]}

{learner["card"]}

═══════════════════════════════════════════════════════════════════
CONSISTENCY CHECKLIST - VERIFY BEFORE GENERATING:
═══════════════════════════════════════════════════════════════════
{mentor["name"]} - CHECK ALL FEATURES FROM CARD ABOVE
{learner["name"]} - CHECK ALL FEATURES FROM CARD ABOVE

ANY DEVIATION FROM ABOVE IS AN ERROR. REGENERATE IF NEEDED.
═══════════════════════════════════════════════════════════════════
"""

    # 构建主提示词
    prompt_parts = [
        f"Technical education manga/comic illustration.",
        "",
        f"=== ART STYLE ===",
        style["prompt"],
        "",
        character_section,
        "",
        f"=== SCENE ===",
        args.prompt,
        "",
    ]
    
    # 添加对话
    if dialogue_section:
        prompt_parts.extend([
            f"=== DIALOGUE ===",
            dialogue_section,
            "Dialogue should be in clean speech bubbles, text in Chinese.",
            "Use manga-style speech bubbles with tails pointing to speakers.",
            ""
        ])
    
    # 添加技术图示
    if args.tech_diagram:
        prompt_parts.extend([
            f"=== TECHNICAL DIAGRAM IN SCENE ===",
            f"Include a clear technical diagram showing: {args.tech_diagram}",
            "The diagram should be visible on a whiteboard, screen, or floating in the scene.",
            "Keep diagram simple and readable, using boxes, arrows, and labels.",
            ""
        ])
    
    # 质量要求
    prompt_parts.extend([
        "=== QUALITY REQUIREMENTS ===",
        "• Professional manga illustration quality",
        "• Characters must be clearly recognizable with all their signature features",
        "• Text in speech bubbles must be readable",
        "• Technical diagrams must be clear and accurate",
        "• Good composition with clear focal point",
        "• Expressions should match the dialogue emotion",
        "",
        f"=== AVOID ===",
        style["negative"] + ", text errors, inconsistent character design, cluttered composition, unreadable text"
    ])
    
    return "\n".join(prompt_parts)


def find_nanobanana():
    """查找 nanobanana.py"""
    possible_paths = [
        os.path.expandvars("${HOME}/.claude/skills/nanobanana-skill/nanobanana.py"),
        "/mnt/user-data/uploads/nanobanana.py",
        "/mnt/skills/user/nanobanana-skill/nanobanana.py",
        os.path.expandvars("${CLAUDE_PLUGIN_ROOT}/skills/nanobanana-skill/nanobanana.py"),
        "./nanobanana.py",
        "../nanobanana-skill/nanobanana.py",
        str(Path(__file__).parent / "nanobanana.py"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


def main():
    parser = argparse.ArgumentParser(
        description="技术科普漫画生成器 - 码叔带你学技术",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
画风选项:
  manga       日式漫画风格（清晰线条、动态表情）- 推荐
  minimal     简约线条风格（黑白、专业感）
  cyberpunk   赛博朋克风格（霓虹、科技感）
  sketch      手绘涂鸦风格（白板画、轻松）

角色组选项:
  naruto      火影师徒（卡卡西 & 鸣人）- 默认，热血修行风
  coder       程序员搭档（码叔 & 小新）- 职场日常风

示例:
  # 基础用法（默认使用卡卡西和鸣人）
  %(prog)s --prompt "在训练场讲解" --dialogue "鸣人:Docker是什么？|卡卡西:就像忍术卷轴"
  
  # 使用程序员角色组
  %(prog)s --preset coder --prompt "办公室场景" --dialogue "小新:Pod是什么？|码叔:就像一个集装箱"
  
  # 赛博朋克风格讲AI
  %(prog)s --style cyberpunk --prompt "未来城市背景" --dialogue "鸣人:AI Agent是什么？"
        """
    )
    
    parser.add_argument(
        "--prompt",
        type=str,
        help="场景描述（必需，除非使用 --list-styles）"
    )
    parser.add_argument(
        "--dialogue",
        type=str,
        default=None,
        help="对话内容，格式：角色:内容|角色:内容"
    )
    parser.add_argument(
        "--preset",
        type=str,
        default="naruto",
        choices=list(CHARACTER_PRESETS.keys()),
        help="角色组选择 (默认: naruto)"
    )
    parser.add_argument(
        "--style",
        type=str,
        default="manga",
        choices=list(STYLE_TEMPLATES.keys()),
        help="画风选择 (默认: manga)"
    )
    parser.add_argument(
        "--tech-diagram",
        type=str,
        default=None,
        help="技术图示描述（会在画面中展示）"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="tech_manga_page.png",
        help="输出文件名 (默认: tech_manga_page.png)"
    )
    parser.add_argument(
        "--size",
        type=str,
        default="1024x1024",
        help="图片尺寸 (默认: 1024x1024，推荐竖版 768x1024)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-3-pro-image-preview",
        help="Gemini 模型"
    )
    parser.add_argument(
        "--show-prompt",
        action="store_true",
        help="仅显示生成的提示词，不生成图片"
    )
    parser.add_argument(
        "--list-styles",
        action="store_true",
        help="列出所有可用画风"
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="列出所有可用角色组"
    )
    parser.add_argument(
        "--show-characters",
        action="store_true",
        help="显示当前角色组的详细角色卡"
    )
    
    args = parser.parse_args()
    
    # 列出画风
    if args.list_styles:
        print("可用画风:")
        print("-" * 60)
        for code, style in STYLE_TEMPLATES.items():
            print(f"\n【{style['name']}】 --style {code}")
            # 显示简短描述
            first_line = style["prompt"].split("\n")[0]
            print(f"    {first_line}")
        return
    
    # 列出角色组
    if args.list_presets:
        print("可用角色组:")
        print("-" * 60)
        for code, preset in CHARACTER_PRESETS.items():
            mentor = preset["mentor"]
            learner = preset["learner"]
            print(f"\n【{preset['name']}】 --preset {code}")
            print(f"    {preset['description']}")
            print(f"    导师: {mentor['emoji']} {mentor['name']}")
            print(f"    学员: {learner['emoji']} {learner['name']}")
        return
    
    # 显示角色卡
    if args.show_characters:
        preset = get_character_cards(args.preset)
        print("=" * 60)
        print(f"角色组: {preset['name']}")
        print("=" * 60)
        print(f"\n【导师 - {preset['mentor']['name']}】")
        print("-" * 40)
        print(preset['mentor']['card'])
        print(f"\n【学员 - {preset['learner']['name']}】")
        print("-" * 40)
        print(preset['learner']['card'])
        return
    
    # 检查必需参数
    if not args.prompt:
        parser.error("请提供 --prompt 参数（场景描述）")
    
    # 构建提示词
    full_prompt = build_prompt(args)
    
    # 仅显示提示词
    if args.show_prompt:
        print("=" * 80)
        print("生成的提示词:")
        print("=" * 80)
        print(full_prompt)
        print("=" * 80)
        return
    
    # 查找 nanobanana
    nanobanana_path = find_nanobanana()
    if nanobanana_path is None:
        print("错误: 找不到 nanobanana.py", file=sys.stderr)
        print("请确保 nanobanana skill 已安装", file=sys.stderr)
        sys.exit(1)
    
    # 生成图片
    style_name = STYLE_TEMPLATES[args.style]["name"]
    
    print(f"🎨 生成技术科普漫画...")
    print(f"   画风: {style_name}")
    print(f"   角色: 码叔 + 小新")
    print(f"   输出: {args.output}")
    if args.dialogue:
        print(f"   对话: {args.dialogue[:50]}..." if len(args.dialogue) > 50 else f"   对话: {args.dialogue}")
    if args.tech_diagram:
        print(f"   图示: {args.tech_diagram}")
    print()
    
    cmd = [
        "python3",
        nanobanana_path,
        "--prompt", full_prompt,
        "--output", args.output,
        "--size", args.size,
        "--model", args.model
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print(f"\n✅ 技术漫画已生成: {args.output}")
    
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
