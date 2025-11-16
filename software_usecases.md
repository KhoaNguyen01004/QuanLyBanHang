# Bảng Use Case Phần Mềm (tiếng Việt)

Bảng use case dưới đây được tổng hợp từ bảng yêu cầu trong file `software_requirements.md`. Các use case được phân nhóm chi tiết theo vai trò và ngữ cảnh sử dụng, bao gồm các yêu cầu chức năng và phi chức năng liên quan. Mỗi use case bao gồm mã định danh duy nhất, tên, mô tả chi tiết, các yêu cầu chính (bao gồm yêu cầu), và các yêu cầu mở rộng (extension requirements) nếu có.

## 1. Use Case Chung (General Use Cases)
Áp dụng cho tất cả người dùng, không phân biệt vai trò cụ thể.

| Mã Use Case | Tên Use Case | Mô tả | Bao gồm Yêu cầu | Extension Requirements |
|-------------|--------------|-------|-----------------|-----------------------|
| UC-GEN-001 | Đăng ký tài khoản | Người dùng tạo tài khoản mới với thông tin cơ bản như email, username, password. | F-CUS-001, NF-SYS-001 | Không có |
| UC-GEN-002 | Đăng nhập hệ thống | Người dùng nhập thông tin đăng nhập để truy cập hệ thống, sử dụng session cookies hoặc JWT. | F-CUS-002, F-SYS-001, F-SYS-002 | NF-SYS-002 (HTTPS trong production) |
| UC-GEN-003 | Duy trì session | Hệ thống quản lý session tự động hết hạn sau thời gian không hoạt động. | F-SYS-002 | Không có |
| UC-GEN-004 | Health Check | Kiểm tra trạng thái hệ thống để đảm bảo hoạt động bình thường. | F-SYS-008 | NF-SYS-004 (chạy test trước deploy) |
| UC-GEN-005 | Cấu hình CORS | Hệ thống kiểm soát nguồn gốc request dựa trên danh sách cho phép. | F-SYS-005 | NF-SYS-003 (liệt kê domain chính xác) |
| UC-GEN-006 | Khởi chạy ứng dụng | Sử dụng Procfile hoặc entrypoint để chạy ASGI app. | F-SYS-006 | Không có |
| UC-GEN-007 | Cấu hình cơ sở dữ liệu | Hệ thống hỗ trợ cấu hình DB qua biến môi trường. | F-SYS-007 | Không có |
| UC-GEN-008 | Logging và bảo mật | Ghi log sự kiện mà không lộ thông tin bí mật. | NF-SYS-005 | NF-ADM-006 (truy xuất log để kiểm tra gian lận) |

## 2. Use Case Dành Cho Khách Hàng (Customer Use Cases)
Áp dụng cho người dùng cuối (khách hàng) khi tương tác với hệ thống mua bán.

| Mã Use Case | Tên Use Case | Mô tả | Bao gồm Yêu cầu | Extension Requirements |
|-------------|--------------|-------|-----------------|-----------------------|
| UC-CUS-001 | Xem trang chủ và sản phẩm | Người dùng truy cập trang chủ để xem danh sách sản phẩm, lọc/tìm kiếm, và cập nhật tồn kho thời gian thực. | F-CUS-003, F-CUS-004, NF-CUS-001, NF-SYS-006 | F-SYS-004 (WebSocket cho cập nhật tồn kho) |
| UC-CUS-002 | Thêm sản phẩm vào giỏ hàng | Người dùng đã đăng nhập thêm sản phẩm vào giỏ, hệ thống kiểm tra tồn kho và báo lỗi nếu không đủ. | F-CUS-005, F-CUS-007, NF-ADM-002 | F-SYS-003 (duy trì giỏ cho khách chưa đăng nhập) |
| UC-CUS-003 | Quản lý giỏ hàng | Người dùng chỉnh sửa số lượng, xóa mặt hàng, hoặc xóa toàn bộ giỏ hàng. | F-CUS-005b, F-CUS-006 | Không có |
| UC-CUS-004 | Checkout và thanh toán | Người dùng xác nhận đơn hàng, hệ thống tạo hóa đơn và chuyển đến trang xác nhận. | F-CUS-008, F-CUS-009, F-CUS-012 | NF-CUS-002 (tương thích mobile và in ấn) |
| UC-CUS-005 | In hóa đơn | Người dùng in hoặc lưu hóa đơn sau checkout. | F-CUS-010 | Không có |
| UC-CUS-006 | Xem lịch sử mua hàng | Người dùng xem lại các đơn hàng đã mua, bao gồm chi tiết hóa đơn. | F-CUS-011 | Không có |
| UC-CUS-007 | Đăng xuất | Người dùng chủ động đăng xuất để xóa session. | F-CUS-013 | Không có |

## 3. Use Case Dành Cho Quản Trị Viên (Admin Use Cases)
Áp dụng cho quản trị viên để quản lý hệ thống và dữ liệu.

| Mã Use Case | Tên Use Case | Mô tả | Bao gồm Yêu cầu | Extension Requirements |
|-------------|--------------|-------|-----------------|-----------------------|
| UC-ADM-001 | Quản lý sản phẩm | Admin tạo, sửa, xóa, sao lưu sản phẩm qua API. | F-ADM-001, F-ADM-005 | NF-ADM-001 (bảo vệ server-side) |
| UC-ADM-002 | Cập nhật tồn kho | Admin thay đổi tồn kho trực tiếp và broadcast cập nhật qua WebSocket. | F-ADM-002, NF-ADM-002 | NF-SYS-007 (chịu tải đồng thời) |
| UC-ADM-003 | Xem đơn hàng | Admin truy cập toàn bộ đơn hàng của hệ thống. | F-ADM-003 | Không có |
| UC-ADM-004 | Nạp dữ liệu hàng loạt | Admin sử dụng script để nạp sản phẩm khi triển khai. | F-ADM-004 | Không có |
| UC-ADM-005 | Truy xuất log | Admin xem log sự kiện để kiểm tra và bảo mật. | F-ADM-006 | NF-SYS-005 (logging an toàn) |

## 4. Ghi Chú
- Các use case trên được suy ra từ yêu cầu chức năng trong `software_requirements.md`. Mỗi use case có thể bao gồm nhiều yêu cầu để mô tả luồng hoàn chỉnh.
- Extension requirements là các yêu cầu bổ sung hoặc mở rộng, như bảo mật, hiệu suất, hoặc tích hợp.
- Khi thêm tính năng mới, hãy cập nhật bảng này để duy trì tính nhất quán.
- Tài liệu này hỗ trợ truy vết từ yêu cầu đến use case và ngược lại.
