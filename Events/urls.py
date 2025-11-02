from django.urls import path
from . import views

urlpatterns = [
    path('tao/', views.tao_su_kien, name='tao_su_kien'),
    path('chinh-sua/<int:event_id>/', views.chinh_sua_su_kien, name='chinh_sua_su_kien'),
    path('<int:event_id>/xoa/', views.xoa_su_kien, name='xoa_su_kien'),
    path('phe-duyet/', views.phe_duyet_su_kien, name='phe_duyet_su_kien'),
    path('<int:event_id>/dang-ky/', views.dang_ky_tham_gia, name='dang_ky_tham_gia'),
    path('<int:event_id>/huy-dang-ky/', views.huy_dang_ky_tham_gia, name='huy_dang_ky_tham_gia'),
    path('', views.danh_sach_su_kien, name='danh_sach_su_kien'),
    path('nguoi-dang-ky/<int:event_id>/', views.danh_sach_nguoi_dang_ky, name='danh_sach_nguoi_dang_ky'),
]
