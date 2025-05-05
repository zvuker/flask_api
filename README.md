REST API, реализованный на Flask. Позволяет управлять товарами и оформлять заказы.

1. установка flasck: 
      pip install Flask

2. запуск сервер:
      python app.py

3. API будет доступен по адресу: 
      http://localhost:5000

4. Endpoints: 
4.1 /products:
  4.1.1 GET /products — получить список всех товаров.
  4.1.2 GET /products/<id> — получить товар по ID.
  4.1.3 POST /products — добавить новый товар.

          пример тела запроса(json):
                {
                  "name": "Tablet",
                  "price": 799.99,
                  "stock": 30
                }
         пример ответа(json):
              {
                "success": true,
                "product": {
                  "id": 3,
                  "name": "Tablet",
                  "price": 799.99,
                  "stock": 30
                }
              }

  4.1.4 DELETE /products/<id> — удалить товар.
  4.1.5 PUT /products/<id> — полностью обновить товар.

        пример тела запроса(json):
                {
                  "name": "Smartphone",
                  "price": 599.99,
                  "stock": 80
                }
                
  4.1.6 PATCH /products/<id> — частично обновить товар.

4.2 /orders
  4.2.1 POST /orders — оформить заказ.

        пример тела запроса(json):
                {
                  "items": [
                  {"product_id": 1, "quantity": 2},
                  {"product_id": 2, "quantity": 1}
                  ]
                }

4.3 /reset
  4.3.1 POST /reset — сбросить базу данных к начальному состоянию.

Функционал: 
  - поддержка всех CRUD-операций для товаров.
  - поддержка создания заказов.
  - простая in-memory база данных.
  - возможность сброса базы через /reset.


