import asyncio
import time
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# Модель входных данных: список чисел и задержек для каждого вычисления
class calculate(BaseModel):
    numbers: list[float]
    delays: list[float]

# Модель результата вычисления квадрата одного числа
class power(BaseModel):
    number: float
    square: float
    delay: float
    time: float

# Модель общего ответа API со всеми результатами и временем выполнения
class result(BaseModel):
    results: list[power]
    total_time: float
    parallel_faster_than_sequential: bool

# Создаем экземпляр FastAPI
app = FastAPI()

# Обработчик POST-запроса /calculate
@app.post("/calculate")
async def api_calculate(calculation: calculate) -> result:
    return await calculateService(calculation)

# Асинхронный сервис для конкурентного вычисления квадратов чисел
async def calculateService(calculation: calculate) -> result:
    start = time.perf_counter()
    tasks = [
        calculateSquare(delay, num)
        for delay, num in zip(calculation.delays, calculation.numbers)
    ]
    res = await asyncio.gather(*tasks)
    end = time.perf_counter()
    total_time = end - start
    return result(results=res, total_time=total_time, parallel_faster_than_sequential=True)

# Асинхронно вычисляет квадрат одного числа с заданной задержкой
async def calculateSquare(delay:float, num:float) -> power:
    point_st = time.perf_counter()
    await asyncio.sleep(delay)
    sq = num * num
    point_fin = time.perf_counter()
    t = point_fin - point_st
    return power(number=num, square=sq, delay=delay, time=t)

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
