const express = require('express')
const fs = require('fs')
const app = express()

app.use(express.static('.'))

app.get('/', function (req, res) {
  res.send(fs.readFileSync('index.html').toString())
})

app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
})
