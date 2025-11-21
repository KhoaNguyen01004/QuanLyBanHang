# Sơ đồ ERD – Ứng dụng Bán Hàng

Phiên bản: 1.0  
Ngày cập nhật: 2025-11-21  
Tệp PlantUML: `Diagrams/software_erd.puml`

---
## 1. Mục đích
- Chuẩn hóa mô hình dữ liệu quan hệ đang triển khai trong `app/models` để phục vụ phân tích nghiệp vụ, thiết kế API và kiểm thử.
- Đảm bảo sự nhất quán giữa ERD, yêu cầu trong `software_requirements.md` và các sơ đồ DFD/Use Case.
- Làm cơ sở để đánh giá tác động khi mở rộng chức năng (ví dụ payment gateway, khuyến mãi).

---
## 2. Phạm vi & Giả định
| Chủ đề            | Quyết định/ Giả định                                                                 |
|-------------------|---------------------------------------------------------------------------------------|
| Phiên bản DB      | Bám theo SQLAlchemy models hiện tại, chưa mô tả bảng log hoặc bảng cấu hình hệ thống |
| Giỏ khách vãng lai| `carts.user_id` có thể null; `session_id` dùng để map giỏ tạm thời                   |
| Thanh toán        | Đơn hàng lưu trạng thái nội bộ (`orders.status`), chưa tách bảng thanh toán          |
| Hóa đơn           | Hóa đơn được sinh từ thông tin của `orders` và `order_items`, không có bảng riêng    |
| Tag sản phẩm      | `items.tags` lưu dạng chuỗi phân tách, chưa chuẩn hóa thành bảng phụ                 |

---
## 3. Danh sách thực thể
| Thực thể  | Bảng       | Mô tả ngắn                                                                 | Nguồn chính              |
|-----------|------------|-----------------------------------------------------------------------------|--------------------------|
| User      | `users`    | Tài khoản khách hàng/merchant với thông tin xác thực                      | `app/models/user.py`     |
| Cart      | `carts`    | Giỏ hàng hiện tại của user hoặc guest session                              | `app/models/cart.py`     |
| CartItem  | `cart_items`| Chi tiết từng sản phẩm trong giỏ                                           | `app/models/cart_item.py`|
| Item      | `items`    | Danh mục sản phẩm, tồn kho và metadata                                     | `app/models/item.py`     |
| Order     | `orders`   | Đơn hàng sau khi checkout, trạng thái thanh toán                           | `app/models/order.py`    |
| OrderItem | `order_items`| Chi tiết sản phẩm thuộc một đơn, lưu số lượng và đơn giá tại thời điểm mua | `app/models/order_item.py`|

---
## 4. Thuộc tính chính
### User (`users`)
- `id` (PK, varchar).
- `username`, `email`: không đặt unique constraint trong schema hiện tại.
- `hashed_password`: lưu hash.
- `created_at`, `updated_at`: audit.

### Item (`items`)
- `id` (PK, serial).
- `name`, `description`, `price` (`double precision`).
- `stock`: tồn kho.
- `picture_path`, `tags` (nullable).
- `created_at`, `updated_at`.

### Cart (`carts`)
- `id` (PK, serial).
- `user_id` (FK `users.id`, nullable) + `session_id` (nullable).
- `created_at`, `updated_at`.

### CartItem (`cart_items`)
- `id` (PK, serial).
- `cart_id` (FK `carts.id`), `item_id` (FK `items.id`).
- `quantity`: số lượng (int, mặc định >0 theo logic ứng dụng).

### Order (`orders`)
- `id` (PK, serial).
- `user_id` (FK `users.id`).
- `total_amount` (`double precision`), `status` (varchar).
- `created_at`, `updated_at`.

### OrderItem (`order_items`)
- `id` (PK, serial).
- `order_id` (FK `orders.id`), `item_id` (FK `items.id`).
- `quantity`, `unit_price` (`double precision`).

---
## 5. Quan hệ & Bội số
| Quan hệ                 | Kiểu (PK/FK)                   | Bội số       | Ghi chú nghiệp vụ                                               |
|-------------------------|-------------------------------|--------------|-----------------------------------------------------------------|
| User – Cart             | `carts.user_id -> users.id`   | 1 User có 0..* Cart | Cho phép nhiều giỏ (phục vụ thiết bị khác nhau).                 |
| Cart – CartItem         | `cart_items.cart_id -> carts.id` | 1 Cart có 0..* CartItem | Xóa cart cascade sang cart_items.                               |
| Item – CartItem         | `cart_items.item_id -> items.id` | 1 Item có 0..* CartItem | Kiểm tồn realtime khi thêm giỏ.                                 |
| User – Order            | `orders.user_id -> users.id`  | 1 User có 0..* Order | Checkout yêu cầu đăng nhập.                                     |
| Order – OrderItem       | `order_items.order_id -> orders.id` | 1 Order có 1..* OrderItem | Mỗi đơn phải có ít nhất một dòng sản phẩm.                      |
| Item – OrderItem        | `order_items.item_id -> items.id` | 1 Item có 0..* OrderItem | Dữ liệu dùng để báo cáo bán hàng.                               |

---
## 6. Ràng buộc & Truy vết yêu cầu
| Ràng buộc dữ liệu                                         | Yêu cầu liên quan                   |
|-----------------------------------------------------------|-------------------------------------|
| `users.email` và `users.username` unique                  | F-CUS-001, F-CUS-002                |
| `cart_items.quantity >= 1`                                | F-CUS-005, NF-CUS-001               |
| Checkout chỉ chấp nhận cart có chủ sở hữu hợp lệ          | F-CUS-008, F-SYS-003                |
| `orders.status` phản ánh kết quả thanh toán               | F-CUS-008a, F-CUS-012               |
| Cập nhật tồn kho giảm stock đồng bộ với order_items tạo   | NF-CUS-003, F-MER-002               |
| `order_items.unit_price` khóa giá để audit                | NF-SYS-004, F-MER-003               |

---
## 7. Ghi chú thiết kế
- Có thể tách `merchant` thành bảng riêng nếu cần phân quyền chi tiết; hiện dùng cùng bảng `users` với role khác nhau.
- `items.tags` định dạng chuỗi, cần chuẩn hóa thành bảng `item_tags` khi yêu cầu tìm kiếm nâng cao xuất hiện.
- Cần migration riêng nếu bổ sung bảng `payments` hoặc `invoices` để mở rộng tích hợp gateway.
- Đối với báo cáo monitor, dữ liệu log vẫn nằm ngoài ERD (P8 không sử dụng DB).

---
## 8. Tham chiếu PlantUML
Sơ đồ nằm trong `Diagrams/software_erd.puml` và có thể xuất hình (
`plantuml -tpng Diagrams/software_erd.puml`).

````plantuml
@startuml ERD_Shop
' ...xem file để biết đầy đủ thuộc tính và quan hệ...
@enduml
````

Tài liệu này sẽ được cập nhật song song mỗi khi model SQLAlchemy thay đổi để đảm bảo truy vết dữ liệu ↔ yêu cầu ↔ sơ đồ.
