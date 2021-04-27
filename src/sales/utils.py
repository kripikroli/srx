import uuid, base64
from customers.models import Customer
from profiles.models import Profile
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns


def generate_code():
    return str(uuid.uuid4()).replace('-', '').upper()[:12]

def get_salesman_from_id(val):
    return Profile.objects.get(id=val).user.username

def get_customer_from_id(val):
    return Customer.objects.get(id=val)


def get_graph():

    buffer = BytesIO()

    plt.savefig(buffer, format='png')

    buffer.seek(0)

    image_png = buffer.getvalue()

    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')

    buffer.close()

    return graph


def get_chart(chart_type, data, **kwargs):

    plt.switch_backend('AGG')

    fig = plt.figure(figsize=(10,4))

    if chart_type == 'barchart':
        # plt.bar(data['transaction_id'], data['price'])
        sns.barplot(x='transaction_id', y='price', data=data)

    elif chart_type == 'piechart':
        labels = kwargs.get('labels')
        plt.pie(data=data, x='price', labels=labels)

    elif chart_type == 'linechart':
        plt.plot(data['transaction_id'], data['price'], color='orange', marker='o')

    else:
        print('no chart')

    plt.tight_layout()

    chart = get_graph()

    return chart