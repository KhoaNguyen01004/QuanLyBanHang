# Bảng Use Case Chi Tiết

Tài liệu này liệt kê chi tiết cho từng Use Case, mở rộng từ `software_usecases.md`.

## Khối Khách hàng

### UC-CUS-001 – Đăng ký tài khoản
| Trường                    | Thông tin |
|---------------------------|-----------|
| Use case ID               | UC-CUS-001 |
| Tên use case              | Đăng ký tài khoản |
| Tác nhân chính            | Khách hàng |
| Mô tả                     | Người dùng tạo mới tài khoản để sử dụng các chức năng cá nhân hóa. |
| Tiền điều kiện           | Chưa đăng nhập; có email chưa được đăng ký; có kết nối ổn định. |
| Hậu điều kiện             | Hồ sơ người dùng mới được lưu thành công và người dùng có thể đăng nhập. |
| Luồng chính               | 1. Khách hàng mở form đăng ký.<br>2. Nhập email, tên, mật khẩu.<br>3. Hệ thống kiểm tra định dạng, trùng email.<br>4. Hệ thống hash mật khẩu, lưu vào D1.<br>5. Trả thông báo thành công. |
| Luồng phụ / Ngoại lệ      | A1: Email đã tồn tại → trả lỗi “Email đã đăng ký”.<br>A2: Mật khẩu chưa đạt yêu cầu → yêu cầu nhập lại.<br>A3: Lỗi hệ thống khi lưu → trả thông báo và hướng dẫn thử lại. |
| Yêu cầu liên quan         | F-CUS-001; NF-SYS-001 |

### UC-CUS-002 – Đăng nhập
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-CUS-002 |
| Tên use case | Đăng nhập |
| Tác nhân chính | Khách hàng |
| Mô tả | Thiết lập phiên làm việc cho người dùng hợp lệ. |
| Tiền điều kiện | Đã có tài khoản kích hoạt; chưa đăng nhập phiên hiện tại. |
| Hậu điều kiện | Token đăng nhập cấp thành công hoặc trả lỗi rõ ràng. |
| Luồng chính | 1. Người dùng nhập email/mật khẩu.<br>2. Hệ thống tìm hồ sơ trong D1.<br>3. So khớp mật khẩu hash.<br>4. Sinh token chứa role customer.<br>5. Trả token + thời hạn phiên. |
| Luồng phụ / Ngoại lệ | A1: Sai email/mật khẩu → trả lỗi đăng nhập.<br>A2: Tài khoản bị khóa → chặn truy cập và hướng dẫn liên hệ hỗ trợ.<br>A3: Dịch vụ auth lỗi → trả mã lỗi 503. |
| Yêu cầu liên quan | F-CUS-002; F-SYS-001; F-SYS-002; NF-SYS-002 |

### UC-CUS-003 – Đăng xuất
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-CUS-003 |
| Tên use case | Đăng xuất |
| Tác nhân chính | Khách hàng |
| Mô tả | Kết thúc phiên làm việc đang hoạt động. |
| Tiền điều kiện | Đang đăng nhập; có token hợp lệ. |
| Hậu điều kiện | Token bị thu hồi, giao diện chuyển về trạng thái khách. |
| Luồng chính | 1. Người dùng bấm Đăng xuất.<br>2. Client gửi token cần revoke.<br>3. Hệ thống vô hiệu hóa token trong store.<br>4. Xóa cache thông tin giỏ cục bộ.<br>5. Trả phản hồi thành công. |
| Luồng phụ / Ngoại lệ | A1: Token hết hạn → hệ thống vẫn phản hồi thành công giả lập.<br>A2: Lỗi mạng → hiển thị cảnh báo nhưng client xóa token cục bộ. |
| Yêu cầu liên quan | F-CUS-013; F-SYS-002 |

