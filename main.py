from asyncio import run
from asyncio import sleep
from rich import print
from functools import wraps

import typer


class AsyncTyper(typer.Typer):
    def async_command(self, *args, **kwargs):
        def decorator(async_func):
            @wraps(async_func)
            def sync_func(*_args, **_kwargs):
                return run(async_func(*_args, **_kwargs))
            self.command(*args, **kwargs)(sync_func)
            return async_func

        return decorator


app = AsyncTyper()

@app.async_command()
async def my_async_command(
        time: int = typer.Option(1)
    ):
    await sleep(time)
    print(f"Sleep [yellow]{time}[/yellow] seconds is [red]done[/red]!")
    
@app.command()
async def my_normal_command():
    ...

if __name__ == "__main__":
    app()
