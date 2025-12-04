#!/usr/bin/env python3
"""
3D Historical Gourmet Diorama Generator
Generate 3D food diorama images for cities using Google Gemini API

标准 Skill 设计：代码与数据分离
"""
import sys
import json
import argparse
import subprocess
import os
from pathlib import Path


class CityDatabase:
    """城市数据库管理类"""
    
    def __init__(self, data_dir=None):
        """
        初始化城市数据库
        
        Args:
            data_dir: 数据目录路径。如果为 None，自动查找
        """
        self.data_dir = self._find_data_dir(data_dir)
        self.cities = self._load_cities()
    
    def _find_data_dir(self, data_dir):
        """查找数据目录"""
        if data_dir and os.path.exists(data_dir):
            return data_dir
        
        # 尝试多个可能的位置
        script_dir = Path(__file__).parent
        possible_paths = [
            script_dir / "../data",  # 标准位置
            script_dir / "data",     # 同目录
            Path.home() / ".claude/skills/food-diorama-skill/data",  # 用户目录
            Path("/mnt/skills/user/food-diorama-skill/data"),  # MCP 目录
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        # 如果都不存在，返回标准位置（即使不存在）
        return script_dir / "../data"
    
    def _load_cities(self):
        """加载城市数据"""
        cities = {}
        
        # 1. 尝试加载主数据文件
        main_file = self.data_dir / "cities.json"
        if main_file.exists():
            try:
                with open(main_file, 'r', encoding='utf-8') as f:
                    cities.update(json.load(f))
            except Exception as e:
                print(f"警告: 无法加载 {main_file}: {e}", file=sys.stderr)
        
        # 2. 加载单个城市文件（允许用户自定义）
        if self.data_dir.exists():
            for file_path in self.data_dir.glob("*.json"):
                if file_path.name == "cities.json":
                    continue  # 跳过主文件
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        city_data = json.load(f)
                        # 假设单个文件只包含一个城市
                        if isinstance(city_data, dict):
                            # 如果是 {"城市名": {...}} 格式
                            if len(city_data) == 1:
                                cities.update(city_data)
                            else:
                                # 假设文件名就是城市名
                                city_name = file_path.stem
                                cities[city_name] = city_data
                except Exception as e:
                    print(f"警告: 无法加载 {file_path}: {e}", file=sys.stderr)
        
        return cities
    
    def get_city(self, city_name):
        """获取城市数据"""
        return self.cities.get(city_name)
    
    def list_cities(self):
        """列出所有城市"""
        return sorted(self.cities.keys())
    
    def add_city(self, city_name, city_data, save_to_file=True):
        """
        添加新城市
        
        Args:
            city_name: 城市名称
            city_data: 城市数据字典
            save_to_file: 是否保存到单独的文件
        """
        self.cities[city_name] = city_data
        
        if save_to_file:
            # 保存到单独的 JSON 文件
            city_file = self.data_dir / f"{city_name}.json"
            os.makedirs(self.data_dir, exist_ok=True)
            
            with open(city_file, 'w', encoding='utf-8') as f:
                json.dump({city_name: city_data}, f, ensure_ascii=False, indent=2)
            
            print(f"✓ 已保存城市数据到: {city_file}")


def generate_prompt(city_name, city_data):
    """生成 AI 提示词"""
    
    prompt = f"""A stunning, vibrant 3D rendered image of the **{city_name}** historical gourmet theme. Isometric view at 45 degrees, featuring a perfectly divided circular miniature landscape.

**【Artistic City Name Plaque】**
Next to (or behind) the circular base, there stands a massive, highly designed 3D Chinese characters "**{city_name}**". This text is not flat but a solid sculpture.
* **Material**: The text is made of **{city_data['city_material']}**.
* **Decoration**: Surrounded by **{city_data['city_decoration']}**, appearing magnificent and artistic.

**【Core Base】**
The circular platform is a massive, steaming **{city_data['base']}**. 
* **Material**: {city_data['base_desc']}, with edges showing golden crispy baked texture.
* **Historical Inscription**: Etched in light gold small seal script: "**{city_data['history_text']}**", with frosted gold luster.

**【First Quadrant (Top-Left - Morning Taste)】**
Displays a giant **{city_data['q1']['name']}**. {city_data['q1']['texture']}.
* **Interaction**: Miniature Pop Mart figures are {city_data['q1']['action']}.
* **Label**: Floating 3D bubble text: 『**{city_data['q1']['name']}**』.

**【Second Quadrant (Top-Right - Historical Feast)】**
Here stands **{city_data['q2']['name']}**. {city_data['q2']['texture']}.
* **Interaction**: Figures wearing **{city_data['q2']['costume']}** are {city_data['q2']['action']}.
* **Historical Silhouette**: Faintly in the background appears a translucent holographic silhouette of **{city_data['q2']['historical_figure']}**.
* **Label**: Floating 3D bubble text: 『**{city_data['q2']['name']}**』.

**【Third Quadrant (Bottom-Right - Street Smoke)】**
Shows **{city_data['q3']['name']}**. {city_data['q3']['texture']}.
* **Interaction**: Figures are {city_data['q3']['action']}.
* **Historical Silhouette**: Steam transforms into miniature silhouettes of **{city_data['q3']['historical_scene']}**.
* **Label**: Floating 3D bubble text: 『**{city_data['q3']['name']}**』.

**【Fourth Quadrant (Bottom-Left - Sweet Culture)】**
Here is **{city_data['q4']['name']}**. {city_data['q4']['texture']}.
* **Interaction**: Figures are {city_data['q4']['action']}.
* **Historical Silhouette**: Light and shadow of **{city_data['q4']['cultural_symbol']}** dancing in the background.
* **Label**: Floating 3D bubble text: 『**{city_data['q4']['name']}**』.

**【Technical Parameters】**
Pop Mart style, Pixar style 3D render, Isometric view, high saturation, vivid colors, depth of field, tilt-shift photography, C4D, Octane Render, 4k resolution, ray tracing, subsurface scattering on food, hyper-realistic food textures contrasted with cute chibi figures."""

    return prompt


def find_nanobanana():
    """查找 nanobanana.py"""
    nanobanana_paths = [
        "${HOME}/.claude/skills/nanobanana-skill/nanobanana.py",
        "/mnt/user-data/uploads/nanobanana.py",
        "${CLAUDE_PLUGIN_ROOT}/skills/nanobanana-skill/nanobanana.py",
        "./nanobanana.py",
        "../nanobanana-skill/nanobanana.py"
    ]
    
    for path in nanobanana_paths:
        expanded_path = os.path.expandvars(path)
        if os.path.exists(expanded_path):
            return expanded_path
    
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate 3D Historical Gourmet Diorama - 标准 Skill 版本"
    )
    parser.add_argument(
        "city",
        type=str,
        nargs="?",
        help="City name (e.g., 西安, 重庆, 成都, 北京, 广州, 温州)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output image filename (default: <city>-diorama.png)"
    )
    parser.add_argument(
        "--size",
        type=str,
        default="1024x1024",
        help="Image size/aspect ratio (default: 1024x1024)"
    )
    parser.add_argument(
        "--resolution",
        type=str,
        default="2K",
        choices=["1K", "2K", "4K"],
        help="Image resolution (default: 2K)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-3-pro-image-preview",
        help="Model to use (default: gemini-3-pro-image-preview)"
    )
    parser.add_argument(
        "--show-prompt",
        action="store_true",
        help="Show the generated prompt without generating image"
    )
    parser.add_argument(
        "--list-cities",
        action="store_true",
        help="List all available cities"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=None,
        help="Custom data directory path"
    )
    
    args = parser.parse_args()
    
    # 初始化城市数据库
    try:
        db = CityDatabase(args.data_dir)
    except Exception as e:
        print(f"错误: 无法初始化城市数据库: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 列出城市
    if args.list_cities:
        cities = db.list_cities()
        if not cities:
            print("警告: 没有找到任何城市数据")
            print(f"数据目录: {db.data_dir}")
            print("\n请确保数据文件存在:")
            print("  - cities.json (主数据文件)")
            print("  - 或单个城市的 JSON 文件")
        else:
            print("Available cities in database:")
            for city in cities:
                print(f"  - {city}")
        return
    
    # 检查是否提供了城市名称
    if not args.city:
        parser.error("请提供城市名称 (或使用 --list-cities 查看可用城市)")
    
    # 获取城市数据
    city_data = db.get_city(args.city)
    if not city_data:
        print(f"错误: 城市 '{args.city}' 不在数据库中", file=sys.stderr)
        print(f"\n可用城市: {', '.join(db.list_cities())}", file=sys.stderr)
        print(f"\n提示: 你可以在 {db.data_dir} 目录下添加新城市的 JSON 文件", file=sys.stderr)
        sys.exit(1)
    
    # 生成提示词
    prompt = generate_prompt(args.city, city_data)
    
    # 仅显示提示词
    if args.show_prompt:
        print("=" * 80)
        print("GENERATED PROMPT:")
        print("=" * 80)
        print(prompt)
        print("=" * 80)
        return
    
    # 设置默认输出文件名
    if args.output is None:
        args.output = f"{args.city}-diorama.png"
    
    # 查找 nanobanana
    nanobanana_path = find_nanobanana()
    if nanobanana_path is None:
        print("错误: 找不到 nanobanana.py", file=sys.stderr)
        print("请确保 nanobanana skill 已安装", file=sys.stderr)
        sys.exit(1)
    
    # 调用 nanobanana 生成图片
    print(f"Generating 3D food diorama for {args.city}...")
    print(f"Output: {args.output}")
    print(f"Size: {args.size}, Resolution: {args.resolution}")
    print()
    
    cmd = [
        "python3",
        nanobanana_path,
        "--prompt", prompt,
        "--output", args.output,
        "--size", args.size,
        "--resolution", args.resolution,
        "--model", args.model
    ]
    
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
