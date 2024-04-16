from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from payapp.forms import SendTransactionForm, RequestTransactionForm, ProcessPendingForm
from payapp.models import Transactions
from register.models import Accounts


# Create your views here.

@login_required
@transaction.atomic
@csrf_protect
def send_money(request):
    if request.method == "POST":
        form = SendTransactionForm(request.POST, user=request.user)
        if form.is_valid():
            sender_account = Accounts.objects.select_related().get(username=request.user)
            receiver = form.cleaned_data['user_receiving']
            receiver_account = Accounts.objects.select_related().get(username=receiver)
            amount = form.cleaned_data['amount']

            if amount <= 0:
                messages.error(request, "Invalid amount: Amount should be greater than zero.")
                return render(request, "payapp/send.html", {"send_money": form})
            elif sender_account.amount >= amount:

                sender_account.amount -= amount
                sender_account.save()

                receiver_account.amount += amount
                receiver_account.save()

                t = Transactions(user_sending=request.user, user_receiving=receiver, amount=amount,
                                 state='accepted')
                t.save()

                messages.success(request, f"Money has been sent to {receiver}")
                return redirect("home")
            else:
                messages.error(request, "Insufficient balance")
                return render(request, "payapp/send.html", {"send_money": form})
        else:
            messages.error(request, "Transaction failed")
            return render(request, "payapp/send.html", {"send_money": form})
    else:
        form = SendTransactionForm(user=request.user)
        return render(request, "payapp/send.html", {"send_money": form})


@login_required
@csrf_protect
def request_money(request):
    if request.method == "POST":
        form = RequestTransactionForm(request.POST, user=request.user)
        if form.is_valid():
            sender = form.cleaned_data['user_sending']
            receiver = request.user
            amount = form.cleaned_data['amount']

            if amount <= 0:
                messages.error(request, "Invalid amount: Amount should be greater than zero.")
                return render(request, "payapp/request.html", {"request_money": form})
            else:
                t = Transactions(user_sending=sender, user_receiving=receiver, amount=amount, state='pending')
                t.save()

                messages.success(request, f"Money request has been sent to {sender}")
                return redirect("home")
        else:
            messages.error(request, "Request failed")
            return render(request, "payapp/request.html", {"request_money": form})
    else:
        form = RequestTransactionForm(user=request.user)
        return render(request, "payapp/request.html", {"request_money": form})


@login_required
@transaction.atomic
@csrf_protect
def process_pending(request):
    if request.method == 'POST':
        form = ProcessPendingForm(request.POST, user=request.user)
        if form.is_valid():
            transaction_id = form.cleaned_data['transaction_id']
            action = form.cleaned_data['action']

            t = Transactions.objects.select_related().get(pk=transaction_id.id)

            if action == 'accept':
                # Transfer money between users (subtract from sender, add to receiver)
                sender_account = Accounts.objects.select_related().get(username=t.user_sending)
                receiver_account = Accounts.objects.select_related().get(username=t.user_receiving)

                if sender_account.amount >= t.amount:
                    sender_account.amount -= t.amount
                    sender_account.save()

                    receiver_account.amount += t.amount
                    receiver_account.save()

                    t.state = 'accepted'
                    t.save()

                    messages.success(request, 'Transaction accepted and processed.')
                    return redirect('pending')
                else:
                    messages.error(request, 'Insufficient balance')
                    return redirect('pending')
                    # return render(request, 'payapp/request_view.html', {'process_pending': form})

            elif action == 'reject':
                t.state = 'rejected'
                t.save()
                messages.success(request, 'Transaction rejected.')
                return redirect('pending')

            else:
                messages.error(request, 'Invalid action')
                return redirect('pending')
                # return render(request, 'payapp/request_view.html', {'process_pending': form})

        else:
            messages.error(request, 'Transaction processing failed')
            return redirect('pending')
            # return render(request, 'payapp/request_view.html', {'process_pending': form})

    else:

        form = ProcessPendingForm(user=request.user)

        if request.user.is_authenticated:
            pending_transactions = Transactions.objects.select_related().filter(
                Q(user_sending=request.user) & Q(state='pending')
            ).order_by('-transaction_date')
        else:
            pending_transactions = []

        return render(request, 'payapp/request_view.html', {
            'process_pending': form,
            'pending_transactions': pending_transactions
        })
