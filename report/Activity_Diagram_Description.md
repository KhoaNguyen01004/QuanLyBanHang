# Mô tả biểu đồ hoạt động (Activity Diagrams) cho ứng dụng QuanLyBanHang

## 1. Biểu đồ hoạt động mua hàng (Purchase Activity Diagram)

Biểu đồ hoạt động mua hàng mô tả quy trình mua sắm của khách hàng trong ứng dụng bán hàng trực tuyến, được chia thành các mục dựa trên các hoạt động chính.

### 1.1 Truy cập trang chủ và duyệt sản phẩm
- Quy trình bắt đầu khi khách hàng truy cập trang chủ của ứng dụng.
- Khách hàng duyệt các sản phẩm có sẵn trên trang chủ.

### 1.2 Chọn sản phẩm
- Khách hàng chọn một sản phẩm cụ thể từ danh sách sản phẩm được hiển thị.

### 1.3 Thêm sản phẩm vào giỏ hàng hoặc tiếp tục duyệt
- Nếu khách hàng quyết định thêm sản phẩm vào giỏ hàng, hệ thống cập nhật giỏ hàng với sản phẩm đã chọn.
- Nếu không, khách hàng tiếp tục duyệt sản phẩm và quay lại bước duyệt sản phẩm.

### 1.4 Xem giỏ hàng
- Sau khi thêm sản phẩm hoặc tiếp tục duyệt, khách hàng xem nội dung giỏ hàng để kiểm tra các mục đã chọn.

### 1.5 Tiến hành thanh toán hoặc tiếp tục mua sắm
- Nếu khách hàng chọn tiếp tục thanh toán, quy trình chuyển sang nhập thông tin giao hàng và thanh toán.
- Nếu không, khách hàng tiếp tục mua sắm và quay lại duyệt sản phẩm.

### 1.6 Nhập thông tin giao hàng và thanh toán
- Khách hàng nhập các thông tin cần thiết cho giao hàng và thanh toán.

### 1.7 Xác nhận thanh toán
- Hệ thống xử lý và xác nhận thông tin thanh toán từ khách hàng.

### 1.8 Thanh toán thành công: Tạo đơn hàng và gửi xác nhận
- Nếu thanh toán thành công, hệ thống tạo đơn hàng mới, gửi email xác nhận và hiển thị hóa đơn cho khách hàng.
- Quy trình kết thúc tại đây với việc hiển thị hóa đơn.

### 1.9 Thanh toán thất bại: Thông báo lỗi và thử lại
- Nếu thanh toán thất bại, hệ thống thông báo lỗi thanh toán.
- Khách hàng có thể thử lại thanh toán hoặc chỉnh sửa giỏ hàng, sau đó quay lại xem giỏ hàng.

### 1.10 Kết thúc quy trình
- Quy trình mua hàng kết thúc khi khách hàng nhận được hóa đơn hoặc quyết định tiếp tục mua sắm mà không thanh toán.

Biểu đồ này nhấn mạnh các điểm quyết định quan trọng như việc thêm sản phẩm, xem giỏ hàng và xác nhận thanh toán, đảm bảo trải nghiệm mua sắm liền mạch và an toàn.

## 2. Biểu đồ hoạt động ứng dụng cửa hàng (Shop Application - User Activity Flow)

Biểu đồ hoạt động chi tiết hơn mô tả luồng hoạt động của người dùng trong ứng dụng cửa hàng, bao gồm cả người dùng đã đăng nhập và chưa đăng nhập, được chia thành các mục dựa trên các hoạt động chính.

### 2.1 Truy cập trang chủ và tải sản phẩm
- Quy trình bắt đầu khi người dùng truy cập trang chủ.
- Hệ thống tải danh sách sản phẩm từ cơ sở dữ liệu hoặc API.
- Middleware theo dõi hoạt động cuối cùng; nếu không hoạt động >1 giờ, phiên bị xóa và chuyển hướng về trang chủ.

### 2.2 Xử lý đăng nhập
- Nếu người dùng đã đăng nhập, tải tên người dùng và email từ phiên.
- Nếu chưa đăng nhập, mở trang đăng nhập.
  - Nếu thông tin hợp lệ, tạo phiên và chuyển hướng về trang chủ.
  - Nếu không, hiển thị lỗi và yêu cầu đăng nhập lại.

### 2.3 Duyệt và lọc sản phẩm (vòng lặp mua sắm)
- Người dùng duyệt và lọc sản phẩm.

### 2.4 Thêm sản phẩm vào giỏ hàng
- Nếu chọn thêm sản phẩm, hệ thống đảm bảo có giỏ hàng (dựa trên user_id hoặc session_id), kiểm tra tồn kho.
  - Nếu đủ hàng, giảm tồn kho, thêm vào giỏ và phát sóng cập nhật qua WebSocket.
  - Nếu hết hàng, hiển thị thông báo hết hàng.

