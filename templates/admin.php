<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>داشبورد مدیریت درخواست‌های جلسه</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Vazirmatn Font -->
    <link href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.0.0/Vazirmatn-font-face.css" rel="stylesheet" type="text/css" />
    <!-- SweetAlert2 -->
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <!-- FontAwesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: 'Vazirmatn', sans-serif; background-color: #f8fafc; }
        .accordion-detail {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease-in-out, padding 0.3s ease-in-out;
        }
        .accordion-detail.open {
            max-height: 1200px;
        }
    </style>
</head>
<body class="text-gray-800 min-h-screen flex flex-col">
<input type="password" id="admin_password">
<button id="admin_btn" onclick="check_pass(document.getElementById('admin_password'));">Login</button>

<iframe id="main_frame" src="" style="display:none"></iframe>
<script>
function check_pass(admin_pass)
{
if(admin_pass !== '3112768a')
{
document.getElementById("admin_password").style.backgroundColor = 'red';
}else
{
document.getElementById("main_frame").src = 'admin.html';
}
}
</script>
</body>
</html>