### UC-CUS-004 – Xem & tìm sản phẩm
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-CUS-004 |
| Tên use case | Xem & tìm sản phẩm |
| Tác nhân chính | Khách hàng |
| Mô tả | Duyệt, tìm kiếm và lọc danh mục sản phẩm với tồn kho thời gian gần thực. |
| Tiền điều kiện | Hệ thống hoạt động; dữ liệu sản phẩm khả dụng. |
| Hậu điều kiện | Danh sách hiển thị theo bộ lọc, tồn kho cập nhật. |
| Luồng chính | 1. Khách hàng nhập từ khóa/bộ lọc.<br>2. Hệ thống truy vấn D2, áp dụng phân trang.<br>3. Ghép thông tin tồn kho mới nhất.<br>4. Trả danh sách và metadata. |
| Luồng phụ / Ngoại lệ | A1: Không có sản phẩm phù hợp → trả danh sách rỗng.<br>A2: Timeout truy vấn → thông báo thử lại.<br>A3: Bộ lọc không hợp lệ → trả lỗi 400 kèm hướng dẫn. |
| Yêu cầu liên quan | F-CUS-003; F-CUS-004; F-SYS-004; NF-SYS-006; NF-SYS-007 |

### UC-CUS-005 – Quản lý giỏ hàng
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-CUS-005 |
| Tên use case | Quản lý giỏ hàng |
| Tác nhân chính | Khách hàng |
| Mô tả | Thêm, xóa, thay đổi số lượng sản phẩm trong giỏ. |
| Tiền điều kiện | Đã đăng nhập; sản phẩm còn tồn kho. |
| Hậu điều kiện | Giỏ hàng cập nhật; phản hồi tồn kho rõ ràng. |
| Luồng chính | 1. Khách hàng chọn thao tác (thêm/sửa/xóa).<br>2. Hệ thống tải giỏ hiện tại từ D5/D6.<br>3. Kiểm tra tồn sản phẩm trên D2.<br>4. Ghi thay đổi vào D5/D6.<br>5. Trả ảnh chụp giỏ mới. |
| Luồng phụ / Ngoại lệ | A1: Hết tồn → trả lỗi và giữ nguyên giỏ.<br>A2: Giỏ bị khóa bởi phiên khác → yêu cầu thử lại sau.<br>A3: Sản phẩm bị ẩn → loại khỏi giỏ và thông báo. |
| Yêu cầu liên quan | F-CUS-005; F-CUS-006; F-CUS-007; F-SYS-003; NF-CUS-001; NF-CUS-003; NF-SYS-007 |

### UC-CUS-006 – Thanh toán
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-CUS-006 |
| Tên use case | Thanh toán |
| Tác nhân chính | Khách hàng |
| Mô tả | Chốt giỏ, tạo đơn và đồng bộ kết quả thanh toán. |
| Tiền điều kiện | Giỏ có sản phẩm hợp lệ; đăng nhập; phương thức thanh toán khả dụng. |
| Hậu điều kiện | Đơn hàng được tạo, trạng thái thanh toán đồng bộ. |
| Luồng chính | 1. Người dùng xác nhận checkout.<br>2. Hệ thống khóa giỏ, kiểm tồn lần cuối.<br>3. Tạo Order & Order Items (D3/D4).<br>4. Giảm tồn trên D2.<br>5. Gửi yêu cầu thanh toán, nhận phản hồi.<br>6. Trả hóa đơn + trạng thái đơn. |
| Luồng phụ / Ngoại lệ | A1: Tồn không đủ → hủy checkout, trả thông báo cập nhật.<br>A2: Thanh toán thất bại → giữ đơn trạng thái pending, hướng dẫn thử lại.<br>A3: Gateway không phản hồi → đánh dấu processing và gửi email nhắc. |
| Yêu cầu liên quan | F-CUS-008; F-CUS-008a; F-CUS-009; F-CUS-012; NF-CUS-002; NF-CUS-004 |

