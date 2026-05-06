# ETL Schema Mapping

Documents the column mapping from raw Excel input to clean DataFrame columns for each sheet processed in `ETL.ipynb`.

## Overview

All sheets are read via `client.read_excel_many()` with these shared options:

| Option | Value |
|---|---|
| `skiprows` | `1` (data headers are on row 2) |
| `on_error` | `"skip"` |
| `on_missing_sheet` | `"skip"` |

Every resulting DataFrame includes a `source` column (auto-added as `_source` by `read_excel_many`, then renamed) that records the originating file path.

---

## Sheet: Report

**Excel columns read:** `A:M`

| Original Header (Vietnamese) | Renamed Column |
|---|---|
| Code | `code` |
| Phân cấp đơn vị | `phan_cap_don_vi` |
| Mã đơn vị | `ma_don_vi` |
| Tên đơn vị | `ten_don_vi` |
| Khoản mục | `khoan_muc` |
| Chỉ tiêu | `chi_tieu` |
| Năm | `nam` |
| Quý | `quy` |
| Số tiền tổng | `so_tien_tong` |
| Nguồn thông tin (Các ghi chú khác về dữ liệu, nguồn thông tin,...nếu cần để sau có thể follow up) | `nguon_thong_tin` |
| Phân loại ổn định và không ổn định | `phan_loai_on_dinh_khong_on_dinh` |
| Phân loại Bên trong và bên ngoài | `phan_loai_ben_trong_ben_ngoai` |
| Đối tượng giao dịch kinh tế | `doi_tuong_giao_dich_kinh_te` |
| *(auto)* `_source` | `source` |

> `nguon_thong_tin` has a multi-line original header that was collapsed to a single identifier.

---

## Sheet: Key drivers

**Excel columns read:** `A:J`

| Original Header (Vietnamese) | Renamed Column |
|---|---|
| Group | `group` |
| Code | `code` |
| Phân cấp đơn vị | `phan_cap_don_vi` |
| Mã đơn vị | `ma_don_vi` |
| Tên đơn vị | `ten_don_vi` |
| Chỉ tiêu | `chi_tieu` |
| Cấu phần value chain | `cau_phan_value_chain` |
| Key drivers | `key_drivers` |
| Phân loại Ổn định & Không ổn định *(merged)* | `phan_loai_on_dinh_khong_on_dinh` |
| Rationale ổn định or không ổn định | `rationale_on_dinh_khong_on_dinh` |
| Phân loại Bên trong và bên ngoài | `phan_loai_ben_trong_ben_ngoai` |
| *(auto)* `_source` | `source` |

> **Column merge:** The sheet contains two near-duplicate columns — `"Phân loại Ổn định & Không ổn định"` and `"Phân loại ổn định và không ổn định"` — that differ only in punctuation. They are combined with `.combine_first()` (first column takes priority; NaNs are filled from the second), then the duplicate is dropped before renaming.

---

## Sheet: Ratio_commit

**Excel columns read:** `A:J`

| Original Header (Vietnamese) | Renamed Column |
|---|---|
| Phân cấp đơn vị | `phan_cap_don_vi` |
| Mã đơn vị | `ma_don_vi` |
| Tên đơn vị | `ten_don_vi` |
| Chỉ tiêu cam kết | `chi_tieu_cam_ket` |
| Công thức | `cong_thuc` |
| Giá trị cam kết | `gia_tri_cam_ket` |
| Năm | `nam` |
| Quý | `quy` |
| Giá trị thực hiện | `gia_tri_thuc_hien` |
| Status (ok/ break) | `status` |
| *(auto)* `_source` | `source` |
| Nguồn số liệu | `nguon_so_lieu` |
| Định kỳ | `dinh_ky` |

> `status` categorical values: `"ok"` or `"break"`.

---

## Sheet: ADL input

**Excel columns read:** `A:I`

| Original Header (Vietnamese) | Renamed Column |
|---|---|
| Phân cấp đơn vị | `phan_cap_don_vi` |
| Mã đơn vị | `ma_don_vi` |
| Tên đơn vị | `ten_don_vi` |
| Năm | `nam` |
| Giai đoạn ngành (Industry Lifecycle) ▼ | `giai_doan_nganh` |
| Vị thế cạnh tranh (Competition) ▼ | `vi_the_canh_tranh` |
| Mức độ tin cậy ▼ | `muc_do_tin_cay` |
| Cơ sở đánh giá / Rationale (ngành, DN, market...) | `co_so_danh_gia` |
| Thị phần ước tính (%) | `thi_phan_uoc_tinh` |
| *(auto)* `_source` | `source` |

> Columns marked ▼ are Excel dropdown fields. `thi_phan_uoc_tinh` is a percentage value (0–100).