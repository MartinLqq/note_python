# 设计模式

# 资源

 《精通Python设计模式》

[浅谈Python设计模式](https://www.cnblogs.com/littlefivebolg/p/9929016.html) 



**python-patterns**:   https://github.com/faif/python-patterns 



# 三类

1. 创建模式，提供实例化的方法，为适合的状况提供相应的对象创建方法。
2. 结构化模式，通常用来处理实体之间的关系，使得这些实体能够更好地协同工作。
3. 行为模式，用于在不同的实体建进行通信，为实体之间的通信提供更容易，更灵活的通信方法。

 

# 创建型

## 1、Factory Method（工厂方法）

- 延迟一个类的实例化,  在程序运行时动态决定要创建哪个类的实例 。
- 根据用户输入的不同，调用相同的工厂，将会输出不同的结果。
- 罗列需要考虑的情况并给出对应的处理。



【例1】使用 `ShapeFactory` 创造不同的 `shape`

```python
class Circle(object):
    def draw(self):
        print 'draw circle'

class Rectangle(object):
    def draw(self):
        print 'draw Rectangle'

class ShapeFactory(object):
    def create(self, shape):
        if shape == 'Circle':
            return Circle()
        elif shape == 'Rectangle':
            return Rectangle()
        else:
            return None

fac = ShapeFactory()
obj = fac.create('Circle')
obj.draw()
```



【例2】实现生产、开发、测试等不同模式下的配置

```python
# 在config.py模块下
class Config(object):
    """Base config."""
    # 放置两种模式下共同的配置
    pass

class DevelopConfig(Config):
    """Dev env config."""
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class ProductConfig(Config):
    """Prod env config."""
    LOG_LEVEL = logging.ERROR


config = {
    "development": DevelopConfig,
    "production": ProductConfig
}


# __init__.py模块下
def create_app(config_name):  # 如config_name='development'
    app = Flask(__name__)
    app.config.from_object(config[config_name])
```



【例3】根据不同的数据库类型，得到不同的数据库连接字符串

> 实际的情况一般是根据数据库连接字符串来判断数据库类型,  选择对应的处理器

```python
db_url_formats = dict(
    # 使用pymysql进行连接
    mysql='mysql+pymysql://{username}:{password}@{server}/{dbname}',
    # 使用psycopg2进行连接
    postgresql='postgresql://{username}:{passwrod}@{server}/{dbname}',
)


def connect(db, *arg, **kwargs):
    try:
        db_url = db_url_formats[db.lower()].format(
            username=kwargs['username'],
            password=kwargs['password'],
            server=kwargs['server'],
            dbname=kwargs['db'],
        )
    except KeyError:
        print('do sth.')
    return db_url
```

  



## 2、Abstract Factory（抽象工厂）

调用一个接口,  根据输入的不同,  选择不同的工厂,  每个工厂都有自己的生产方式

根据用户输入的不同，调用相同的接口，去调用不同的工厂进行不同的生产，得出不同的输出结果 



抽象工厂模式提供一个创建一系列相关或相互依赖对象的接口，而无需指定它们的类

抽象工厂最大的有点是：代码量少了很多，通过反射的方法就可以找出函数，比如在单元测试框架里，抽象方法是大量使用到的。

在抽象工厂就是利用反射机制实现的，反射是非常重要的，会大量使用到

反射就是通过字符串的形式，导入模块；通过字符串的形式，去模块寻找指定函数，并执行。利用字符串的形式去对象（模块）中操作（查找/获取/删除/添加）成员，一种基于字符串的事件驱动！

上面的概念指出了使用反射需要掌握的知识点：

（1）通过字符串的形式，导入模块——>要用到: `__import__()`

（2）通过字符串的形式，去模块寻找指定函数并执行 ——> 用要到：`getattr()`

（3）利用字符串的形式去对象（模块）中操作（查找/获取/删除/添加）成员——>要用到：`setattr(),hasattr(),delattr()`



【例1】

　1、通过一个 `GameEnvironment` 去管理两个游戏：`FrogWorld`、`WizerdWorld` ，根据用户输入的不同的年龄去决定其去玩那个游戏，是青蛙世界还是巫师世界呢？

　2、而每个游戏类即 `FrogWorld`、`WizerdWorld` ，又分别管理着 两个角色 --（`Frog`青蛙、`Bug`臭虫）和（`Wizerd`巫师、`Ork`怪兽）

```python
class Frog:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def interact_with(self, obstacle):
        print('{} the Frog encounters {} and {}!'.format(self,
        obstacle, obstacle.action()))


class Bug:

    def __str__(self):
        return 'a bug'

    def action(self):
        return 'eats it'


class FrogWorld:

    def __init__(self, name):
        print(self)
        self.player_name = name

    def __str__(self):
        return '\n\n\t------ Frog World -------'

    def make_character(self):
        return Frog(self.player_name)

    def make_obstacle(self):
        return Bug()


class Wizard:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


    def interact_with(self, obstacle):
        print(
            '{} the Wizard battles against {} and {}!'.format(
            self,
            obstacle,
            obstacle.action()))


class Ork:

    def __str__(self):
        return 'an evil ork'

    def action(self):
        return 'kills it'


class WizardWorld:

    def __init__(self, name):
        print(self)
        self.player_name = name

    def __str__(self):
        return '\n\n\t------ Wizard World -------'

    def make_character(self):
        return Wizard(self.player_name)

    def make_obstacle(self):
        return Ork()

class GameEnvironment:

    def __init__(self, factory):
        self.hero = factory.make_character()
        self.obstacle = factory.make_obstacle()

    def play(self):
        self.hero.interact_with(self.obstacle)

def validate_age(name):
    try:
        age = input('Welcome {}. How old are you? '.format(name))
        age = int(age)
    except ValueError as err:
        print("Age {} is invalid, please try again...".format(age))
        return (False, age)
    return (True, age)

def main():
    name = input("Hello. What's your name? ")
    valid_input = False
    while not valid_input:
        valid_input, age = validate_age(name)
    game = FrogWorld if age < 18 else WizardWorld
    environment = GameEnvironment(game(name))
    environment.play()

main()

```





## 3、Builder（建造者）

- 当我们想要创建一个由多个部分构成的对象，而且他们的构建需要一步接一步的地完成，只有当各个部分都创建好，这个对象才算完整。
- 建造者模式通常用于补充工厂模式的不足，尤其是在如下场景中：
  1. 要求一个对象有不同的表现，并且希望将对象的构造与表现解耦。
  2. 要求在某个时间点创建对象，但在稍后的时间点再访问。 如操作数据库的 ORM，ORM 中一个很重要的概念 **延迟加载**，其实就是建造者模式最常见的应用。 

```python
class Pizza:
    def __init__(self, builder):
        self.garlic = builder.garlic
        self.extra_cheese  = builder.extra_cheese

    def __str__(self):
        garlic = 'yes' if self.garlic else 'no'
        cheese = 'yes' if self.extra_cheese else 'no'
        info = ('Garlic: {}'.format(garlic), 'Extra cheese: {}'.format(cheese))
        return '\n'.join(info)

    class PizzaBuilder:
        def __init__(self):
            self.extra_cheese = False
            self.garlic = False

        def add_garlic(self):
            self.garlic = True
            return self

        def add_extra_cheese(self):
            self.extra_cheese = True
            return self

        def build(self):
            return Pizza(self)

if __name__ == '__main__':
    pizza = Pizza.PizzaBuilder().add_garlic().add_extra_cheese().build()
    print(pizza)
```



## 4、Prototype（原型）

## 5、Singleton（单例）



#  结构型

## 6、Adapter Class/Object（适配器）

- 将一个类的接口转换成为客户希望的另外一个接口.
- Adapter Pattern使得原本由于接口不兼容而不能一起工作的那些类可以一起工作



## 7、Bridge（桥接）

## 8、Composite（组合）

## 9、Decorator（装饰）

## 10、Facade（外观）

## 11、Flyweight（享元）

## 12、Proxy（代理）



#  行为型

## 13、Interpreter（解释器）

## 14、Template Method（模板方法）

## 15、Chain of Responsibility（责任链）

## 16、Command（命令）

## 17、Iterator（迭代器）

## 18、Mediator（中介者）

## 19、Memento（备忘录）

## 20、Observer（观察者, 发布订阅模式）

```python
class Publisher:

    def __init__(self):
        self._observers = dict()

    def register(self, observer):
        self._observers[observer.__class__.__name__] = observer

    def unrigister(self, observer):
        self._observers.pop(observer.name)

    def notify(self, msg):
        for _name, obs in self._observers.items():
            obs.do_somthing(msg)


class Martin:
    """Observer: Martin."""
    def do_somthing(self, msg):
        print('Martin received: ', msg)


class John:
    """Observer: John."""
    def do_somthing(self, msg):
        print('John received: ', msg)


if __name__ == '__main__':
    pub = Publisher()
    pub.register(Martin())
    pub.register(John())

    # 通知所有观察者(订阅者)
    pub.notify('time to eat')
    print()
    pub.notify('time to sleep')

```



## 21、State（状态）

## 22、Strategy（策略）

## 23、Visitor（访问者）