# DFD Level 2 – Phân Rã Chi Tiết

Phiên bản: 1.0  
Ngày cập nhật: 2025-11-20  
Tài liệu này mở rộng DFD Level 1 bằng cách phân rã các tiến trình có nghiệp vụ phức tạp thành các tiến trình con (Level 2). Mỗi sơ đồ Level 2 tập trung vào một tiến trình từ P1..P8 để tránh quá tải thông tin. Các sơ đồ PlantUML liên quan nằm trong thư mục `Diagrams/` dưới dạng một file riêng cho từng tiến trình.

---
## 1. Tổng quan phạm vi Level 2
| Tiến trình                 | Lý do phân rã                                      | Số tiến trình con | Diagram                                          | Ghi chú                  |
|----------------------------|----------------------------------------------------|-------------------|--------------------------------------------------|--------------------------|
| P1 Đăng ký/Xác thực        | Bao gồm đăng ký, đăng nhập, đăng xuất và cấp token | 4                 | `Diagrams/software_dfd_level2_p1_auth.puml`      | Gộp cả khách & người bán |
| P3 Quản lý Giỏ             | Gồm đọc giỏ, kiểm tồn, ghi giỏ                     | 3                 | `Diagrams/software_dfd_level2_p3_cart.puml`      | Cân bằng D5/D6           |
| P4 Thanh toán & Hóa đơn    | Chốt giỏ, tạo đơn, cập nhật tồn                    | 4                 | `Diagrams/software_dfd_level2_p4_checkout.puml`  | Giải quyết path lỗi tồn  |
| P5 Quản lý Sản phẩm        | CRUD + batch upload                                | 3                 | `Diagrams/software_dfd_level2_p5_items.puml`     | Không mô tả upload ảnh   |
| P6 Cập nhật Tồn kho        | Điều chỉnh thủ công + batch + broadcast            | 3                 | `Diagrams/software_dfd_level2_p6_inventory.puml` | Chia sẻ chung D2         |
| P7 Quản lý Đơn hàng (Read) | Hai vai trò đọc khác nhau + drill down             | 3                 | `Diagrams/software_dfd_level2_p7_orders.puml`    | Không tạo/ghi đơn        |
| P2 Duyệt & Tìm Sản phẩm    | Luồng đã atomic ở Level 1                          | —                 | —                                                | Không cần Level 2        |
| P8 Log & Giám sát          | Luồng monitoring đơn giản                          | —                 | —                                                | Không cần Level 2        |

---
## 2. Quy tắc cân bằng
- Không bổ sung actor hay data store mới so với Level 1. Các luồng nội bộ chỉ phân rã thêm nhưng phải kết thúc bằng DF đã có ở Level 1.
- Mã DF ở Level 2 dùng dạng `DF-L2-Px-y` để dễ truy vết ngược lên DF-00x/10x.
- Khi một tiến trình có hai nhánh nghiệp vụ khác nhau (ví dụ checkout thành công vs. lỗi tồn kho), nhánh được mô tả bằng luồng dữ liệu riêng nhưng vẫn nằm trong cùng sơ đồ.

---
## 3. P1 – Đăng ký / Xác thực
- Diagram: `Diagrams/software_dfd_level2_p1_auth.puml`
- Subprocesses: P1.1 Capture & Validate, P1.2 Lookup / Persist, P1.3 Verify Credential, P1.4 Issue / Revoke Session.
- Actor: Khách hàng, Người bán.
- Data Store: D1 Người dùng.

| Flow ID     | Nguồn | Đích  | Nội dung chính                                                   |
|-------------|-------|-------|------------------------------------------------------------------|
| DF-L2-P1-01 | Actor | P1.1  | Payload đăng ký / đăng nhập / đăng xuất (email, mật khẩu, token) |
| DF-L2-P1-02 | P1.1  | P1.2  | Thông tin người dùng đã chuẩn hóa                                |
| DF-L2-P1-03 | P1.2  | D1    | Hồ sơ người dùng cần lưu/cập nhật                                |
| DF-L2-P1-04 | P1.2  | P1.3  | Hồ sơ người dùng đã tra cứu                                      |
| DF-L2-P1-05 | P1.3  | P1.4  | Kết quả xác thực + quyền                                         |
| DF-L2-P1-06 | P1.4  | Actor | Token, trạng thái phiên                                          |
| DF-L2-P1-07 | P1.4  | P1.2  | Thông tin phiên cần revoke                                       |

---
## 4. P3 – Quản lý Giỏ
- Diagram: `Diagrams/software_dfd_level2_p3_cart.puml`
- Subprocesses: P3.1 Load Cart Context, P3.2 Validate & Price Items, P3.3 Persist Cart.
- Actor: Khách hàng.
- Data Store: D5 Giỏ hàng, D6 Chi tiết giỏ, D2 Sản phẩm.

