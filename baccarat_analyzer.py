# baccarat_analyzer.py

import os

# ----------------------------------------------------
# 1. การกำหนดค่าและไฟล์ (Configuration)
# ----------------------------------------------------

HISTORY_FILE = 'baccarat_history.txt'

PAYOUT_ODDS = {
    'P': '1:1',
    'B': '0.9:1 (5% commission)',
    'T': '8:1'
}

# ----------------------------------------------------
# 2. ฟังก์ชันจัดการไฟล์ประวัติ (Load / Save)
# ----------------------------------------------------

def load_history():
    """โหลดประวัติจากไฟล์"""
    try:
        if not os.path.exists(HISTORY_FILE):
            return []

        with open(HISTORY_FILE, 'r') as f:
            content = f.read().strip()

        if content:
            valid = [r.strip().upper() for r in content.split(',') if r.strip() in ('B','P','T')]
            return valid

        return []

    except Exception as e:
        print(f"⚠️ Error loading history: {e}")
        return []


def save_history(history):
    """บันทึกลงไฟล์"""
    try:
        with open(HISTORY_FILE, 'w') as f:
            f.write(",".join(history))
    except Exception as e:
        print(f"⚠️ Error saving history: {e}")


# ----------------------------------------------------
# 3. ฟังก์ชันวิเคราะห์ลาย Baccarat
# ----------------------------------------------------

def analyze_pattern(history):
    """วิเคราะห์ Dragon / Chop + จำกัด Dragon ไม่เกิน 4"""

    bp = [r for r in history if r in ('B', 'P')]

    if len(bp) < 3:
        return "Insufficient data (Need at least 3 B/P results)", []

    last_three = bp[-3:]
    a, b, c = last_three[0], last_three[1], last_three[2]  # a=first, b=mid, c=last

    # ---------------------------------------------------------
    # 🔥 1. ตรวจลาย Dragon (3 ตัวล่าสุดเท่ากัน)
    # ---------------------------------------------------------
    if a == b == c:

        # นับ streak ยาวแค่ไหน
        streak = 1
        last = c
        for i in range(len(bp)-2, -1, -1):  # ไล่ย้อนดูย้อนหลัง
            if bp[i] == last:
                streak += 1
            else:
                break

        # จำกัดสูงสุด 4  
        if streak >= 5:
            return f"⚠️ Dragon Overlimit ({streak}). High Risk: DO NOT bet", last_three

        # ถ้าไม่เกิน 4 ตา → เล่นตามมังกรได้
        side = "Banker" if last == 'B' else "Player"
        return f"🐉 Dragon streak ({streak}). Bet {side}", last_three

    # ---------------------------------------------------------
    # 🔁 2. ลาย Chop (สลับ)
    # BPB หรือ PBP
    # ---------------------------------------------------------
    if a != b and b != c:
        if c == 'B':
            return "🔁 Chop detected. Bet Player", last_three
        else:
            return "🔁 Chop detected. Bet Banker", last_three

    # ---------------------------------------------------------
    # ❓ 3. ลายไม่ชัดเจน
    # ---------------------------------------------------------
    return "No clear pattern detected. Observe only.", last_three


# ----------------------------------------------------
# 4. โปรแกรมหลัก (Real-time Analyzer)
# ----------------------------------------------------

def main_analyzer():

    history = load_history()

    print("--------------------------------------------------")
    print(" 🎲 Baccarat Real-time Analyzer v2.0 🎲")
    print("--------------------------------------------------")
    print(f"Loaded History File: {HISTORY_FILE}")
    print(f"Total Records: {len(history)}")
    print("--------------------------------------------------")
    print("💡 Input B / P / T")
    print("💡 Input 'exit' to quit")
    print("--------------------------------------------------")

    if history:
        print("\nCurrent History:")
        print(", ".join(history))
    else:
        print("\nNo history found. Start inputting results!")

    # main loop
    while True:
        user_input = input(f"\nNext Result (B/P/T): ").strip().upper()

        if user_input in ('EXIT', 'QUIT'):
            save_history(history)
            print("History saved. Goodbye!")
            break

        if user_input not in ('B','P','T'):
            print("❌ Invalid input. Use only B, P, T.")
            continue

        history.append(user_input)
        save_history(history)
        print(f"✅ Recorded: {user_input}")

        # วิเคราะห์
        recommendation, last_three = analyze_pattern(history)

        print("\n==================================================")
        print("📊 Analysis Report")
        if last_three:
            print(f"Last 3 B/P: {last_three}")
        print(f"Recommendation: {recommendation}")
        print("==================================================")


# ----------------------------------------------------
# เริ่มโปรแกรม
# ----------------------------------------------------

if __name__ == "__main__":
    main_analyzer()
