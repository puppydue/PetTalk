Tôi đang làm việc trong dự án Django có tên **PetTalk**, cấu trúc project như sau:

```
PetTalk/
├── manage.py
│
├── PetTalk/              # Project chính (chứa settings, urls, views)
│
├── forum/                # App chính để test layout base
│
├── templates/            # Chứa file HTML (base.html, ...)
│
└── static/
    └── css/
        └── base.css
```

Hiện dự án đã có:
- `base.html`: giao diện tổng thể của website (header, sidebar, layout 3 cột, kế thừa được cho các app khác)
- `base.css`: stylesheet toàn cục, đã chỉnh:
  - màu nền trang thành `#FFF2CC`
  - giãn cách giữa các ô sidebar bằng `margin-bottom`
  - giữ layout responsive (ẩn sidebar ở màn hình nhỏ)
- `forum` app có:
  - `views.py` với view `post_list` dùng để test base layout
  - `urls.py` với path `''` trỏ đến `post_list`
  - `templates/forum/post_list.html` kế thừa từ base.html (chỉ có nội dung trống để kiểm tra layout)
- `settings.py` đã được cấu hình:
  - `TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']`
  - `STATICFILES_DIRS = [BASE_DIR / 'static']`
  - Đã thêm `'forum'` vào `INSTALLED_APPS`
- `urls.py` trong project chính đã `include('forum.urls')`
- Đã test thành công tại `http://127.0.0.1:8000/forum/`
  → Hiển thị giao diện PetTalk với header, sidebar, màu nền vàng nhạt chuẩn

Mục tiêu tiếp theo: mở rộng layout này cho các app khác (events, badges, moderation, accounts),  
mỗi app sẽ có file `urls.py`, `views.py`, `templates/<app>/...` kế thừa `base.html`.

👉 ChatGPT, hãy tiếp tục hỗ trợ tôi dựa trên setup Django này (không cần tạo lại base hoặc cấu trúc).

# 👥 TEAM_GUIDE.md — Hướng dẫn làm việc nhóm với Git/GitHub cho PetTalk

> Dành cho **người mới hoàn toàn**. Làm theo tuần tự là chạy được ngay.  
> Mọi lệnh đều gõ trong **Terminal** (PyCharm Terminal hoặc CMD/PowerShell).

---

## 0) Cài và cấu hình ban đầu (mỗi máy chỉ làm 1 lần)
```bash
# Kiểm tra đã cài Git chưa (có version là OK)
git --version

# Cấu hình tên & email (hiển thị trên commit)
git config --global user.name "Tên của bạn"
git config --global user.email "email-dang-ky-github@example.com"

# (khuyến nghị) Lưu đăng nhập HTTPS để đỡ nhập lại
git config --global credential.helper store
```

> Nếu dùng SSH: `ssh-keygen -t ed25519` → copy `~/.ssh/id_ed25519.pub` vào GitHub (Settings → SSH keys).

---

## 1) Lấy mã nguồn về máy (clone)
```bash
# Chọn thư mục muốn lưu code
cd D:\5. Junior\Lập trình web\Dự án\PetTalk\GitHub

# Clone project
git clone https://github.com/<org-or-user>/PetTalk.git

# Vào folder dự án
cd PetTalk
```

### Thiết lập môi trường Python
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 2) Quy ước nhánh (branch) & đặt tên
- Mỗi tính năng / task = **1 nhánh riêng**.
- Mẫu tên nhánh: `<tên-người>/<module>-<mô-tả-ngắn>`  
  Ví dụ:
  - `nam`
  - `minh`
  - `khanh`
  - `hoan`
  - `hung`

Tạo nhánh mới từ `main`:
```bash
git checkout main :Di chuyển đến nhánh Main
git pull: Lấy đồng bộ file từ hệ thống xuống local
git checkout -b minh: tạo nhánh mới tên là "minh"
```

Kiểm tra nhánh hiện tại đang ở nhánh nào:
```bash
git branch
```

---

## 3) Quy trình làm việc hằng ngày
1. **Pull** code mới nhất về `main`:
   ```bash
   git checkout main
   git pull
   ```
2. **Tạo/đổi sang nhánh cá nhân** cho task đang làm:
   ```bash
   git checkout -b <ten-nhanh-moi>   # nếu là task mới
   # hoặc
   git checkout <ten-nhanh-cu>       # nếu tiếp tục task cũ
   ```
