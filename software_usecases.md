# Bảng Use Case Phần Mềm

Tài liệu này liệt kê các Use Case theo góc nhìn nghiệp vụ, bám sát các yêu cầu trong `software_requirements.md`.

## 1. Use Case Chung (General Use Cases)
Áp dụng cho mọi người dùng.

| Mã Use Case | Tên Use Case        | Mô tả                                                                                        | Bao gồm Yêu cầu                 | Extension Requirements                                |
|-------------|---------------------|----------------------------------------------------------------------------------------------|---------------------------------|-------------------------------------------------------|
| UC-GEN-001  | Đăng ký tài khoản   | Người dùng cung cấp email, tên và mật khẩu để tạo tài khoản mới.                             | F-CUS-001, NF-SYS-001           | Không có                                              |
| UC-GEN-002  | Đăng nhập hệ thống  | Người dùng nhập thông tin tài khoản để bắt đầu phiên đăng nhập.                              | F-CUS-002, F-SYS-001, F-SYS-002 | NF-SYS-002 (kết nối an toàn trong triển khai)         |
| UC-GEN-003  | Duy trì phiên       | Hệ thống tự động theo dõi thời gian hoạt động và kết thúc phiên sau thời gian quy định.      | F-SYS-002                       | Không có                                              |
| UC-GEN-004  | Kiểm tra tình trạng | Người dùng hoặc nền tảng có thể kiểm tra nhanh hệ thống còn hoạt động bình thường hay không. | F-SYS-008                       | NF-SYS-004 (kiểm thử trước phát hành)                 |
| UC-GEN-006  | Khởi động hệ thống  | Hệ thống khởi chạy và kích hoạt các thành phần bảo mật, phiên, cập nhật tồn kho.             | F-SYS-006                       | Không có                                              |
| UC-GEN-007  | Cấu hình dữ liệu    | Thiết lập kết nối cơ sở dữ liệu phù hợp với môi trường (mặc định dạng nhẹ, có thể nâng cấp). | F-SYS-007                       | Không có                                              |
| UC-GEN-008  | Ghi log & giám sát  | Ghi lại sự kiện quan trọng mà không phơi bày thông tin nhạy cảm.                             | NF-SYS-001, NF-SYS-002          | F-MER-006 (người bán xem log để phát hiện bất thường) |

## 2. Use Case Dành Cho Khách Hàng
Mô tả các tương tác chính của khách hàng trên giao diện.

| Mã Use Case | Tên Use Case             | Mô tả                                                                                               | Bao gồm Yêu cầu                             | Extension Requirements                  |
|-------------|--------------------------|-----------------------------------------------------------------------------------------------------|---------------------------------------------|-----------------------------------------|
| UC-CUS-001  | Xem & tìm sản phẩm       | Khách hàng xem danh sách sản phẩm, tìm kiếm, lọc và nhận cập nhật tồn kho gần thời gian thực.       | F-CUS-003, F-CUS-004, NF-SYS-006            | F-SYS-004 (kênh cập nhật tồn kho)       |
| UC-CUS-002  | Quản lý giỏ hàng         | Khách hàng đã đăng nhập có thể thêm sản phẩm, thay đổi số lượng, xóa từng sản phẩm hoặc xóa tất cả. | F-CUS-005, F-CUS-006, NF-CUS-001, F-SYS-003 | Không có                                |
| UC-CUS-003  | Kiểm tra tồn & đồng thời | Khi cập nhật giỏ, hệ thống kiểm tra tồn kho và xử lý tranh chấp khi nhiều người cùng thao tác.      | F-CUS-007, NF-MER-002                       | Không có                                |
| UC-CUS-004  | Thanh toán               | Khách hàng xác nhận mua; nếu chưa đăng nhập bị yêu cầu đăng nhập; sau đó thấy hóa đơn chi tiết.     | F-CUS-008, F-CUS-009, F-CUS-012             | NF-CUS-002 (tối ưu đa thiết bị & in ấn) |
| UC-CUS-005  | In hóa đơn               | Khách hàng in hoặc lưu hóa đơn sau khi thanh toán thành công.                                       | F-CUS-010                                   | Không có                                |
| UC-CUS-006  | Lịch sử mua hàng         | Khách hàng xem lại danh sách đơn đã mua và mở chi tiết từng hóa đơn.                                | F-CUS-011                                   | Không có                                |
| UC-CUS-007  | Đăng xuất                | Khách hàng kết thúc phiên và trở về trạng thái chưa đăng nhập.                                      | F-CUS-013                                   | Không có                                |

## 3. Use Case Dành Cho Người Bán (Merchant)
Tương tác quản lý sản phẩm và đơn hàng.

| Mã Use Case | Tên Use Case         | Mô tả                                                                                                       | Bao gồm Yêu cầu       | Extension Requirements                   |
|-------------|----------------------|-------------------------------------------------------------------------------------------------------------|-----------------------|------------------------------------------|
| UC-MER-001  | Quản lý sản phẩm     | Người bán tạo, chỉnh sửa, xóa, hoặc ẩn sản phẩm; có thể sao lưu thông tin.                                  | F-MER-001, F-MER-005  | NF-MER-001 (kiểm tra quyền phía máy chủ) |
| UC-MER-002  | Cập nhật tồn kho     | Người bán thay đổi số lượng tồn và hệ thống gửi cập nhật cho người duyệt sản phẩm.                          | F-MER-002, NF-MER-002 | NF-SYS-007 (chịu tải kết nối đồng thời)  |
| UC-MER-003  | Xem đơn hàng         | Người bán xem toàn bộ đơn phát sinh để theo dõi hoạt động bán hàng.                                         | F-MER-003             | Không có                                 |
| UC-MER-004  | Nạp dữ liệu sản phẩm | Người bán sử dụng biểu mẫu/CSV để cập nhật nhiều sản phẩm cùng lúc mà không cần thao tác kỹ thuật phức tạp. | F-MER-004             | Không có                                 |
| UC-MER-005  | Giám sát & log       | Người bán xem log sự kiện quan trọng để phát hiện bất thường/gian lận.                                      | F-MER-006             | Không có                                 |

## 4. Ghi Chú
- ID yêu cầu trong cột "Bao gồm Yêu cầu" phản ánh nguồn gốc chức năng hoặc ràng buộc chất lượng.
- Extension Requirements thể hiện yêu cầu bổ trợ hoặc mở rộng ngoài luồng chính.
- Khi có thay đổi nghiệp vụ, cập nhật trước bảng yêu cầu rồi đồng bộ lại use case.
