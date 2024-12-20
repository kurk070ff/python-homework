import streamlit as st
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Определение функции модели Лотки-Вольтерры
def lotka_volterra_model(t, y, alpha, beta, delta, gamma):
    prey, predator = y
    dprey_dt = alpha * prey - beta * prey * predator
    dpredator_dt = delta * prey * predator - gamma * predator
    return [dprey_dt, dpredator_dt]

# Заголовок приложения
st.title("Модель Лотки-Вольтерры")

# Боковая панель
st.sidebar.header("Параметры модели")
alpha = st.sidebar.number_input("Коэффициент роста жертв (α)", min_value=0.1, max_value=5.0, value=1.0)
beta = st.sidebar.number_input("Коэффициент хищничества (β)", min_value=0.1, max_value=5.0, value=0.1)
delta = st.sidebar.number_input("Коэффициент размножения хищников (δ)", min_value=0.1, max_value=5.0, value=0.1)
gamma = st.sidebar.number_input("Смертность хищников (γ)", min_value=0.1, max_value=5.0, value=1.0)

prey_0 = st.sidebar.number_input("Начальная популяция жертв", min_value=1, max_value=1000, value=40)
predator_0 = st.sidebar.number_input("Начальная популяция хищников", min_value=1, max_value=1000, value=9)
t_max = st.sidebar.number_input("Время моделирования (t_max)", min_value=1.0, max_value=100.0, value=50.0)

preset = st.sidebar.selectbox(
    "Выбрать готовый набор параметров",
    ["Нет", "Стабильная экосистема", "Резкое сокращение жертв"]
)

if preset == "Стабильная экосистема":
    alpha, beta, delta, gamma, prey_0, predator_0, t_max = 1.0, 0.1, 0.1, 1.0, 50, 10, 50.0
elif preset == "Резкое сокращение жертв":
    alpha, beta, delta, gamma, prey_0, predator_0, t_max = 1.0, 0.2, 0.1, 1.0, 20, 15, 50.0

# Интегрирование ОДУ
t_span = (0, t_max)
y0 = [prey_0, predator_0]
t_eval = np.linspace(0, t_max, 500)

solution = solve_ivp(lotka_volterra_model, t_span, y0, args=(alpha, beta, delta, gamma), t_eval=t_eval)

prey, predator = solution.y
t = solution.t

# Отображение графиков
st.subheader("Результаты моделирования")
fig, axs = plt.subplots(3, 1, figsize=(6, 16))
axs[0].plot(t, prey, label="Жертвы")
axs[0].plot(t, predator, label="Хищники")
axs[0].set_title("Популяции от времени")
axs[0].set_xlabel("Время")
axs[0].set_ylabel("Популяция")
axs[0].legend()

axs[1].plot(t, prey, label="Жертвы")
axs[1].set_title("Популяция жертв от времени")
axs[1].set_xlabel("Время")
axs[1].set_ylabel("Популяция")

axs[2].plot(prey, predator)
axs[2].set_title("Фазовый портрет")
axs[2].set_xlabel("Жертвы")
axs[2].set_ylabel("Хищники")

st.pyplot(fig)
