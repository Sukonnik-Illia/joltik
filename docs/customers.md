Things to do before:
- init app
- make dependency injected db_session to be able to make queries from routes

customers CRUD:
- create `POST /customer` accepts json with customer data
- update `PUT /customer/<customer_id>`
- delete `DELETE /customer/<customer_id>`
- get all `GET /customer`
- get one `GET /customer/<customer_id>`

How to create endpoints:
- create request/responce models if needed
- create endpoint function and bind it to route
