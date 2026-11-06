from __future__ import annotations

import csv
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "equipment"

ITEMS = [
    ("自由重量", "哑铃", "Dumbbells", "dumbbells", "small weights", "两端是成对配重；固定器械区里通常按重量成排摆放。"),
    ("自由重量", "壶铃", "Kettlebells", "kettlebell", "small weights", "球形或钟形配重，上方带一个整体把手。"),
    ("杠铃与杠铃片", "EZ 曲杆", "EZ Curl Bar", "ezbar", "bar & plates", "握持段呈波浪弯曲，和直杠外形区别明显。"),
    ("杠铃与杠铃片", "奥林匹克杠铃", "Olympic Barbell", "olympicbar", "bar & plates", "长直杆两端有较粗的套筒，可装大孔杠铃片。"),
    ("杠铃与杠铃片", "标准杠铃", "Standard Barbell", "standardbar", "bar & plates", "直杆两端较细，常见于轻型或家用套装；和奥林匹克杆的套筒规格不同。"),
    ("杠铃与杠铃片", "六角杠 / 陷阱杠", "Trap Bar", "trapbar", "bar & plates", "杠身是六边形或菱形，人站在框内握住两侧把手。"),
    ("杠铃与杠铃片", "杠铃片", "Weight Plates", "plates", "bar & plates", "中心孔套在杠铃或器械的插片杆上；不同直径和孔径并存。"),
    ("训练凳与训练架", "可调节训练凳", "Adjustable Bench", "adjustablebench", "benches & racks", "靠背角度可调；通常可以平放、上斜，有些型号也能下斜。"),
    ("训练凳与训练架", "平板训练凳", "Flat Bench", "flatbench", "benches & racks", "整张靠垫保持水平，不带角度调节结构。"),
    ("训练凳与训练架", "可调下斜训练凳", "Adjustable Decline Bench", "declinebench", "benches & racks", "靠垫向下倾斜，常带脚踝固定滚垫。"),
    ("训练凳与训练架", "奥林匹克平板卧推架", "Olympic Flat Bench", "olympicflat", "benches & racks", "平凳与两侧杠铃托架连在一体；不是单独的平板凳。"),
    ("训练凳与训练架", "奥林匹克上斜卧推架", "Olympic Incline Bench", "olympicincline", "benches & racks", "斜靠背配固定杠铃托架，整体比可调训练凳更像一体机。"),
    ("训练凳与训练架", "奥林匹克下斜卧推架", "Olympic Decline Bench", "olympicdecline", "benches & racks", "下斜靠垫配杠铃托架，通常带脚踝固定垫。"),
    ("训练凳与训练架", "牧师凳", "Preacher Curl Bench", "preacherbench", "benches & racks", "前方有一块宽斜垫作为手臂支撑，通常配独立座椅。"),
    ("训练凳与训练架", "背伸凳 / 罗马椅", "Hyperextension Bench", "hyperbench", "benches & racks", "斜垫和脚踝固定滚垫组成，常见 45 度角支撑架。"),
    ("训练凳与训练架", "引体、双杠与抬膝综合架", "Chin Up, Dip & Leg Raise Station", "dipstation", "benches & racks", "上方有引体把手，中间有双杠把手和背垫/肘垫。"),
    ("训练凳与训练架", "史密斯机", "Smith Machine", "smith", "benches & racks", "杠铃沿两根导轨上下移动，立柱上有安全挂钩。"),
    ("训练凳与训练架", "深蹲架 / 力量架", "Power Rack", "rack", "benches & racks", "四根立柱围成框架，配安全杆与多档挂钩；外观不同于史密斯机的导轨杠。"),
    ("滑轮与拉力器", "单侧可调滑轮", "Adjustable Pulley", "singlepulley", "cable machines", "一根立柱配配重片和可上下调节的滑轮。"),
    ("滑轮与拉力器", "双侧可调滑轮 / 龙门架", "Dual Adjustable Pulley", "crossover", "cable machines", "两根带配重的立柱相对摆放，中间留出训练空间。"),
    ("滑轮与拉力器", "坐姿划船机", "Cable Row Machine", "cable-row", "cable machines", "坐垫前有脚踏板和低位拉索；配重塔通常在侧后方。"),
    ("滑轮与拉力器", "高位下拉机", "Lat Pulldown Machine", "latpulldown", "cable machines", "高位滑轮配长横杆，下方有座椅和大腿固定垫。"),
    ("固定配重器械", "站姿多功能飞鸟机", "Standing Multi Flight", "multiflight", "weight machines", "两侧可调拉索围绕中间开放空间布置，常用于多方向拉索训练。"),
    ("固定配重器械", "腹肌训练机", "Abdominal Machine", "abmachine", "weight machines", "有靠背、座垫和前方握把/滚垫，主架连接配重塔。"),
    ("固定配重器械", "髋外展机", "Hip Abduction Machine", "hipabduction", "weight machines", "坐姿并将大腿靠在两侧垫块外侧；同一器械常兼有内收功能。"),
    ("固定配重器械", "髋内收机", "Hip Adduction Machine", "hipadduction", "weight machines", "坐姿并将大腿靠在两侧垫块内侧；外观常与髋外展机相近。"),
    ("固定配重器械", "辅助引体 / 双杠机", "Assisted Pull-Up / Dip Machine", "assisted", "weight machines", "带可升降膝垫或踏板，旁边有引体/双杠把手和配重塔。"),
    ("固定配重器械", "二头弯举机", "Biceps Curl Machine", "bicepsmachine", "weight machines", "座椅前方有斜置手臂垫与握把，通常连配重塔。"),
    ("固定配重器械", "小腿训练机", "Calf Machine", "calfmachine", "weight machines", "座椅或肩垫、脚踏板与脚踝滚垫组合；不同型号姿态差异较大。"),
    ("固定配重器械", "坐姿胸推机", "Chest Press Machine", "chestpress", "weight machines", "靠背座椅两侧有向前推的握把，配重塔与机架相连。"),
    ("固定配重器械", "夹胸 / 后束飞鸟机", "Pec Fly / Rear Delt Machine", "pecfly", "weight machines", "座椅两侧有可转动的长臂/肘垫，部分机型可反向使用。"),
    ("固定配重器械", "臀推机", "Hip Thrust Machine", "hipthrust", "weight machines", "有靠背或肩背垫、臀部支撑位和可旋转的髋部压垫。"),
    ("固定配重器械", "腿屈伸机", "Leg Extension Machine", "legextension", "weight machines", "坐姿，膝前下方有一根可转动的腿垫滚轴。"),
    ("固定配重器械", "俯卧腿弯举机", "Lying Leg Curl Machine", "lyingcurl", "weight machines", "俯卧长垫床，脚踝端有滚轴，配重塔位于一端。"),
    ("固定配重器械", "坐姿腿弯举机", "Seated Leg Curl Machine", "seatedcurl", "weight machines", "有靠背座椅、大腿压垫和小腿滚轴。"),
    ("固定配重器械", "45 度腿举机", "45-Degree Leg Press", "legpress", "weight machines", "座椅和脚踏板沿斜轨布置；部分型号使用插片配重，部分使用配重塔。"),
    ("固定配重器械", "哈克深蹲机", "Hack Squat Machine", "hacksquat", "weight machines", "斜向滑轨配肩垫、靠背和脚踏板；常带装片杆。"),
    ("固定配重器械", "背部伸展机", "Back Extension Machine", "backextension", "weight machines", "坐姿靠背或前倾支撑垫连接阻力臂/配重塔。"),
    ("固定配重器械", "三头肌推压机", "Triceps Press Machine", "tricepspress", "weight machines", "坐姿靠背配侧边握把，手臂伸展方向的固定器械。"),
    ("插片式器械", "插片式平板胸推机", "Plate-Loaded Flat Chest Press", "platechest", "plate-loaded machines", "两侧杠杆臂各有插片杆，座椅和靠背位于中间。"),
    ("插片式器械", "插片式下斜胸推机", "Plate-Loaded Decline Chest Press", "platedecline", "plate-loaded machines", "斜置靠背配向前推的杠杆臂，阻力片挂在两侧。"),
    ("插片式器械", "高位划船机", "Plate-Loaded High Row", "highrow", "plate-loaded machines", "高位把手和胸垫/座椅组合，侧边可加载杠铃片。"),
    ("插片式器械", "插片式上斜推胸机", "Plate-Loaded Incline Press", "plateincline", "plate-loaded machines", "上斜靠背和前推把手，杠杆臂两侧带插片杆。"),
    ("插片式器械", "片装硬拉训练机", "Deadlift Trap Machine", "deadliftmachine", "plate-loaded machines", "低位可握把手与两侧装片杠杆组成，具体结构会因品牌而异。"),
    ("插片式器械", "V 型深蹲机", "Plate-Loaded V-Squat", "vsquat", "plate-loaded machines", "肩背垫与脚踏平台沿弧形/斜轨移动，通常两侧装片。"),
    ("插片式器械", "T 型杠划船机", "T-Bar Row Machine", "tbarrow", "plate-loaded machines", "一端固定转轴，另一端有把手和胸垫/脚踏板。"),
    ("插片式器械", "坐姿二头弯举机", "Seated Biceps Curl Machine", "preacher-machine", "plate-loaded machines", "座椅前方有斜臂垫和弯举握把，阻力由杠杆臂或配重提供。"),
    ("插片式器械", "坐姿侧平举机", "Seated Lateral Raise Machine", "lateralraise", "plate-loaded machines", "坐姿，两侧手臂垫/握把随杠杆向外抬起，常见装片结构。"),
    ("插片式器械", "坐姿腿举机", "Seated Leg Press", "seatedlegpress", "plate-loaded machines", "坐姿背靠斜垫、正前方大脚踏板，通常两侧装片。"),
    ("插片式器械", "肩推机", "Shoulder Press Machine", "shoulderpress", "plate-loaded machines", "靠背座椅两侧有上推把手，常见杠杆臂和装片杆。"),
    ("插片式器械", "三头肌伸展机", "Triceps Extension Machine", "tricepsextension", "plate-loaded machines", "座椅/靠背配侧边杠杆臂，手握把手做伸展轨迹。"),
    ("有氧器械", "跑步机", "Treadmill", "treadmill", "cardio", "有连续跑带、侧扶手和前方控制台。"),
    ("有氧器械", "椭圆机", "Elliptical Machine", "elliptical", "cardio", "双脚踏板沿椭圆轨迹移动，常配活动长把手。"),
    ("有氧器械", "室内划船器", "Rowing Machine", "rowing", "cardio", "长滑轨、可滑动座垫、脚踏板和拉手；和坐姿划船力量器械不同。"),
    ("有氧器械", "楼梯机", "Stair Climber", "stairclimber", "cardio", "连续转动的阶梯踏板配扶手和控制台。"),
    ("有氧器械", "固定自行车", "Stationary Bike", "bike", "cardio", "车架固定，带座椅、脚蹬和控制台。"),
    ("小型训练器材", "弹力带", "Resistance Band", "band", "accessories", "可为环形带，也可为带把手的管状带。"),
    ("小型训练器材", "训练垫", "Exercise Mat", "mat", "accessories", "薄型可卷垫；瑜伽垫是常见类型之一。"),
    ("小型训练器材", "有氧踏板", "Aerobic Step", "step", "accessories", "低矮长方踏台，常见可拆高度垫块。"),
    ("小型训练器材", "半球平衡球", "Half Ball Trainer", "halfbball", "accessories", "半球形弹性上表面，下面是平底支撑盘。"),
    ("小型训练器材", "普拉提球 / 健身球", "Pilates Ball", "pilatesball", "accessories", "轻质圆球；健身房里的大小可能与本示意不同。"),
    ("小型训练器材", "腹肌轮", "Abdominal Wheel", "wheel", "accessories", "一个或两个轮子配贯穿手柄。"),
    ("小型训练器材", "跳箱", "Plyometric Box", "box", "accessories", "稳定的立方或长方箱体，健身房常见木箱或软包箱。"),
]


