# Bảng Yêu Cầu Phần Mềm (tiếng Việt)

## 1. Phạm vi & nguồn tham chiếu
Các yêu cầu dưới đây được tổng hợp sau khi rà soát mã nguồn `app/api/*`, service `app/services/shop_services.py`, giao diện `templates/*.html`, cấu hình `.env`, cùng bộ kiểm thử trong `tests/`. Mục tiêu là phản ánh đúng hành vi thực tế (FastAPI + SQLAlchemy + Jinja + WebSocket) và những thay đổi mới như in hóa đơn.

## 2. Yêu cầu theo phân hệ/ngữ cảnh

### 2.1 Yêu cầu chức năng

#### 2.1.1 Các yêu cầu chức năng cần có

Hệ thống phải đáp ứng các yêu cầu chức năng sau đây để đảm bảo hoạt động hiệu quả cho vai trò khách hàng:

- **F-CUS-001**: Hệ thống cho phép người dùng tạo tài khoản mới thông qua trang `/register` hoặc API `/api/users`, với các trường bắt buộc bao gồm email, username và password.

- **F-CUS-002**: Người dùng có thể đăng nhập vào hệ thống qua form trên trang `/login` sử dụng session cookies, và hệ thống sẽ hiển thị thông báo lỗi nếu thông tin đăng nhập không chính xác.

- **F-CUS-003**: Trang chủ (`/`) phải hiển thị danh sách sản phẩm được lấy từ API `/api/items`, kèm theo trạng thái đăng nhập hiện tại của người dùng.

- **F-CUS-004**: Người dùng có thể thực hiện chức năng lọc và tìm kiếm sản phẩm, đồng thời xem cập nhật tồn kho theo thời gian thực thông qua WebSocket.

- **F-CUS-005**: Chỉ những người dùng đã đăng nhập mới được phép thêm sản phẩm vào giỏ hàng; nếu chưa đăng nhập, hệ thống sẽ báo lỗi và không thực hiện thao tác.

- **F-CUS-005b**: Giỏ hàng phải cung cấp chức năng "Remove All" để người dùng có thể xóa toàn bộ sản phẩm chỉ với một lần nhấn, và nhận được phản hồi rõ ràng về thành công hoặc thất bại.

- **F-CUS-006**: Hệ thống cho phép chỉnh sửa số lượng sản phẩm, xóa từng mặt hàng khỏi giỏ hàng; nếu giỏ hàng trống, phải hiển thị thông báo phù hợp.

- **F-CUS-007**: Khi thêm hoặc cập nhật giỏ hàng, hệ thống phải kiểm tra tồn kho và báo lỗi nếu số lượng hàng không đủ.

- **F-CUS-008**: Khi nhấn nút Checkout, hệ thống sẽ xác thực trạng thái đăng nhập; nếu chưa đăng nhập, người dùng sẽ được chuyển hướng đến trang login.

- **F-CUS-009**: Sau khi checkout thành công, trang `/checkout` phải hiển thị hóa đơn chi tiết bao gồm các mục, giá cả, thuế và tổng tiền.

- **F-CUS-010**: Nút "In hóa đơn" phải kích hoạt `window.print` với mẫu HTML được tối ưu hóa để người dùng có thể in hoặc lưu hóa đơn dưới dạng PDF.

- **F-CUS-011**: Người dùng có thể xem lại lịch sử mua hàng tại trang `/purchases`, bao gồm các đường dẫn để mở lại hóa đơn.

- **F-CUS-012**: Sau checkout, người dùng có thể chọn tiếp tục mua sắm bằng cách quay lại trang chủ (`/`) hoặc ở lại trang xác nhận.

- **F-CUS-013**: Người dùng có thể chủ động đăng xuất thông qua đường dẫn `/logout`, dẫn đến việc xóa session và chuyển hướng về trang chủ.

Ngoài ra, hệ thống phải đáp ứng các yêu cầu phi chức năng sau:

- **NF-CUS-001**: Các thao tác trên giỏ hàng (thêm, sửa, xóa) phải phản hồi trong thời gian dưới 500ms để đảm bảo trải nghiệm mượt mà trên web.

- **NF-CUS-002**: Trang checkout và chức năng in hóa đơn phải hiển thị tốt trên cả desktop và mobile, đồng thời tương thích với khổ giấy A4.

