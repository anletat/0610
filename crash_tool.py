
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Crash Game Tool", layout="wide")

def detect_trends(history, target=2.0):
    last_10 = history[-10:] if len(history) >= 10 else history
    last_3 = history[-3:] if len(history) >= 3 else history

    low_count = sum(1 for x in last_10 if x < 2)
    high_count = sum(1 for x in last_10 if x >= 2.5)

    # immediate gray zone: 3 recent < x2
    if len(last_3) == 3 and all(x < 2 for x in last_3):
        return "gray", "🚫 Rủi ro cao: 3 ván gần nhất < x2 → Chuỗi xám có thể tiếp tục."

    # recently a big bomb (x10+) -> caution
    if any(x >= 10 for x in last_10):
        return "neutral", "⚠ Vừa có ván rất cao (x10+). Có thể xuất hiện chuỗi xám. Đề nghị đợi."

    # many highs -> green
    if high_count >= 5:
        return "green", "✅ Xu hướng xanh: Nhiều ván >= x2.5 trong 10 ván gần nhất → Cơ hội tốt."

    risk_ratio = low_count / len(last_10) if len(last_10) > 0 else 0
    if risk_ratio > 0.7:
        return "gray", f"🚫 Nguy cơ chuỗi xám rất cao ({low_count}/10 ván < x2)."
    elif risk_ratio > 0.5:
        return "neutral", f"⚠ Rủi ro trung bình cao ({low_count}/10 ván < x2)."
    else:
        return "green", f"✅ Tương đối an toàn ({low_count}/10 ván < x2). Có thể cân nhắc vào x{target}."

def bet_suggestions(balance, base_bet):
    fixed = [round(base_bet, 2)] * 5
    martingale = [round(base_bet * (1.5 ** i), 2) for i in range(4)]
    incremental = [round(base_bet + (i * 0.2 * base_bet), 2) for i in range(4)]
    return {
        "Fixed Bet (safe)": fixed,
        "Mini Martingale (x1.5) - gồng tối đa 4 ván": martingale,
        "Incremental Safe (tăng dần nhẹ)": incremental
    }

def plot_history(history, target):
    fig, ax = plt.subplots(figsize=(9, 3))
    ax.plot(history[-20:], marker="o")
    ax.axhline(y=target, linestyle="--")
    ax.set_title("Lịch sử 20 ván gần nhất (trái → mới nhất bên phải)")
    ax.set_ylabel("Hệ số crash")
    ax.set_xlabel("Ván (gần nhất)")
    ax.grid(alpha=0.2)
    return fig

st.title("🎮 Crash Game Tool — Dự báo chuỗi & Gợi ý cược")
st.write("Gõ hoặc dán lịch sử hệ số crash (ví dụ: 1.3, 1.8, 2.5, ...). Tool sẽ phân tích xu hướng xanh/xám và gợi ý cách chia vốn.")

col1, col2 = st.columns([2,1])

with col1:
    history_input = st.text_area("Lịch sử hệ số Crash (cách nhau bằng dấu phẩy):", value="1.3, 1.4, 2.1, 1.8, 3.2, 1.5, 2.7, 1.2, 1.6, 2.8")
    target = st.number_input("Mức cash out mong muốn (ví dụ 2.0, 2.62):", value=2.0, step=0.01)
    base_bet = st.number_input("Số tiền cược ban đầu ($):", min_value=0.01, value=0.5, step=0.01)
    balance = st.number_input("Vốn hiện có ($):", min_value=0.1, value=10.0, step=0.1)
    analyze = st.button("Phân tích & Gợi ý")

with col2:
    st.markdown("### 📌 Hướng dẫn nhanh")
    st.markdown("- Nhập ít nhất 5 ván để có dự báo đáng tin.")
    st.markdown("- Nếu cảnh báo chuỗi xám → nên đợi hoặc giảm cược.")
    st.markdown("- Khi chuỗi xanh xuất hiện → cân nhắc mức cash out hợp lý và chia vốn an toàn.")
    st.markdown("---")
    st.markdown("### 🔧 Tính năng")
    st.markdown("- Phân tích chuỗi xám / xanh.")
    st.markdown("- Gợi ý 3 chiến lược cược.")
    st.markdown("- Biểu đồ 20 ván gần nhất.")
    st.markdown("- Xuất file sample (download) để lưu lịch sử.")

if analyze:
    try:
        history = [float(x.strip()) for x in history_input.split(",") if x.strip() != ""]
        if len(history) < 5:
            st.error("⚠ Vui lòng nhập ít nhất 5 giá trị hệ số Crash để phân tích.")
        else:
            trend, message = detect_trends(history, target)
            if trend == "green":
                st.success(message)
            elif trend == "neutral":
                st.warning(message)
            else:
                st.error(message)

            # Suggestions
            st.subheader("💡 Gợi ý số tiền cược cho 3 chiến lược")
            suggestions = bet_suggestions(balance, base_bet)
            for name, bets in suggestions.items():
                total = round(sum(bets), 2)
                st.markdown(f"**{name}** — cược mẫu: {bets}  •  Tổng gồng: ${total}")
                # Simple guidance for each strategy
                if name.startswith("Fixed"):
                    st.caption("Cược đều mỗi ván — an toàn cho vốn nhỏ.")
                elif "Martingale" in name:
                    st.caption("Gấp nhẹ 1.5x sau mỗi thua — giới hạn gồng 4 ván.")
                else:
                    st.caption("Tăng dần nhẹ, giảm rủi ro so với martingale.")

            # Chart
            st.subheader("📊 Biểu đồ lịch sử")
            fig = plot_history(history, target)
            st.pyplot(fig)

            # Download sample data
            st.download_button("Download sample history", data=",".join([str(x) for x in history]), file_name="history_sample.txt")
    except Exception as e:
        st.error(f"Lỗi khi xử lý dữ liệu: {e}")
