import unittest
import main

#Urocza klasa do testowania mojego ambitnego programu
class GIR_TEST(unittest.TestCase):
	def test_NoModfArgs(self):
		args = "gir -g Kamarov/projekt-testowy".split()
		gir = main.GIR()
		flen = len(args)
		gir.commandManage(args)
		assert flen == len(args)
	
	
	pass


#uruchamianie testu
if __name__ == "__main__":
	unittest.main()
