import click

from gevault.admin import Admin
from gevault.refresh import Refresh
from gevault.users import Users

@click.group()
def main():
    pass

@main.command()
@click.argument('function', required=True)
@click.option('-c', '--config', default=None, required=False)
@click.option('-s', '--server', default="default", required=False)
def admin(**kwargs):
    admin_class = Admin(config_file=kwargs["config"], server_name=kwargs["server"])
    getattr(admin_class, kwargs["function"])()

@main.command()
@click.argument('function', required=True)
@click.argument('user', required=False)
@click.option('-c', '--config', default=None, required=False)
@click.option('-s', '--server', default="default", required=False)
def users(**kwargs):
    users_class = Users(config_file=kwargs["config"], server_name=kwargs["server"])
    getattr(users_class, kwargs["function"])(kwargs.get('user', None))

@main.command()
@click.option('-c', '--config', default=None, required=False)
@click.option('-s', '--server', default="default", required=False)
def refresh(**kwargs):
    Refresh(config_file=kwargs["config"], server_name=kwargs["server"])

if __name__ == '__main__':
    main()
