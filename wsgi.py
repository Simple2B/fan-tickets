#!/user/bin/env python
from app import create_app
from app.commands import init_shell_commands

app = create_app()
init_shell_commands(app)


if __name__ == "__main__":
    app.run()
