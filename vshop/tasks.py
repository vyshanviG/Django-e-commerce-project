from celery import shared_task
from .models import Transaction
import time
import random

@shared_task
def process_payment(transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)

    # Simulate gateway delay
    time.sleep(5)

    success = random.choice([True, True, False])  # mostly success

    if success:
        transaction.status = 'success'
        transaction.payment_id = f"PAY-{transaction.id}"
        transaction.save()

        order = transaction.order
        order.status = 'paid'
        order.save()
    else:
        transaction.status = 'failed'
        transaction.save()

    return transaction.status