### 2.2 Các chức năng cần có dành cho vai trò **Quản trị viên (Admin)**
| ID | Mô tả yêu cầu | Loại |
| --- | --- | --- |
| F-ADM-001 | Được phép tạo/sửa/xóa/sao lưu sản phẩm qua các API `/api/items` (POST, PUT, DELETE). | Functional |
| F-ADM-002 | Có thể cập nhật tồn kho trực tiếp; hệ thống phải broadcast thay đổi tới client qua WebSocket. | Functional |
| F-ADM-003 | Có thể xem toàn bộ đơn hàng (không chỉ đơn của mình) bằng API `/api/orders` hoặc công cụ DB. | Functional |
| F-ADM-004 | Có thể dùng script `scripts/populate_items.py` để nạp dữ liệu hàng loạt khi triển khai mới. | Functional |
| F-ADM-005 | Có thể vô hiệu hóa (soft delete) sản phẩm; sản phẩm ẩn cần được loại khỏi kết quả `/api/items`. | Functional |
| F-ADM-006 | Có thể truy xuất log sự kiện (đăng nhập, checkout) để kiểm tra gian lận. | Functional |
| NF-ADM-001 | Các thao tác quản trị phải được bảo vệ bởi kiểm tra quyền server-side (không tin vào client). | Non-functional |
| NF-ADM-002 | Thay đổi tồn kho phải đảm bảo tính nhất quán dưới tải song song (transaction/locking). | Non-functional |

### 2.3 Các yêu cầu chức năng chung của **hệ thống nền tảng**
| ID | Mô tả yêu cầu | Loại |
| --- | --- | --- |
| F-SYS-001 | Hệ thống hỗ trợ session cookies cho web và JWT token cho API (`/api/users/token`). | Functional |
| F-SYS-002 | Middleware phải tự động hết hạn session sau 60 phút không hoạt động và redirect về `/`. | Functional |
| F-SYS-003 | Cho phép duy trì giỏ hàng cho khách chưa đăng nhập bằng cách gắn session_id vào DB. | Functional |
| F-SYS-004 | Cung cấp WebSocket `/ws/stock-updates` để push cập nhật tồn kho cho mọi client. | Functional |
| F-SYS-005 | Cấu hình CORS phải dựa vào biến `ALLOWED_ORIGINS` (danh sách nguồn cụ thể, không dùng `*`). | Functional |
| F-SYS-006 | Procfile / entrypoint phải khởi chạy `python app/main.py` để phục vụ ASGI app với middleware. | Functional |
| F-SYS-007 | Cho phép cấu hình DB qua `DATABASE_URL` (SQLite mặc định, Postgres trên Supabase/Railway). | Functional |
| F-SYS-008 | Cung cấp health check `/health` để nền tảng triển khai kiểm tra trạng thái. | Functional |

### 2.4 Các yêu cầu **phi chức năng** chung
| ID | Mô tả yêu cầu | Loại |
| --- | --- | --- |
| NF-SYS-001 | Mật khẩu lưu trong DB phải được băm (bcrypt) và không ghi log giá trị thô. | Non-functional |
| NF-SYS-002 | Tất cả request nhạy cảm phải đi qua HTTPS trong môi trường production (Railway). | Non-functional |
| NF-SYS-003 | `ALLOWED_ORIGINS` phải liệt kê chính xác domain (ví dụ `https://quanlybanhang.up.railway.app`) để tránh lỗi 307/CORS. | Non-functional |
| NF-SYS-004 | Build/deploy phải chạy test pytest (`tests/`) trước khi phát hành để đảm bảo hồi quy. | Non-functional |
| NF-SYS-005 | Logging phải tránh thông tin bí mật, hỗ trợ xoay vòng khi dung lượng lớn. | Non-functional |
| NF-SYS-006 | Trang chủ phải tải 100 sản phẩm trong < 1.5 giây trên môi trường 2 vCPU/1GB RAM (chuẩn Railway). | Non-functional |
| NF-SYS-007 | WebSocket phải chịu được ít nhất 500 kết nối đồng thời mà không ảnh hưởng đến khả năng checkout. | Non-functional |
| NF-SYS-008 | README và sơ đồ (`Diagrams/Activity.puml`, `Diagrams/State.puml`) phải luôn cập nhật khi thêm tính năng mới (ví dụ in hóa đơn). | Non-functional |

## 3. Ghi chú truy vết & mở rộng
- Các ID ở trên nên được tham chiếu trong test hoặc tài liệu thiết kế để truy vết 2 chiều (Yêu cầu ↔ Code ↔ Test).
- Khi bổ sung tính năng mới (ví dụ phương thức thanh toán, vai trò mới), hãy tạo nhóm ID mới theo cấu trúc tương tự và cập nhật bảng này.
