# Bảng Yêu Cầu Phần Mềm (tiếng Việt)

## 1. Phạm vi & nguồn tham chiếu
Các yêu cầu dưới đây được tổng hợp sau khi rà soát mã nguồn `app/api/*`, service `app/services/shop_services.py`, giao diện `templates/*.html`, cấu hình `.env`, cùng bộ kiểm thử trong `tests/`. Mục tiêu là phản ánh đúng hành vi thực tế (FastAPI + SQLAlchemy + Jinja + WebSocket) và những thay đổi mới như in hóa đơn.

## 2. Yêu cầu theo phân hệ/ngữ cảnh

### 2.1 Các chức năng cần có dành cho vai trò **Khách hàng**
| ID         | Mô tả yêu cầu                                                                                                                                                                                                                                                                                     | Loại           |
|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| F-CUS-001  | Cho phép tạo tài khoản tại `/register`/`/api/users` với các trường bắt buộc (email, username, password).                                                                                                                                                                                          | Functional     |
| F-CUS-002  | Cho phép đăng nhập qua form `/login` (session cookies) và nhận thông báo lỗi khi sai thông tin.                                                                                                                                                                                                   | Functional     |
| F-CUS-003  | Trang chủ (`/`) phải liệt kê sản phẩm lấy từ `/api/items`, kèm trạng thái đăng nhập hiện tại.                                                                                                                                                                                                     | Functional     |
| F-CUS-004  | Người dùng có thể lọc/ tìm sản phẩm và xem tồn kho cập nhật theo thời gian thực (WebSocket).                                                                                                                                                                                                      | Functional     |
| F-CUS-005  | Chỉ người dùng đã đăng nhập mới được phép thêm sản phẩm vào giỏ hàng. Nếu chưa đăng nhập, hệ thống sẽ báo lỗi và không thực hiện thao tác này. Ngoài ra, giao diện phải hiển thị thông báo (toast) yêu cầu đăng nhập khi người dùng chưa đăng nhập mà cố gắng thêm sản phẩm vào giỏ hàng.         | Functional     |
| F-CUS-005b | Giỏ hàng phải cung cấp thao tác "Remove All" giúp người dùng xóa toàn bộ sản phẩm chỉ với một lần bấm và nhận phản hồi thành công/thất bại rõ ràng.                                                                                                                                               | Functional     |
| F-CUS-006  | Cho phép chỉnh sửa số lượng, xóa mặt hàng khỏi giỏ; nếu giỏ rỗng phải hiển thị thông báo tương ứng.                                                                                                                                                                                               | Functional     |
| F-CUS-007  | Khi thêm/cập nhật giỏ, hệ thống phải kiểm tra tồn kho và báo lỗi nếu không đủ hàng.                                                                                                                                                                                                               | Functional     |
| F-CUS-007b | Khi nhiều người dùng thêm cùng một sản phẩm vào giỏ hàng cùng lúc, hệ thống phải xử lý race condition: chỉ người đến trước được thêm nếu còn hàng, các yêu cầu sau sẽ bị từ chối nếu hết hàng. Việc kiểm tra và cập nhật tồn kho/giỏ phải đảm bảo tính nhất quán và atomic (transaction/locking). | Functional     |
| F-CUS-008  | Khi nhấn Checkout, hệ thống xác thực đăng nhập; nếu chưa đăng nhập phải chuyển đến trang login.                                                                                                                                                                                                   | Functional     |
| F-CUS-009  | Sau Checkout thành công, trang `/checkout` phải hiển thị hóa đơn chi tiết (mục, giá, thuế, tổng).                                                                                                                                                                                                 | Functional     |
| F-CUS-010  | Nút "In hóa đơn" phải gọi `window.print` với mẫu HTML tối ưu để người dùng in hoặc lưu PDF.                                                                                                                                                                                                       | Functional     |
| F-CUS-011  | Người dùng xem lại lịch sử mua hàng tại `/purchases`, bao gồm đường dẫn mở lại hóa đơn.                                                                                                                                                                                                           | Functional     |
| F-CUS-012  | Người dùng có thể tiếp tục mua sắm sau checkout (quay lại `/`) hoặc ở lại trang xác nhận.                                                                                                                                                                                                         | Functional     |
| F-CUS-013  | Người dùng chủ động đăng xuất (/logout) để xóa session và quay về trang chủ.                                                                                                                                                                                                                      | Functional     |
| NF-CUS-001 | Thao tác giỏ (thêm, sửa, xóa) phải phản hồi < 500ms để đảm bảo trải nghiệm mượt trên web.                                                                                                                                                                                                         | Non-functional |
| NF-CUS-002 | Trang checkout + in hóa đơn phải hiển thị tốt trên desktop/mobile và tương thích khổ giấy A4.                                                                                                                                                                                                     | Non-functional |

