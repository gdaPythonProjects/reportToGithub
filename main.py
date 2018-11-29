import sys, getopt
from github import Github
import os
import string


#argv = sys.argv
#argc = len(sys.argv)
class GIR:

	#Funkcja do logowania sie na githuba
	def loginToGithub(self,_userName, _passwd):
		return Github(_userName, _passwd)

	#Interfejs logowania do githuba
	def loginProcedure(self):
		Gname = input("Github user name: ")
		Gpasswd = input("Github password: ")
		return self.loginToGithub(Gname, Gpasswd)


	#funkcja do listowania bledow - zwraca posortowane wg daty utworzenia bledy z danego repo
	def listIssuesFromRepo(self,_gitHub, _repoName, wall=True):
		repo = _gitHub.get_repo(_repoName)
		issues = repo.get_issues(state="open")

		#wypisujemy intefajse
		if wall == True:
			print ("*"*40)
			print ("Issues List for repo ", repo.name, ":")
			print ("*"*40, end="\n\n")

		#pobieramy posortowane bledy wg. daty ich utworzenia
		toRet = sorted(issues, key=lambda x:  x.created_at)

		if(wall == False):
			return toRet

		for i in sorted(issues, key=lambda x:  x.created_at):
			print (i.title, end="\t")
			print (i.user, ": ")
			print ("\n\n",i.body)
	
		return toRet


	#laduje tres bledu z wskazanego pliku o ile istnieje 
	def loadIssueMsgFromFile(self, _filename):
		if not os.path.isfile(_filename):
			print("File: ",_filename, " not exists!")
			return ""
		f = open(_filename, "r")
		toRet = f.read()
		f.close()
		return toRet


	#Funkcja do zapisu bledow do wskazanego pliku
	def saveIssuesToFile(self, _github, _repoName, _filename):
	
		if os.path.isfile(_filename):
			inp = input("Do you want overwrite file? (Y/N): ")
	
			while(str(inp).upper() !=  "Y") and (str(inp).upper() !=  "N"):
				inp = input("(Y/N)")
				print (inp)
			#user sie rozmyslil
			if inp == "N":
				return

		#TODO: exceptiony
		f = open(_filename, "w")
		iList = self.listIssuesFromRepo (_github, _repoName, wall=False)
		for i in iList:
			f.write(str(i.created_at))
			f.write("\n")
			f.write(str(i.user))
			f.write("\n")
			f.write(str(i.title))
			f.write("\n")
			f.write(i.body)
			f.write("\n\n")
		f.close()
		pass

	#Pobieramy wiadomosc issue z pliku o ile istnieje
	def getBodyFromFile(self,_filename):
		if not os.path.isfile(_filename):
			print("File: %s not exists!", _filename)
			return ""
		f = open(_filename, "r")
		return f.read()


	#wrzucamy zalogowane repo i wrzucamy podany issue
	def sendIssue(self, _repo, _tittle, _body):
		_repo.create_issue(title=_tittle, body=_body)

	#Pomoc przy skladni
	def manPage(self):
		print ("gir - help page")
		print ("\n\n")
		print ("Usage:\n\n")
		print ("\tgir -g [--get] {repo name}: get issues from repo and display on console")
		print ("\tgir -g [--get] {repo name} -f [--file] {filename}: get issues from repo and save to file")
		print ("\tgir -p [--push] {repo name} -t [--title] -f [--filename]: send issue to repo using title and issue body from file")
		print ("\tgir -h [--help] : this page")
		print ("\n\n\n")
		print ("Examples:\n\n")
		print ("\tgir -g Microsoft/MS-DOS -f out.txt")
		print ("\tgir -p Microsoft/MS-DOS -t \"Too old\"-f myIssueBody.txt")
		print ("\n\n\n")
		pass


	#wrzucamy tablice polecen i w zaleznosci od tego podejmujey akcje 
	def commandManage(self, _args):
		_args = _args[1:]
		argc = len(_args)

		#gir -h(--help)
		if argc == 1:
			#man page
			try:
				opt, _args = getopt.getopt(_args, "h", ["help"])
				#print(opt)
			except getopt.GetoptError as err:
				print(str(err))
				return
			self.manPage()
			pass
		#gir -g(--get) [repo name]
		elif argc == 2:
			try:
				opt, _args = getopt.getopt(_args, "g:", ["get="])
				#print(opt)
			except getopt.GetoptError as err:
				print(str(err))
				return
			g = self.loginProcedure()
			self.listIssuesFromRepo(g, opt[0][1], wall=True)

			pass
		#gir -g(--get) [repo name] -f(--file) [output file]
		elif argc == 4:
			try:
				opt, _args = getopt.getopt(_args, "g:f:", ["get=","file="])
				#print(opt)
			except getopt.GetoptError as err:
				print(str(err))
				return
			g = self.loginProcedure()
			aRepName = opt[0][1]
			aFileName = opt[1][1]
			self.saveIssuesToFile(g, aRepName, aFileName)
			pass
		#gir -p(--push) [repo name] -t(--title) [issue title] -f(--file) [input file with body]
		elif argc == 6:
			try:
				opt, _args = getopt.getopt(_args, "p:t:f:", ["push=", "title=","file="])
				#print(opt)
			except getopt.GetoptError as err:
				print(str(err))
				return
			g = self.loginProcedure()
			aRepName = opt[0][1]
			aTit = opt[1][1]
			aFile = opt[2][1]
			tmp = g.get_repo(aRepName)
		
			msgBody = self.getBodyFromFile(aFile)
			if msgBody == "":
				print("There is no body to send issue!")
				return
			self.sendIssue(tmp, aTit, msgBody)
			pass
		#man page
		else:
			self.manPage()
			pass



		pass

if __name__ == "__main__":
	argv = sys.argv
	tmp = GIR()
	tmp.commandManage(argv)
