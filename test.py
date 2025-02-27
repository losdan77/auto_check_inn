import time
import asyncio
from fastapi import FastAPI


app = FastAPI()


@app.get('/main')
async def main():
    start_time = time.time()

    inn_array = [111, 222, 333]


    first_func_tasks = [asyncio.to_thread(first_func, inn) for inn in inn_array]
    second_func_tasks = [asyncio.to_thread(second_func, inn) for inn in inn_array]
    third_func_tasks = [asyncio.to_thread(third_func, inn) for inn in inn_array]

    # (
    #     first_func_info,
    #     second_func_info,
    #     third_func_info,
    # ) = await asyncio.gather(
    #     asyncio.gather(*first_func_tasks),
    #     asyncio.gather(*second_func_tasks),
    #     asyncio.gather(*third_func_tasks),
    # )
    first_func_info = await asyncio.gather(*first_func_tasks)
    second_func_info = await asyncio.gather(*second_func_tasks)
    third_func_info = await asyncio.gather(*third_func_tasks)
    
    end_time = time.time()
    time_proccesing = end_time - start_time
    print(time_proccesing)

    return time_proccesing, first_func_info, second_func_info, third_func_info

def first_func(inn):
    print('--start first_func')
    time.sleep(3)
    print('--end first_func')
    return {f'{inn}': 1}

def second_func(inn):
    print('--start second_func')
    time.sleep(3)
    print('--end second_func')
    return {f'{inn}': 2}

def third_func(inn):
    print('--start third_func')
    time.sleep(3)
    print('--end third_func')
    return {f'{inn}': 3}    
