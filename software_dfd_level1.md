# DFD Mức 1 – Phân Rã Tiến Trình “Ứng Dụng Bán Hàng”

DFD Mức 1 phải dựa trên (cân bằng với) DFD Mức 0. Nghĩa là mọi luồng dữ liệu đi vào/ra tiến trình tổng “Ứng Dụng Bán Hàng” ở Level 0 phải xuất hiện được phân bổ trong các tiến trình con ở Level 1. Việc bạn thấy “thiếu tiến trình” là do sơ đồ trước chỉ bao quát chức năng lõi. Dưới đây là phiên bản mở rộng chi tiết hơn.

## Tiến trình (Level 1) mở rộng
1.0 Quản Lý Khách Hàng: Đăng ký, cập nhật hồ sơ, quản lý phân hạng.
2.0 Quản Lý Sản Phẩm: Duy trì thông tin sản phẩm, giá, trạng thái kinh doanh.
3.0 Quản Lý Đơn Hàng: Tạo, xác nhận, theo dõi trạng thái đơn, liên kết khách hàng & khuyến mãi.
4.0 Quản Lý Tồn Kho: Điều chỉnh tồn, ghi nhận nhập từ nhà cung cấp, cung cấp số lượng khả dụng cho đặt hàng.
5.0 Xử Lý Thanh Toán: Khởi tạo giao dịch, truyền chi tiết tới cổng, nhận phản hồi, lưu kết quả.
6.0 Quản Lý Vận Chuyển: Tạo yêu cầu giao, liên kết đối tác vận chuyển, theo dõi lộ trình, trạng thái.
7.0 Quản Lý Trả Hàng & Bảo Hành: Tiếp nhận yêu cầu, thẩm định, cập nhật kết quả và điều chỉnh tồn kho nếu hoàn nhập.
8.0 Quản Lý Khuyến Mãi: Tạo/chỉnh sửa chiến dịch, mã giảm giá, điều kiện áp dụng.
9.0 Báo Cáo & Phân Tích: Tổng hợp đa chiều (bán hàng, tồn kho, khách hàng, vận chuyển, trả hàng, khuyến mãi, thanh toán).

## Thực thể ngoài
- Khách Hàng: Đặt đơn, cập nhật thông tin, yêu cầu trả hàng.
- Nhân Viên Bán Hàng: Quản trị nghiệp vụ, nhập điều chỉnh tồn, xem báo cáo.
- Nhà Cung Cấp: Cung ứng sản phẩm (phiếu nhập).
- Cổng Thanh Toán: Xử lý giao dịch tài chính.
- Đối Tác Vận Chuyển: Thực hiện giao hàng, phản hồi trạng thái.

## Kho dữ liệu
- D1 Khách Hàng: Hồ sơ, phân hạng.
- D2 Sản Phẩm: Thông tin, giá, thuộc tính.
- D3 Đơn Hàng: Header, dòng đơn, trạng thái.
- D4 Thanh Toán: Giao dịch, kết quả, phương thức.
- D5 Vận Chuyển: Vận đơn, lộ trình, trạng thái.
- D6 Trả Hàng: Yêu cầu, lý do, kết quả xử lý.
- D7 Khuyến Mãi: Chiến dịch, mã, điều kiện.

## Dòng dữ liệu tiêu biểu (rút gọn)
- Khách Hàng → 3.0: Yêu cầu đặt hàng
- 3.0 → Khách Hàng: Xác nhận / Trạng thái
- Khách Hàng ↔ 1.0: Đăng ký / Cập nhật / Tra cứu
- 3.0 → 5.0: Khởi tạo thanh toán
- 5.0 ↔ Cổng Thanh Toán: Chi tiết / Trạng thái giao dịch
- 3.0 → 6.0: Yêu cầu giao hàng
- 6.0 ↔ Đối Tác Vận Chuyển: Lệnh / Trạng thái
- Khách Hàng → 7.0: Yêu cầu trả hàng
- 7.0 → Khách Hàng: Kết quả xử lý
- 8.0 → 3.0: Điều kiện khuyến mãi áp dụng
- 4.0 → 3.0: Tồn khả dụng
- 3.0 ↔ D3: Ghi / Tra cứu đơn
- 5.0 ↔ D4: Ghi / Tra cứu thanh toán
- 6.0 ↔ D5: Ghi / Tra cứu vận đơn
- 7.0 ↔ D6: Ghi / Tra cứu yêu cầu trả
- 8.0 ↔ D7: Ghi / Tra cứu khuyến mãi
- 1.0 ↔ D1: Ghi / Tra cứu khách hàng
- 2.0 ↔ D2: Ghi / Tra cứu sản phẩm
- Các kho → 9.0: Dữ liệu báo cáo tổng hợp

## Cân bằng (Balancing) với Level 0
- Tất cả luồng chính: đặt hàng, thanh toán, tồn kho, giao hàng, khách hàng, trả hàng, khuyến mãi, báo cáo được phân bổ vào tiến trình con.
- Không xuất hiện luồng mới với thực thể ngoài mà không có ý nghĩa tiềm ẩn ở Level 0 (nếu Level 0 chưa có “Đối Tác Vận Chuyển” bạn cần cập nhật lại Level 0 để cân bằng).

## Khuyến nghị
- Xác nhận lại Level 0: bổ sung thực thể ngoài nào còn thiếu để đảm bảo cân bằng.
- Nếu phạm vi dự án không cần trả hàng hoặc khuyến mãi, có thể gỡ 7.0 / 8.0 để giản lược.
- Mỗi tiến trình có thể tiếp tục phân rã thành Level 2 (ví dụ: 3.0 gồm: 3.1 Kiểm Tra Tồn, 3.2 Áp Khuyến Mãi, 3.3 Ghi Đơn, 3.4 Đồng Bộ Trạng Thái).

## Ghi chú
- Bảo mật / xác thực không thể hiện trong DFD (phi chức năng).
- Nhật ký hệ thống, phân quyền có thể thêm kho riêng nếu cần ở phiên bản sau.
