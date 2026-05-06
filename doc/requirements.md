# GELEX CASHPLAN — App Requirements

**Project:** 2026 Phoenix · Kế hoạch dòng tiền 2026–2030  
**Stack:** Streamlit + Plotly · Data unit: triệu VNĐ  
**Entry point:** `streamlit run app.py` from project root  

---

## 1. General

| Requirement | Detail |
|---|---|
| Pages | P2, P3, P4, P5 (P1 Tổng quan deferred) |
| Navigation | Left sidebar with page links |
| Global filters | NĂM (2026–2030 checkboxes), QUÝ (Q1–Q4 checkboxes), NHÓM ĐƠN VỊ (dropdown: Tất cả / GEE / GEL) |
| Data source | Live SharePoint via `gex_msgraph.GraphClient`, same credentials as ETL notebook (`.env`) |
| Cache | `@st.cache_data(ttl=3600)` — 1-hour refresh; manual "Làm mới dữ liệu" button in sidebar |
| Auth | None (internal use) |
| Number display | Large numbers in KPI cards auto-formatted: ≥1,000,000 → T, ≥1,000 → B (e.g. 5,500,000 triệu → 5.5T) |
| Colors | GEE = `#4C72B0` (blue), GEL = `#9467bd` (purple) |
| Language | Vietnamese UI labels; snake_case column names in code |

---

## 2. Data Sources

### df_report — Sheet "Report" (A:M, skiprows=1)
Columns: `code, phan_cap_don_vi, ma_don_vi, ten_don_vi, khoan_muc, chi_tieu, nam, quy, so_tien_tong, nguon_thong_tin, phan_loai_on_dinh_khong_on_dinh, phan_loai_ben_trong_ben_ngoai, doi_tuong_giao_dich_kinh_te, source`

Key derived fields:
- CF36 rows: `code.str.startswith("CF36")`
- Internal: `phan_loai_ben_trong_ben_ngoai == "Bên trong"`
- Period label: `f"{nam}-Q{quy}"`

### df_key_drivers — Sheet "Key drivers" (A:J, skiprows=1)
Columns: `group, code, phan_cap_don_vi, ma_don_vi, ten_don_vi, chi_tieu, cau_phan_value_chain, key_drivers, phan_loai_on_dinh_khong_on_dinh, rationale_on_dinh_khong_on_dinh, phan_loai_ben_trong_ben_ngoai, source`

### df_ratio_commit — Sheet "Ratio_commit" (A:J, skiprows=1)
Columns: `phan_cap_don_vi, ma_don_vi, ten_don_vi, chi_tieu_cam_ket, cong_thuc, gia_tri_cam_ket, nam, quy, gia_tri_thuc_hien, status, source, nguon_so_lieu, dinh_ky`

`status` values: `"ok"` | `"break"`

### df_adl — Sheet "ADL input" (A:I, skiprows=1)
Columns: `phan_cap_don_vi, ma_don_vi, ten_don_vi, nam, giai_doan_nganh, vi_the_canh_tranh, muc_do_tin_cay, co_so_danh_gia, thi_phan_uoc_tinh, source`

### df_summary — computed from df_list_files + status DataFrames
Columns include: `folder_name, folder_path, file_name, file_path, file_modified, report_status, key_drivers_status, ratio_commit_status, adl_input_status`

Status values: `"success"` | `"missing_sheet"` | `NaN` (no file)

---

## 3. Page Specifications

### P2 — Theo dõi dữ liệu (Data Tracking)

**Purpose:** Show which subsidiaries have submitted complete Excel files.

> Note: The mockup shows 3 sheets (Report, Key drivers, Ratio_commit) but the actual schema has **4 sheets** — ADL input is also tracked. All 4 must be "success" for a unit to be "Hoàn chỉnh".

**KPI row (3 cards):**
- HOÀN CHỈNH: count of units where report + key_drivers + ratio_commit + adl_input all = "success"
- CHƯA ĐỦ SHEET: count of units with file but at least one of the 4 sheets missing
- CHƯA NỘP: count of units with no file (file_path = NaN)