3. **Code → Test local**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```
4. **Commit theo lô nhỏ, rõ nghĩa**:
   ```bash
   git add .
   git commit -m "[Forum] Add: Post create/list/detail views"
   ```
5. **Push nhánh lên GitHub**:
   ```bash
   git push -u origin <ten-nhanh>
   ```
6. **Tạo Pull Request (PR)** trên GitHub → gắn reviewer → chờ review → **merge** vào `main`.

7. **Cập nhật lại nhánh của bạn sau khi `main` đổi**:
   ```bash
   git checkout <ten-nhanh-cua-ban>
   git fetch
   git merge main        # (dễ dùng cho người mới)
   # hoặc: git rebase main
   # Sửa conflict nếu có → chạy test lại
   ```

---

## 4) Quy tắc commit & đặt tên
- Cấu trúc commit: `[App] <Action>: <Mô tả ngắn>`
- Action gợi ý: `Add`, `Fix`, `Update`, `Refactor`, `Remove`, `Style`
- Ví dụ:
  - `[Events] Add: Event create form & template`
  - `[Moderation] Fix: wrong status filter`
  - `[Accounts] Update: profile view + tests`

---

## 5) File KHÔNG được commit (đã trong .gitignore)
```
venv/
.env
db.sqlite3
__pycache__/
.idea/
.vscode/
.DS_Store
Thumbs.db
media/
```

---

## 6) Tạo Pull Request (PR) đúng chuẩn
1. Push nhánh lên GitHub: `git push -u origin <ten-nhanh>`  
2. Mở repo → **Compare & pull request**.  
3. **Title**: ngắn gọn, kèm app.  
4. **Description**: liệt kê thay đổi chính, ảnh chụp UI nếu có.  
5. **Assign** 1–2 reviewer.  
6. Khi được approve → **Merge** → xoá nhánh nếu đã xong.

> PR nhỏ, rõ ràng thì review/merge nhanh và ít conflict.

---

## 7) Xử lý conflict (đụng code)
- Khi `merge`/`rebase` báo conflict:
  1. Mở **PyCharm → Git → Resolve Conflicts** (UI 3 cột).
  2. Chọn giữ phần đúng (`Accept Yours` / `Accept Theirs` / hoặc merge thủ công).
  3. Lưu file → `git add <file>`
  4. Tiếp tục merge/rebase:
     ```bash
     git merge --continue      # nếu đang merge
     git rebase --continue     # nếu đang rebase
     ```
  5. Chạy lại:
     ```bash
     python manage.py migrate
     python manage.py runserver
     ```

---

## 8) Các lệnh nhanh thường dùng
```bash
# Trạng thái thay đổi
git status

# Xem log commit ngắn gọn
git log --oneline --graph --decorate --all

# Hủy thay đổi file chưa add
git checkout -- path\to\file

# Hủy file đã add (bỏ staged)
git reset HEAD path\to\file

# Đổi nhánh
git checkout main

# Xóa nhánh local đã merge xong
git branch -d <ten-nhanh>

# Xóa nhánh trên remote
git push origin --delete <ten-nhanh>
```

---

## 9) Lỗi phổ biến & cách sửa nhanh
| Lỗi | Nguyên nhân | Cách sửa |
|-----|-------------|---------|
| `! [rejected] main -> main (fetch first)` | Repo remote đã có commit (README, .gitignore) | `git pull origin main --allow-unrelated-histories` rồi `git push` |
| `error: failed to push some refs` | Local cũ hơn remote | `git pull --rebase` rồi `git push` |
| Conflict khi merge | Hai người sửa cùng dòng | Resolve conflict trong PyCharm → add → continue |
| Commit nhầm vào `main` | Lỡ làm trên nhánh chính | Tạo nhánh mới từ commit đó: `git checkout -b <ten-nhanh>` rồi tiếp tục làm trên nhánh mới |
| Quên add requirements | Máy khác chạy thiếu lib | Cài lib → `pip freeze > requirements.txt` → commit file này |

---

## 10) Data & môi trường dùng chung
- Cấu hình bí mật để trong `.env` (KHÔNG commit).
- Dùng `requirements.txt` để đồng bộ thư viện:
  ```bash
  pip install <ten-thu-vien>
  pip freeze > requirements.txt
  git add requirements.txt
  git commit -m "Update: requirements with <ten-thu-vien>"
  git push
  ```
- (Tuỳ chọn) Chia sẻ dữ liệu mẫu:
  ```bash
  # Xuất data mẫu (chỉ model cần thiết)
  python manage.py dumpdata app_name.ModelName --indent 2 > sample_data.json
  # Nạp data mẫu
  python manage.py loaddata sample_data.json
  ```

---

## 11) Vai trò & phạm vi chỉnh sửa (khuyến nghị)
- `settings.py`, `urls.py`, `base.html`: thay đổi có **review**.
- Mỗi người **chỉ sửa app của mình** trừ khi fix bug chung.
- Tạo Issue/Task cho mỗi việc → gắn nhánh tương ứng.

---

## 12) Checklist trước khi tạo PR
- [ ] Pull `main` mới nhất & merge vào nhánh đang làm
- [ ] Chạy `makemigrations`, `migrate`, `runserver` OK
- [ ] Không commit file nhạy cảm/venv/db
- [ ] Cập nhật `requirements.txt` nếu cài lib mới
- [ ] Screenshot UI (nếu có thay đổi giao diện)

---

## 13) Glossary nhanh
- **Repository (repo):** “Kho” code trên GitHub.
- **Clone:** Tải repo về máy.
- **Commit:** Một mốc thay đổi đã lưu.
- **Branch:** Nhánh làm việc song song.
- **Pull Request (PR):** Yêu cầu gộp code vào nhánh khác (thường là `main`).
- **Merge/Rebase:** Hợp nhất lịch sử.
- **Conflict:** Đụng dòng code, cần giải quyết thủ công.

---

> **Mọi người nhớ:** luôn `git pull` trước khi bắt đầu ngày mới; mỗi task = 1 nhánh; PR nhỏ + rõ = merge nhanh. Cần hỗ trợ thì ping vào nhóm! 🚀
