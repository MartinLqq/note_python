"""Mygit Init."""
import click


def print_version(ctx: click.Context, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()


def abort_if_false(ctx: click.Context, param, value):
    if not value:
        ctx.abort()



@click.command()
@click.argument('filename', required=False)
def main(filename):
    click.echo(filename)


if __name__ == '__main__':
    main()