### 2.2 Các chức năng cần có dành cho vai trò **Quản trị viên (Admin)**
| ID         | Mô tả yêu cầu                                                                                   | Loại           |
|------------|-------------------------------------------------------------------------------------------------|----------------|
| F-ADM-001  | Được phép tạo/sửa/xóa/sao lưu sản phẩm qua các API `/api/items` (POST, PUT, DELETE).            | Functional     |
| F-ADM-002  | Có thể cập nhật tồn kho trực tiếp; hệ thống phải broadcast thay đổi tới client qua WebSocket.   | Functional     |
| F-ADM-003  | Có thể xem toàn bộ đơn hàng (không chỉ đơn của mình) bằng API `/api/orders` hoặc công cụ DB.    | Functional     |
| F-ADM-004  | Có thể dùng script `scripts/populate_items.py` để nạp dữ liệu hàng loạt khi triển khai mới.     | Functional     |
| F-ADM-005  | Có thể vô hiệu hóa (soft delete) sản phẩm; sản phẩm ẩn cần được loại khỏi kết quả `/api/items`. | Functional     |
| F-ADM-006  | Có thể truy xuất log sự kiện (đăng nhập, checkout) để kiểm tra gian lận.                        | Functional     |
| NF-ADM-001 | Các thao tác quản trị phải được bảo vệ bởi kiểm tra quyền server-side (không tin vào client).   | Non-functional |
| NF-ADM-002 | Thay đổi tồn kho phải đảm bảo tính nhất quán dưới tải song song (transaction/locking).          | Non-functional |

### 2.3 Các yêu cầu chức năng chung của **hệ thống nền tảng**
| ID        | Mô tả yêu cầu                                                                                                          | Loại       |
|-----------|------------------------------------------------------------------------------------------------------------------------|------------|
| F-SYS-001 | Hệ thống hỗ trợ session cookies cho web và JWT token cho API (`/api/users/token`).                                     | Functional |
| F-SYS-002 | Middleware phải tự động hết hạn session sau 60 phút không hoạt động và redirect về `/`.                                | Functional |
| F-SYS-003 | Không duy trì giỏ hàng cho khách chưa đăng nhập. Chỉ người dùng đã đăng nhập mới được phép thêm sản phẩm vào giỏ hàng. | Functional |
| F-SYS-004 | Cung cấp WebSocket `/ws/stock-updates` để push cập nhật tồn kho cho mọi client.                                        | Functional |
| F-SYS-005 | Cấu hình CORS phải dựa vào biến `ALLOWED_ORIGINS` (danh sách nguồn cụ thể, không dùng `*`).                            | Functional |
| F-SYS-006 | Procfile / entrypoint phải khởi chạy `python app/main.py` để phục vụ ASGI app với middleware.                          | Functional |
| F-SYS-007 | Cho phép cấu hình DB qua `DATABASE_URL` (SQLite mặc định, Postgres trên Supabase/Railway).                             | Functional |
| F-SYS-008 | Cung cấp health check `/health` để nền tảng triển khai kiểm tra trạng thái.                                            | Functional |

### 2.4 Các yêu cầu **phi chức năng** chung
| ID         | Mô tả yêu cầu                                                                                                                   | Loại           |
|------------|---------------------------------------------------------------------------------------------------------------------------------|----------------|
| NF-SYS-001 | Mật khẩu lưu trong DB phải được băm (bcrypt) và không ghi log giá trị thô.                                                      | Non-functional |
| NF-SYS-002 | Tất cả request nhạy cảm phải đi qua HTTPS trong môi trường production (Railway).                                                | Non-functional |
| NF-SYS-003 | `ALLOWED_ORIGINS` phải liệt kê chính xác domain (ví dụ `https://quanlybanhang.up.railway.app`) để tránh lỗi 307/CORS.           | Non-functional |
| NF-SYS-004 | Build/deploy phải chạy test pytest (`tests/`) trước khi phát hành để đảm bảo hồi quy.                                           | Non-functional |
| NF-SYS-005 | Logging phải tránh thông tin bí mật, hỗ trợ xoay vòng khi dung lượng lớn.                                                       | Non-functional |
| NF-SYS-006 | Trang chủ phải tải 100 sản phẩm trong < 1.5 giây trên môi trường 2 vCPU/1GB RAM (chuẩn Railway).                                | Non-functional |
| NF-SYS-007 | WebSocket phải chịu được ít nhất 500 kết nối đồng thời mà không ảnh hưởng đến khả năng checkout.                                | Non-functional |
| NF-SYS-008 | README và sơ đồ (`Diagrams/Activity.puml`, `Diagrams/State.puml`) phải luôn cập nhật khi thêm tính năng mới (ví dụ in hóa đơn). | Non-functional |

## 3. Ghi chú truy vết & mở rộng
- Các ID ở trên nên được tham chiếu trong test hoặc tài liệu thiết kế để truy vết 2 chiều (Yêu cầu ↔ Code ↔ Test).
- Khi bổ sung tính năng mới (ví dụ phương thức thanh toán, vai trò mới), hãy tạo nhóm ID mới theo cấu trúc tương tự và cập nhật bảng này.
