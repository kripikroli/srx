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

def get_key(res_by):
    if res_by == 'transaction':
        key = 'transaction_id'
    else:
        key = 'created_at'
    return key

def get_chart(chart_type, data, results_by, **kwargs):

    plt.switch_backend('AGG')

    fig = plt.figure(figsize=(10,4))

    key = get_key(results_by)
    d = data.groupby(key, as_index=False)['total_price'].agg('sum')

    if chart_type == 'barchart':
        # plt.bar(data['transaction_id'], data['price'])
        # plt.bar(d[key], d['total_price'])
        # sns.barplot(x='transaction_id', y='price', data=data)
        sns.barplot(x=key, y='total_price', data=d)

    elif chart_type == 'piechart':
        labels = kwargs.get('labels')
        # plt.pie(data=data, x='price', labels=labels)
        plt.pie(data=d, x='total_price', labels=d[key])

    elif chart_type == 'linechart':
        # plt.plot(data['transaction_id'], data['price'], color='orange', marker='o')
        plt.plot(d[key], d['total_price'], color='orange', marker='o')

    else:
        print('no chart')

    plt.tight_layout()

    chart = get_graph()

    return chart