from django.contrib.auth.models import User

for i in range(1, 6):
    User.objects.create_user(
        username=f'user{i}',
        email=f'user{i}@example.com',
        password='password123'
    )
    print(f'Test user {i} created.')