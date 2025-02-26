import time
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get('/main')
async def main():
    start_time = time.time()

    await first_func()
    await second_func()
    await third_func()

    end_time = time.time()
    time_proccesing = end_time - start_time
    print(time_proccesing)

    return time_proccesing

async def first_func():
    print('--start first_func')
    await asyncio.sleep(3)
    print('--end first_func')

async def second_func():
    print('--start second_func')
    await asyncio.sleep(3)
    print('--end second_func')

async def third_func():
    print('--start third_func')
    await asyncio.sleep(3)
    print('--end third_func')    
