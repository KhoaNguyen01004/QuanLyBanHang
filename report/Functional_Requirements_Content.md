# Nội Dung Yêu Cầu Chức Năng Cho Báo Cáo

## 2.1 Yêu Cầu Chức Năng

### 2.1.1 Các Yêu Cầu Chức Năng Cần Có

Hệ thống quản lý bán hàng phải đáp ứng các yêu cầu chức năng sau đây để đảm bảo hoạt động hiệu quả cho vai trò khách hàng:

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
