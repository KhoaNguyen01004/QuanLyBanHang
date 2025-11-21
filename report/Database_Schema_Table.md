# Thiết kế bảng ràng buộc dữ liệu - QuanLyBanHang

Dưới đây là thiết kế bảng cho cơ sở dữ liệu QuanLyBanHang, bao gồm các trường, kiểu dữ liệu, ràng buộc và mô tả. Các ràng buộc toàn vẹn bao gồm khóa chính, khóa ngoại, không null, duy nhất, kiểm tra và mặc định.

## Tóm tắt 4 ràng buộc chính

| Tên bảng     | Khóa chính (Primary Key) | Khóa ngoại (Foreign Key)                  | Không null (Not Null)                     | Duy nhất (Unique) |
|--------------|---------------------------|--------------------------------------------|--------------------------------------------|-------------------|
| users       | id                        | -                                          | id, username, email, hashed_password      | username, email   |
| items       | id                        | -                                          | id, name, price, stock                    | -                 |
| carts       | id                        | user_id -> users.id                        | id                                        | -                 |
| cart_items  | id                        | cart_id -> carts.id, item_id -> items.id   | id, cart_id, item_id, quantity            | -                 |
| orders      | id                        | user_id -> users.id                        | id, user_id, total_amount, status         | -                 |
| order_items | id                        | order_id -> orders.id, item_id -> items.id | id, order_id, item_id, quantity, price    | -                 |

## Bảng users

| Tên trường      | Kiểu dữ liệu | Ràng buộc dữ liệu                          | Mô tả                          |
|-----------------|--------------|--------------------------------------------|--------------------------------|
| id              | varchar(5)  | PRIMARY KEY, NOT NULL                      | Mã định danh duy nhất của người dùng |
| username        | varchar     | NOT NULL, UNIQUE                           | Tên đăng nhập của người dùng   |
| email           | varchar     | NOT NULL, UNIQUE                           | Địa chỉ email của người dùng   |
| hashed_password | varchar     | NOT NULL                                   | Mật khẩu đã mã hóa            |
| created_at      | timestamp   | DEFAULT now()                              | Thời gian tạo tài khoản       |
| updated_at      | timestamp   | DEFAULT now()                              | Thời gian cập nhật cuối cùng  |

## Bảng items

| Tên trường   | Kiểu dữ liệu | Ràng buộc dữ liệu                          | Mô tả                          |
|--------------|--------------|--------------------------------------------|--------------------------------|
| id           | integer     | PRIMARY KEY, NOT NULL                      | Mã định danh duy nhất của sản phẩm |
| name         | varchar     | NOT NULL                                   | Tên sản phẩm                   |
| description  | text        |                                            | Mô tả sản phẩm                 |
| price        | float       | NOT NULL, CHECK (price > 0)                | Giá sản phẩm                   |
| stock        | integer     | NOT NULL, CHECK (stock >= 0)               | Số lượng tồn kho               |
| picture_path | varchar     |                                            | Đường dẫn hình ảnh             |
| tags         | varchar     |                                            | Thẻ phân loại                  |
| created_at   | timestamp   | DEFAULT now()                              | Thời gian tạo sản phẩm         |
| updated_at   | timestamp   | DEFAULT now()                              | Thời gian cập nhật cuối cùng  |

## Bảng carts

| Tên trường | Kiểu dữ liệu | Ràng buộc dữ liệu                          | Mô tả                          |
|------------|--------------|--------------------------------------------|--------------------------------|
| id         | integer     | PRIMARY KEY, NOT NULL                      | Mã định danh duy nhất của giỏ hàng |
| user_id    | varchar(5)  | FOREIGN KEY REFERENCES users(id)           | Mã người dùng sở hữu giỏ hàng |
| session_id | varchar     |                                            | ID phiên cho người dùng chưa đăng nhập |
| created_at | timestamp   | DEFAULT now()                              | Thời gian tạo giỏ hàng         |
| updated_at | timestamp   | DEFAULT now()                              | Thời gian cập nhật cuối cùng  |
|            |              | CHECK (user_id IS NOT NULL OR session_id IS NOT NULL) | Ít nhất một trong user_id hoặc session_id phải có giá trị |