**Group cards (one per group: GEE, GEL):**
- Title: "{Group} Group"
- Sub-title: "{hoàn chỉnh}/{total} hoàn chỉnh"
- Progress bar: completion %
- Unit badges (chips): one per CTTV in group, colored by status (green = hoàn chỉnh, orange = chưa đủ, grey = chưa nộp)

**Detail table columns:**
| Column | Source | Notes |
|---|---|---|
| Mã đơn vị | `ma_don_vi` | Clickable → P4 |
| Tên đơn vị | `ten_don_vi` | |
| Group | derived from folder_name | GEE / GEL |
| Sheet Report | `report_status` | ✓ green / ✗ red |
| Sheet Key drivers | `key_drivers_status` | ✓ / ✗ |
| Sheet Ratio_commit | `ratio_commit_status` | ✓ / ✗ |
| Sheet ADL input | `adl_input_status` | ✓ / ✗ |
| Cập nhật lần cuối | `file_modified` | date only |
| Trạng thái | derived | "Hoàn chỉnh" (green) / "Chưa đủ" (orange) / "Chưa nộp" (grey) |

Filter: exclude rows where folder_name starts with "00" (template/admin folders).

---

### P3 — Dashboard chiến lược (Strategic Dashboard)

**Purpose:** Group-level cash flow overview and analysis.

**KPI row (4 cards):**
- Lưu chuyển tiền thuần tổng hợp: `sum(so_tien_tong)` (all rows, filtered by global year/quy)
- CF36 Bên trong (Cổ tức nội bộ): `sum(so_tien_tong)` where code starts with CF36 AND phan_loai_ben_trong_ben_ngoai = "Bên trong"
- Số CTTV: count of distinct `ma_don_vi`
- Số Kỳ: count of distinct (nam, quy) combinations in filtered data

**Tab 1 — Sankey nội bộ (CF36)**
- Source data: df_report rows where `code.str.startswith("CF36")` and `phan_loai_ben_trong_ben_ngoai == "Bên trong"`
- Sankey nodes: CTTV → Sub-Holding (GEE/GEL) → GELEX (Tập đoàn)
- Link width: `|so_tien_tong|`; direction sign distinguishes inflow vs outflow
- In-tab filters: Kỳ/Năm (year selector), Quý (Q1–Q4 buttons), Loại giao dịch (Tất cả dropdown), Phân loại ổn định (Tất cả / Ổn định / Không ổn định), Phân loại Nội/Ngoại (Tất cả / Bên trong / Bên ngoài)

**Tab 2 — Heatmap Net CF**
- Plotly heatmap: rows = `ma_don_vi`, cols = period label "{nam}-Q{quy}", values = `sum(so_tien_tong)`
- Color scale: red (negative) → white (zero) → green (positive)
- Annotate each cell with formatted value (e.g. "90B")
- In-tab filters: Phân loại ổn định, Phân loại Nội/Ngoại, Khoản mục (Tất cả / CFO / CFI / CFF)

**Tab 3 — Tích lũy dư tiền**
- Sum `so_tien_tong` per period (x-axis), compute cumulative sum
- Plotly combo: bar (net CF per period) + line (cumulative)
- Display toggle: Tổng hợp / Ổn định/KOĐ (side-by-side stacked) / Stacked bar
- Info alert when cumulative first exceeds 100B: "Tích lũy surplus vượt 100B từ kỳ {period} — Tập đoàn có thể lên kế hoạch triển khai vốn đầu tư mới."

---

### P4 — Chi tiết CTTV (Subsidiary Detail)

**Purpose:** Drill into a single subsidiary's cash flow, key drivers, and covenants.

**Page-level filters (top of page, not sidebar):**
- MÃ ĐƠN VỊ: dropdown (default: first unit alphabetically)
- KHOẢN MỤC (CF DETAIL): toggle buttons CFO / CFI / CFF (multi-select allowed)

**Header:** Tên đơn vị (large), Group badge, "X. CTTV" label

**KPI row:** One card per selected quarter (from global NĂM/QUÝ filter) showing sum of so_tien_tong + final card "TỔNG KỲ CHỌN"

