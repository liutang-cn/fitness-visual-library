from __future__ import annotations

import csv
import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PACK_DIR = ROOT / "assets" / "exercise-pack"
RAW = "https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/"

EQUIPMENT_ZH = {
    "dumbbell": "哑铃",
    "kettlebell": "壶铃",
    "barbell": "杠铃",
    "olympic barbell": "奥林匹克杠铃",
    "ez barbell": "EZ曲杆",
    "trap bar": "六角杠 / 陷阱杠",
    "cable": "滑轮 / 拉力器",
    "leverage machine": "杠杆固定器械",
    "smith machine": "史密斯机",
    "sled machine": "雪橇 / 推蹬器械",
    "body weight": "自重",
    "band": "弹力带",
    "resistance band": "弹力带",
    "stability ball": "健身球",
    "medicine ball": "药球",
    "assisted": "辅助器械",
    "weighted": "负重",
    "rope": "绳索",
    "roller": "滚轮",
    "wheel roller": "腹肌轮",
    "stationary bike": "固定自行车",
    "elliptical machine": "椭圆机",
    "stepmill machine": "楼梯机",
    "upper body ergometer": "上肢功率车",
    "skierg machine": "滑雪机",
}

NAME_ZH = {
    "barbell bench press": "杠铃卧推",
    "barbell incline bench press": "杠铃上斜卧推",
    "barbell decline bench press": "杠铃下斜卧推",
    "barbell bent over row": "杠铃俯身划船",
    "barbell deadlift": "杠铃硬拉",
    "barbell full squat": "杠铃深蹲",
    "barbell front squat": "杠铃前蹲",
    "barbell shoulder press": "杠铃肩上推举",
    "dumbbell bench press": "哑铃卧推",
    "dumbbell incline bench press": "哑铃上斜卧推",
    "dumbbell lateral raise": "哑铃侧平举",
    "dumbbell shoulder press": "哑铃肩上推举",
    "dumbbell biceps curl": "哑铃弯举",
    "dumbbell bent over row": "哑铃俯身划船",
    "dumbbell one arm row": "单臂哑铃划船",
    "cable seated row": "绳索坐姿划船",
    "cable lat pulldown": "绳索高位下拉",
    "cable chest press": "绳索胸推",
    "cable lateral raise": "绳索侧平举",
    "cable triceps pushdown": "绳索下压",
    "lever chest press": "杠杆胸推机",
    "lever shoulder press": "杠杆肩推机",
    "lever seated row": "杠杆坐姿划船机",
    "lever leg extension": "杠杆腿屈伸机",
    "lever lying leg curl": "杠杆俯卧腿弯举机",
    "lever horizontal one leg press": "杠杆水平单腿举",
    "smith bench press": "史密斯卧推",
    "smith squat": "史密斯深蹲",
    "smith shoulder press": "史密斯肩推",
    "kettlebell swing": "壶铃摆动",
    "kettlebell goblet squat": "壶铃高脚杯深蹲",
    "kettlebell one arm row": "单臂壶铃划船",
    "ez barbell curl": "EZ曲杆弯举",
    "ez barbell lying triceps extension": "EZ曲杆仰卧臂屈伸",
    "pull-up": "引体向上",
    "pull up": "引体向上",
    "push-up": "俯卧撑",
    "plank": "平板支撑",
    "band shoulder press": "弹力带肩推",
    "band seated row": "弹力带坐姿划船",
    "stability ball crunch": "健身球卷腹",
    "medicine ball slam": "药球砸地",
}