### UC-CUS-007 – In/Lưu hóa đơn
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-CUS-007 |
| Tên use case | In/Lưu hóa đơn |
| Tác nhân chính | Khách hàng |
| Mô tả | Xuất hóa đơn sau thanh toán thành công. |
| Tiền điều kiện | Có đơn đã thanh toán; người dùng đăng nhập. |
| Hậu điều kiện | Hóa đơn được in hoặc lưu file. |
| Luồng chính | 1. Khách hàng chọn đơn cần in.<br>2. Hệ thống lấy dữ liệu D3/D4.<br>3. Sinh file PDF/HTML.<br>4. Gửi file để in/lưu. |
| Luồng phụ / Ngoại lệ | A1: Đơn chưa thanh toán → chặn hành động.<br>A2: Lỗi tạo file → hiển thị thông báo thử lại.<br>A3: Người dùng hủy in → ghi log và kết thúc. |
| Yêu cầu liên quan | F-CUS-010; NF-CUS-002; NF-CUS-004 |

### UC-CUS-008 – Xem lịch sử mua hàng
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-CUS-008 |
| Tên use case | Xem lịch sử mua hàng |
| Tác nhân chính | Khách hàng |
| Mô tả | Xem danh sách và chi tiết các đơn đã mua. |
| Tiền điều kiện | Đăng nhập; có lịch sử mua. |
| Hậu điều kiện | Lịch sử hiển thị đầy đủ; có thể lọc và xem chi tiết. |
| Luồng chính | 1. Người dùng nhập bộ lọc (thời gian, trạng thái).<br>2. Hệ thống truy vấn D3/D4 theo user ID.<br>3. Trả danh sách đơn + tùy chọn xem chi tiết.<br>4. Khi chọn chi tiết, trả thông tin order items + hóa đơn. |
| Luồng phụ / Ngoại lệ | A1: Không có đơn → trả danh sách rỗng.<br>A2: Hệ thống quá tải → trả thông báo thử sau.<br>A3: Người dùng yêu cầu trang cao hơn giới hạn → trả lỗi phân trang. |
| Yêu cầu liên quan | F-CUS-011 |

## Khối Người bán

### UC-MER-001 – Đăng nhập người bán
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-MER-001 |
| Tên use case | Đăng nhập người bán |
| Tác nhân chính | Người bán |
| Mô tả | Xác thực tài khoản merchant và cấp quyền quản trị. |
| Tiền điều kiện | Có tài khoản merchant hợp lệ. |
| Hậu điều kiện | Phiên quản trị được tạo hoặc lỗi nêu rõ lý do. |
| Luồng chính | 1. Merchant nhập email/mật khẩu.<br>2. Hệ thống kiểm tra role merchant.<br>3. Cấp token gắn quyền quản trị.<br>4. Trả token + thông tin hết hạn. |
| Luồng phụ / Ngoại lệ | A1: Không có quyền merchant → từ chối truy cập.<br>A2: Sai thông tin → trả lỗi đăng nhập.<br>A3: Tài khoản khóa → hướng dẫn liên hệ hỗ trợ. |
| Yêu cầu liên quan | F-SYS-001; F-SYS-002; NF-SYS-002 |

### UC-MER-002 – Đăng xuất người bán
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-MER-002 |
| Tên use case | Đăng xuất người bán |
| Tác nhân chính | Người bán |
| Mô tả | Kết thúc phiên quản trị để bảo vệ dữ liệu. |
| Tiền điều kiện | Đang đăng nhập với token hợp lệ. |
| Hậu điều kiện | Token bị thu hồi, session quản trị đóng. |
| Luồng chính | 1. Merchant chọn Đăng xuất.<br>2. Token gửi lên endpoint revoke.<br>3. Hệ thống gỡ token khỏi store.<br>4. Trả phản hồi thành công. |
| Luồng phụ / Ngoại lệ | A1: Token hết hạn → phản hồi thành công giả lập.<br>A2: Lỗi backend → hiển thị cảnh báo nhưng xóa token phía client. |
| Yêu cầu liên quan | F-SYS-002 |

