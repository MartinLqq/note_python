



callback参数 + flask.copy_current_request_context

```
from flask import copy_current_request_context

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
	@copy_current_request_context
	def can_disconnect():
		disconnect()
		session['receive_count'] = session.get('receive_count', 0) + 1
		
	# for this emit we use a callback function
	# when the callback function is invoked we know that the message has been
	# received and it is safe to disconnect
	emit('my_response', {'data': 'Disconnected!', 'count': session['receive_count']},         callback=can_disconnect)

```