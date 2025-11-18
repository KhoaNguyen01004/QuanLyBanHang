# Bảng Truy Vết (Traceability Matrix)

Tài liệu này liên kết các Yêu Cầu (Requirements) với các Use Case để đảm bảo đầy đủ phạm vi và dễ kiểm tra bao phủ.

## 1. Hướng dẫn đọc
- "Use Case Chính" (Primary): Use Case thể hiện trực tiếp luồng chính đáp ứng yêu cầu.
- "Use Case Extension": Use Case dùng yêu cầu ở dạng bổ trợ/phụ (ví dụ: cập nhật tồn kho thời gian thực, yêu cầu hiệu năng).
- Mỗi yêu cầu nên có tối thiểu một Use Case Chính. Nếu có từ hai trở lên, xem xét trùng lặp hoặc khả năng gộp.

## 2. Truy vết Yêu Cầu Chức Năng Khách Hàng
| Requirement | Mô tả rút gọn                                 | Use Case Chính | Use Case Extension          |
|-------------|-----------------------------------------------|----------------|-----------------------------|
| F-CUS-001   | Đăng ký tài khoản                             | UC-GEN-001     | -                           |
| F-CUS-002   | Đăng nhập                                     | UC-GEN-002     | -                           |
| F-CUS-003   | Hiển thị sản phẩm + trạng thái đăng nhập      | UC-CUS-001     | -                           |
| F-CUS-004   | Tìm kiếm & lọc sản phẩm                       | UC-CUS-001     | -                           |
| F-CUS-005   | Thêm / sửa số lượng / xóa từng sản phẩm (giỏ) | UC-CUS-002     | -                           |
| F-CUS-006   | Xóa tất cả sản phẩm trong giỏ                 | UC-CUS-002     | -                           |
| F-CUS-007   | Kiểm tra tồn kho & xử lý đồng thời            | UC-CUS-003     | -                           |
| F-CUS-008   | Kiểm tra đăng nhập trước thanh toán           | UC-CUS-004     | -                           |
| F-CUS-009   | Hiển thị hóa đơn chi tiết sau thanh toán      | UC-CUS-004     | UC-CUS-005 (in)             |
| F-CUS-010   | In / lưu hóa đơn                              | UC-CUS-005     | UC-CUS-004 (sau thanh toán) |
| F-CUS-011   | Xem lịch sử mua                               | UC-CUS-006     | -                           |
| F-CUS-012   | Tiếp tục mua sắm sau thanh toán               | UC-CUS-004     | -                           |
| F-CUS-013   | Đăng xuất                                     | UC-CUS-007     | -                           |

## 3. Truy vết Yêu Cầu Chức Năng Người Bán (Merchant)
| Requirement | Mô tả rút gọn                      | Use Case Chính | Use Case Extension        |
|-------------|------------------------------------|----------------|---------------------------|
| F-MER-001   | Tạo/chỉnh sửa/xóa/sao lưu sản phẩm | UC-MER-001     | -                         |
| F-MER-002   | Cập nhật tồn kho                   | UC-MER-002     | UC-CUS-001 (hiển thị tồn) |
| F-MER-003   | Xem danh sách đơn hàng             | UC-MER-003     | -                         |
| F-MER-004   | Cập nhật hàng loạt (CSV/Excel)     | UC-MER-004     | -                         |
| F-MER-005   | Ẩn sản phẩm                        | UC-MER-001     | -                         |
| F-MER-006   | Xem log sự kiện                    | UC-MER-005     | UC-GEN-007                |

## 4. Truy vết Yêu Cầu Chức Năng Hệ Thống
| Requirement | Mô tả rút gọn                            | Use Case Chính | Use Case Extension     |
|-------------|------------------------------------------|----------------|------------------------|
| F-SYS-001   | Phiên đăng nhập / token                  | UC-GEN-002     | -                      |
| F-SYS-002   | Tự động kết thúc phiên                   | UC-GEN-003     | -                      |
| F-SYS-003   | Giỏ chỉ dành cho người đã đăng nhập      | UC-CUS-002     | UC-CUS-003 (gián tiếp) |
| F-SYS-004   | Kênh cập nhật tồn kho gần thời gian thực | UC-CUS-001     | UC-MER-002             |
| F-SYS-006   | Khởi động thành phần hệ thống            | UC-GEN-005     | -                      |
| F-SYS-007   | Cấu hình kết nối CSDL linh hoạt          | UC-GEN-006     | UC-MER-002 (chịu tải)  |
| F-SYS-008   | Kiểm tra tình trạng hoạt động            | UC-GEN-004     | -                      |

