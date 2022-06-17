from tempfile import NamedTemporaryFile
from fastapi import FastAPI, BackgroundTasks
from starlette.responses import JSONResponse

app = FastAPI()

def create_tmp_file(filename: str):
    """creates a pid file in current dir"""
    with open(filename, 'w', encoding='utf8') as f:
        print(f'writing {filename}')
        f.write('1')


@app.get('/', status_code=202)
def home():
    """빈 응답을 리턴하고 백그라운드 태스크를 실행하는 엔드포인트"""
    tasks = BackgroundTasks()
    with NamedTemporaryFile(prefix='with', mode='w', encoding='utf8', delete=True) as f:
        tasks.add_task(create_tmp_file, f.name)
        return JSONResponse({'filename': f.name}, status_code=202, background=tasks)


@app.get('/without-return', status_code=202)
def without_return():
    """백그라운드 태스크를 리턴하지 않는 엔드포인트"""
    tasks = BackgroundTasks()
    filename = None
    with NamedTemporaryFile(prefix='without', mode='w', encoding='utf8', delete=True) as f:
        tasks.add_task(create_tmp_file, f.name)
        filename = f.name
    return JSONResponse({'filename': filename}, status_code=202)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('fastapi_study.day3.standalone_tasks:app', port=4000, reload=True)

