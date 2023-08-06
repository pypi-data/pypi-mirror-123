class Vat:
    def __init__(self, name, money = 0.0 ,bmoney = 0.0):
        self.name = name
        self.money = money
        self.bmoney = bmoney
        

    def result1(self, money):
        self.money *= 1.07
        
        
    def result2(self, bmoney):
        self.bmoney -= self.money
        
    def check_money(self):
        print("ราคารวมภาษีมูลค่าเพิ่ม: {} บาท".format(self.money))
        print("ภาษีมูลค่าเพิ่ม 7%: {} บาท".format(self.bmoney))

a1 = Vat("PP")
a1.money = 1000
a1.result1(1000)

a1.bmoney = 1000
a1.result2(1000)


a1.check_money()