## 5. Truy vết Yêu Cầu Phi Chức Năng Khách Hàng & Người Bán
| Requirement | Mô tả rút gọn                              | Use Case Chính | Use Case Extension     |
|-------------|--------------------------------------------|----------------|------------------------|
| NF-CUS-001  | Phản hồi giỏ nhanh (<500ms)                | UC-CUS-002     | UC-CUS-003             |
| NF-CUS-002  | Giao diện thanh toán & hóa đơn đa thiết bị | UC-CUS-004     | UC-CUS-005             |
| NF-MER-001  | Kiểm tra quyền phía máy chủ                | UC-MER-001     | UC-MER-002, UC-MER-005 |
| NF-MER-002  | Nhất quán tồn kho dưới tải đồng thời       | UC-MER-002     | UC-CUS-003             |

## 6. Truy vết Yêu Cầu Phi Chức Năng Hệ Thống
| Requirement | Mô tả rút gọn                                 | Use Case Chính | Use Case Extension |
|-------------|-----------------------------------------------|----------------|--------------------|
| NF-SYS-001  | Mật khẩu hash & không lộ trên log             | UC-GEN-001     | UC-GEN-007         |
| NF-SYS-002  | Kết nối an toàn cho thao tác nhạy cảm         | UC-GEN-002     | UC-GEN-007         |
| NF-SYS-004  | Kiểm thử tự động trước phát hành              | UC-GEN-004     | -                  |
| NF-SYS-006  | Hiển thị 100 SP nhanh (<1.5s)                 | UC-CUS-001     | -                  |
| NF-SYS-007  | Cập nhật tồn thời gian thực chịu >500 kết nối | UC-MER-002     | UC-CUS-001         |

## 7. Truy vết Use Case → Yêu Cầu (Danh sách ngược)
| Use Case   | Yêu cầu chính (Functional)       | Yêu cầu phụ / phi chức năng |
|------------|----------------------------------|-----------------------------|
| UC-GEN-001 | F-CUS-001                        | NF-SYS-001                  |
| UC-GEN-002 | F-CUS-002, F-SYS-001, F-SYS-002  | NF-SYS-002                  |
| UC-GEN-003 | F-SYS-002                        | -                           |
| UC-GEN-004 | F-SYS-008                        | NF-SYS-004                  |
| UC-GEN-005 | F-SYS-006                        | -                           |
| UC-GEN-006 | F-SYS-007                        | -                           |
| UC-GEN-007 | (ghi log) NF-SYS-001, NF-SYS-002 | F-MER-006                   |
| UC-CUS-001 | F-CUS-003, F-CUS-004             | F-SYS-004, NF-SYS-006       |
| UC-CUS-002 | F-CUS-005, F-CUS-006             | NF-CUS-001, F-SYS-003       |
| UC-CUS-003 | F-CUS-007                        | NF-MER-002                  |
| UC-CUS-004 | F-CUS-008, F-CUS-009, F-CUS-012  | NF-CUS-002                  |
| UC-CUS-005 | F-CUS-010                        | NF-CUS-002 (in ấn)          |
| UC-CUS-006 | F-CUS-011                        | -                           |
| UC-CUS-007 | F-CUS-013                        | -                           |
| UC-MER-001 | F-MER-001, F-MER-005             | NF-MER-001                  |
| UC-MER-002 | F-MER-002                        | NF-MER-002, NF-SYS-007      |
| UC-MER-003 | F-MER-003                        | -                           |
| UC-MER-004 | F-MER-004                        | -                           |
| UC-MER-005 | F-MER-006                        | -                           |

## 8. Đánh giá Bao Phủ & Ghi chú
- Mọi yêu cầu chức năng đều có ít nhất một Use Case Chính; không có yêu cầu bị bỏ trống.
- Một số yêu cầu phi chức năng lặp lại ở nhiều Use Case (NF-SYS-001, NF-SYS-002) — chấp nhận được vì phạm vi toàn hệ thống.
- F-SYS-004 (kênh cập nhật tồn kho) xuất hiện chủ yếu như extension (UC-CUS-001) vì nó hỗ trợ hiển thị; cân nhắc một Use Case kỹ thuật riêng nếu cần chi tiết triển khai sau.
- Không phát hiện xung đột nội dung giữa yêu cầu và use case sau lần chuẩn hóa gần nhất.

## 9. Khuyến nghị Tiếp Theo
1. Gắn mã yêu cầu vào kịch bản kiểm thử tự động (test IDs) để đảm bảo truy vết đủ vòng.
2. Đánh dấu yêu cầu có nhiều hơn 2 Use Case liên quan để xem có cần giảm trùng lặp mô tả.
3. Khi thêm tính năng mới (ví dụ phương thức thanh toán): cập nhật cả hai chiều bảng truy vết.
4. Xem xét bổ sung Use Case vận hành (Operational) nếu sau này cần mô tả quy trình giám sát hoặc xử lý lỗi import.

---
Generated: (tự động) dựa trên phiên bản hiện tại của `software_requirements.md` và `software_usecases.md`.

