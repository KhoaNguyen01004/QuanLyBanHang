# Nội Dung Yêu Cầu Phi Chức Năng Cho Báo Cáo

## 2.2 Yêu Cầu Phi Chức Năng

### 2.2.1 Các Yêu Cầu Phi Chức Năng Cần Có

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
