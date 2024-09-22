const WebSocket = require('ws');


let socketUrl = 'wss://localhost:6868'

 // create socket
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0
var socket = new WebSocket(socketUrl)

// read user infor
var user = {
    "license":"b6e4f009-b8d0-4789-b41c-7f0d9bd38e4e",
    "clientId":"5QrYSU73hpG39guyaa3cHBEWvLShdwYSqj1ty6t4",
    "clientSecret":"rBzlhHAREbyRTdT1UmH11NVjeVEYF40eGmoASESOqb24JRz9PN6IxblRPt5soI9xUBrzvLPMq5ZBa7W1N2NAOAdbW8Lq4VaFH4JYPlk5RlHDm43hQYuWngC3i0bKIgqk",
    "debit":1
}

function requestAccess() {
    return new Promise(function(resolve, reject){
        const REQUEST_ACCESS_ID = 1
        let requestAccessRequest = {
            "jsonrpc": "2.0", 
            "method": "requestAccess", 
            "params": { 
                "clientId": user.clientId, 
                "clientSecret": user.clientSecret
            },
            "id": REQUEST_ACCESS_ID
        }
        socket.on('open',async ()=>{
            // console.log('start send request: ',requestAccessRequest)
            socket.send(JSON.stringify(requestAccessRequest));
    
            socket.on('message', (data)=>{
                console.log(data)
                try {
                    if(JSON.parse(data)['id']==REQUEST_ACCESS_ID){
                        resolve(data)
                    }
                } catch (error) {}
            })
        })
    })
}
function authorize() {
    return new Promise(function(resolve, reject){
        const AUTHORIZE_ID = 4
        let authorizeRequest = { 
            "jsonrpc": "2.0", "method": "authorize", 
            "params": { 
                "clientId": user.clientId, 
                "clientSecret": user.clientSecret, 
                "license": user.license,
                "debit": user.debit
            },
            "id": AUTHORIZE_ID
        }
        socket.on('open', async ()=>{
            socket.send(JSON.stringify(authorizeRequest))
            socket.on('message', (data)=>{
                console.log(data)
                try {
                    if(JSON.parse(data)['id']==AUTHORIZE_ID){
                        let cortexToken = JSON.parse(data)['result']['cortexToken']
                        resolve(cortexToken)
                    }
                } catch (error) {
                    console.log(error)
                }
            })
        })

        
    })
}
async function checkGrantAccessAndQuerySessionInfo() {
    let requestAccessResult = ""
    await requestAccess().then((result)=>{requestAccessResult=result})

    let accessGranted = JSON.parse(requestAccessResult)

    // check if user is logged in CortexUI
    if ("error" in accessGranted){
        console.log('You must login on CortexUI before request for grant access then rerun')
        throw new Error('You must login on CortexUI before request for grant access')
    }else{
        console.log(accessGranted['result']['message'])
        // console.log(accessGranted['result'])
        if(accessGranted['result']['accessGranted']){
            await querySessionInfo()
        }
        else{
            console.log('You must accept access request from this app on CortexUI then rerun')
            throw new Error('You must accept access request from this app on CortexUI')
        }
    }   
}

authorize().then(data=>{
    console.log(data)
}).catch(error=>{
    console.log(error)
})   // request access