| Flow ID     | Nguồn      | Đích       | Nội dung                                                  |
|-------------|------------|------------|-----------------------------------------------------------|
| DF-L2-P3-01 | Khách hàng | P3.1       | Payload thao tác giỏ (cart_id, item_id, quantity, action) |
| DF-L2-P3-02 | P3.1       | D5/D6      | Khóa giỏ và danh sách cart item hiện tại                  |
| DF-L2-P3-03 | P3.1       | P3.2       | Ảnh chụp giỏ hiện tại                                     |
| DF-L2-P3-04 | P3.2       | D2         | Danh sách item cần đối chiếu tồn và giá                   |
| DF-L2-P3-05 | P3.2       | P3.3       | Giỏ đã chuẩn hóa + thông tin tồn/giá hợp lệ               |
| DF-L2-P3-06 | P3.3       | D5/D6      | Bản ghi giỏ/carte item mới                                |
| DF-L2-P3-07 | P3.3       | Khách hàng | Ảnh chụp giỏ sau thao tác (DF-103)                        |

---
## 5. P4 – Thanh toán & Hóa đơn
- Diagram: `Diagrams/software_dfd_level2_p4_checkout.puml`
- Subprocesses: P4.1 Validate Cart Snapshot, P4.2 Reserve & Price, P4.3 Create Order & Items, P4.4 Finalize Payment & Stock.
- Actor: Khách hàng.
- Data Store: D5 Giỏ hàng, D6 Chi tiết giỏ, D3 Đơn hàng, D4 Chi tiết đơn, D2 Sản phẩm.

| Flow ID     | Nguồn      | Đích            | Nội dung                                           |
|-------------|------------|-----------------|----------------------------------------------------|
| DF-L2-P4-01 | Khách hàng | P4.1            | Payload checkout (cart_id, phương thức thanh toán) |
| DF-L2-P4-02 | P4.1       | D5/D6           | Snapshot giỏ và cart items đã khóa                 |
| DF-L2-P4-03 | P4.1       | P4.2            | Giỏ hợp lệ + thông tin khách hàng                  |
| DF-L2-P4-04 | P4.2       | D2              | Danh sách item cần kiểm tồn cuối                   |
| DF-L2-P4-05 | P4.2       | P4.3            | Dòng hàng đủ tồn + giá cuối                        |
| DF-L2-P4-06 | P4.3       | D3              | Bản ghi đơn mới                                    |
| DF-L2-P4-07 | P4.3       | D4              | Bản ghi order item mới                             |
| DF-L2-P4-08 | P4.3       | P4.4            | Thông tin đơn hoàn chỉnh + tổng số tiền            |
| DF-L2-P4-09 | P4.4       | D2              | Danh sách item cần giảm tồn                        |
| DF-L2-P4-10 | P4.4       | Khách hàng      | Hóa đơn/biên nhận với chi tiết thanh toán          |
| DF-L2-P4-11 | P4.4       | P3.3 (implicit) | Thông tin dọn giỏ / invalidate cache               |

---
## 6. P5 – Quản lý Sản phẩm
- Diagram: `Diagrams/software_dfd_level2_p5_items.puml`
- Subprocesses: P5.1 Capture Request, P5.2 Apply CRUD, P5.3 Batch Import Summary.
- Actor: Người bán.
- Data Store: D2 Sản phẩm.

| Flow ID     | Nguồn     | Đích      | Nội dung                                                |
|-------------|-----------|-----------|---------------------------------------------------------|
| DF-L2-P5-01 | Người bán | P5.1      | Payload CRUD/batch sản phẩm (metadata, giá, trạng thái) |
| DF-L2-P5-02 | P5.1      | P5.2      | Yêu cầu CRUD đã chuẩn hóa                               |
| DF-L2-P5-03 | P5.2      | D2        | Dữ liệu sản phẩm mới/cập nhật/xóa                       |
| DF-L2-P5-04 | P5.2      | P5.3      | Kết quả từng bản ghi (success/error)                    |
| DF-L2-P5-05 | P5.3      | Người bán | Tổng hợp kết quả CRUD/batch (DF-107/113)                |

---
## 7. P6 – Cập nhật Tồn kho
- Diagram: `Diagrams/software_dfd_level2_p6_inventory.puml`
- Subprocesses: P6.1 Capture Adjustment, P6.2 Validate Batch, P6.3 Apply & Broadcast.
- Actor: Người bán.
- Data Store: D2 Sản phẩm.

| Flow ID     | Nguồn     | Đích      | Nội dung                                       |
|-------------|-----------|-----------|------------------------------------------------|
| DF-L2-P6-01 | Người bán | P6.1      | Payload điều chỉnh tồn (item_id, delta, lý do) |
| DF-L2-P6-02 | P6.1      | P6.2      | Danh sách điều chỉnh đã chuẩn hóa              |
| DF-L2-P6-03 | P6.2      | D2        | Tồn hiện tại cho các item                      |
| DF-L2-P6-04 | P6.2      | P6.3      | Điều chỉnh hợp lệ                              |
| DF-L2-P6-05 | P6.3      | D2        | Bản cập nhật tồn kho                           |
| DF-L2-P6-06 | P6.3      | Người bán | Báo cáo trạng thái tồn mới (DF-108)            |
| DF-L2-P6-07 | P6.3      | P2        | Sự kiện tồn mới (item_id, stock hiện tại)      |

