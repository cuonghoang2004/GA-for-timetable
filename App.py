import random
import pandas as pd
from collections import defaultdict

# Cấu hình lịch
DAYS = ['T2', 'T3', 'T4', 'T5', 'T6']
SLOTS = ['Sáng', 'Chiều']

# Sinh thời khóa biểu ngẫu nhiên
def generate_random_timetable(classes, rooms):
    return {
        cls: (random.choice(DAYS), random.choice(SLOTS), random.choice(rooms))
        for cls in classes
    }

# Đánh giá độ phù hợp
def calculate_fitness(timetable):
    score = 0
    usage = defaultdict(list)
    for cls, (day, slot, room) in timetable.items():
        usage[(day, slot, room)].append(cls)
    for k, v in usage.items():
        if len(v) > 1:
            score -= (len(v) - 1) * 10  # Trừ điểm nếu trùng phòng cùng lúc
    return score

# Lai ghép giữa 2 cá thể
def crossover(p1, p2, classes):
    return {cls: p1[cls] if random.random() < 0.5 else p2[cls] for cls in classes}

# Đột biến ngẫu nhiên
def mutate(timetable, classes, rooms, rate=0.1):
    mutated = timetable.copy()
    for cls in classes:
        if random.random() < rate:
            mutated[cls] = (random.choice(DAYS), random.choice(SLOTS), random.choice(rooms))
    return mutated

# Thuật toán di truyền chính
def genetic_algorithm(classes, rooms, generations=100, pop_size=50):
    population = [generate_random_timetable(classes, rooms) for _ in range(pop_size)]
    for gen in range(generations):
        population.sort(key=calculate_fitness, reverse=True)
        best = calculate_fitness(population[0])
        print(f"Gen {gen}: Best score = {best}")
        if best == 0:
            break
        next_gen = population[:10]
        while len(next_gen) < pop_size:
            p1, p2 = random.sample(population[:20], 2)
            child = crossover(p1, p2, classes)
            next_gen.append(mutate(child, classes, rooms))
        population = next_gen
    return population[0]

# ----- PHẦN MAIN -----
if __name__ == "__main__":
    print("🚀 Bắt đầu chạy thuật toán tạo thời khóa biểu...")

    # Đọc dữ liệu từ Excel
    try:
        df = pd.read_excel("Timetable.xlsx")
        df = df[['Mã_lớp', 'Phòng']].dropna()
        classes = df['Mã_lớp'].unique().tolist()
        rooms = df['Phòng'].unique().tolist()
        print(f"📄 Đọc dữ liệu thành công: {len(classes)} lớp, {len(rooms)} phòng.")
    except Exception as e:
        print("❌ Lỗi khi đọc file Excel:", e)
        exit()

    # Chạy thuật toán
    best_schedule = genetic_algorithm(classes, rooms)

    # Xuất kết quả
    output = pd.DataFrame([
        {"Mã_lớp": cls, "Thứ": day, "Buổi": slot, "Phòng": room}
        for cls, (day, slot, room) in best_schedule.items()
    ])
    output.to_excel("Best_Timetable.xlsx", index=False)
    print("✅ Đã lưu thời khóa biểu vào: Best_Timetable.xlsx")