### 2.5 Xem và chỉnh sửa giỏ hàng
- Nếu xem giỏ hàng:
  - Nếu giỏ trống, hiển thị giỏ trống.
  - Nếu không, hiển thị mục với số lượng.
  - Người dùng có thể cập nhật số lượng: xóa (tăng tồn kho), thêm (giảm tồn kho), hoặc đặt về 0 (xóa mục).

### 2.6 Tiến hành thanh toán
- Nếu chọn thanh toán:
  - Nếu đã xác thực, tạo đơn hàng từ giỏ (sao chép mục và xóa giỏ), hiển thị xác nhận và biên lai.
    - Có thể in biên lai (mở cửa sổ in client) hoặc xem đơn hàng cũ.
    - Sau mua, có thể tiếp tục mua sắm hoặc ở lại xác nhận.
  - Nếu chưa xác thực, chuyển hướng đến đăng nhập.

### 2.7 Kết thúc vòng lặp mua sắm
- Khi không tiếp tục mua sắm, người dùng ở trạng thái rảnh (giữ phiên).

### 2.8 Đăng xuất hoặc quay về trang chủ
- Nếu đăng xuất, xóa phiên và chuyển hướng về trang chủ.
- Nếu không, quay về trang chủ hoặc hoạt động mới.

Biểu đồ này bao gồm các khía cạnh kỹ thuật như xử lý phiên, cập nhật thời gian thực qua WebSocket và quản lý trạng thái giỏ hàng, phản ánh luồng hoạt động toàn diện của ứng dụng.

## 3. Biểu đồ trạng thái (State Diagram)

Biểu đồ trạng thái mô tả các trạng thái chính và chuyển đổi giữa chúng trong ứng dụng QuanLyBanHang, tập trung vào các miền cốt lõi như xác thực (Auth), giỏ hàng (Cart) và đơn hàng (Order). Biểu đồ được chia thành các mục dựa trên các trạng thái và chuyển đổi chính.

### 3.1 Trạng thái xác thực (Auth States)

- **Anonymous**: Trạng thái ban đầu cho người dùng chưa đăng nhập. Từ đây, người dùng có thể chuyển sang Authenticated thông qua đăng nhập thành công (sử dụng API /api/users/login hoặc /api/users/token).
- **Authenticated**: Trạng thái khi người dùng đã đăng nhập thành công. Từ đây, người dùng có thể chuyển về Anonymous thông qua đăng xuất (/logout) hoặc hết thời gian phiên (>1 giờ không hoạt động).

### 3.2 Trạng thái giỏ hàng (Cart States)

- **NonExistent**: Trạng thái ban đầu khi chưa có giỏ hàng. Chuyển sang Active khi tạo hoặc lấy giỏ hàng (get_or_create_cart với user_id hoặc session_id).
- **Active**: Trạng thái khi giỏ hàng đang hoạt động. Từ đây:
  - Có thể thêm mục (stock--), cập nhật số lượng hoặc xóa mục (stock++).
  - Nếu xóa tất cả mục, chuyển sang Empty.
  - Nếu tiến hành thanh toán, chuyển sang CheckedOut.
- **Empty**: Trạng thái khi giỏ hàng trống. Có thể chuyển sang Active khi thêm mục đầu tiên.
- **CheckedOut**: Trạng thái sau khi thanh toán. Từ đây, có thể chuyển sang Active nếu người dùng tiếp tục mua sắm sau đặt hàng (thêm mục mới).

### 3.3 Trạng thái đơn hàng (Order States)

- **Building**: Trạng thái khi đơn hàng đang được xây dựng từ giỏ hàng (create_order_from_cart, sao chép mục và xóa giỏ).
- **Completed**: Trạng thái khi đơn hàng được hoàn thành (commit giao dịch, giỏ hàng được xóa). Từ đây:
  - Có thể chuyển sang PrintableReceipt khi người dùng chọn in biên lai (hành động frontend).
  - Có thể chuyển sang Archived (chưa triển khai, cho lưu trữ lâu dài trong tương lai).
- **PrintableReceipt**: Trạng thái tạm thời khi cửa sổ in biên lai được mở (hành động client-side). Sau khi đóng cửa sổ in, chuyển về Completed (không thay đổi trạng thái vĩnh viễn).

### 3.4 Quan hệ giữa các trạng thái

- **Auth và Cart**: Người dùng Authenticated có thể xác định user_id cho giỏ hàng liên tục. Người dùng Anonymous sử dụng session_id cho giỏ hàng khách.
- **Cart và Order**: Khi Cart chuyển sang CheckedOut, Order được tạo và chuyển sang Completed.

Biểu đồ trạng thái này giúp hiểu rõ vòng đời của các đối tượng chính trong ứng dụng, đảm bảo quản lý trạng thái nhất quán và ngăn ngừa các chuyển đổi không hợp lệ.
