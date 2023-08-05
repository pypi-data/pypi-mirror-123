# ringding - Simple framework to create awesome WebSocket APIs

## What is ringding?

Ringding is a framework to communicate between a Python server and JavaScript client(s) based on WebSocket.
Compared to Web API frameworks like Flask or FastAPI, the ringding API is specified in a more "Python-API-style" way using classes rather than using decorators and "magic strings".
The call of API functions on the JavaScript side also looks more like function calls.

## When do I want to use ringding?

* When you want to call function on your server and don't want to provide a full-fledged REST-API.
* When you want to minimize the overhead from HTTP-headers (especially in Single-Page-Applications / SPAs).
* When you want to publish a Python-API to a JavaScript client.
* When the server should notify the clients about events.

## What technology does ringding use?

Ringding is transmitting the data using WebSockets.

## How do I use ringding?

Ringding provides a JavaScript-client and a Python server. 
The JavaScript client ringdingjs is hosted by the server on the endpoint `/client.js`. 
But you can also extract `ringdingjs.js` from source and put it somewhere in your 
project. It is located in `clients/js/ringdingjs.js`. You will want to use the 
corresponding package.json for Node since Node not support WebSockets by default.
If you want to use ringdingjs in browser apps, you don't need any dependencies.

An example Python backend:

```python
import ringding


class MyApi:
    def get_name(self):
        return 'Alfred'
    
    def sum(self, a, b):
        return a + b


if __name__ == '__main__':
    ringding.RdServer(port=8001).serve(MyApi)
```

In NodeJS, you can use ringding like this:
```javascript
const { RD, CallApi } = require('ringdingjs')

async function communicate() {
    await RD.connect('ws://localhost:8001')
    
    const name = await CallApi().MyApi.get_name()
    console.log('The name is', name)
    
    // You can provide keyword arguments to a function call.
    let sum = await CallApi().MyApi.sum({a: 5, b: 2})
    
    // You can also use the more flexible direct call:
    let another_sum = await RD.call("MyApi.sum(*)", {a: 4, b: 2}) 
    
    console.log('The sum is: ', sum)
    
    RD.disconnect()
}

communicate()
```

Alternatively in a browser, you can connect and call the sum-function like this:
```html
<head>
    <meta charset="UTF-8">
    <title>Hello ringding</title>
</head>
<body>
    <div>Calling "API.sum()" with arguments {a: 5, b: 2}"</div>
    <div>Response: <span id="response"></span></div>
</body>
<script data-main="scripts/app" src="http://localhost:8001/client.js"></script>
<script>
    async function run_example() {

        // Connect to server
        await RD.connect('ws://localhost:8001')

        // Send a message
        const response = await CallApi().MyApi.sum({a: 5, b: 2})

        // Read the response
        console.log('Response:', response)
        document.getElementById('response').innerText = String(response)
    }
    run_example()
</script>
</html>
```

## Other features

**Chained calls**

With chained calls you can call multiple parameterized functions on a server:

`RD.call('Api.create_user(*user_data).get_hash(hash_type), {user_data: {name: 'Fido', age: 42}, hash_type: 'md5'}` 

**Advanced return types**

You can return every JSON-supported datatype (including lists and dicts with simple datatypes) or dataclasses.

```python
import ringding

import dataclasses


@dataclasses.dataclass
class AdvancedReturnType:
    name: str
    age: int


class Api:
    def get_user(self):
        return AdvancedReturnType('Fido', 42)
    
if __name__ == '__main__':
    ringding.RdServer(port=8001).serve(Api)
```

The corresponding JavaScript call is this

```javascript
const response = await CallApi().Api.get_user()
console.log(response.name) // "Fido"
console.log(response.age)  // 42
```
**Nested APIs**

I would recommend to use properties for nested Sub-API's on python side

```python
import ringding


class Nested:
    def do_something(self):
        return 'I did something'

    
class Api:
    @property
    def NestedApi(self):
        return Nested()
    
if __name__ == '__main__':
    ringding.RdServer(port=8001).serve(Api)
```

And the JavaScript-call would be `CallApi().Api.NestedApi.do_something()`

**A word on Typescript**

You might want to create an own object of CallApi() and cast you API specification to that object.
That way you could get an API with autocompletion powered by Typescript.

## Roadmap

* An interface to browse API's and their documentation