## Bảng cart_items

| Tên trường | Kiểu dữ liệu | Ràng buộc dữ liệu                          | Mô tả                          |
|------------|--------------|--------------------------------------------|--------------------------------|
| id         | integer     | PRIMARY KEY, NOT NULL                      | Mã định danh duy nhất của mục giỏ hàng |
| cart_id    | integer     | NOT NULL, FOREIGN KEY REFERENCES carts(id) | Mã giỏ hàng chứa mục này       |
| item_id    | integer     | NOT NULL, FOREIGN KEY REFERENCES items(id) | Mã sản phẩm trong giỏ hàng     |
| quantity   | integer     | NOT NULL, CHECK (quantity > 0)             | Số lượng sản phẩm              |

## Bảng orders

| Tên trường   | Kiểu dữ liệu | Ràng buộc dữ liệu                          | Mô tả                          |
|--------------|--------------|--------------------------------------------|--------------------------------|
| id           | integer     | PRIMARY KEY, NOT NULL                      | Mã định danh duy nhất của đơn hàng |
| user_id      | varchar(5)  | NOT NULL, FOREIGN KEY REFERENCES users(id) | Mã người dùng đặt đơn hàng     |
| total_amount | float       | NOT NULL, CHECK (total_amount > 0)         | Tổng số tiền của đơn hàng      |
| status       | varchar     | NOT NULL                                   | Trạng thái đơn hàng            |
| created_at   | timestamp   | DEFAULT now()                              | Thời gian tạo đơn hàng         |
| updated_at   | timestamp   | DEFAULT now()                              | Thời gian cập nhật cuối cùng  |

## Bảng order_items

| Tên trường | Kiểu dữ liệu | Ràng buộc dữ liệu                          | Mô tả                          |
|------------|--------------|--------------------------------------------|--------------------------------|
| id         | integer     | PRIMARY KEY, NOT NULL                      | Mã định danh duy nhất của mục đơn hàng |
| order_id   | integer     | NOT NULL, FOREIGN KEY REFERENCES orders(id)| Mã đơn hàng chứa mục này       |
| item_id    | integer     | NOT NULL, FOREIGN KEY REFERENCES items(id) | Mã sản phẩm trong đơn hàng     |
| quantity   | integer     | NOT NULL, CHECK (quantity > 0)             | Số lượng sản phẩm              |
| price      | float       | NOT NULL, CHECK (price > 0)                | Giá sản phẩm tại thời điểm đặt |

## Ràng buộc toàn vẹn bổ sung

- **Khóa ngoại (Foreign Keys):**
  - carts.user_id -> users.id (nhiều giỏ hàng cho một người dùng)
  - cart_items.cart_id -> carts.id (nhiều mục cho một giỏ hàng)
  - cart_items.item_id -> items.id (mục giỏ hàng tham chiếu đến sản phẩm)
  - orders.user_id -> users.id (nhiều đơn hàng cho một người dùng)
  - order_items.order_id -> orders.id (nhiều mục cho một đơn hàng)
  - order_items.item_id -> items.id (mục đơn hàng tham chiếu đến sản phẩm)

- **Ràng buộc kiểm tra (Check Constraints):**
  - items.price > 0: Giá sản phẩm phải dương
  - items.stock >= 0: Tồn kho không âm
  - carts: Ít nhất user_id hoặc session_id phải có giá trị
  - cart_items.quantity > 0: Số lượng phải dương
  - orders.total_amount > 0: Tổng tiền phải dương
  - order_items.quantity > 0: Số lượng phải dương
  - order_items.price > 0: Giá phải dương

- **Ràng buộc duy nhất (Unique Constraints):**
  - users.username: Tên đăng nhập duy nhất
  - users.email: Email duy nhất

- **Giá trị mặc định (Default Values):**
