let unirest = require('unirest');
let res;


exports.handler = function(event, context, callback) {
    unirest.get(event.body)
    .end(function (response) {
        res = response.body;
        let getResponse = {
            statusCode: 200,
            headers: {
                "Access-Control-Allow-Origin" : "*"
            },
            body: JSON.stringify(res)
        };
        console.log(getResponse)
        // callback(null,getResponse);
    });
}


// event1 ={"body":"https://www.baidu.com/"}
// handler(event1,"","")
