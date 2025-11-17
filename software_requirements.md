# Bảng Yêu Cầu Phần Mềm

## 1. Phạm vi & nguồn tham chiếu
Tài liệu này mô tả các yêu cầu chức năng và phi chức năng ở góc nhìn nghiệp vụ cho một ứng dụng bán hàng trực tuyến.

## 2. Yêu cầu theo phân hệ/ngữ cảnh

### 2.1 Các chức năng dành cho vai trò **Khách hàng**
| ID         | Mô tả yêu cầu                                                                                                                                    | Loại           |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| F-CUS-001  | Khách hàng có thể đăng ký tài khoản mới với email, tên người dùng và mật khẩu hợp lệ.                                                            | Functional     |
| F-CUS-002  | Khách hàng có thể đăng nhập bằng thông tin đã đăng ký và nhận thông báo rõ ràng nếu sai thông tin.                                               | Functional     |
| F-CUS-003  | Trang chủ hiển thị danh sách sản phẩm cùng trạng thái đăng nhập hiện tại của khách hàng.                                                         | Functional     |
| F-CUS-004  | Khách hàng có thể tìm kiếm và lọc sản phẩm; thông tin tồn kho được cập nhật gần thời gian thực.                                                  | Functional     |
| F-CUS-005  | Chỉ khách hàng đã đăng nhập mới được phép thêm sản phẩm vào giỏ; nếu chưa đăng nhập hệ thống báo lỗi và hiển thị thông báo yêu cầu đăng nhập.    | Functional     |
| F-CUS-005b | Giỏ hàng có nút "Xóa tất cả" để xoá toàn bộ sản phẩm trong một thao tác, phản hồi thành công/thất bại rõ ràng.                                   | Functional     |
| F-CUS-006  | Khách hàng có thể thay đổi số lượng từng sản phẩm hoặc xóa từng sản phẩm khỏi giỏ; nếu giỏ rỗng hiển thị thông báo phù hợp.                      | Functional     |
| F-CUS-007  | Khi thêm hoặc cập nhật giỏ, hệ thống kiểm tra tồn kho và từ chối nếu không đủ hàng.                                                              | Functional     |
| F-CUS-007b | Khi nhiều khách hàng cùng thêm một sản phẩm gần như đồng thời, hệ thống xử lý tranh chấp: chỉ chấp nhận cho đến khi hết hàng, đảm bảo nhất quán. | Functional     |
| F-CUS-008  | Khi tiến hành thanh toán, hệ thống kiểm tra trạng thái đăng nhập; nếu chưa đăng nhập sẽ chuyển hướng tới bước đăng nhập.                         | Functional     |
| F-CUS-009  | Sau thanh toán thành công, khách hàng nhìn thấy hóa đơn chi tiết gồm các mục, giá, thuế và tổng cộng.                                            | Functional     |
| F-CUS-010  | Khách hàng có thể in hoặc lưu hóa đơn dưới dạng PDF qua nút "In hóa đơn".                                                                        | Functional     |
| F-CUS-011  | Khách hàng xem lại lịch sử mua hàng và mở lại chi tiết hóa đơn của từng đơn.                                                                     | Functional     |
| F-CUS-012  | Sau khi thanh toán, khách hàng có thể tiếp tục mua sắm hoặc ở lại trang xác nhận.                                                                | Functional     |
| F-CUS-013  | Khách hàng có thể đăng xuất để kết thúc phiên đăng nhập.                                                                                         | Functional     |
| NF-CUS-001 | Các thao tác giỏ (thêm, sửa, xóa) phản hồi trong thời gian ngắn (< 500ms) để đảm bảo trải nghiệm mượt.                                           | Non-functional |
| NF-CUS-002 | Trang thanh toán và hóa đơn tối ưu cho cả màn hình máy tính và thiết bị di động, bố cục phù hợp chuẩn in A4.                                     | Non-functional |

