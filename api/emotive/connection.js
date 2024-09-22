const WebSocket = require('ws')
const url = 'wss://localhost:6868'
const connection = new WebSocket(url)

connection.onopen = () => {
    connection.send({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "queryHeadsets"
    })
}

connection.onerror = (error) => {
    console.log(error)
}

connection.onmessage = (e) => {
    console.log(e.data)
}