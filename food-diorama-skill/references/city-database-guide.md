# City Database Extension Guide

## Adding a New City

To add a new city to the food diorama generator, you need to define its food culture across four quadrants:

### Data Structure Template

```python
"城市名": {
    "base": "基础圆盘食物",
    "base_desc": "圆盘的详细视觉描述",
    "history_text": "蚀刻在底座的历史铭文(8-12字)",
    "city_material": "城市名牌的材质特征",
    "city_decoration": "名牌周围的装饰元素",
    
    # 第一象限:晨之味 (左上)
    "q1": {
        "name": "早餐美食名称",
        "desc": "美食外观描述",
        "texture": "质感和细节描述",
        "action": "小人互动动作",
        "costume": ""  # 可选
    },
    
    # 第二象限:历史硬菜 (右上)
    "q2": {
        "name": "传统硬菜名称",
        "desc": "美食外观描述",
        "texture": "质感和细节描述",
        "action": "小人互动动作",
        "costume": "历史服饰描述",
        "historical_figure": "相关历史人物"
    },
    
    # 第三象限:市井烟火 (右下)
    "q3": {
        "name": "街头小吃名称",
        "desc": "美食外观描述",
        "texture": "质感和细节描述",
        "action": "小人互动动作",
        "historical_scene": "历史场景描述"
    },
    
    # 第四象限:甜蜜文化 (左下)
    "q4": {
        "name": "甜品小吃名称",
        "desc": "美食外观描述",
        "texture": "质感和细节描述",
        "action": "小人互动动作",
        "cultural_symbol": "文化符号描述"
    }
}
```

### Field Descriptions

#### Base Platform
- **base**: The signature food that forms the circular platform
- **base_desc**: Detailed visual description with colors, textures, steam, etc.
- **history_text**: 8-12 character historical phrase about the city
- **city_material**: Material for the 3D city name sculpture (e.g., stone, neon, jade)
- **city_decoration**: Decorative elements around the name (clouds, leaves, ribbons)

#### Quadrant Fields
- **name**: Food item name in Chinese
- **desc**: Brief appearance description
- **texture**: Detailed texture, colors, reflections, layers
- **action**: What the miniature figure is doing (e.g., "用筷子夹起", "正在品尝")
- **costume** (Q2 only): Traditional costume style
- **historical_figure** (Q2 only): Related historical person
- **historical_scene** (Q3 only): Historical setting or street scene
- **cultural_symbol** (Q4 only): Cultural element or symbol

### Tips for Good Descriptions

1. **Be visually specific**: Describe colors, textures, steam, reflections
2. **Use food terminology**: 酥脆, 晶莹, 焦黄, 软糯, 金黄, 红油
3. **Include interactions**: Small figures create scale contrast
4. **Add cultural depth**: Historical figures, scenes, symbols add meaning
5. **Balance the quadrants**: Mix breakfast, feast, street, and sweet

### Example: Adding Hangzhou (杭州)

```python
"杭州": {
    "base": "西湖醋鱼",
    "base_desc": "一个巨大的、淋着酱汁的西湖醋鱼圆盘,鱼身泛着琥珀色光泽",
    "history_text": "上有天堂下有苏杭",
    "city_material": "西湖玉石与青瓷",
    "city_decoration": "荷花与丝绸飘带",
    "q1": {
        "name": "葱包烩",
        "desc": "金黄的油条包裹着葱段,表面刷着甜面酱",
        "texture": "油条酥脆,甜面酱泛着光泽",
        "action": "咬葱包烩"
    },
    "q2": {
        "name": "东坡肉",
        "desc": "方正的红烧肉块,肥瘦相间",
        "texture": "肉皮焦糖化,肥肉晶莹剔透",
        "action": "用筷子夹起肉块",
        "costume": "宋朝文人长袍",
        "historical_figure": "苏东坡"
    },
    "q3": {
        "name": "片儿川",
        "desc": "宽面条浸在笋片与雪菜的汤中",
        "texture": "面条滑润,笋片脆嫩",
        "action": "挑起面条",
        "historical_scene": "西湖边茶馆"
    },
    "q4": {
        "name": "桂花糕",
        "desc": "白色糕体嵌着金黄桂花",
        "texture": "糕体绵软,桂花点点闪耀",
        "action": "切块",
        "cultural_symbol": "满陇桂雨与断桥"
    }
}
```

## Integration Steps

1. Edit `scripts/generate_food_diorama.py`
2. Add your city entry to the `CITY_DATABASE` dictionary
3. Test with: `python3 generate_food_diorama.py 杭州 --show-prompt`
4. Generate: `python3 generate_food_diorama.py 杭州`
5. Iterate on descriptions if needed

## Food Selection Guidelines

### Q1 - Morning Taste (晨之味)
Traditional breakfast items, often liquid-based (粥, 汤, 豆浆)

### Q2 - Historical Feast (历史硬菜)
Signature main dishes with historical significance
Must include historical figure or dynasty reference

### Q3 - Street Smoke (市井烟火)
Popular street food that represents local daily life
Should include a street scene or market setting

### Q4 - Sweet Culture (甜蜜文化)
Traditional desserts or snacks
Include cultural symbols unique to the region

## Quality Checklist

- [ ] Each food has distinct visual characteristics
- [ ] Textures are described with specific adjectives
- [ ] Actions create believable figure interactions
- [ ] Historical elements add cultural depth
- [ ] City material reflects local architecture/culture
- [ ] All four quadrants balance variety and representation
