# Ứng dụng Quản Lý Bán Hàng
## Tóm tắt dự án
- Dạng đồ án môn **Kỹ Thuật Phần Mềm**: thu thập yêu cầu → mô hình hóa → hiện thực mẫu → kiểm thử.
- Thành viên nhóm đóng vai BA, Designer, Developer và QA để tạo bộ artefact hoàn chỉnh.
- Sản phẩm cuối kỳ: tài liệu đặc tả + sơ đồ PlantUML + prototype minh họa.

## 1. Bối cảnh môn học
- Dự án thuộc môn **Kỹ Thuật Phần Mềm** tại SIU, tập trung thực hành quy trình phát triển phần mềm có kiểm soát.
- Nhóm sinh viên chịu trách nhiệm thu thập yêu cầu, đặc tả, phân tích thiết kế (DFD, Use Case), hiện thực mô-đun mẫu và chuẩn bị tài liệu bàn giao.

## 2. Mục tiêu dự án
1. Cung cấp nền tảng bán hàng trực tuyến cho Khách hàng và Người bán.
2. Thiết lập cơ chế giám sát vận hành (Monitor) để theo dõi giao dịch, log và cảnh báo.
3. Xây dựng bộ artefact (SRS, Use Case, DFD, kế hoạch kiểm thử) đáp ứng chuẩn môn học.

## 3. Phạm vi chức năng chính
- **Khách hàng**: đăng ký/đăng nhập, quản lý giỏ hàng, thanh toán, in hóa đơn, xem lịch sử.
- **Người bán**: quản lý sản phẩm, tồn kho, đơn hàng, cập nhật hàng loạt, truy xuất báo cáo/log.
- **Monitor**: giám sát trạng thái hệ thống, nhận cảnh báo bất thường, xuất báo cáo vận hành.
- Các chức năng phi chức năng: bảo mật phiên, hiệu năng truy xuất tồn kho, ghi log và giám sát cơ bản.

## 4. Artefact quan trọng
| Artefact                                   | Mô tả ngắn gọn                                  |
|--------------------------------------------|-------------------------------------------------|
| `software_requirements.md`                 | Đặc tả yêu cầu chức năng & phi chức năng.       |
| `software_usecases.md`                     | Bảng Use Case bám sát DFD Level 0 (3 actor).    |
| `Diagrams/software_dfd_level0.puml`        | DFD Level 0 cho tiến trình “Ứng Dụng Bán Hàng”. |
| `Diagrams/DFD_Level1.puml`                 | DFD Level 1 phân rã thành các tiến trình con.   |
| `DFD_Level1.md` / `software_dfd_level0.md` | Thuyết minh chi tiết cho từng sơ đồ.            |

## 5. Cấu trúc thư mục nổi bật
- `Diagrams/`: chứa các file PlantUML cho DFD và sơ đồ phụ trợ.
- `Docs/` (nếu có): tài liệu bổ sung như kế hoạch kiểm thử, biên bản họp.
- `src/`: mã nguồn nguyên mẫu (frontend/backend) phục vụ minh họa.
- `tests/`: kịch bản kiểm thử chức năng hoặc kiểm thử đơn vị.
- `README.md`: tài liệu định hướng dự án (file hiện tại).

## 6. Quy trình làm việc gợi ý
1. Thu thập và chuẩn hóa yêu cầu → cập nhật `software_requirements.md`.
2. Diễn tả luồng dữ liệu (DFD Level 0/1) → đối chiếu với Use Case.
3. Thiết kế kiến trúc & mô hình dữ liệu khái quát.
4. Hiện thực từng mô-đun, viết kiểm thử, cập nhật tài liệu.
5. Rà soát peer review và đóng gói bàn giao.

## 7. Hướng phát triển tiếp
- Bổ sung DFD mức 2 cho các tiến trình quan trọng (Thanh toán, Quản lý kho).
- Hoàn thiện mockup giao diện và prototype tương tác.
- Tự động hóa kiểm thử (CI) và bổ sung chỉ số chất lượng (coverage, lint).
- Chuẩn hóa tài liệu triển khai (Deployment Guide, User Guide).

## 8. Phương pháp & Công cụ gợi ý
- Quản lý công việc: GitHub Projects, Kanban weekly sprint.
- Thiết kế & mô hình: PlantUML, Draw.io (mockup), Markdown chuẩn CommonMark.
- Phát triển mẫu: Node.js/Express + PostgreSQL (hoặc stack được hướng dẫn viên phê duyệt).
- Kiểm thử & CI: Jest/Vitest, GitHub Actions với lint + unit test.
