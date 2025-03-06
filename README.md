## Thông tin cá nhân (Họ tên, mã sinh viên)
- Nguyễn Ngọc Lân, 22635801
- Nguyễn Tấn Minh, 22643511
## Mô tả project
### Ý tưởng xây dựng **Tiny To-Do List** bằng Flask  

Tiny To-Do List là một ứng dụng web **đơn giản, nhẹ, dễ sử dụng** giúp người dùng quản lý danh sách công việc hàng ngày. Ứng dụng cho phép người dùng **thêm công việc, đánh dấu hoàn thành, xóa công việc**, và hiển thị danh sách công việc theo trạng thái. Ngoài ra, để mở rộng tính năng, ứng dụng sẽ có hệ thống **đăng nhập**, hỗ trợ nhiều **người dùng** với phân quyền **user và admin**, giúp mỗi người quản lý danh sách công việc riêng biệt.  

---

### **Chức năng chính**  

#### 1️⃣ **Quản lý công việc**  
Người dùng có thể **thêm công việc mới** bằng cách nhập nội dung vào ô input và nhấn nút **"Thêm"**. Danh sách công việc sẽ được hiển thị dưới hai danh mục:  
- **Công việc chưa hoàn thành**: Những công việc đang cần thực hiện.  
- **Công việc đã hoàn thành**: Những công việc đã được đánh dấu xong.  

Người dùng có thể **đánh dấu hoàn thành** công việc bằng cách tick vào checkbox. Khi đó, công việc sẽ được chuyển sang danh mục "Đã hoàn thành". Nếu muốn xóa một công việc đã hoàn thành, người dùng có thể nhấn nút **"Xóa"**.  

#### 2️⃣ **Đăng nhập & phân quyền**  
Hệ thống sẽ có hai loại tài khoản:  
- **Người dùng (User)**: Chỉ có thể quản lý danh sách công việc của riêng họ.  
- **Quản trị viên (Admin)**: Có quyền quản lý tất cả tài khoản người dùng, xem danh sách công việc của mọi người, và thực hiện các thao tác như chỉnh sửa hoặc xóa công việc.  

Người dùng cần **đăng ký tài khoản** bằng email và mật khẩu. Sau khi đăng ký, họ có thể **đăng nhập** để truy cập danh sách công việc cá nhân.  

#### 3️⃣ **Trang quản trị (Admin Dashboard)**  
Admin sẽ có một **bảng điều khiển (Dashboard)** để quản lý toàn bộ hệ thống, bao gồm:  
- Xem danh sách tất cả tài khoản người dùng  
- Xóa tài khoản vi phạm hoặc không hoạt động  
- Xem và quản lý công việc của từng người dùng  

#### 4️⃣ **Chỉnh sửa công việc**  
Người dùng có thể chỉnh sửa nội dung công việc nếu cần thay đổi hoặc cập nhật thông tin.  

#### 5️⃣ **Lưu trữ dữ liệu**  
Dữ liệu sẽ được lưu trong **SQLite**, giúp người dùng truy cập công việc mọi lúc mọi nơi mà không bị mất dữ liệu.  

---

### **Luồng hoạt động**  
1️⃣ Người dùng đăng ký tài khoản, đăng nhập vào hệ thống.  
2️⃣ Họ có thể thêm công việc mới vào danh sách cá nhân.  
3️⃣ Công việc hiển thị theo hai trạng thái: **Chưa hoàn thành** và **Đã hoàn thành**.  
4️⃣ Người dùng có thể đánh dấu hoàn thành hoặc xóa công việc.  
5️⃣ Admin có quyền quản lý danh sách công việc và tài khoản người dùng.  

---

### **Hướng phát triển mở rộng**  
- **Thêm thông báo nhắc nhở công việc** (gửi email hoặc hiển thị trên giao diện).  
- **Hỗ trợ deadline**: Đặt thời gian hoàn thành cho từng công việc.  
- **Tích hợp API để đồng bộ dữ liệu với ứng dụng di động**.  
- **Hỗ trợ chế độ nhóm**: Người dùng có thể chia sẻ công việc với người khác.  

Tiny To-Do List là một ứng dụng phù hợp cho cả cá nhân và nhóm nhỏ, giúp tối ưu hóa công việc hàng ngày theo cách đơn giản và hiệu quả. 🚀
## Hướng dẫn cài đặt, chạy
Hãy cd đến thư mực bạn vừa clone và thực hiện các câu lệnh sau để cài đặt và chạy ứng dụng:<br>
- python -m venv myenv 
- myenv\Scripts\Activate
- pip install flask 
- pip install flask-session
- $env:FLASK_APP = flaskr
- flask run 
## Link project đã triển khai của bạn
https://github.com/wsunicorn/flask-tiny-app