import matplotlib.pyplot as plt
import numpy as np
import math
from tabulate import tabulate


def f1(x, y):
    return y + (1+x)*y*y


def f2(x, y):
    return (x**2+1)*y/(2*x)


def f3(x, y):
    return math.e**(math.tan(x/2))


def f4(x, y):
    return (x*y+x**2+y**3)**(-1)


def f5(x, y):
    return math.sin(x)*math.cos(y)


def method_Euler(func, y0, a, b, h):
    ans = [y0]
    xi = a
    yi = y0
    while xi < b:
        y_1 = yi+h*func(a, yi)
        yi = yi+h/2*(func(a, yi)+func(xi+h, y_1))
        ans.append(yi)
        xi += h
    return ans


def method_Adams(func, y0, a, b, h):
    ans = method_Euler(func, y0, a, a+h*3, h)
    list_of_funcs = []
    xi = a-h
    for i in range(len(ans)):
        list_of_funcs.append(func(a+h*i, ans[i]))
        xi += h
    yi = ans[-1]
    while xi < b:
        delta1_func = list_of_funcs[-1] - list_of_funcs[-2]
        delta2_func = list_of_funcs[-1] - 2*list_of_funcs[-2] + list_of_funcs[-3]
        delta3_func = list_of_funcs[-1] - 3*list_of_funcs[-2] + 3*list_of_funcs[-3] - list_of_funcs[-4]
        yi = yi + h*list_of_funcs[-1] + h*h/2 * delta1_func + 5*h*h*h/12 * delta2_func + 3*h**4/8 * delta3_func
        ans.append(yi)
        xi += h
        list_of_funcs.append(func(xi, yi))
    return ans


def read_data():
    print("Прежде всего выберете одну из предложенных функций\n"
          "1. y + (1+x)y^2\n"
          "2. (x^2+1)y / (2x)\n"
          "3. e^(tg(x/2))\n"
          "4. 1/(xy+x^2+y^3)\n"
          "5. sin(x)*cos(y)")
    n = None
    while n is None:
        try:
            n = int(input())
            if n < 1 or n > 5:
                print("Так сложно ввести число от 1 до 5?")
                n = None
        except:
            print("Так сложно ввести число от 1 до 5?")
    print("С функцией разобрались. Какое у нас будет начальное условие у0?")
    y0 = None
    while y0 is None:
        try:
            y0 = float(input())
        except:
            print("А че ты 'Войну и Мир' не ввел?")
    print("Теперь выберем диапазон. Введите отрезок [a, b] через пробел")
    a, b = None, None
    h = None
    while h is None:
        try:
            a, b = map(float, input().split())
        except:
            print("Два числа. Через пробел. Что тут непонятного?")
            continue
        print("С каким шагом h будем двигаться?")
        try:
            h = float(input())
            if h == 0:
                print("Вы ошиблись дверью. Клуб юмористов этажом выше")
                h = None
                continue
        except:
            print("Чел, введи одно чертово число!")
            continue
        if abs(a-b)/h > 1000:
            print("Я вам че, Никола Тесла? Давай числа поменьше")
            print("Введи а и b еще раз")
            a, b, h = None, None, None
    if a > b and h > 0:
        print("Приколист, тоже мне. a и b меняю местами")
        a, b = b, a
    if a < b and h < 0:
        print("Так. Давай я знак h поменяю")
        h = -h
    print("Неужели справился?")
    functions = [f1, f2, f3, f4, f5]
    return functions[n-1], y0, a, b, h


def build_graph(results, left, right):
    for result in results:
        x = np.linspace(left, right, len(result))
        plt.plot(x, result)
    print("Закройте график, чтобы продолжить")
    plt.show()


def rule_of_Runge(func, y0, a, h):
    R_for_Euler = (method_Euler(func, y0, a, a + 2 * h, h)[-1] - method_Euler(func, y0, a, a + 2 * h, 2 * h)[-1])/3
    R_for_Adams = (method_Adams(func, y0, a, a + 2 * h, h)[-1] - method_Adams(func, y0, a, a + 2 * h, 2 * h)[-1])/15
    print("Погрешность методом Эйлера:", R_for_Euler)
    print("Погрешность методом Адамса:", R_for_Adams)


def main():
    print("Математичка задала решить задачу Коши, а ты тупой как птушник? Хорошо, что тебе досталась эта прога")
    while True:
        func, y0, a, b, h = read_data()
        result_of_Euler = method_Euler(func, y0, a, b, h)
        result_of_Adams = method_Adams(func, y0, a, b, h)
        x = np.linspace(a, b, len(result_of_Adams))
        table_data = []
        for i in range(len(result_of_Euler)):
            table_data.append([x[i], result_of_Euler[i], result_of_Adams[i]])
        print(tabulate(table_data, headers=["x", "method Euler", "method Adams"]))
        rule_of_Runge(func, y0, a, h)
        build_graph([result_of_Euler, result_of_Adams], a, b)
        print("Это все, что ты хотел? Вводи exit, если да")
        ans = input()
        if ans == "exit":
            print("Тогда пока")
            break
        else:
            print("Ну давай продолжим")


main()
