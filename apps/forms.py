import re

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import Form, Textarea, IntegerField, DecimalField
from django.forms.fields import CharField
from django.forms.models import ModelForm

from apps.models import User, Order, Thread, Product, AdminSetting, Payment


class AuthForm(Form):
    phone_number = CharField(max_length=50)
    password = CharField(max_length=10)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return make_password(password)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        digits_only = "+" + re.sub(r"\D", "", phone_number)
        return digits_only

    def save(self):
        phone_number = self.cleaned_data.get("phone_number")
        password = self.cleaned_data.get("password")
        obj, _ = User.objects.get_or_create(phone_number=phone_number, password=password)
        return obj


class ProfileForm(Form):
    first_name = CharField(required=False)
    last_name = CharField(required=False)
    district_id = CharField(required=False)
    address = CharField(required=False)
    telegram_id = IntegerField(required=False)
    about = CharField(required=False)

    def update(self, user):
        data = self.cleaned_data
        User.objects.filter(pk=user.id).update(**data)


class ChangePasswordForm(Form):
    old = CharField(required=False)
    new = CharField(required=False)
    confirm = CharField(required=False)

    def clean_confirm(self):
        new = self.data.get('new')
        confirm = self.cleaned_data.get('confirm')
        if new != confirm:
            raise ValidationError("Not Match!")

    def clean_new(self):
        return make_password(self.cleaned_data.get('new'))

    def update(self, user):
        password = self.cleaned_data.get('new')
        User.objects.filter(pk=user.id).update(password=password)


class OrderForm(Form):
    last_name = CharField(max_length=255)
    phone_number = CharField(max_length=20)
    product_id = IntegerField()
    thread_id = IntegerField(required=False)
    amount = DecimalField(max_digits=10, decimal_places=0, required=False)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        digits_only = "+" + re.sub(r"\D", "", phone_number)
        return digits_only

    def save(self, user):
        deliver_price = AdminSetting.objects.first().deliver_price
        order = Order.objects.create(**self.cleaned_data, owner_id=user.id)
        amount = order.product.price * order.quantity + deliver_price
        thread_id = self.cleaned_data.get('thread_id')
        if thread_id:
            thread = Thread.objects.filter(pk=thread_id).first()
            amount -= thread.discount_sum
        order.amount = amount
        order.save()
        return order


class ThreadForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False

    class Meta:
        model = Thread
        fields = 'name', 'discount_sum', 'product', 'user'

    def clean_discount_sum(self):
        product_id = self.data.get('product')
        product = Product.objects.filter(pk=product_id).first()
        discount_sum = self.cleaned_data.get('discount_sum')
        if discount_sum == None:
            discount_sum = 0
        if product.sell_price < discount_sum:
            raise ValidationError("Chegirma miqdori berilgandan ko'p")
        return discount_sum


class OrderModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment_operator'].required = False
        self.fields['quantity'].required = False
        self.fields['send_date'].required = False
        self.fields['district'].required = False
        self.fields['status'].required = False

    class Meta:
        model = Order
        fields = 'quantity', 'send_date', 'district', 'status', 'comment_operator'


class PaymentModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False

    class Meta:
        model = Payment
        fields = 'amount', 'card_number', 'user'

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 100000:
            raise ValidationError("Minimal yechib olish summasi 100 ming so'm!!!")
        return amount

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if not card_number.isdigit() or len(card_number) != 16:
            raise ValidationError("Karta raqamlarda muamo!!!")
        return card_number
