from flask import request, jsonify, Flask

from src.utils.log import logger


app = Flask(__name__)


@app.route('/')
def index():
    """Index page."""

    logger.info('request args: %s', request.args)

    logger.debug('debug log')
    logger.info('info log')
    logger.warning('warning log')
    logger.error('error log')
    try:
        1 / 0
    except ZeroDivisionError as err:
        logger.exception('exception log, %s', err)

    logger.critical('critical log')

    return jsonify({
        'results': """当时间的主人，命运的主宰，灵魂的舵手。 
生活就像海洋，只有意志坚强的人，才能到达彼岸。 
你因成功而内心充满喜悦的时候，就没有时间颓废。 
无论何人，若是失去耐心，就是失去灵魂。 
我们应当努力奋斗，有所作为。这样，我们就可以说，我们没有虚度年华，并有可能在时间的沙滩上留下我们的足迹。 
当许多人在一条路上徘徊不前时，他们不得不让开一条大路，让那珍惜时间的人赶到他们的前面去。 
人类学会走路，也得学会摔跤，而且只有经过摔跤他才能学会走路。 
""".splitlines()
    })