**2-column layout:**
- Left (60%): Plotly bar+line — "Dòng tiền theo thời gian"; bar = net CF per period, line = cumulative; x = period label
- Right (40%): "CF36 — {chi_tieu} (Bên trong)" panel — list of periods with counterparty (doi_tuong_giao_dich_kinh_te) and amount; filtered to CF36 + Bên trong rows for selected unit

**Section: Chi tiết chỉ tiêu — Sheet Report**
Table columns: Code, Khoản mục (badge), Chỉ tiêu, Phân loại ổn định (badge), Phân loại Nội/Ngoài, Đối tượng giao dịch, Số tiền tổng  
Filtered by: selected unit + selected khoản mục + global year/quy

**Section: Key Drivers — Sheet Key drivers**
Table columns: Group, Code, Chỉ tiêu, Cấu phần value chain (badge), Key drivers, Phân loại Ổn định (badge), Rationale  
Filtered by: selected unit (no year filter — drivers are structural, not time-series)

**Section: Covenant Tracking — Sheet Ratio_commit**
Two sub-tabs (one per distinct `chi_tieu_cam_ket` found for that unit):
- Plotly line chart: x = period, y = `gia_tri_thuc_hien` (actual) + dashed line at `gia_tri_cam_ket` (threshold)
- Color line: green if status = "ok", red if status = "break"
- Below chart: KPI card showing current value, cam kết threshold, bank name + loan amount (from `nguon_so_lieu`), maturity date

**Section: ADL Assessment — Sheet ADL input**
Table columns: Năm, Giai đoạn ngành, Vị thế cạnh tranh, Mức độ tin cậy, Thị phần ước tính (%), Cơ sở đánh giá  
Filtered by: selected unit (all years shown — one row per năm so reviewers can see how positioning evolves)  
Purpose: let all viewers see the full strategic positioning data for that CTTV alongside its financial data

---

### P5 — Ma trận ADL (ADL Matrix)

**Purpose:** Strategic positioning of all CTTVs on the ADL (Arthur D. Little) framework.

**Tab 1 — Ma trận**
- 5×4 grid table rendered with st.columns or HTML
- Rows (vi_the_canh_tranh, top to bottom): Dominant, Strong, Favourable, Tenable, Weak
- Cols (giai_doan_nganh, left to right): Embryonic, Growth, Mature, Ageing
- Each cell: descriptive strategy text (static) + CTTV badges from df_adl that match that cell's (vi_the_canh_tranh, giai_doan_nganh)
- Badge color: GEE = blue, GEL = purple

**Tab 2 — Bảng tổng hợp**
Table columns: Mã đơn vị, Tên đơn vị, Group, Giai đoạn ngành, Vị thế cạnh tranh, Mức độ tin cậy, Thị phần ước tính (%), Cơ sở đánh giá  
Filtered by: global NĂM (ADL assessments are annual) and NHÓM ĐƠN VỊ

**Tab 3 — Phân bổ vốn**
ADL signal logic (derived, not stored in data):
| Competitive Position | Embryonic | Growth | Mature | Ageing |
|---|---|---|---|---|
| Dominant | Invest | Invest | Hold | Harvest |
| Strong | Invest | Invest | Hold | Harvest |
| Favourable | Selective | Selective | Hold | Divest |
| Tenable | Selective | Selective | Divest | Divest |
| Weak | Divest | Divest | Divest | Divest |

Display: table with Mã đơn vị + Signal badge (color-coded: Invest=green, Hold=grey, Harvest=yellow, Divest=red) + Thị phần ước tính + suggested capital weight (proportional to Invest units)

---

## 4. Non-Functional Requirements

| Requirement | Detail |
|---|---|
| Load time | Data fetch < 60s on first load (SharePoint API); cache hit < 2s |
| Error handling | Missing sheet → skip (already handled by ETL); show warning in sidebar if any unit has errors |
| Responsive layout | `st.set_page_config(layout="wide")` |
| Locale | No locale dependency — format numbers in Python, not locale-aware formatters |
| File encoding | UTF-8 for all .py files |
