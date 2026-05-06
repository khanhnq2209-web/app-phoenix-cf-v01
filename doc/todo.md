# GELEX CASHPLAN — Implementation Todo

Track progress phase by phase. Check off items as they are completed.

---

## Phase 0 — Project Setup

- [x] Create `requirements.txt` with: `streamlit`, `plotly`, `pandas`, `python-dotenv`, `gex_msgraph`
- [x] Create `utils/` directory
- [ ] Verify `.env` has all required vars (Azure AD client_id, tenant_id, client_secret or username/password for "das_u1")
- [x] Confirm `streamlit run app.py` resolves imports from `utils/` correctly

---

## Phase 1 — Skeleton

- [x] `app.py` — `st.set_page_config(layout="wide")`, sidebar global filters (NĂM, QUÝ, NHÓM ĐƠN VỊ), "Làm mới dữ liệu" button, page navigation
- [x] `utils/data_loader.py` — `load_data()` function: async SharePoint calls wrapped in `asyncio.run()`, `@st.cache_data(ttl=3600)`, returns dict with keys: `report`, `key_drivers`, `ratio_commit`, `adl`, `summary`
- [x] `utils/charts.py` — stub file; add chart functions incrementally per phase
- [x] `pages/p2_tracking.py` — stub with page title
- [x] `pages/p3_dashboard.py` — stub with page title
- [x] `pages/p4_detail.py` — stub with page title
- [x] `pages/p5_adl.py` — stub with page title
- [ ] Smoke test: `streamlit run app.py` loads without error, sidebar renders, pages navigate correctly

---

## Phase 2 — P2 Theo dõi dữ liệu

- [x] Derive CTTV group mapping from `folder_name` (strip leading number + dot)
- [x] Compute unit-level status: hoàn chỉnh (all 4 sheets success) / chưa đủ / chưa nộp from `df_summary`
- [x] KPI row: 3 metric cards (hoàn chỉnh count, chưa đủ, chưa nộp)
- [x] Group cards: GEE and GEL, with progress bar and unit badge chips
- [x] Detail table with ✓/✗ for all 4 sheets (Report, Key drivers, Ratio_commit, ADL input) and Trạng thái badge
- [x] Filter: exclude folder_name starting with "00"
- [x] Apply global NHÓM ĐƠN VỊ filter to table and group cards

---

## Phase 3 — P3 Dashboard chiến lược

- [ ] KPI row: 4 metric cards (net CF total, CF36 internal total, CTTV count, period count)
- [ ] Apply global NĂM/QUÝ/NHÓM filters to df_report before KPI calc
- [ ] **Tab 1 — Sankey:**
  - [ ] Filter to CF36 + Bên trong rows
  - [ ] Build node list: CTTV names + GEE/GEL + GELEX
  - [ ] Build link list with source/target indices and values
  - [ ] Render `go.Sankey` in Plotly
  - [ ] Add in-tab filter widgets (Kỳ/Năm, Quý, Loại giao dịch, ổn định, nội/ngoại)
- [ ] **Tab 2 — Heatmap:**
  - [ ] Pivot df_report to ma_don_vi × period label
  - [ ] Render `go.Heatmap` with RdYlGn colorscale + cell annotations
  - [ ] Add in-tab filter widgets (ổn định, nội/ngoại, khoản mục)
- [ ] **Tab 3 — Tích lũy dư tiền:**
  - [ ] Group by period, compute net CF and cumulative sum
  - [ ] Render combo bar+line chart
  - [ ] Display toggle (Tổng hợp / Ổn định/KOĐ / Stacked bar)
  - [ ] Alert banner logic: find first period cumulative > 100B

---

## Phase 4 — P4 Chi tiết CTTV

- [x] Page-level MÃ ĐƠN VỊ dropdown (populated from distinct ma_don_vi in df_report)
- [x] KHOẢN MỤC toggle buttons (CFO / CFI / CFF, multi-select)
- [x] Header: unit name, group badge, CTTV count label
- [x] KPI row: one card per selected (nam, quy) + TỔNG KỲ CHỌN
- [x] Left col: bar+line "Dòng tiền theo thời gian" chart
- [x] Right col: CF36 Bên trong panel — list view
- [x] Section: Chi tiết chỉ tiêu table (df_report filtered to unit + khoản mục)
- [x] Section: Key Drivers table (df_key_drivers filtered to unit)
- [x] Section: Covenant Tracking
  - [x] Detect distinct chi_tieu_cam_ket for selected unit → one sub-tab each
  - [x] Line chart: actual vs commitment threshold line
  - [x] KPI card: current value, cam kết, bank info from nguon_so_lieu
- [x] Section: ADL Assessment (df_adl filtered to selected unit, all years, tabular)

---

## Phase 5 — P5 Ma trận ADL

- [ ] Define static ADL axis labels (5 rows × 4 cols) and strategy text per cell
- [ ] **Tab 1 — Ma trận:**
  - [ ] Render 5×4 grid with st.columns
  - [ ] Populate CTTV badges from df_adl (match vi_the_canh_tranh + giai_doan_nganh)
  - [ ] Color badges by group (GEE/GEL)
- [ ] **Tab 2 — Bảng tổng hợp:**
  - [ ] Table with all ADL columns
  - [ ] Apply global NĂM and NHÓM filters
- [ ] **Tab 3 — Phân bổ vốn:**
  - [ ] Map (vi_the_canh_tranh, giai_doan_nganh) → signal (Invest/Hold/Harvest/Divest) using lookup table
  - [ ] Table with signal badge + capital weight suggestion

---

## Phase 6 — Polish

- [ ] Consistent color theme (GEE blue, GEL purple) applied to all charts and badges
- [ ] Number formatter utility: triệu → B/T shorthand
- [ ] Sidebar warning if any unit failed to load (non-success, non-missing_sheet status)
- [ ] `st.spinner` while data loads on first run
- [ ] Empty state messages when filters return no data
- [ ] Test with all 25+ CTTV files loaded (full data, not just a subset)
