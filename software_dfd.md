# Sơ Đồ DFD Hệ Thống Bán Hàng (Context & Level 1)

(Revision 2: Đã làm sạch file PlantUML `Diagrams/software_dfd.puml`, khôi phục cú pháp chuẩn cho hai sơ đồ @startuml DFD_Level_0 và @startuml DFD_Level_1.)

Tài liệu này mô tả Data Flow Diagram (DFD) cho ứng dụng bán hàng trong repo. Hai mức chi tiết được cung cấp:
- Level 0 (Context): Thể hiện hệ thống như một hộp đen và các tương tác chính với tác nhân bên ngoài.
- Level 1: Phân rã hệ thống thành các tiến trình nghiệp vụ, kho dữ liệu và các luồng dữ liệu chi tiết.

## 1. Mục tiêu
DFD giúp hình dung luồng dữ liệu đi vào, đi ra và di chuyển nội bộ giữa các tiến trình và kho dữ liệu, hỗ trợ:
- Đánh giá phạm vi xử lý.
- Xác định điểm kiểm soát, log và hiệu năng.
- Cơ sở cho thiết kế dịch vụ hoặc API.

## 2. Phạm vi & Giả định
- Chưa tích hợp cổng thanh toán bên thứ ba; thanh toán xử lý nội bộ (có thể mở rộng thành tiến trình riêng P4a sau này).
- Session / token được trừu tượng trong tiến trình P1 (Đăng ký / Xác thực).
- Cache sản phẩm (nếu có) được coi là một lớp tối ưu nằm trong D2 (Items) hoặc memory layer không vẽ riêng.
- Giỏ hàng lưu ở kho tạm thời D4 (Cart Session) liên kết với người dùng đã đăng nhập.

## 3. Danh sách Tiến trình (Processes)
| Mã | Tên | Mô tả chính | Yêu cầu liên quan |
|----|-----|------------|------------------|
| P1 | Đăng ký / Xác thực | Quản lý tạo tài khoản, đăng nhập, đăng xuất, cấp token | F-CUS-001, F-CUS-002, F-CUS-013, F-SYS-001, F-SYS-002 |
| P2 | Duyệt & Tìm Sản Phẩm | Cung cấp danh sách, tìm kiếm, lọc, hiển thị tồn kho gần thời gian thực | F-CUS-003, F-CUS-004, F-SYS-004, NF-SYS-006, NF-SYS-007 |
| P3 | Quản lý Giỏ | Thêm/sửa/xóa mục giỏ, kiểm tra tồn kho & tính nhất quán | F-CUS-005, F-CUS-006, F-CUS-007, F-SYS-003, NF-CUS-001, NF-CUS-003 |
| P4 | Thanh toán & Hóa đơn | Tạo đơn hàng, sinh hóa đơn, xác nhận, cho phép tiếp tục mua | F-CUS-008, F-CUS-008a, F-CUS-009, F-CUS-010, F-CUS-012, NF-CUS-002, NF-CUS-004 |
| P5 | Quản lý Sản phẩm | CRUD + Ẩn sản phẩm, sao lưu thông tin | F-MER-001, F-MER-005, NF-MER-001 |
| P6 | Cập nhật Tồn kho | Cập nhật số lượng, xử lý hàng loạt, phát sự kiện cập nhật | F-MER-002, NF-MER-002, NF-SYS-007 |
| P7 | Đơn hàng & Lịch sử | Truy vấn đơn hàng và lịch sử mua cho khách & người bán | F-CUS-011, F-MER-003 |
| P8 | Log & Giám sát | Ghi log sự kiện, trả về trạng thái health | F-SYS-008, F-MER-006, NF-SYS-001, NF-SYS-002 |
| P9 | Khởi động & Cấu hình | Thiết lập kết nối DB, khởi tạo thành phần nền | F-SYS-006, F-SYS-007 |

## 4. Kho Dữ liệu (Data Stores)
| Mã | Tên | Nội dung | Nguồn cập nhật chính |
|----|-----|----------|----------------------|
| D1 | Users | Thông tin người dùng (email, hash mật khẩu, vai trò) | P1 |
| D2 | Items | Danh mục & thuộc tính sản phẩm, trạng thái hiển thị | P5 |
| D3 | Inventory | Số lượng tồn kho theo sản phẩm | P6 |
| D4 | Carts (Session) | Các mục trong giỏ tạm theo người dùng | P3, bị xóa/gộp bởi P4 |
| D5 | Orders | Đơn hàng (mục, tổng, thuế, thời gian) | P4 |
| D6 | Logs | Sự kiện (đăng nhập, thanh toán, cập nhật tồn, quản lý SP) | P1, P4, P5, P6, P8 |

## 5. Tác nhân bên ngoài (External Entities)
| Actor | Vai trò | Dòng dữ liệu vào | Dòng dữ liệu ra |
|-------|--------|------------------|------------------|
| Khách hàng | Người mua | Thông tin đăng ký, đăng nhập, thao tác giỏ, thanh toán, truy vấn lịch sử | Token, danh sách SP, trạng thái giỏ, hóa đơn, lịch sử đơn |
| Người bán | Quản trị hàng | Đăng nhập, CRUD sản phẩm, cập nhật tồn, xem đơn, xem log | Xác nhận CRUD, tồn kho mới, danh sách đơn, log sự kiện |
| Người vận hành | Vận hành hệ thống | Yêu cầu khởi động, cấu hình DB | Kết quả khởi động, trạng thái cấu hình |
| Nền tảng giám sát | Giám sát | Ping health | Trạng thái health, metric đơn giản |