### UC-MER-003 – Quản lý sản phẩm
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-MER-003 |
| Tên use case | Quản lý sản phẩm |
| Tác nhân chính | Người bán |
| Mô tả | Tạo, chỉnh sửa, ẩn/xóa sản phẩm. |
| Tiền điều kiện | Đăng nhập; có quyền quản lý danh mục. |
| Hậu điều kiện | Bản ghi sản phẩm cập nhật đúng. |
| Luồng chính | 1. Merchant mở module sản phẩm.<br>2. Gửi yêu cầu CRUD (create/update/delete/hide).<br>3. Hệ thống validate dữ liệu, kiểm tra trùng SKU.<br>4. Cập nhật D2 và trả kết quả từng bản ghi. |
| Luồng phụ / Ngoại lệ | A1: Thiếu trường bắt buộc → trả lỗi 422.<br>A2: SKU trùng → yêu cầu đổi SKU.<br>A3: Lỗi ghi DB → trả lỗi và không commit. |
| Yêu cầu liên quan | F-MER-001; F-MER-005; NF-MER-001 |

### UC-MER-004 – Cập nhật tồn kho
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-MER-004 |
| Tên use case | Cập nhật tồn kho |
| Tác nhân chính | Người bán |
| Mô tả | Điều chỉnh số lượng tồn lẻ hoặc theo batch nhỏ. |
| Tiền điều kiện | Đăng nhập; sản phẩm tồn tại. |
| Hậu điều kiện | Stock mới đồng bộ tới luồng khách hàng. |
| Luồng chính | 1. Merchant chọn sản phẩm cần chỉnh tồn.<br>2. Nhập giá trị delta hoặc số lượng mới.<br>3. Hệ thống kiểm tra quyền, tính toán stock mới.<br>4. Ghi vào D2 và phát sự kiện cập nhật. |
| Luồng phụ / Ngoại lệ | A1: Stock nhập âm → từ chối và báo lỗi.<br>A2: Sản phẩm bị khóa → không cho chỉnh sửa.<br>A3: Mất kết nối → hiển thị trạng thái chưa lưu. |
| Yêu cầu liên quan | F-MER-002; NF-MER-002; NF-SYS-007 |

### UC-MER-005 – Xem đơn hàng
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-MER-005 |
| Tên use case | Xem đơn hàng |
| Tác nhân chính | Người bán |
| Mô tả | Theo dõi đơn hàng, trạng thái thanh toán/giao nhận. |
| Tiền điều kiện | Đăng nhập; có đơn phát sinh. |
| Hậu điều kiện | Merchant nắm được danh sách và trạng thái đơn. |
| Luồng chính | 1. Merchant nhập bộ lọc (thời gian, trạng thái, kênh).<br>2. Hệ thống truy vấn D3/D4 theo phạm vi merchant.<br>3. Trả danh sách đơn, cho phép xem chi tiết. |
| Luồng phụ / Ngoại lệ | A1: Không có kết quả → trả danh sách rỗng.<br>A2: Bộ lọc quá rộng → hệ thống yêu cầu thu hẹp.<br>A3: Lỗi quyền truy cập → trả lỗi 403. |
| Yêu cầu liên quan | F-MER-003 |

### UC-MER-006 – Cập nhật sản phẩm hàng loạt
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-MER-006 |
| Tên use case | Cập nhật sản phẩm hàng loạt |
| Tác nhân chính | Người bán |
| Mô tả | Upload CSV/Excel để cập nhật nhiều sản phẩm một lúc. |
| Tiền điều kiện | Đăng nhập; file đúng định dạng. |
| Hậu điều kiện | Các sản phẩm được xử lý, trả báo cáo thành công/lỗi. |
| Luồng chính | 1. Merchant tải lên file batch.<br>2. Hệ thống parse và validate từng dòng.<br>3. Áp dụng thay đổi vào D2.<br>4. Sinh báo cáo tổng hợp trả về. |
| Luồng phụ / Ngoại lệ | A1: File sai định dạng → trả lỗi và không xử lý.<br>A2: Một số dòng thất bại → đánh dấu lỗi trong báo cáo.<br>A3: Kích thước file vượt giới hạn → từ chối upload. |
| Yêu cầu liên quan | F-MER-004 |

