os.chdir('/Users/aserwaahWZB/Projects/Ghana religion/Design documents/data processing')



days = [11, 15]
month_days = ["02_{}".format(i) for i in days]

raw_files = list()

for day in month_days:
    day_files = os.listdir(os.path.join(os.getcwd(),
                                        "payments",
                                        day))
    day_files_folder = [os.path.join("payments", day, fname)
                        for fname in day_files]
    raw_files.extend(day_files_folder)


all_pay = list()

for name in raw_files:
    with open(name, "rU") as myfile:
        pay = [l for l in csv.reader(myfile)]
        all_pay.extend(pay)

with open("all_payments.csv", "w") as myfile:
    bob = csv.writer(myfile)
    [bob.writerow(r) for r in all_pay]
