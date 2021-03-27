/*
    自定义 log 函数
*/
var log = function() {
    console.log.apply(console, arguments)
}

/*
    封装一个函数，简化 document.querySelector 的写法
*/
var $ = function(selector) {
    return document.querySelector(selector)
}

/*
    封装的 ajax 函数
*/
var ajax = function(method, path, data, reseponseCallback) {
    var r = new XMLHttpRequest()

    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    r.setRequestHeader('Content-Type', 'application/json')

    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4 && r.status==200) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            reseponseCallback(r.response)
        }
    }

    // 把数据转换成 json 格式字符串
    data = JSON.stringify(data)

    // 发送请求
    r.send(data)
}

/*
    时间戳的 y-m-d H:M:S 格式化
 */
var dateFormat = function(seconds) {
    var date = new Date(seconds * 1000)
    var year = date.getFullYear()
    var month = date.getMonth() + 1
    var day = date.getDate()

    var hour = date.getHours()
    var minu = date.getMinutes()
    var sec = date.getSeconds()

    month = month >= 10 ? month : '0' + month
    day = day >= 10 ? day : '0' + day
    hour = hour >= 10 ? hour : '0' + hour
    minu = minu >= 10 ? minu : '0' + minu
    sec = sec >= 10 ? sec : '0' + sec

    return `${year}-${month}-${day} ${hour}:${minu}:${sec}`
}