## 6. Luồng Dữ liệu Chính (Chọn lọc)
| Từ | Đến | Dữ liệu | Ghi chú |
|----|-----|--------|--------|
| Customer | P3 | Thêm/xóa/cập nhật mục giỏ | Yêu cầu phiên hợp lệ từ P1 |
| P3 | D4 | Bản ghi giỏ cập nhật | Kiểm tra tồn D3 trước ghi |
| P3 | Customer | Phản hồi giỏ (thành công/thất bại) | <500ms (NF-CUS-001) |
| P6 | D3 | Số lượng tồn mới | Có thể hàng loạt CSV |
| P6 | P2 | Sự kiện tồn thay đổi | Đẩy cập nhật realtime |
| P4 | D5 | Đơn hàng mới | Sinh ID đơn |
| P4 | Customer | Hóa đơn chi tiết | PDF / trang hiển thị |
| P4 | D6 | Log thanh toán | Phục vụ giám sát/gian lận |
| P1 | D6 | Log đăng nhập/đăng ký | Bảo mật: không ghi mật khẩu |
| P5 | D6 | Log quản lý sản phẩm | Theo dõi thay đổi |
| P6 | D6 | Log tồn kho | Theo dõi điều chỉnh |
| P8 | Monitor | Health snapshot | {status, timestamp} |
| P9 | D2/D3 | Nạp cache ban đầu | Tùy chọn tối ưu hiệu năng |

## 7. Ràng buộc & Phi chức năng liên quan luồng dữ liệu
- Hiệu năng: P2 phải trả về danh sách 100 SP < 1.5s (NF-SYS-006).
- Đồng thời: P3 + P6 + P4 cần đảm bảo nhất quán tồn kho (NF-CUS-003, NF-MER-002, NF-SYS-007).
- Bảo mật: Mật khẩu hash (NF-SYS-001); kết nối an toàn cho đăng nhập & thanh toán (NF-SYS-002).
- Khả dụng: Health check (P8) cung cấp tín hiệu đơn giản (F-SYS-008).

## 8. Quan hệ giữa Tiến trình
| Nguồn | Đích | Mục đích |
|-------|------|---------|
| P1 | P3/P4 | Xác thực phiên trước thao tác nhạy cảm |
| P6 | P2 | Cập nhật realtime tồn kho cho UI |
| P4 | P7 | Thêm đơn mới vào lịch sử |
| P5 | P2 | Sản phẩm mới/ẩn cập nhật danh sách |
| P4 | D6 | Ghi log thanh toán |
| P1 | D6 | Ghi log sự kiện đăng nhập |

## 9. Ghi chú Thiết kế & Mở rộng Tương lai
- Có thể tách Payment Gateway thành tiến trình P4a nếu tích hợp bên thứ ba.
- Cơ chế đẩy tồn kho (P6→P2) có thể hiện thực bằng WebSocket (đã có `websocket_manager.py`) hoặc SSE; hiện ở mức logic.
- Logs (D6) nên chuẩn hóa dạng (timestamp, actor, action, entity_id, status).
- Tối ưu đọc sản phẩm: thêm cache memory phía P2 hoặc CDN cho ảnh.

## 10. Tham chiếu Diagram
Xem file PlantUML: `Diagrams/software_dfd.puml` (hai khối @startuml DFD_Level_0 và @startuml DFD_Level_1).

## 11. Kiểm tra Nhất quán với Use Cases
- Mỗi use case chính tương ứng ít nhất một tiến trình (VD: UC-CUS-002 ↔ P3; UC-GEN-002 ↔ P1; UC-CUS-003 ↔ P4).
- Không có tiến trình nào thiếu kho dữ liệu cần thiết.

## 12. Data Dictionary (Tóm tắt trường quan trọng)
| Thực thể | Trường chính | Mô tả |
|----------|--------------|-------|
| Users | user_id (PK), email, password_hash, role, created_at | Quản lý danh tính và quyền |
| Items | item_id (PK), name, description, price, status, image_path | Danh mục sản phẩm |
| Inventory | item_id (FK), quantity, updated_at | Số lượng tồn hiện tại |
| Carts | cart_id (PK), user_id (FK), updated_at | Định danh giỏ người dùng |
| CartItems | cart_id (FK), item_id (FK), quantity | Mục trong giỏ |
| Orders | order_id (PK), user_id (FK), total_amount, tax_amount, created_at | Bản ghi đơn hàng |
| OrderItems | order_id (FK), item_id (FK), quantity, unit_price | Chi tiết dòng đơn |
| Logs | log_id (PK), actor_id, actor_role, action, entity_type, entity_id, status, timestamp | Audit & giám sát |

## 13. Kết luận
DFD cung cấp góc nhìn luồng dữ liệu, hỗ trợ kiểm tra đầy đủ phạm vi và là nền để thiết kế API, event hoặc microservice nếu mở rộng.

---
Nếu cần thêm Level 2 cho một tiến trình (ví dụ P4 phân rã thành Kiểm tra tồn cuối, Tính tổng, Tạo hóa đơn, Ghi log), hãy yêu cầu tiếp.
