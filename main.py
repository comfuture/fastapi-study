import click
import uvicorn

@click.command()
@click.option('--app', '-a', required=True, help='module name')
@click.option('--module', '-m', default='app', help='fast app instance')
@click.option('--port', '-p', default=4000, help='port number')
@click.option('--reload', '-r', is_flag=True, default=True)
def main(app, module, port, reload):
    """study apps cli
    ex)
    $ python main.py -a day1.homework -m app -p 4000 -r
    """
    if not app.startswith('fastapi_study.'):
        app = f'fastapi_study.{app}'
    uvicorn.run(f'{app}:{module}', port=port, reload=reload)

if __name__ == '__main__':
    main() # pylint: disable=no-value-for-parameter
