from django.urls import path
from.import views
urlpatterns=[
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('blog',views.blog,name='blog'),
    path('shop',views.shop,name='shop'),
    path('service',views.service,name='service'),    
    path('login/', views.loginpage, name='loginpage'),
    path('adminindex',views.admin,name='admin'),
    path('addproduct/',views.add_product, name='add_product'),
    path('viewproduct/',views.viewproduct, name='viewproduct'),
    path('update_product/<int:id>/',views.update_product,name="update_product"),
    path('del_product/<int:id>/',views.del_product,name="del_product"),
    path('add_complaint/', views.add_complaint, name='add_complaint'),
    path('complaint_success/', views.complaint_success, name='complaint_success'),
    path('view_complaints/', views.view_complaints, name='view_complaints'),
    path('logout_request/', views.logout_request, name='logout_request'),
    path('pro/<int:id>/', views.pro, name='pro'),
    path('view_cart', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout',views.checkout, name='checkout'),
    path('config/', views.stripe_config),  # new
    path('create-checkout-session/', views.create_checkout_session), 
    path('payment',views.payment,name='payment'),
    path('payment_success',views.payment_success,name='payment_success'),
    path('process_payment',views.process_payment,name='process_payment'),
    path('payment_successful',views.payment_successful,name='payment_successful'),
    path('payment_statuss',views.payment_statuss,name='payment_statuss'),
    path('process_payment/<int:product_id>/', views.process_payment, name='process_payment'),
    path('view_payment/', views.view_payment, name='view_payment'),
    path('payment_status',views.payment_status,name='payment_status'),
    path('Review',views.payment_status,name='payment_status'),
    path('Review_rate/<int:product_id>/',views.Review_rate,name='Review_rate'),
    path('review_success',views.review_success,name='review_success'),
    path('view_reviews',views.view_reviews,name='view_reviews'),
    path('view_booking/',views.view_booking, name='view_booking'),
    path('admin_view_cart',views.admin_view_cart,name='admin_view_cart'),
    path('custorders',views.custorders,name='custorders'),
    path('addorder',views.addorder,name='addorder'),
    path('vieworder',views.vieworder,name='vieworder'),
    path('updateorder/<int:id>/',views.updateorder,name='updateorder'),
    path('vieworder',views.vieworder,name='vieworder'),

    











]