
import pandas as pd
import random
from collections import defaultdict
import os

DAYS = ['T2', 'T3', 'T4', 'T5', 'T6']
SLOTS = ['Sáng', 'Chiều']

# Sinh thoi khoa bieu ngau nhien
def generate_random_timetable(classes, rooms):
    return {
        cls: (random.choice(DAYS), random.choice(SLOTS), random.choice(rooms))
        for cls in classes
    }

# Ham danh gia do phu hop
def calculate_fitness(timetable):
    score = 0
    usage = defaultdict(list)
    class_seen = set()

    for cls, (day, slot, room) in timetable.items():
        usage[(day, slot, room)].append(cls)
        if cls in class_seen:
            score -= 50
        else:
            class_seen.add(cls)

    for v in usage.values():
        if len(v) > 1:
            score -= (len(v) - 1) * 10

    return score

# Lai ghep

def crossover(p1, p2, classes):
    return {cls: p1[cls] if random.random() < 0.5 else p2[cls] for cls in classes}

# Dot bien

def mutate(timetable, classes, rooms, rate=0.1):
    mutated = timetable.copy()
    for cls in classes:
        if random.random() < rate:
            mutated[cls] = (random.choice(DAYS), random.choice(SLOTS), random.choice(rooms))
    return mutated

# Thuat toan di truyen chinh
def genetic_algorithm(classes, rooms, generations=100, pop_size=50):
    population = [generate_random_timetable(classes, rooms) for _ in range(pop_size)]
    for gen in range(generations):
        population.sort(key=calculate_fitness, reverse=True)
        best = calculate_fitness(population[0])
        print(f"  Gen {gen}: Best score = {best}")
        if best == 0:
            break
        next_gen = population[:10]
        while len(next_gen) < pop_size:
            p1, p2 = random.sample(population[:20], 2)
            child = crossover(p1, p2, classes)
            next_gen.append(mutate(child, classes, rooms))
        population = next_gen
    return population[0]

# Chay theo nhom
def run_for_group(df_group, group_name):
    classes = df_group['Mã_lớp'].astype(str).unique().tolist()
    rooms = df_group['Phòng'].dropna().unique().tolist()
    print(f"\n✨ Nhóm: {group_name} - {len(classes)} lớp, {len(rooms)} phòng")
    best_schedule = genetic_algorithm(classes, rooms)
    result = pd.DataFrame([
        {'Mã_lớp': cls, 'Thứ': day, 'Buổi': slot, 'Phòng': room, 'Nhóm': group_name}
        for cls, (day, slot, room) in best_schedule.items()
    ])
    return result
def run_full_algorithm_from_df(df):
    """
    Chạy thuật toán di truyền theo nhóm từ DataFrame đầu vào.
    Trả về DataFrame kết quả.
    """
    df = df[['Trường_Viện_Khoa', 'Mã_lớp', 'Phòng']].dropna()
    groups = df['Trường_Viện_Khoa'].unique()

    all_results = []
    for g in groups:
        df_group = df[df['Trường_Viện_Khoa'] == g]
        result = run_for_group(df_group, g)
        all_results.append(result)

    final_df = pd.concat(all_results, ignore_index=True)
    return final_df

# Phan main
if __name__ == "__main__":
    print("\U0001f680 Bắt đầu xếp thời khóa biểu theo nhóm...")
    try:
        df = pd.read_excel("Timetable.xlsx")
        df = df[['Trường_Viện_Khoa', 'Mã_lớp', 'Phòng']].dropna()
        groups = df['Trường_Viện_Khoa'].unique()

        all_results = []
        for g in groups:
            df_group = df[df['Trường_Viện_Khoa'] == g]
            result = run_for_group(df_group, g)
            all_results.append(result)

        final_df = pd.concat(all_results, ignore_index=True)
        final_df.to_excel("Full_Timetable.xlsx", index=False)
        print("\n✅ Đã lưu thời khóa biểu hoàn chỉnh vào: Full_Timetable.xlsx")

    except Exception as e:
        print("❌ Lỗi khi xử lý:", e)