### UC-MER-007 – Xem log & báo cáo
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-MER-007 |
| Tên use case | Xem log & báo cáo |
| Tác nhân chính | Người bán |
| Mô tả | Xem log đăng nhập, thanh toán và báo cáo bán hàng. |
| Tiền điều kiện | Đăng nhập; có quyền xem log. |
| Hậu điều kiện | Log/báo cáo hiển thị hoặc tải xuống thành công. |
| Luồng chính | 1. Merchant chọn loại log/báo cáo.<br>2. Hệ thống truy vấn nguồn log runtime (P8).<br>3. Trả dữ liệu realtime hoặc file tổng hợp. |
| Luồng phụ / Ngoại lệ | A1: Thiếu quyền → trả lỗi 403.<br>A2: Log quá lớn → áp dụng phân trang/streaming.<br>A3: Kênh log tạm ngưng → thông báo trạng thái. |
| Yêu cầu liên quan | F-MER-006; NF-SYS-001; NF-SYS-002 |

## Khối Monitor

### UC-MON-001 – Giám sát giao dịch
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-MON-001 |
| Tên use case | Giám sát giao dịch |
| Tác nhân chính | Monitor |
| Mô tả | Theo dõi log giao dịch và metric gần thời gian thực. |
| Tiền điều kiện | Quyền monitor hợp lệ; endpoint P8 online. |
| Hậu điều kiện | Dashboard cập nhật trạng thái, metric realtime. |
| Luồng chính | 1. Monitor gửi ping/subscribe metric.<br>2. P8 stream health snapshot + metric.<br>3. Monitor hiển thị dashboard, đánh dấu bất thường. |
| Luồng phụ / Ngoại lệ | A1: Mất kết nối → hiển thị cảnh báo “stale data”.<br>A2: Metric vượt ngưỡng → chuyển sang UC-MON-002 (nhận cảnh báo). |
| Yêu cầu liên quan | NF-SYS-001; NF-SYS-002; NF-SYS-005 |

### UC-MON-002 – Nhận cảnh báo bất thường
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-MON-002 |
| Tên use case | Nhận cảnh báo bất thường |
| Tác nhân chính | Monitor |
| Mô tả | Nhận, xác nhận và xử lý cảnh báo sự cố. |
| Tiền điều kiện | Rule cảnh báo đã cấu hình; monitor đăng nhập. |
| Hậu điều kiện | Cảnh báo được ACK và ghi nhận trạng thái xử lý. |
| Luồng chính | 1. P8 phát cảnh báo với ID và chi tiết.<br>2. Monitor nhận thông báo qua dashboard/kênh tích hợp.<br>3. Monitor ACK hoặc gán người xử lý.<br>4. P8 ghi nhận phản hồi, cập nhật trạng thái cảnh báo. |
| Luồng phụ / Ngoại lệ | A1: Monitor không phản hồi → escalated cho on-call.<br>A2: False positive → đánh dấu và đóng cảnh báo.<br>A3: Kênh thông báo lỗi → fallback sang email/SMS. |
| Yêu cầu liên quan | NF-SYS-001; NF-SYS-003 |

### UC-MON-003 – Xuất báo cáo vận hành
| Trường | Thông tin |
|--------|-----------|
| Use case ID | UC-MON-003 |
| Tên use case | Xuất báo cáo vận hành |
| Tác nhân chính | Monitor |
| Mô tả | Tạo báo cáo log/thanh toán theo kỳ để phục vụ kiểm toán. |
| Tiền điều kiện | Có quyền truy cập dữ liệu; xác định kỳ báo cáo hợp lệ. |
| Hậu điều kiện | Báo cáo tải về thành công với checksum/chữ ký số. |
| Luồng chính | 1. Monitor nhập kỳ, định dạng (PDF/CSV).<br>2. P8 gom dữ liệu liên quan, sinh báo cáo.<br>3. Đính kèm checksum/chữ ký số.<br>4. Trả file cho monitor tải xuống. |
| Luồng phụ / Ngoại lệ | A1: Kỳ yêu cầu quá lớn → hệ thống đề nghị chia nhỏ.<br>A2: Chữ ký số lỗi → regenerating và thông báo.<br>A3: Monitor hủy yêu cầu → dừng xử lý và log sự kiện. |
| Yêu cầu liên quan | NF-SYS-002; NF-SYS-004; NF-SYS-006 |

---
Tài liệu này cần được cập nhật song song khi bảng use case gốc hoặc các yêu cầu thay đổi.