def ln(x1, y1, x2, y2, width=18, color="#737d86", extra=""):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" {extra}/>'


def rect(x, y, w, h, fill="#252b31", rx=8, stroke="#11181e", sw=6, transform=""):
    tr = f' transform="{transform}"' if transform else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{tr}/>'


def ellipse(cx, cy, rx, ry, fill="#252b31", stroke="#11181e", sw=6):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def path(d, fill="none", stroke="#303840", sw=16, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def tube(x1, y1, x2, y2, width=19):
    return ln(x1, y1, x2, y2, width + 8, "#272e35") + ln(x1, y1, x2, y2, width, "url(#steel)") + ln(x1, y1, x2, y2, max(2, width // 5), "#e1e5e8")


def pad(x, y, w, h, radius=14, transform=""):
    return rect(x, y, w, h, "url(#pad)", radius, "#10161c", 7, transform)


def stack(x=605, y=300, h=245):
    out = rect(x, y, 90, h, "#20272d", 8, "#10161c", 7)
    for i in range(1, 8):
        yy = y + i * h / 8
        out += ln(x + 8, yy, x + 82, yy, 5, "#929ba3")
    return out


def dumbbells():
    return ellipse(420, 530, 215, 44, "#eef0f1", "#d9dde0", 2) + ln(267, 390, 570, 490, 38, "#77818a") + path("M170 320 L220 290 L270 320 L270 440 L220 470 L170 440 Z", "#171d22", "#0c1116", 9) + path("M550 415 L600 385 L650 415 L650 535 L600 565 L550 535 Z", "#171d22", "#0c1116", 9) + path("M210 323 L240 306 L240 456", "none", "#69747c", 5) + path("M590 419 L620 401 L620 551", "none", "#69747c", 5)


def kettlebell():
    return ellipse(410, 555, 205, 40, "#eef0f1", "#d9dde0", 2) + path("M305 395 C300 235 520 235 515 395", "none", "#171d22", 34) + path("M330 380 C330 273 495 273 490 380", "none", "#69747c", 11) + path("M270 400 Q410 335 550 400 L585 520 Q580 615 410 640 Q240 615 235 520 Z", "url(#pad)", "#10161c", 8) + ellipse(410, 530, 118, 100, "#343c43", "#69747c", 5)


def barbell(ez=False, trap=False, standard=False, plates=True):
    if trap:
        return ellipse(410, 560, 250, 42, "#eef0f1", "#d9dde0", 2) + path("M235 330 L555 330 L620 435 L555 535 L235 535 L170 435 Z", "none", "#171d22", 22) + ln(275, 330, 275, 535, 22, "#75808a") + ln(515, 330, 515, 535, 22, "#75808a") + ln(275, 435, 515, 435, 18, "#bdc3c8")
    if ez:
        d = "M160 430 L230 430 L275 360 L330 500 L385 360 L440 500 L495 360 L550 430 L640 430"
        out = ellipse(410, 560, 250, 42, "#eef0f1", "#d9dde0", 2) + path(d, "none", "#59636c", 32) + path(d, "none", "#cbd1d5", 15)
    else:
        out = ellipse(410, 560, 250, 42, "#eef0f1", "#d9dde0", 2) + ln(160, 430, 660, 430, 34 if not standard else 24, "#69747c") + ln(160, 422, 660, 422, 8, "#dce0e3")
    if plates:
        for x, r in [(190, 72), (220, 96), (600, 72), (630, 96)]:
            out += ellipse(x, 430, 16, r, "#171d22", "#080c10", 5) + ellipse(x, 430, 7, r-13, "#48515a", "#8c959d", 3)
    return out


def bench(style="flat"):
    out = ellipse(410, 595, 250, 42, "#eef0f1", "#d9dde0", 2)
    if style == "incline":
        out += pad(340, 230, 115, 245, 18, "rotate(-32 397 350)")
        out += pad(420, 420, 125, 92, 15, "rotate(-32 482 466)")
    elif style in ("decline", "olympicdecline"):
        out += pad(305, 300, 110, 245, 18, "rotate(18 360 420)") + pad(400, 520, 125, 78, 16)
        out += tube(242, 265, 242, 365, 25) + tube(600, 265, 600, 365, 25) + tube(230, 260, 612, 260, 24)
        out += pad(212, 240, 60, 110, 15) + pad(572, 240, 60, 110, 15)
    else:
        out += pad(290, 355, 300, 90, 20)
        if style == "adjustable":
            out += pad(350, 195, 120, 225, 18, "rotate(-18 410 305)")
    out += tube(320, 435, 265, 565, 21) + tube(545, 435, 605, 565, 21) + tube(260, 565, 610, 565, 23)
    if style in ("olympicflat", "olympicincline"):
        out += tube(235, 250, 235, 420, 24) + tube(635, 250, 635, 420, 24) + tube(220, 255, 650, 255, 23)
        out += ln(185, 255, 220, 255, 20, "#4b545c") + ln(650, 255, 685, 255, 20, "#4b545c")
        out += pad(180, 220, 30, 70, 12) + pad(675, 220, 30, 70, 12)
    return out


def cable_machine(kind="single"):
    out = ellipse(410, 600, 250, 42, "#eef0f1", "#d9dde0", 2)
    if kind == "crossover":
        for x in (205, 615):
            out += tube(x, 210, x, 550, 28) + tube(x, 210, x+38, 210, 26) + rect(x-36, 350, 72, 170, "#303840", 5, "#171d22", 6)
            out += tube(x, 280, x+90 if x < 410 else x-90, 280, 12)
            out += path(f"M{x} 280 Q410 210 {410 if x<410 else 410} 340", "none", "#535d66", 6)
        out += tube(205, 210, 615, 210, 22) + tube(205, 550, 615, 550, 24)
        return out
    out += tube(520, 190, 520, 560, 28) + stack(560, 300, 215) + tube(430, 550, 620, 550, 22)
    if kind == "single":
        out += tube(520, 285, 335, 285, 12) + ellipse(335,285,14,14,"#c5cbd0") + path("M335 285 L335 435", "none", "#4e5962", 6)
        out += path("M335 435 Q335 475 385 475", "none", "#505a63", 8)
    elif kind == "pulldown":
        out += pad(230, 350, 150, 65, 15) + tube(260, 415, 260, 535, 20) + pad(252, 300, 20, 80, 7) + path("M520 235 L410 235 L340 260 L285 235", "none", "#47515a", 9) + tube(284,235,250,235,18) + tube(520,235,560,235,18)
    elif kind == "row":
        out += pad(260, 440, 130, 60, 12) + tube(290, 500, 285, 555, 18) + path("M340 420 L275 500 L220 500 L210 540 L330 540", "none", "#333b42", 12) + path("M520 335 L425 335 L370 420", "none", "#4a545c", 7) + path("M370 420 L345 450", "none", "#4a545c", 7) + ln(205, 505, 260, 505, 15, "#636e77")
    else:
        out += pad(320, 420, 130, 62, 12) + pad(315, 320, 140, 110, 12) + path("M520 255 L430 255 L375 280 L300 255", "none", "#4a545c", 8) + tube(300,255,275,255,17) + tube(520,255,560,255,17)
    return out


def tower(kind="rack"):
    out = ellipse(410, 600, 250, 42, "#eef0f1", "#d9dde0", 2)
    for x in (250, 570):
        out += tube(x, 180, x, 550, 28)
        for y in range(215, 505, 40):
            out += ellipse(x, y, 5, 5, "#d5dade", "#4d5861", 2)
    out += tube(250, 185, 570, 185, 24) + tube(250, 550, 570, 550, 25)
    if kind == "smith":
        out += tube(345, 195, 345, 505, 13) + tube(475,195,475,505,13) + ln(300, 340, 520, 340, 27, "#606b73") + ln(300, 332, 520, 332, 8, "#d7dce0")
        for x in (315, 505): out += rect(x-8, 320, 16, 42, "#f0b84a", 4, "#9e731d", 3)
    elif kind == "dip":
        out += tube(250, 195, 250, 290, 20) + tube(570,195,570,290,20) + tube(250,290,340,290,18) + tube(480,290,570,290,18)
        out += pad(360, 355, 95, 185, 16) + tube(365, 355, 350, 540, 18) + tube(445,355,460,540,18)
        out += tube(250,550,220,575,18) + tube(570,550,600,575,18)
    else:
        out += tube(250, 185, 570, 185, 22) + tube(215, 385, 605, 385, 24) + tube(250, 500, 570, 500, 20)
        for x in (220,600): out += tube(x,385,x,430,18)
    return out


def selector(kind="chest"):
    out = ellipse(410, 600, 250, 42, "#eef0f1", "#d9dde0", 2) + tube(575, 190, 575, 550, 27) + stack(595, 300, 220)
    # Main upright and seat/back structure.
    out += tube(575, 190, 420, 190, 22) + tube(420,190,420,390,20)
    if kind in ("chest", "shoulder", "biceps", "triceps"):
        out += pad(355, 270, 105, 150, 14) + pad(350, 420, 180, 65, 14) + tube(390,485,340,565,20) + tube(480,485,520,565,20)
        if kind == "biceps":
            out += pad(280, 365, 160, 60, 16, "rotate(-20 360 395)") + path("M320 365 Q280 310 290 260", "none", "#47515a", 20) + path("M290 260 L260 245", "none", "#47515a", 16)
        elif kind == "triceps":
            out += path("M420 270 Q315 250 300 340 L315 390", "none", "#505b64", 16) + path("M300 340 L270 390", "none", "#505b64", 16)
        else:
            for side in (-1,1):
                x=400+side*25
                out += path(f"M{x} 335 Q{x+side*90} 300 {x+side*115} 240 L{x+side*120} 200", "none", "#505b64", 20)
                out += ln(x+side*120, 200, x+side*120, 165, 14, "#313a42")
    elif kind in ("legext", "seatedcurl"):
        out += pad(350, 300, 105, 160, 14) + pad(340, 455, 190, 56, 14) + tube(390,510,340,565,18) + tube(490,510,525,565,18) + path("M390 455 Q470 500 500 530", "none", "#454f57", 20) + ellipse(500,530,34,17,"#292f35")
    elif kind == "lyingcurl":
        out += pad(260,350,280,60,12) + pad(520,320,48,75,12) + tube(300,410,270,555,18) + tube(490,410,535,555,18) + path("M440 405 Q500 455 530 475", "none", "#454f57", 20) + ellipse(530,475,34,17,"#292f35")
    elif kind == "row":
        out += pad(300,400,125,60,12) + pad(305,320,36,100,8) + tube(360,460,340,555,18) + path("M430 425 L470 475 L490 475 L500 510", "none", "#454f57", 12) + ln(450,470,500,470,14,"#454f57")
    elif kind == "legpress":
        out += pad(345,390,115,68,12,"rotate(-25 400 420)") + pad(270,290,120,100,12,"rotate(-25 330 340)") + path("M250 285 L510 500 L560 540", "none", "#444e57", 22) + path("M245 300 L490 510", "none", "#929ba3", 7)
    elif kind == "fly":
        out += pad(355,300,105,150,14) + pad(350,435,180,60,14) + tube(390,495,350,565,18) + tube(490,495,530,565,18)
        out += path("M350 320 Q270 300 260 405 Q265 465 335 455", "none", "#4a545d", 20) + path("M460 320 Q540 300 550 405 Q545 465 475 455", "none", "#4a545d", 20)
    elif kind == "hip":
        out += pad(360,285,100,165,14) + pad(340,440,185,56,14) + tube(380,496,335,565,18) + tube(490,496,530,565,18)
        out += tube(350,385,290,385,18) + tube(470,385,530,385,18) + pad(270,360,44,75,14) + pad(515,360,44,75,14)
    elif kind == "ab":
        out += pad(335,285,120,175,14) + pad(355,445,170,55,14) + tube(390,500,345,565,18) + tube(485,500,530,565,18) + path("M340 320 Q280 330 300 410 L340 430", "none", "#46515a", 18) + tube(300,400,325,420,16)
    elif kind == "calf":
        out += pad(345,390,130,65,12) + pad(360,300,100,120,14) + tube(385,455,350,560,18) + tube(465,455,505,560,18) + tube(330,340,510,340,22) + pad(330,315,50,55,12)
    elif kind == "hipthrust":
        out += pad(250,390,260,70,20) + pad(450,330,80,110,18) + tube(270,460,245,555,20) + tube(475,440,535,555,20) + path("M310 385 Q420 330 535 360", "none", "#4b555d", 20) + pad(430,330,125,48,16)
    else:  # general trunk machine
        out += pad(350,280,110,165,14) + pad(335,435,185,58,14) + tube(370,490,340,565,18) + tube(490,490,530,565,18)
    return out


def plate_machine(kind="platechest"):
    out = ellipse(410, 600, 250, 42, "#eef0f1", "#d9dde0", 2)
    out += tube(270,240,270,530,26) + tube(550,240,550,530,26) + tube(270,530,550,530,24) + pad(350,360,155,75,14) + pad(370,260,115,150,14)
    out += tube(345,435,320,550,19) + tube(505,435,530,550,19)
    if kind in ("platechest", "platedecline", "plateincline", "shoulder", "triceps"):
        angle = -14 if kind == "plateincline" else (16 if kind == "platedecline" else 0)
        transform = f"rotate({angle} 430 360)" if angle else ""
        out += path("M385 365 Q300 335 310 260 L280 215", "none", "#3c464e", 20, f'transform="{transform}"' if transform else "")
        out += path("M475 365 Q560 335 550 260 L580 215", "none", "#3c464e", 20, f'transform="{transform}"' if transform else "")
        out += ln(280,215,250,190,15,"#333c44") + ln(580,215,610,190,15,"#333c44")
        for x in (225, 635): out += ellipse(x, 230, 24, 45, "#171d22", "#05090d", 5) + ellipse(x,230,10,30,"#515b63","#9ca4ab",3)
    elif kind == "row":
        out += path("M520 300 L475 240 L420 245 L390 315", "none", "#333c44", 23) + path("M400 315 L360 270 L325 270", "none", "#333c44", 20) + pad(300,285,95,50,12)
        for x in (235, 600): out += ellipse(x, 300, 26, 50, "#171d22", "#05090d", 5)
    elif kind == "legpress":
        out += path("M250 260 L520 470 L575 525", "none", "#303941", 25) + pad(210,220,110,130,12,"rotate(-35 265 285)") + pad(400,430,125,85,12,"rotate(-35 462 470)")
        for x in (245,580): out += ellipse(x,300,25,48,"#171d22","#05090d",5)
    elif kind == "hacksquat":
        out += path("M280 260 L490 260 L520 490", "none", "#303941", 24) + pad(300,270,120,120,12,"rotate(-28 360 330)") + pad(465,430,125,80,12,"rotate(-10 520 470)")
        for x in (240,600): out += ellipse(x,300,25,48,"#171d22","#05090d",5)
    elif kind == "vsquat":
        out += path("M290 260 Q370 220 460 270 L510 440", "none", "#303941", 24) + pad(310,245,140,95,14) + pad(450,410,130,80,14)
        for x in (240,600): out += ellipse(x,300,25,48,"#171d22","#05090d",5)
    else:
        out += path("M370 300 L330 225 M480 300 L530 225", "none", "#303941", 20) + pad(280,300,52,65,12) + pad(515,300,52,65,12)
        for x in (230, 610): out += ellipse(x, 300, 25, 48, "#171d22", "#05090d", 5)
    return out


def smallgear(kind):
    out = ellipse(410, 590, 250, 40, "#eef0f1", "#d9dde0", 2)
    if kind == "band":
        return out + path("M230 360 C230 220 590 220 590 360 C590 500 230 500 230 360", "none", "#51a978", 30) + path("M310 380 C310 300 510 300 510 380", "none", "#b3dfc0", 12)
    if kind == "mat":
        return out + path("M230 430 L500 330 L610 390 L335 490 Z", "#387ab3", "#225578", 7) + path("M335 490 L335 550 Q340 600 395 575 L610 485 L610 390", "#4f93c7", "#225578", 7) + ln(400, 468, 580, 405, 4, "#d2e7f4")
    if kind == "step":
        return out + path("M210 450 L580 450 L630 500 L260 500 Z", "#313941", "#11171d", 7) + path("M260 500 L630 500 L630 555 L260 555 Z", "#737d86", "#313941", 7) + path("M210 450 L260 500 L260 555 L210 505 Z", "#59636c", "#313941", 7) + ln(290,455,570,455,5,"#aeb5bb")
    if kind == "halfball":
        return out + ellipse(410, 480, 185, 125, "#2788cc", "#15577f", 8) + rect(225, 480, 370, 70, "#282f36", 14, "#10161c", 7) + path("M250 480 A160 100 0 0 1 570 480", "none", "#8dcbee", 10)
    if kind == "pilatesball":
        return out + ellipse(410, 440, 175, 175, "#9ca4aa", "#656d74", 8) + path("M280 390 Q410 350 540 390 M255 440 Q410 400 565 440 M275 490 Q410 530 545 490", "none", "#dfe3e6", 8)
    if kind == "wheel":
        return out + ellipse(410, 425, 110, 165, "#262d33", "#11171c", 8) + ellipse(410, 425, 66, 102, "#69747d", "#d4d9dd", 7) + ln(180,425,640,425,28,"#313941") + ln(180,425,180,425,48,"#161c22") + ln(640,425,640,425,48,"#161c22")
    if kind == "box":
        return out + path("M260 340 L485 275 L600 355 L365 430 Z", "#d7bd95", "#735a39", 6) + path("M260 340 L365 430 L365 560 L260 470 Z", "#b39264", "#735a39", 6) + path("M365 430 L600 355 L600 480 L365 560 Z", "#c3a477", "#735a39", 6) + rect(292, 385, 38, 20, "#403a32", 4, "#403a32", 2)
    return out


def cardio(kind):
    out = ellipse(410, 605, 255, 42, "#eef0f1", "#d9dde0", 2)
    if kind == "treadmill":
        out += path("M200 500 L555 500 L590 535 L205 535 Z", "#252c32", "#11171d", 8) + tube(250, 500, 300, 280, 22) + tube(560,500,510,270,22) + tube(300,280,510,270,20) + rect(425,210,115,60,"#1f2830",8,"#11171d",6) + ln(230,470,270,500,13,"#616c75")
    elif kind == "bike":
        out += ellipse(350,455,100,105,"#252c32","#11171d",8) + ellipse(350,455,50,55,"#87919a","#343c44",5) + tube(350,455,480,335,18) + tube(350,455,250,335,18) + tube(480,335,250,335,18) + tube(480,335,505,245,18) + tube(490,250,570,250,16) + tube(250,335,230,250,18) + pad(205,225,90,22,9) + tube(250,335,225,355,13) + rect(490,205,72,42,"#303941",8,"#11171d",5) + tube(280,560,430,560,17)
    elif kind == "rowing":
        out += path("M200 505 L610 505 L640 530 L205 530 Z", "#313940", "#11171d", 7) + tube(255,500,305,300,20) + tube(305,300,465,300,20) + pad(365,278,80,45,12) + path("M460 300 L500 350 L520 430", "none", "#303941", 16) + path("M520 430 Q450 395 380 430", "none", "#303941", 10) + rect(465,240,60,42,"#252d34",7,"#11171d",5)
    elif kind == "stairs":
        out += path("M300 500 L530 500 L550 275 L430 275 Z", "#313941", "#11171d", 7) + path("M310 470 L445 470 L445 430 L315 430 Z M315 420 L450 420 L450 380 L320 380 Z M320 370 L455 370 L455 330 L325 330 Z M325 320 L460 320 L460 280 L330 280 Z", "#252d34", "#59636c", 5) + tube(315,275,275,195,18) + tube(530,275,575,195,18) + tube(275,195,575,195,18) + rect(398,210,72,45,"#252d34",6,"#11171d",5)
    else:
        out += ellipse(360,460,75,112,"#252d34","#11171d",8) + ellipse(360,460,35,65,"#7c8790","#414a52",5) + tube(360,460,485,330,20) + tube(360,460,265,360,20) + path("M485 330 Q560 300 570 410 L530 490", "none", "#323a42", 20) + path("M265 360 Q230 280 340 250", "none", "#323a42", 20) + rect(455,215,82,48,"#252d34",7,"#11171d",5) + tube(360,560,515,560,18)
    return out


def icon(kind):
    if kind == "dumbbells": return dumbbells()
    if kind == "kettlebell": return kettlebell()
    if kind == "ezbar": return barbell(ez=True, plates=False)
    if kind == "olympicbar": return barbell(plates=True)
    if kind == "standardbar": return barbell(standard=True, plates=False)
    if kind == "trapbar": return barbell(trap=True)
    if kind == "plates": return ellipse(410,590,240,42,"#eef0f1","#d9dde0",2) + ellipse(410,390,170,170,"#20262c","#080d11",10) + ellipse(410,390,120,120,"#343c43","#929aa1",6) + ellipse(410,390,45,45,"#fff","#333b42",8)
    if kind in ("flatbench","adjustablebench","declinebench","olympicflat","olympicincline","olympicdecline"): return bench({"flatbench":"flat","adjustablebench":"adjustable","declinebench":"decline","olympicflat":"olympicflat","olympicincline":"olympicincline","olympicdecline":"olympicdecline"}[kind])
    if kind == "preacherbench": return bench("flat") + pad(275,315,230,52,16,"rotate(-22 390 340)") + tube(295,365,355,435,20) + tube(500,365,475,435,20)
    if kind == "hyperbench": return ellipse(410,590,250,42,"#eef0f1","#d9dde0",2) + path("M300 295 L475 480 L525 520", "none", "#303840", 26) + pad(260,250,210,66,16,"rotate(-40 365 280)") + pad(500,470,70,42,14) + tube(340,345,290,565,22) + tube(470,470,540,565,22) + tube(260,565,560,565,20)
    if kind == "smith": return tower("smith")
    if kind in ("rack","dipstation"): return tower("dip" if kind=="dipstation" else "rack")
    if kind in ("singlepulley","crossover","cable-row","latpulldown"): return cable_machine({"singlepulley":"single","crossover":"crossover","cable-row":"row","latpulldown":"pulldown"}[kind])
    if kind in ("chestpress","shoulderpress","bicepsmachine","tricepspress","legextension","seatedcurl","lyingcurl","row","legpress","pecfly","hipabduction","hipadduction","abmachine","hipthrust","calfmachine","backextension","multiflight","assisted"):
        mapper={"chestpress":"chest","shoulderpress":"shoulder","bicepsmachine":"biceps","tricepspress":"triceps","legextension":"legext","seatedcurl":"seatedcurl","lyingcurl":"lyingcurl","row":"row","legpress":"legpress","pecfly":"fly","hipabduction":"hip","hipadduction":"hip","abmachine":"ab","hipthrust":"hipthrust","calfmachine":"calf","backextension":"trunk","multiflight":"fly","assisted":"chest"}
        out=selector(mapper[kind])
        if kind == "assisted": out += pad(345,505,130,35,10,"rotate(5 410 520)") + tube(410,505,410,535,18)
        if kind == "multiflight": out += tube(200,195,200,555,26)+tube(630,195,630,555,26)+tube(200,195,630,195,22)+path("M200 250 Q340 230 390 350 M630 250 Q485 230 430 350","none","#4e5962",9)
        return out
    if kind in ("platechest","platedecline","plateincline","highrow","deadliftmachine","vsquat","tbarrow","preacher-machine","lateralraise","seatedlegpress","tricepsextension","hacksquat"):
        mapper={"platechest":"platechest","platedecline":"platedecline","plateincline":"plateincline","highrow":"row","deadliftmachine":"deadlift","vsquat":"vsquat","tbarrow":"row","preacher-machine":"biceps","lateralraise":"shoulder","seatedlegpress":"legpress","tricepsextension":"triceps","hacksquat":"hacksquat"}
        return plate_machine(mapper[kind])
    if kind in ("treadmill","elliptical","rowing","stairclimber","bike"): return cardio(kind)
    if kind in ("band","mat","step","halfbball","pilatesball","wheel","box"): return smallgear(kind)
    return rect(280,300,250,180,"#303840",20)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def main():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for i, (category, zh, en, kind, tag, clue) in enumerate(ITEMS, 1):
        filename = f"{i:02d}_{zh.replace(' / ', '_')}_{slug(en)}.svg"
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(zh)} | {html.escape(en)}</title><desc id="desc">Gym equipment reference illustration, generic type, not a brand product photo.</desc>
<defs><linearGradient id="steel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#58636c"/><stop offset=".28" stop-color="#e1e5e8"/><stop offset=".55" stop-color="#9aa3aa"/><stop offset=".8" stop-color="#f0f2f3"/><stop offset="1" stop-color="#68727a"/></linearGradient><linearGradient id="pad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#40474e"/><stop offset="1" stop-color="#171d22"/></linearGradient></defs>
<rect width="800" height="800" fill="#fff"/>{icon(kind)}</svg>'''
        (ASSET_DIR / filename).write_text(svg, encoding="utf-8")
        rows.append({"id": f"EQ{i:03d}", "category": category, "name_zh": zh, "name_en": en, "kind": kind, "tag": tag, "clue": clue, "file": "assets/equipment/" + filename, "type": "通用器械示意图 / Generic equipment illustration"})
    (ROOT / "data" / "equipment.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    with (ROOT / "data" / "equipment.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Created {len(rows)} equipment illustrations in {ASSET_DIR}")


if __name__ == "__main__":
    main()
