# Nội Dung Yêu Cầu Cho Báo Cáo

## 2.1 Yêu Cầu Chức Năng

### 2.1.1 Các Yêu Cầu Chức Năng Cần Có

Hệ thống quản lý bán hàng phải cung cấp các chức năng thiết yếu sau đây để hỗ trợ người dùng (khách hàng) trong quá trình mua sắm trực tuyến một cách hiệu quả và an toàn:

- **Quản lý tài khoản**: Cho phép người dùng tạo tài khoản mới, đăng nhập và đăng xuất khỏi hệ thống để bảo vệ thông tin cá nhân và duy trì phiên làm việc.

- **Xem và tìm kiếm sản phẩm**: Hiển thị danh sách sản phẩm trên trang chủ, hỗ trợ chức năng lọc và tìm kiếm để người dùng dễ dàng khám phá các mặt hàng, đồng thời cập nhật tồn kho theo thời gian thực.

- **Quản lý giỏ hàng**: Cho phép người dùng thêm, chỉnh sửa số lượng, xóa sản phẩm khỏi giỏ hàng, bao gồm cả chức năng xóa toàn bộ giỏ hàng, với kiểm tra tồn kho để tránh đặt hàng vượt quá số lượng có sẵn.

- **Thanh toán và checkout**: Xác thực đăng nhập trước khi tiến hành thanh toán, hiển thị hóa đơn chi tiết sau khi hoàn tất giao dịch, và cung cấp tùy chọn in hóa đơn để lưu trữ hoặc in ấn.

- **Lịch sử mua hàng**: Cho phép người dùng xem lại các đơn hàng đã thực hiện, bao gồm các đường dẫn để truy cập lại hóa đơn chi tiết.

- **Điều hướng sau mua hàng**: Sau khi checkout, người dùng có thể chọn tiếp tục mua sắm hoặc ở lại trang xác nhận để theo dõi trạng thái đơn hàng.


<!-- Tại đây, bạn có thể thêm các yêu cầu chi tiết với ID như F-CUS-001, v.v. -->

## 2.3 Yêu Cầu Phi Chức Năng

### 2.3.1 Các Yêu Cầu Phi Chức Năng Cần Có

Ngoài các chức năng thiết yếu, hệ thống quản lý bán hàng phải đáp ứng các yêu cầu phi chức năng sau đây để đảm bảo hiệu suất, bảo mật và trải nghiệm người dùng tối ưu:

- **Hiệu suất**: Các thao tác trên giỏ hàng như thêm, sửa hoặc xóa sản phẩm phải phản hồi trong thời gian dưới 500ms để mang lại trải nghiệm mượt mà trên nền tảng web.

- **Khả năng tương thích**: Trang checkout và chức năng in hóa đơn phải hiển thị chính xác trên cả thiết bị desktop và mobile, đồng thời tương thích với khổ giấy A4 để hỗ trợ in ấn dễ dàng.

- **Bảo mật**: Mật khẩu người dùng phải được mã hóa bằng thuật toán bcrypt trước khi lưu trữ trong cơ sở dữ liệu, và không được ghi log dưới dạng thô để ngăn chặn rò rỉ thông tin.

- **An toàn mạng**: Tất cả các yêu cầu nhạy cảm phải được truyền tải qua giao thức HTTPS trong môi trường sản xuất để bảo vệ dữ liệu khỏi các cuộc tấn công man-in-the-middle.

- **Cấu hình CORS**: Danh sách các nguồn gốc được phép (ALLOWED_ORIGINS) phải được liệt kê chính xác theo từng domain cụ thể, tránh sử dụng ký tự đại diện (*) để ngăn chặn lỗi CORS và tăng cường bảo mật.

- **Kiểm thử và triển khai**: Quá trình build và deploy phải bao gồm việc chạy bộ kiểm thử pytest để đảm bảo không có hồi quy, đồng thời duy trì tính nhất quán trong các phiên bản phát hành.

- **Ghi log**: Hệ thống ghi log phải tránh lưu trữ thông tin bí mật, hỗ trợ cơ chế xoay vòng log khi dung lượng tăng cao để quản lý tài nguyên hiệu quả.

- **Tải và khả năng mở rộng**: Trang chủ phải tải được 100 sản phẩm trong thời gian dưới 1.5 giây trên môi trường tiêu chuẩn (2 vCPU, 1GB RAM), và WebSocket phải xử lý được ít nhất 500 kết nối đồng thời mà không ảnh hưởng đến chức năng checkout.

- **Cập nhật tài liệu**: Các tài liệu như README và sơ đồ hoạt động phải được cập nhật kịp thời khi có thêm tính năng mới, đảm bảo tính nhất quán giữa mã nguồn và tài liệu.

Các yêu cầu phi chức năng này đảm bảo hệ thống không chỉ hoạt động đúng mà còn ổn định, an toàn và hiệu quả trong môi trường thực tế.

<!-- Tại đây, bạn có thể thêm các yêu cầu chi tiết với ID như NF-CUS-001, v.v. -->
