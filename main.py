import streamlit as st
from datetime import time
#from colorama import Fore
import pandas as pd
import numpy as np
#import docx
#import PyPDF2
import markdown
import base64

from datetime import date
from dateutil.relativedelta import relativedelta 
from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode
st.set_page_config(
        page_title="Customer response generator", page_icon=":bird:")

st.header("Tạo hợp đồng vay trong vòng 5 phút!")

lender = st.text_input('**Người cho vay**', 'Nguyễn Văn A')
borrower = st.text_input('**Người nhận vay**', 'Nguyễn Văn B')

# st.write('You selected:', option)

# option = st.selectbox(
#     'Thời hạn',
#     ('6 tháng', '12 tháng', '18 tháng'))

# st.write('You selected:', option)

principal = st.number_input("**Khoản tiền cho vay**", value = 1000000, step=100000, format= "%1i", placeholder="Điền khoản vay...")
lender = "**"+str(lender)+"**"
borrower = "**"+str(borrower)+"**"
#principal = "**VND"+str(principal)+" dong**"
st.write(lender, "cam kết cho" , borrower, "vay **VND", f"{principal:,}", 'đồng**')

#principal = st.slider("Khoản vay", 0, 20, 5)
#st.write("Người vay cần trả ", interest, 'lãi suất mỗi năm')
st.divider()

interest = st.slider('**Lãi suất mỗi năm (%)**', 0, 20, 5)
yearly_interest = int(principal * interest/100)


if interest <20:
    #interest = "**" + str(interest) + "**"
    st.write(borrower, " cần trả", f"**{interest/100:.0%}**" ,' lãi suất mỗi năm - tương đương **VND', f'{yearly_interest:,}', "đồng/năm**")
if interest == 20:
    #interest = "**" + str(interest) + "**"
    st.write(borrower, "cần trả", f"{interest/100:.0%}",' lãi suất mỗi năm - tương đương **VND', f'{yearly_interest:,}', "đồng/năm**")
    st.write("Lưu ý: ", f"{interest/100:.0%}",  "là lãi suất trần của chính phủ Việt Nam")

tenure = st.slider('**Thời hạn cho vay (tháng)**', 0, 36, 6)
tenure = int(tenure)
total_amt = int(principal * (1+interest/100)**(tenure/12))

st.write("Tổng số tiền cần thanh toán trong ", f'**{tenure:,}', "tháng** là **VND", f'{total_amt:,}' , "đồng**")

st.divider()

payment_period = st.selectbox(
    '**Thanh toán lãi suất...**',
    ('Theo tháng', 'Theo quý', 'Theo năm', 'Khi đáo hạn'))

principal_period = st.selectbox(
    '**Thanh toán khoản vay gốc...**',
    ('Theo tháng', 'Theo quý', 'Theo năm', 'Khi đáo hạn'))
# principal_payment = st.selectbox(
#     '**Yêu cầu trả dần cả tiền gốc?**',
#     ('Có', 'Không'))

#if payment_period == "...tháng":
    #int_month = interest/tenure
monthly_int = int(principal * (1+interest/100)**(tenure/12)-principal)/tenure
quarterly_int = int(principal * (1+interest/100)**(tenure/12)-principal)/tenure * 3
yearly_int = int(principal * (1+interest/100)**(tenure/12)-principal)/tenure * 12

monthly_prin = int(principal)/tenure
quarterly_prin = int(principal)/tenure * 3
yearly_prin = int(principal)/tenure * 12

month = []
quarter = []
year = []

month_p = []
quarter_p = []
year_p = []



today = date.today()
due_date = today + relativedelta(months=tenure) 

payment_date = [today]

for x in range(1,tenure +1):
    month.append(monthly_int)
    month_p.append(monthly_prin)
    payment_date.append(payment_date[-1] + relativedelta(months=1))
    if x%3==0:
        quarter.append(quarterly_int)
        quarter_p.append(quarterly_prin)
    else:
        quarter.append(0)
        quarter_p.append(0)
    if x%12==0:
        year.append(yearly_int)
        year_p.append(yearly_prin)
    else:
        year.append(0)
        year_p.append(0)

payment_date = payment_date[1:]


if sum(month) >= sum(quarter):
    quarter[-1] = sum(month) - sum(quarter)

if sum(month_p) >= sum(quarter_p):
    quarter_p[-1] = sum(month_p) - sum(quarter_p)

if sum(month) >= sum(year):
    year[-1] = sum(month) - sum(year)

if sum(month_p) >= sum(year_p):
    year_p[-1] = sum(month_p) - sum(year_p)

if payment_period == "Theo tháng":
    tb_int = month
    #tb_p = month_p
    st.write(borrower," cần thanh toán **VND", f'{int(monthly_int):,}', "đồng/tháng** tiền lãi")
elif payment_period == "Theo quý":
    tb_int = quarter
    #tb_p = quarter_p
    st.write(borrower," cần thanh toán **VND", f'{int(quarterly_int):,}', "đồng/quý** tiền lãi")
else:
    tb_int = year
    #tb_p = year_p
    st.write(borrower," cần thanh toán **VND", f'{int(yearly_int):,}', "đồng/năm** tiền lãi")

if principal_period == "Theo tháng":
    #tb_int = month
    tb_p = month_p
    st.write(borrower," cần thanh toán **VND", f'{int(monthly_prin):,}', "đồng/tháng** tiền gốc")