### 2.2 Các chức năng dành cho vai trò **Người bán (Merchant)**
| ID         | Mô tả yêu cầu                                                                                                                                                         | Loại           |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| F-MER-001  | Người bán có thể tạo mới, chỉnh sửa, xóa hoặc sao lưu thông tin sản phẩm.                                                                                             | Functional     |
| F-MER-002  | Người bán cập nhật số lượng tồn kho và các thay đổi sẽ được thông báo tới người xem sản phẩm.                                                                         | Functional     |
| F-MER-003  | Người bán có thể xem danh sách toàn bộ đơn hàng đã phát sinh trong hệ thống.                                                                                          | Functional     |
| F-MER-004  | Người bán có thể cập nhật nhiều sản phẩm cùng lúc thông qua phương thức đơn giản như tải lên tệp CSV/Excel hoặc biểu mẫu hàng loạt, không cần can thiệp kỹ thuật sâu. | Functional     |
| F-MER-005  | Người bán có thể ẩn (vô hiệu hóa tạm thời) sản phẩm; sản phẩm ẩn sẽ không xuất hiện trong danh sách công khai.                                                        | Functional     |
| F-MER-006  | Người bán có thể xem log sự kiện quan trọng (đăng nhập, thanh toán) để kiểm tra dấu hiệu bất thường hoặc gian lận.                                                    | Functional     |
| NF-MER-001 | Các thao tác quản lý sản phẩm và đơn hàng phải được kiểm tra quyền trên máy chủ, không phụ thuộc kiểm tra phía trình duyệt.                                           | Non-functional |
| NF-MER-002 | Việc thay đổi tồn kho phải đảm bảo nhất quán dưới tải đồng thời.                                                                                                      | Non-functional |

### 2.3 Các yêu cầu chức năng chung của **Hệ thống**
| ID        | Mô tả yêu cầu                                                                                                           | Loại       |
|-----------|-------------------------------------------------------------------------------------------------------------------------|------------|
| F-SYS-001 | Hệ thống hỗ trợ phiên đăng nhập cho giao diện web và cung cấp token truy cập cho tích hợp hoặc ứng dụng khác (nếu cần). | Functional |
| F-SYS-002 | Hệ thống tự động kết thúc phiên làm việc của người dùng sau 60 phút không hoạt động và đưa về trang chính.              | Functional |
| F-SYS-003 | Không duy trì giỏ hàng cho người chưa đăng nhập; chỉ người dùng đăng nhập mới có quyền thêm sản phẩm vào giỏ.           | Functional |
| F-SYS-004 | Hệ thống cung cấp kênh cập nhật tồn kho theo thời gian gần thực (ví dụ cơ chế đẩy thời gian thực) cho người dùng.       | Functional |
| F-SYS-006 | Có cơ chế khởi động tiêu chuẩn đảm bảo toàn bộ thành phần (bảo mật, phiên, cập nhật tồn kho) được kích hoạt khi chạy.   | Functional |
| F-SYS-007 | Hệ thống có thể cấu hình kết nối cơ sở dữ liệu linh hoạt (mặc định dùng dạng nhẹ; có thể chuyển sang dịch vụ khác).     | Functional |
| F-SYS-008 | Cung cấp phương thức kiểm tra tình trạng hoạt động để nền tảng triển khai giám sát sức khỏe hệ thống.                   | Functional |

### 2.4 Các yêu cầu **phi chức năng** chung
| ID         | Mô tả yêu cầu                                                                                                   | Loại           |
|------------|-----------------------------------------------------------------------------------------------------------------|----------------|
| NF-SYS-001 | Mật khẩu phải được lưu dưới dạng hashed và không xuất hiện ở bất kỳ log nào.                                    | Non-functional |
| NF-SYS-002 | Các thao tác nhạy cảm (đăng nhập, thanh toán) phải đi qua kết nối an toàn trong môi trường triển khai thực tế.  | Non-functional |
| NF-SYS-004 | Quy trình phát hành phải chạy bộ kiểm thử tự động trước khi đưa bản cập nhật lên môi trường chính.              | Non-functional |
| NF-SYS-006 | Trang chủ hiển thị 100 sản phẩm trong thời gian ngắn (< 1.5 giây) trên môi trường tài nguyên hạn chế.           | Non-functional |
| NF-SYS-007 | Cơ chế cập nhật thời gian thực phải chịu được ít nhất 500 kết nối đồng thời mà vẫn giữ ổn định việc thanh toán. | Non-functional |

## 3. Ghi chú truy vết & mở rộng
- Các ID ở trên có thể được dùng để truy vết giữa yêu cầu ↔ thiết kế ↔ kiểm thử.
- Khi thêm tính năng mới (ví dụ phương thức thanh toán, vai trò mới), hãy tạo nhóm ID mới theo cấu trúc tương tự và cập nhật bảng này.
