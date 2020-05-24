from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from src import create_app, db

app = create_app()
manager = Manager(app)
Migrate(app, db)  # 将app与db关联
manager.add_command("db", MigrateCommand)  # 将迁移命令添加到manager中

if __name__ == '__main__':
    manager.run()