COMMON = [
    ("barbell", ["barbell bench press", "barbell incline bench press", "barbell bent over row", "barbell deadlift", "barbell full squat", "barbell shoulder press"]),
    ("dumbbell", ["dumbbell bench press", "dumbbell incline bench press", "dumbbell lateral raise", "dumbbell shoulder press", "dumbbell biceps curl", "dumbbell one arm row"]),
    ("cable", ["cable seated row", "cable lat pulldown", "cable chest press", "cable lateral raise", "cable triceps pushdown"]),
    ("leverage machine", ["lever chest press", "lever shoulder press", "lever seated row", "lever leg extension", "lever lying leg curl", "lever horizontal one leg press"]),
    ("smith machine", ["smith bench press", "smith squat", "smith shoulder press"]),
    ("kettlebell", ["kettlebell swing", "kettlebell goblet squat", "kettlebell one arm row"]),
    ("ez barbell", ["ez barbell curl", "ez barbell lying triceps extension"]),
    ("band", ["band shoulder press", "band seated row", "band squat"]),
    ("stability ball", ["stability ball crunch", "back extension on exercise ball", "push-up (on stability ball)"]),
    ("body weight", ["pull-up", "push-up", "plank"]),
]


def get_json() -> list[dict]:
    url = RAW + "data/exercises.json"
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def safe_name(text: str) -> str:
    return re.sub(r"[^\w\-.\u4e00-\u9fff ]+", "", text).replace(" ", "_")[:100]


def choose(data: list[dict], equipment: str, names: list[str]) -> list[dict]:
    by_name = {x["name"].lower(): x for x in data if x.get("equipment") == equipment}
    out = []
    for wanted in names:
        key = wanted.lower()
        if key in by_name:
            out.append(by_name[key])
            continue
        # A fallback keeps the pack useful when the dataset uses a spelling variant.
        hits = [x for x in data if x.get("equipment") == equipment and key in x.get("name", "").lower()]
        if hits:
            out.append(hits[0])
    return out


def download(url: str, path: Path) -> bool:
    if path.exists() and path.stat().st_size > 100:
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "fitness-visual-library/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            path.write_bytes(r.read())
        return path.stat().st_size > 100
    except Exception as e:
        print("download failed", url, e)
        return False


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PACK_DIR.mkdir(parents=True, exist_ok=True)
    data = get_json()
    (DATA_DIR / "exercises-dataset.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    chosen: list[dict] = []
    for equipment, names in COMMON:
        chosen.extend(choose(data, equipment, names))
    seen = set()
    selected = []
    for item in chosen:
        if item["id"] not in seen:
            seen.add(item["id"])
            selected.append(item)
    rows = []
    for item in selected:
        group = item.get("equipment", "")
        name = item.get("name", "")
        name_zh = NAME_ZH.get(name.lower(), "")
        img_rel = item.get("image", "")
        gif_rel = item.get("gif_url", "")
        img_path = PACK_DIR / (safe_name(item["id"] + "_" + name) + ".jpg")
        gif_path = PACK_DIR / (safe_name(item["id"] + "_" + name) + ".gif")
        if img_rel:
            download(RAW + img_rel, img_path)
        if gif_rel:
            download(RAW + gif_rel, gif_path)
        row = {
            "id": item["id"],
            "name_en": name,
            "name_zh": name_zh,
            "equipment_en": group,
            "equipment_zh": EQUIPMENT_ZH.get(group, group),
            "category": item.get("category", ""),
            "target": item.get("target", ""),
            "image_local": "assets/exercise-pack/" + img_path.name,
            "gif_local": "assets/exercise-pack/" + gif_path.name,
            "image_source": RAW + img_rel,
            "gif_source": RAW + gif_rel,
            "attribution": item.get("attribution", ""),
        }
        rows.append(row)
    (DATA_DIR / "精选动作目录.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    with (DATA_DIR / "精选动作目录.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    (DATA_DIR / "equipment-zh.json").write_text(json.dumps(EQUIPMENT_ZH, ensure_ascii=False, indent=2), encoding="utf-8")
    print("records", len(data), "selected", len(rows), "downloaded", sum(1 for r in rows if Path(ROOT / r["image_local"]).exists()))


if __name__ == "__main__":
    main()
