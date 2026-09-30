import streamlit as st
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="wide"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 Ứng dụng tính lãi tiền gửi tiết kiệm")
st.write(
    "Tính toán tiền lãi theo **lãi đơn** hoặc **lãi kép**, "
    "với nhiều hình thức nhận lãi."
)

st.divider()

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")


# =========================
# NHẬP DỮ LIỆU
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Thông tin khoản tiền gửi")

    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=600,
        value=12,
        step=1
    )

    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1
    )

with col2:
    st.subheader("⚙️ Hình thức tính")

    loai_lai = st.radio(
        "Loại lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ],
        horizontal=True
    )

    hinh_thuc_lanh = st.selectbox(
        "Hình thức lãnh lãi",
        [
            "Lãnh lãi hàng tháng",
            "Lãnh lãi hàng quý",
            "Lãnh lãi cuối kỳ"
        ]
    )

st.divider()

# =========================
# TÍNH TOÁN
# =========================

# Lãi suất năm chuyển sang dạng thập phân
lai_suat_nam = lai_suat / 100

# Số tháng trong kỳ hạn
so_thang = ky_han

# Lãi suất theo tháng
lai_suat_thang = lai_suat_nam / 12

# Xác định số kỳ nhận lãi
if hinh_thuc_lanh == "Lãnh lãi hàng tháng":
    so_ky = so_thang
    so_thang_moi_ky = 1

elif hinh_thuc_lanh == "Lãnh lãi hàng quý":
    # Tính theo quý.
    # Nếu kỳ hạn không chia hết cho 3 thì vẫn xử lý phần kỳ cuối.
    so_ky = (so_thang + 2) // 3
    so_thang_moi_ky = 3

else:
    so_ky = 1
    so_thang_moi_ky = so_thang


# =========================
# LÃI ĐƠN
# =========================
if loai_lai == "Lãi đơn":

    # Tổng lãi:
    # I = P * r * t
    tong_lai = tien_gui * lai_suat_nam * (so_thang / 12)

    tong_tien = tien_gui + tong_lai

    # Lãi định kỳ
    if hinh_thuc_lanh == "Lãnh lãi hàng tháng":
        lai_dinh_ky = tien_gui * lai_suat_thang

    elif hinh_thuc_lanh == "Lãnh lãi hàng quý":
        lai_dinh_ky = tien_gui * lai_suat_thang * 3

    else:
        lai_dinh_ky = tong_lai


# =========================
# LÃI KÉP
# =========================
else:

    # Trường hợp lãnh lãi cuối kỳ:
    # Toàn bộ lãi được nhập vào vốn và tính lãi kép.
    if hinh_thuc_lanh == "Lãnh lãi cuối kỳ":

        so_ky_tinh_lai = so_thang

        tong_tien = tien_gui * (
            (1 + lai_suat_thang) ** so_ky_tinh_lai
        )

        tong_lai = tong_tien - tien_gui

        lai_dinh_ky = tong_lai

    else:
        # Với lãnh lãi hàng tháng/quý,
        # lãi của mỗi kỳ được nhập vào vốn để tính lãi kép.
        if hinh_thuc_lanh == "Lãnh lãi hàng tháng":
            tan_suat = 1
        else:
            tan_suat = 3

        so_ky_tinh_lai = so_thang // tan_suat
        thang_du = so_thang % tan_suat

        lai_suat_ky = lai_suat_nam * tan_suat / 12

        tien_hien_tai = tien_gui

        danh_sach_lai = []

        for ky in range(1, so_ky_tinh_lai + 1):
            tien_dau_ky = tien_hien_tai

            lai_ky = tien_dau_ky * lai_suat_ky

            tien_hien_tai += lai_ky

            danh_sach_lai.append(lai_ky)

        # Nếu còn số tháng lẻ
        if thang_du > 0:
            lai_ky_le = (
                tien_hien_tai
                * lai_suat_thang
                * thang_du
            )

            tien_hien_tai += lai_ky_le
            danh_sach_lai.append(lai_ky_le)

        tong_tien = tien_hien_tai
        tong_lai = tong_tien - tien_gui

        if len(danh_sach_lai) > 0:
            lai_dinh_ky = danh_sach_lai[0]
        else:
            lai_dinh_ky = 0


# =========================
# HIỂN THỊ KẾT QUẢ
# =========================

