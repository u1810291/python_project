# coding=utf8
from app import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)


class User(Base):
    __tablename__ = 'user'

    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), index=True, unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    orders = db.relationship('Order', backref='user')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User: {}, {}>'.format(self.name, self.email)


class Order(Base):
    __tablename__ = 'order'

    SERVICE_CONSOLIDATION = 'consolidation'
    SERVICE_PURCHASE = 'purchase'

    STATUS_PENDING = 'pending'  # ожидание рассмотрения оператором
    STATUS_GOODS_PAYMENT_WAITING = 'goods_payment_waiting'  # Ожидание оплаты товаров заказчиком
    STATUS_STOCK_DELIVERY_WAITING = 'stock_delivery_waiting'  # Ожидание доставки на склад в США
    STATUS_DELIVERY_PAYMENT_WAITING = 'delivery_payment_waiting'  # Ожидание оплаты заказчиком услуги доставки
    STATUS_CUSTOMER_DELIVERY_WAITING = 'customer_delivery_waiting'  # Ожидание доставки товара заказчику
    STATUS_FINISHED = 'finished'  # Товар успешно доставлен
    STATUS_REJECTED = 'rejected'  # Отменя по какой-либо причине

    status = db.Column(db.String(256), nullable=False)
    service = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shipping_address = db.Column(db.String(256), nullable=False)
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')
    invoices = db.relationship('Invoice', backref='order', cascade='all, delete-orphan')

    @property
    def service_label(self):
        labels = {
            Order.SERVICE_CONSOLIDATION: 'Консолидация',
            Order.SERVICE_PURCHASE: 'Купить и доставить',
        }
        return labels[self.service]

    @property
    def status_label(self):
        return self.get_status_label_by(self.status)

    @property
    def invoice_purchase(self):
        return self.__get_invoice_by_type(Invoice.TYPE_PURCHASE)

    @property
    def invoice_consolidation(self):
        return self.__get_invoice_by_type(Invoice.TYPE_CONSOLIDATION)

    @property
    def weight(self):
        return sum(item.weight for item in self.items if item.weight is not None)

    @property
    def allowed_statuses(self):
        return self.get_allowed_statuses()

    @classmethod
    def get_allowed_statuses(cls):
        return [
            Order.STATUS_PENDING,
            Order.STATUS_GOODS_PAYMENT_WAITING,
            Order.STATUS_STOCK_DELIVERY_WAITING,
            Order.STATUS_DELIVERY_PAYMENT_WAITING,
            Order.STATUS_CUSTOMER_DELIVERY_WAITING,
            Order.STATUS_FINISHED,
            Order.STATUS_REJECTED,
        ]

    @classmethod
    def get_status_label_by(cls, status):
        labels = {
            Order.STATUS_PENDING: 'В ожидании',
            Order.STATUS_GOODS_PAYMENT_WAITING: 'Ожидает оплаты товаров',
            Order.STATUS_STOCK_DELIVERY_WAITING: 'Ожидает доставки на склад',
            Order.STATUS_DELIVERY_PAYMENT_WAITING: 'Ожидает оплаты доставки',
            Order.STATUS_CUSTOMER_DELIVERY_WAITING: 'Ожидает получения',
            Order.STATUS_FINISHED: 'Успешно доставлено',
            Order.STATUS_REJECTED: 'Отменен',
        }
        return labels[status]

    def __get_invoice_by_type(self, type):
        for invoice in self.invoices:
            if invoice.type == type:
                return invoice

        return None




class OrderItem(Base):
    __tablename__ = 'order_item'

    # common
    url = db.Column(db.String(2048), nullable=False)
    comment = db.Column(db.String(2048))
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    weight = db.Column(db.Float)
    price = db.Column(db.Float)

    # consolidation
    tracking_id = db.Column(db.String(256))

    # purchase
    size = db.Column(db.String(256))
    color = db.Column(db.String(256))
    discount = db.Column(db.String(256))


class Invoice(Base):
    __tablename__ = 'invoice'

    TYPE_CONSOLIDATION = 'consolidation'
    TYPE_PURCHASE = 'purchase'
    SIMSIM_PERCENT = 6.0

    type = db.Column(db.String(256), nullable=False)
    is_paid = db.Column(db.Boolean, nullable=False, default=False)
    stripe_id = db.Column(db.String(256))

    # purchase
    goods_price_total = db.Column(db.Float)

    # consolidation
    delivery_total = db.Column(db.Float)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

    @property
    def simsim_commission(self):
        if self.type != self.TYPE_PURCHASE:
            return 0

        return round(self.goods_price_total * self.SIMSIM_PERCENT / 100, 2)

    @property
    def total(self):
        if self.type == self.TYPE_CONSOLIDATION:
            return self.delivery_total
        else:
            return round(self.goods_price_total + self.simsim_commission, 2)


class Page(Base):
    slug = db.Column(db.String(256), nullable=False, unique=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)


shop_tags = db.Table('shop_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('shop_id', db.Integer, db.ForeignKey('shop.id'))
)


class Shop(Base):
    domain = db.Column(db.String(256), nullable=False, unique=True)
    image = db.Column(db.String(256), nullable=False)
    weight = db.Column(db.Float, nullable=False, default=1)
    tags = db.relationship('Tag', secondary=shop_tags, backref=db.backref('shops', lazy='select'))


class Tag(Base):
    title = db.Column(db.String(256), nullable=False)
    weight = db.Column(db.Float, nullable=False, default=1)


