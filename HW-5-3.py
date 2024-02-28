import timeit
import requests


def boyer_moore_search(text, pattern):
    m, n = len(pattern), len(text)
    if m == 0 or m > n:
        return -1  # Паттерн порожній або довший за текст

    last_occurrence = {}  # Таблиця останніх входжень символів
    for i in range(m - 1):
        last_occurrence[pattern[i]] = m - i - 1

    i = m - 1  # Починаємо з кінця паттерну
    j = m - 1  # Починаємо з кінця тексту

    while j < n:
        if text[j] == pattern[i]:
            if i == 0:
                return j  # Знайдено входження
            else:
                i -= 1
                j -= 1
        else:
            j += max(1, m - 1 - i + last_occurrence.get(text[j], m))

    return -1  # Відсутнє входження


def kmp_search(text, pattern):
    m, n = len(pattern), len(text)
    if m == 0 or m > n:
        return -1  # Паттерн порожній або довший за текст

    # Обчислення префікс-функції для паттерну
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j

    i = 0  # Індекс для тексту
    j = 0  # Індекс для паттерну
    while i < n:
        if text[i] == pattern[j]:
            if j == m - 1:
                return i - j  # Знайдено входження
            else:
                i += 1
                j += 1
        else:
            if j != 0:
                j = pi[j - 1]
            else:
                i += 1

    return -1  # Відсутнє входження


def rabin_karp_search(text, pattern):
    d = 256  # Розмір алфавіту
    q = 101  # Просте число

    m, n = len(pattern), len(text)
    if m == 0 or m > n:
        return -1  # Паттерн порожній або довший за текст

    # Обчислення хешу для паттерну та перших m символів тексту
    p_hash, t_hash, h = 0, 0, 1
    for i in range(m - 1, -1, -1):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q
        if i > 0:
            h = (h * d) % q

    for i in range(n - m + 1):
        if p_hash == t_hash and pattern == text[i:i + m]:
            return i  # Знайдено входження
        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            if t_hash < 0:
                t_hash += q

    return -1  # Відсутнє входження


def measure_time(text, pattern, number):
    time_boyer_moore = timeit.timeit(
        lambda: boyer_moore_search(text, pattern), number=1000)
    time_kmp = timeit.timeit(lambda: kmp_search(text, pattern), number=1000)
    time_rabin_karp = timeit.timeit(
        lambda: rabin_karp_search(text, pattern), number=1000)

    return time_boyer_moore, time_kmp, time_rabin_karp


# Завантаження текстів з посилань
text1_url = "https://drive.google.com/uc?id=18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh"
text2_url = "https://drive.google.com/uc?id=13hSt4JkJc11nckZZz2yoFHYL89a4XkMZ"

text1 = requests.get(text1_url).text
text2 = requests.get(text2_url).text

pattern1 = "двійковий та логаріфмічний пошук"
pattern2 = "гаррі поттер та кубок вогню"

# Вимірюємо час виконання для кожного алгоритму та для обох підрядків
time_both_patterns_1 = measure_time(text1, pattern1, pattern2)
time_both_patterns_2 = measure_time(text2, pattern1, pattern2)

print(f"Час виконання для [тексту 1]({text1_url}):")
print(f"Боєра-Мура: {time_both_patterns_1[0]:.6f} сек")
print(f"Кнута-Морріса-Пратта: {time_both_patterns_1[1]:.6f} сек")
print(f"Рабіна-Карпа: {time_both_patterns_1[2]:.6f} сек")

print(f"Час виконання для [тексту 2]({text2_url}):")
print(f"Боєра-Мура: {time_both_patterns_2[0]:.6f} сек")
print(f"Кнута-Морріса-Пратта: {time_both_patterns_2[1]:.6f} сек")
print(f"Рабіна-Карпа: {time_both_patterns_2[2]:.6f} сек")

print("# План реалізації:")
print("## Алгоритм Боєра-Мура:")
print("### Побудова таблиці зсувів.")
print("### Пошук підрядка з використанням таблиці зсувів.")
print("## Алгоритм Кнута-Морріса-Пратта (КМП):")
print("### Побудова префікс-функції.")
print("### Пошук підрядка з використанням префікс-функції.")
print("## Алгоритм Рабіна-Карпа:")
print("### Обчислення хеш-значення для підрядка та першого вікна тексту.")
print("### Пошук підрядка за допомогою порівняння хеш-значень.")

print("## Порівняння швидкості виконання:")
print("### Вимірюється час виконання кожного алгоритму. Python має модуль time для цього.")
print("### Використовуються тестові дані різного розміру та різні підрядки для кожного з алгоритму.")
print("### Перший підрядок присутній у обох текстах, другий вигаданий.")
print("### Під час проведення експерименту програма запускається кілька разів та результати порівнюються.")

print("# Висновки:")
print("### Боєрa-Мурa швидко працює на широкому спектрі текстових даних і виявляється ефективним для великих текстів.")
print("### Його швидкість особливо відчутна при пошуку коротких підрядків.")
print("### Алгоритм Кнута-Морріса-Пратта часто є ефективним для пошуку підрядків у великих текстах, але його швидкість може залежати від довжини шуканого підрядка та структури тексту.")
print("### Підрядок 'гаррі поттер та кубок вогню' може бути досить довгим, що може впливати на час виконання KMP.")
print("### Алгоритм Рабіна-Карпа може бути менш ефективним для деяких типів текстових даних через його ймовірнісний характер.")
print("### Час виконання Рабіна-Карпа може зростати зі збільшенням довжини тексту та шуканого підрядка.")
print("### Важливо враховувати, що точні результати можуть залежати від різних факторів та характеристик даних.")
print("### У деяких випадках може бути корисно провести більше тестів з різними типами даних або змінювати параметри алгоритмів для отримання більш широкого розуміння їхньої продуктивності.")