elif principal_period == "Theo quý":
    #tb_int = quarter
    tb_p = quarter_p
    st.write(borrower," cần thanh toán **VND", f'{int(quarterly_prin):,}', "đồng/quý** tiền gốc")
else:
    #tb_int = year
    tb_p = year_p
    st.write(borrower," cần thanh toán **VND", f'{int(yearly_prin):,}', "đồng/năm** tiền gốc")
#tb_int


period = np.arange(1,tenure +1)

data = np.array([tb_int, period])


chart_data = pd.DataFrame(
   {
       "Lãi": tb_int,
       "Tháng": period,
       "Gốc": tb_p,
       #"#42c8f5"
   }
)
chart_data = chart_data.style.format(subset=['Lãi'], formatter="{:,.1f}")
#st.bar_chart(chart_data, x='Tháng')

df = pd.DataFrame(
   {
       "Ngày": payment_date,
       "Lãi": tb_int,
       "Gốc": tb_p,
       #"#34ebc6"
       #"#42c8f5"
   }
)

df['Tổng'] = df['Lãi'] + df['Gốc']
df



# gb = GridOptionsBuilder.from_dataframe(df)
# gb.configure_column("Lãi", 
#                     type=["numericColumn","numberColumnFilter","customNumericFormat"], 
#                     valueFormatter="data.Lãi.toLocaleString('en-US');") 
                    
# gb.configure_column("Gốc", 
#                     type=["numericColumn","numberColumnFilter","customNumericFormat"], 
#                     valueFormatter="data.Gốc.toLocaleString('en-US');") 

# gb.configure_column("Tổng", 
#                     type=["numericColumn","numberColumnFilter","customNumericFormat"], 
#                     valueFormatter="data.Tổng.toLocaleString('en-US');") 
# gb.configure_column("Ngày", type=["customDateTimeFormat"], custom_format_string='yyyy-MM-dd')
# vgo = gb.build()
# vgo["autoSizeAllColumns"] = True
# st.write("*Đơn vị: VNĐ*")


# AgGrid(df, gridOptions=vgo,  columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)





    

#st.table(df)

# values = st.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0))
# st.write('Values:', values)

# appointment = st.slider(
#     "Schedule your appointment:",
#     value=(time(11, 30), time(12, 45)))
# st.write("You're scheduled for:", appointment)







st.markdown("<h4 style='text-align: center; color: black;'>CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</h4>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: black;'>Độc lập – Tự do – Hạnh phúc</h5>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>HỢP ĐỒNG CHO VAY TIỀN</h4>", unsafe_allow_html=True)
st.write("Hôm nay, ngày ", today.day,"tháng ", today.month, "năm ", today.year)
st.write("*Chúng tôi gồm có:*")
st.write("**Bên A:**", lender)
st.write("Số CMND:………………………..Cấp ngày:……../……./……..tại:……………………………..")
st.write("Số điện thoại: ………………")
st.write("và")
st.write("**Bên B:**", borrower)
st.write("Số CMND:………………………..Cấp ngày:……../……./……..tại:……………………………..")
st.write("Số điện thoại: ……………….")
st.write("***Sau khi thỏa thuận cùng nhau ký hợp đồng vay tiền với các điều khoản sau:***")
st.write("1. ", lender," đồng ý cho ", borrower, " vay số tiền là: **VND", f"{principal:,}", "đồng**;")
st.write("2. Mục đích vay tiền là:……………………………………………………………………………;")
st.write("3. Tài sản thế chấp là:……………………………………………………………………………...;")
st.write("4. Thời hạn vay là từ ngày ", today.day,"tháng ", today.month, "năm ", today.year, "đến ngày ", due_date.day,"tháng ", due_date.month, "năm ", due_date.year,";")
st.write("5. Phương thức cho vay: …………………………………;")
st.write("6. Lãi suất ",  f"**{interest/100:.0%}**","/năm;")
st.write("7. Kể từ thời điểm Bên B ký vào hợp đồng, Bên B xác nhận đã nhận đủ số tiền do Bên A chuyển giao;")
st.write("8. Hai bên cam kết ký hợp đồng trong trạng thái tinh thần hoàn toàn minh mẫn, sáng xuất không bị lừa dối, ép buộc;")
st.write("9. Hợp đồng này có hiệu kể từ ngày ký và được lập thành 02 (hai) bản, mỗi bên giữ 01 (một) bản có giá trị pháp lý ngang nhau.")
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h6 style='text-align: center; color: black;'>ĐẠI DIỆN BÊN A</h6>", unsafe_allow_html=True)
    #picture = st.camera_input("Take a picture")
    #if picture:
    #    st.image(picture)
with col2:
    st.markdown("<h6 style='text-align: center; color: black;'>ĐẠI DIỆN BÊN B</h6>", unsafe_allow_html=True)
    


#file = /Users/supportsupport/Downloads/ChatGPT/mau-hop-dong-cho-vo-chong-vay-tien.pdf
#with open("mau-hop-dong-cho-vo-chong-vay-tien.pdf", "rb") as f:
#    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
#st.markdown(pdf_display, unsafe_allow_html=True)
# from io import StringIO

# uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
#     # To read file as bytes:
#     bytes_data = uploaded_file.getvalue()
#     st.write(bytes_data)

#     # To convert to a string based IO:
#     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#     st.write(stringio)

#     # To read file as string:
#     string_data = stringio.read()
#     st.write(string_data)

#     # Can be used wherever a "file-like" object is accepted:
#     dataframe = pd.read_csv(uploaded_file)
#     st.write(dataframe)