st.subheader("📊 Kết quả tính toán")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💵 Tiền lãi định kỳ",
        format_money(lai_dinh_ky)
    )

with col2:
    st.metric(
        "📈 Tổng tiền lãi",
        format_money(tong_lai)
    )

with col3:
    st.metric(
        "💰 Tổng tiền gốc + lãi",
        format_money(tong_tien)
    )

st.divider()

# =========================
# THÔNG TIN TÓM TẮT
# =========================

st.subheader("📋 Thông tin khoản gửi")

thong_tin = pd.DataFrame({
    "Thông tin": [
        "Số tiền gửi",
        "Kỳ hạn",
        "Lãi suất",
        "Loại lãi",
        "Hình thức lãnh lãi"
    ],
    "Giá trị": [
        format_money(tien_gui),
        f"{ky_han} tháng",
        f"{lai_suat:.2f}%/năm",
        loai_lai,
        hinh_thuc_lanh
    ]
})

st.table(thong_tin)


# =========================
# BẢNG CHI TIẾT
# =========================

st.subheader("📑 Chi tiết tiền lãi theo kỳ")

chi_tiet = []

tien_hien_tai = tien_gui

if loai_lai == "Lãi đơn":

    if hinh_thuc_lanh == "Lãnh lãi hàng tháng":
        so_ky_chi_tiet = ky_han
        thang_moi_ky = 1

    elif hinh_thuc_lanh == "Lãnh lãi hàng quý":
        so_ky_chi_tiet = (ky_han + 2) // 3
        thang_moi_ky = 3

    else:
        so_ky_chi_tiet = 1
        thang_moi_ky = ky_han

    for ky in range(1, so_ky_chi_tiet + 1):

        if hinh_thuc_lanh == "Lãnh lãi hàng quý":
            thang_thuc_te = min(3, ky_han - (ky - 1) * 3)

        else:
            thang_thuc_te = thang_moi_ky

        lai_ky = (
            tien_gui
            * lai_suat_nam
            * thang_thuc_te
            / 12
        )

        chi_tiet.append({
            "Kỳ": ky,
            "Số dư đầu kỳ": format_money(tien_gui),
            "Tiền lãi kỳ này": format_money(lai_ky),
            "Số dư sau kỳ": format_money(tien_gui + lai_ky)
        })

else:

    # Lãi kép
    if hinh_thuc_lanh == "Lãnh lãi hàng tháng":
        tan_suat = 1

    elif hinh_thuc_lanh == "Lãnh lãi hàng quý":
        tan_suat = 3

    else:
        tan_suat = ky_han

    if hinh_thuc_lanh == "Lãnh lãi cuối kỳ":

        for thang in range(1, ky_han + 1):

            tien_dau = tien_hien_tai

            lai_thang = tien_dau * lai_suat_thang

            tien_hien_tai += lai_thang

            chi_tiet.append({
                "Kỳ": thang,
                "Số dư đầu kỳ": format_money(tien_dau),
                "Tiền lãi kỳ này": format_money(lai_thang),
                "Số dư sau kỳ": format_money(tien_hien_tai)
            })

    else:

        so_ky_chi_tiet = (ky_han + tan_suat - 1) // tan_suat

        for ky in range(1, so_ky_chi_tiet + 1):

            thang_con_lai = ky_han - (ky - 1) * tan_suat

            thang_thuc_te = min(tan_suat, thang_con_lai)

            tien_dau = tien_hien_tai

            lai_ky = (
                tien_dau
                * lai_suat_nam
                * thang_thuc_te
                / 12
            )

            tien_hien_tai += lai_ky

            chi_tiet.append({
                "Kỳ": ky,
                "Số dư đầu kỳ": format_money(tien_dau),
                "Tiền lãi kỳ này": format_money(lai_ky),
                "Số dư sau kỳ": format_money(tien_hien_tai)
            })


df = pd.DataFrame(chi_tiet)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# =========================
# GHI CHÚ
# =========================

st.info(
    "💡 Lưu ý: Đây là công cụ tính toán mô phỏng dựa trên lãi suất "
    "người dùng nhập vào. Lãi suất thực tế của ngân hàng có thể "
    "khác và có thể phụ thuộc vào sản phẩm tiền gửi, số tiền, "
    "kỳ hạn và quy định của từng ngân hàng."
)

st.caption("Ứng dụng tính lãi tiền gửi tiết kiệm bằng Streamlit")
