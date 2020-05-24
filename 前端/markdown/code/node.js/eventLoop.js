// 引入 events 模块
const events = require('events');

// 创建 eventEmitter 对象
const eventEmitter = new events.EventEmitter();

// 绑定事件及事件的处理程序
eventEmitter.on('myEvent', name => {
	console.log('Hello ', name)
})

console.log('事件触发之前.')

// 触发事件
eventEmitter.emit('myEvent', 'Martin')
