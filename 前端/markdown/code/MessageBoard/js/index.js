// let messages = []

updateMessageList()

function updateMessageList () {
    const messages = loadMessages()
    const listContent = document.querySelector('.listContent')

    if (!messages.length) {
        const ul = '<ul><li>空空如也.</li></ul>'
        listContent.innerHTML = ul
        return
    }

    ul = '<ul>'
    for (let msg of messages) {
        ul += `
        <li>
        	${msg.username} 说: ${msg.message}
	        <span class="time">${msg.datetime}</span>
	        <hr>
        </li>
        `
    }
    ul += '</ul>'
    listContent.innerHTML = ul
}

function addMessage () {
    const username = document.querySelector('#username')
    const message = document.querySelector('#message')
    if (!username.value || !message.value) {
        alert('请输入昵称和留言内容')
        return
    }
    // messages.push({
    //     username,
    //     message
    // })
    addOneMessage(username.value, message.value)
    updateMessageList()
    message.value = ''
}


function loadMessages() {
    return JSON.parse(
        localStorage.getItem('messages')
    ) || []
}

function addOneMessage(username, message) {
    const item = {
        username,
        message,
        datetime: getCurrentTime()
    }
    let messages = loadMessages()
    console.log(messages)
    if (!messages) {
        // 初次存储
        messages = [item]
    } else {
        messages.push(item)
    }
    localStorage.setItem('messages', JSON.stringify(messages))
}


function getCurrentTime () {
    const now = new Date()
    return now.toJSON()
}
