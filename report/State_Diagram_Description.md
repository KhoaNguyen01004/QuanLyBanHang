# Mô tả biểu đồ trạng thái (State Diagram) cho ứng dụng QuanLyBanHang

Biểu đồ trạng thái mô tả các trạng thái chính và chuyển đổi giữa chúng trong ứng dụng QuanLyBanHang, tập trung vào các miền cốt lõi như xác thực (Auth), giỏ hàng (Cart) và đơn hàng (Order). Biểu đồ được chia thành các mục dựa trên các trạng thái và chuyển đổi chính.

## 1. Trạng thái xác thực (Auth States)

- **Anonymous**: Trạng thái ban đầu cho người dùng chưa đăng nhập. Từ đây, người dùng có thể chuyển sang Authenticated thông qua đăng nhập thành công (sử dụng API /api/users/login hoặc /api/users/token).
- **Authenticated**: Trạng thái khi người dùng đã đăng nhập thành công. Từ đây, người dùng có thể chuyển về Anonymous thông qua đăng xuất (/logout) hoặc hết thời gian phiên (>1 giờ không hoạt động).

## 2. Trạng thái giỏ hàng (Cart States)

- **NonExistent**: Trạng thái ban đầu khi chưa có giỏ hàng. Chuyển sang Active khi tạo hoặc lấy giỏ hàng (get_or_create_cart với user_id hoặc session_id).
- **Active**: Trạng thái khi giỏ hàng đang hoạt động. Từ đây:
  - Có thể thêm mục (stock--), cập nhật số lượng hoặc xóa mục (stock++).
  - Nếu xóa tất cả mục, chuyển sang Empty.
  - Nếu tiến hành thanh toán, chuyển sang CheckedOut.
- **Empty**: Trạng thái khi giỏ hàng trống. Có thể chuyển sang Active khi thêm mục đầu tiên.
- **CheckedOut**: Trạng thái sau khi thanh toán. Từ đây, có thể chuyển sang Active nếu người dùng tiếp tục mua sắm sau đặt hàng (thêm mục mới).

Lưu ý: Đường dẫn từ Empty sang CheckedOut được đánh dấu là không hợp lệ (Invalid path - prevented) và được hiển thị màu đỏ để ngăn chặn.

## 3. Trạng thái đơn hàng (Order States)

- **Building**: Trạng thái khi đơn hàng đang được xây dựng từ giỏ hàng (create_order_from_cart, sao chép mục và xóa giỏ).
- **Completed**: Trạng thái khi đơn hàng được hoàn thành (commit giao dịch, giỏ hàng được xóa). Từ đây:
  - Có thể chuyển sang PrintableReceipt khi người dùng chọn in biên lai (hành động frontend).
  - Có thể chuyển sang Archived (chưa triển khai, cho lưu trữ lâu dài trong tương lai).
- **PrintableReceipt**: Trạng thái tạm thời khi cửa sổ in biên lai được mở (hành động client-side). Sau khi đóng cửa sổ in, chuyển về Completed (không thay đổi trạng thái vĩnh viễn).

## 4. Quan hệ giữa các trạng thái

- **Auth và Cart**: Người dùng Authenticated có thể xác định user_id cho giỏ hàng liên tục. Người dùng Anonymous sử dụng session_id cho giỏ hàng khách.
- **Cart và Order**: Khi Cart chuyển sang CheckedOut, Order được tạo và chuyển sang Completed.

Biểu đồ trạng thái này giúp hiểu rõ vòng đời của các đối tượng chính trong ứng dụng, đảm bảo quản lý trạng thái nhất quán và ngăn ngừa các chuyển đổi không hợp lệ.
