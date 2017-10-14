var http = require("http");
const fs = require('fs')

http.createServer(function (request, response) {
    response.writeHead(200, {'Content-Type': 'text/html'});
    console.log(fs.readFileSync('index.html').toString())
    response.end(fs.readFileSync('index.html').toString());
}).listen(3000);
console.log('Server running at http://127.0.0.1:3000/');