---
## 8. P7 – Quản lý Đơn hàng (Read)
- Diagram: `Diagrams/software_dfd_level2_p7_orders.puml`
- Subprocesses: P7.1 Fetch Customer History, P7.2 Fetch Merchant View, P7.3 Fetch Order Detail.
- Actor: Khách hàng, Người bán.
- Data Stores: D3 Đơn hàng, D4 Chi tiết đơn.

| Flow ID     | Nguồn      | Đích       | Nội dung                                          |
|-------------|------------|------------|---------------------------------------------------|
| DF-L2-P7-01 | Khách hàng | P7.1       | Tham số truy vấn lịch sử mua (date range, status) |
| DF-L2-P7-02 | P7.1       | D3         | Tiêu chí lọc orders theo user                     |
| DF-L2-P7-03 | P7.1       | Khách hàng | Danh sách lịch sử đơn (DF-105)                    |
| DF-L2-P7-04 | Người bán  | P7.2       | Tham số truy vấn danh sách đơn bán                |
| DF-L2-P7-05 | P7.2       | D3         | Bộ lọc orders dành cho merchant                   |
| DF-L2-P7-06 | P7.2       | Người bán  | Danh sách đơn bán (DF-109)                        |
| DF-L2-P7-07 | Actor      | P7.3       | Yêu cầu chi tiết đơn / hóa đơn                    |
| DF-L2-P7-08 | P7.3       | D3/D4      | ID đơn + item cần truy vấn chi tiết               |
| DF-L2-P7-09 | P7.3       | Actor      | Chi tiết đơn/hóa đơn (DF-104/105/109)             |

---
## 9. Liên kết sơ đồ
| Diagram file                                     | Mô tả          | Cách render                                               |
|--------------------------------------------------|----------------|-----------------------------------------------------------|
| `Diagrams/software_dfd_level2_p1_auth.puml`      | Level 2 cho P1 | `plantuml Diagrams/software_dfd_level2_p1_auth.puml`      |
| `Diagrams/software_dfd_level2_p3_cart.puml`      | Level 2 cho P3 | `plantuml Diagrams/software_dfd_level2_p3_cart.puml`      |
| `Diagrams/software_dfd_level2_p4_checkout.puml`  | Level 2 cho P4 | `plantuml Diagrams/software_dfd_level2_p4_checkout.puml`  |
| `Diagrams/software_dfd_level2_p5_items.puml`     | Level 2 cho P5 | `plantuml Diagrams/software_dfd_level2_p5_items.puml`     |
| `Diagrams/software_dfd_level2_p6_inventory.puml` | Level 2 cho P6 | `plantuml Diagrams/software_dfd_level2_p6_inventory.puml` |
| `Diagrams/software_dfd_level2_p7_orders.puml`    | Level 2 cho P7 | `plantuml Diagrams/software_dfd_level2_p7_orders.puml`    |

---
Các sơ đồ trên đảm bảo sự cân bằng với Level 1 và giữ nguyên các actor/data store đã định nghĩa. Nếu phạm vi mở rộng (ví dụ thêm quy trình trả hàng), cần cập nhật Level 0/1 trước rồi mới bổ sung Level 2 tương ứng.

---
## 10. Định hướng Level 2
| Tiến trình Level 1 | Lý do cần Level 2                          | Nhóm subprocess gợi ý                                       |
|--------------------|--------------------------------------------|-------------------------------------------------------------|
| P1 Auth            | Nhiều bước (đăng ký, đăng nhập, cấp token) | P1.1 Validate input, P1.2 Lookup user, P1.3 Issue token     |
| P3 Cart            | CRUD giỏ + kiểm tồn                        | P3.1 Fetch cart, P3.2 Validate stock, P3.3 Persist cart     |
| P4 Checkout        | Chốt giỏ → đơn → cập nhật tồn              | P4.1 Validate cart, P4.2 Create order, P4.3 Adjust stock    |
| P5 Items CRUD      | CRUD + upload hàng loạt                    | P5.1 Create/Update, P5.2 Delete/Hide, P5.3 Bulk import      |
| P6 Stock Ops       | Batch cập nhật, broadcast event            | P6.1 Manual adjust, P6.2 Batch upload, P6.3 Publish event   |
| P7 Orders Read     | Khác vai trò (customer vs merchant)        | P7.1 Customer history, P7.2 Merchant list, P7.3 Detail view |
| P2 Browse          | Đã đủ chi tiết ở Level 1                   | —                                                           |
| P8 Monitoring      | Thao tác đơn giản                          | —                                                           |
