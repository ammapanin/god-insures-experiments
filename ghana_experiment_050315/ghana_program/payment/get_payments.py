# Code to collect all enumerator payments

import os
import datetime
import csv

base = os.path.dirname(os.path.realpath(__file__))

payments_path = os.path.join(base,
                             "payment_csv")

paypath = os.path.exists(payments_path)

def get_payment(fname):
    with open(fname, "rb") as payfile:
        p = list(csv.reader(payfile))
        desk_pay = tuple(p[0])
    return desk_pay

if paypath:
    desk_files = [os.path.join(payments_path, f) 
                  for f in os.listdir(payments_path)
                  if f[-3:] == "csv"]
    desk_payments = [get_payment(f) 
                     for f in desk_files]

    now = datetime.datetime.now().strftime("%d%m_%H%M")
    pay_write_file = os.path.join(base,
                                  "payments_{}.csv".format(now))

    with open(pay_write_file, "wb") as payfile:
        pay = csv.writer(payfile)
        [pay.writerow(desk)
         for desk in desk_payments]

    print "{} payments written to  {}".format(len(desk_payments, 
                                                  pay_write_file))

elif not paypath:
    print "Error!"

