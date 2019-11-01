from collections import namedtuple

import sys

class standard():
	초성들 = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ","ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
	중성들 = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ","ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
	종성들 = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ","ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

	이중모음 = ["ㅑ", "ㅒ", "ㅕ", "ㅖ", "ㅘ", "ㅙ", "ㅛ", "ㅝ", "ㅞ", "ㅠ", "ㅢ"]
	자음 = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ","ㅅ", "ㅆ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

	def __init__(self):
		self.letters = []
		self.pronunciation = []
		self.error = False

	def fileread(self, input):
		#self.letters = []
		#self.pronunciation = []
		input = sys.argv[1]

		filename_first = '../test/KsponSpeech_'
		filename_third = '.txt'
		filename_second = ''

		if int(input) < 10:
			filename_second = '00000' + input
		elif int(input) < 100:
			filename_second = '0000' + input
		elif int(input) < 1000:
			filename_second = '000' + input
		elif int(input) < 10000:
			filename_second = '00' + input
		elif int(input) < 100000:
			filename_second = '0' + input
		else:
			filename_second = input

		filename = filename_first + filename_second + filename_third

		f = open(filename, 'r')
		data = f.read()
		self.run(data)
		f.close()

	def run(self, input):
		for c in input:
			self.divide(c)

	def divide(self, c):
		letter = namedtuple('Coordinate',['초성','중성','종성'])

		if ord('가') <= ord(c) <= ord('힣'):
			한글번호 = ord(c) - ord("가")
			종성번호 = int(한글번호 % 28)
			중성번호 = int(((한글번호 - 종성번호) / 28 ) % 21)
			초성번호 = int((((한글번호 - 종성번호) / 28 ) / 21))

			letter.종성 = self.종성들[종성번호]
			letter.중성 = self.중성들[중성번호]
			letter.초성 = self.초성들[초성번호]

			self.letters.append(letter)

		elif ord(c) in [ord('.') , ord(',') , ord('/')]:
			letter.초성 = " "
			letter.중성 = " "
			letter.종성 = " "

			self.letters.append(letter)
			

		

	def printLetters(self):
		for letter in self.letters:
			print(letter.초성, letter.중성, letter.종성)
	
	def printPronunciation(self):
		for letter in self.pronunciation:
			print(letter.초성, letter.중성, letter.종성)

			'''if(self.error == False):
				print(letter.초성, letter.중성, letter.종성)
			elif(self.error == True):
				print("Warning! This file has an Error")'''

	def standardrule(self):
		for i in self.letters:
			self.pronunciation.append(i)
		self.standard5()
		self.standard9()
		self.standard10()
		self.standard11()
		self.standard12()
		self.standard13_14()
		self.standard15()
		#self.standard16(self.input)
		self.standard17()
		self.standard18()
		self.standard19()
		self.standard20()
		self.standard23()
		self.standard24_25()
		self.standard30()


		self.standardㅇ()

	def standard5(self):
		'''ㅑ ㅒ ㅕ ㅖ ㅘ ㅙ ㅛ ㅝ ㅞ ㅠ ㅢ’는 이중 모음으로 발음한다.
			다만 3. 자음을 첫소리로 가지고 있는 음절의 ‘ㅢ’는 [ㅣ]로 발음한다'''

		for i in range(0, len(self.letters)):
			if self.letters[i].중성 == "ㅢ" and self.letters[i].초성 in self.자음:
				self.pronunciation[i].중성 = "ㅣ"

	def standard9(self):
		'''받침 ‘ㄲ, ㅋ’, ‘ㅅ, ㅆ, ㅈ, ㅊ, ㅌ’, ‘ㅍ’은 어말 또는 자음 앞에서 각각 대표음 [ㄱ, ㄷ, ㅂ]으로 발음한다'''

		for i in range(0,len(self.letters) - 1):
			if (self.letters[i].종성 == 'ㄲ' or self.letters[i].종성 == 'ㅋ') and self.letters[i+1].초성 != 'ㅇ':
				self.pronunciation[i].종성 = 'ㄱ'
			elif ((self.letters[i].종성 == 'ㅅ' or self.letters[i].종성 == 'ㅆ' or
				  self.letters[i].종성 == 'ㅈ' or self.letters[i].종성 == 'ㅊ' or
				  self.letters[i].종성 == 'ㅌ') and self.letters[i+1].초성 != 'ㅇ'):
				self.pronunciation[i].종성 = 'ㄷ'
			elif self.letters[i].종성 == 'ㅍ' and self.letters[i+1].초성 != 'ㅇ':
				self.pronunciation[i].종성 = 'ㅂ'

		if len(self.letters) > 0:
			temp = self.letters[len(self.letters) - 1]
			if (temp.종성 == 'ㄲ' or temp.종성 == 'ㅋ'):
				self.pronunciation[len(self.letters)-1].종성 = 'ㄱ'
			elif (temp.종성 == 'ㅅ' or temp.종성 == 'ㅆ' or temp.종성 == 'ㅈ' or temp.종성 == 'ㅊ' or temp.종성 == 'ㅌ'):
				self.pronunciation[len(self.letters)-1].종성 = 'ㄷ'
			elif temp.종성 == 'ㅍ':
				self.pronunciation[len(self.letters)-1].종성 = 'ㅂ' 

	def standard10(self):
		'''겹받침 ‘ㄳ’, ‘ㄵ’, ‘ㄼ, ㄽ, ㄾ’, ‘ㅄ’은 어말 또는 자음 앞에서 각각 [ㄱ, ㄴ, ㄹ, ㅂ]으로 발음한다'''
		for i in range(0, len(self.letters)):
			if (i != len(self.letters) - 1):
				if(self.letters[i+1].초성 != 'ㅇ'):
					if(self.letters[i].종성 == 'ㄳ'):
						self.pronunciation[i].종성 = 'ㄱ'
					elif(self.letters[i].종성 == 'ㄵ'):
						self.pronunciation[i].종성 = 'ㄴ'
					elif(self.letters[i].종성 == 'ㄼ' or self.letters[i].종성 == 'ㄽ' or self.letters[i].종성 == 'ㄾ'):
						self.pronunciation[i].종성 = 'ㄹ'
				elif(self.letters[i+1].초성 == 'ㅇ'):
					if(self.letters[i].종성 == 'ㄳ'):
						self.pronunciation[i].종성 = 'ㄱ'
						self.pronunciation[i+1].초성 = 'ㅅ'
					elif(self.letters[i].종성 == 'ㄵ'):
						self.pronunciation[i].종성 = 'ㄴ'
						self.pronunciation[i+1].초성 = 'ㅈ'
					elif(self.letters[i].종성 == 'ㄼ'):
						self.pronunciation[i].종성 = 'ㄹ'
						self.pronunciation[i+1].초성 = 'ㅂ'
					elif(self.letters[i].종성 == 'ㄽ'):
						self.pronunciation[i].종성 = 'ㄹ'
						self.pronunciation[i+1].초성 = 'ㅅ'
					elif(self.letters[i].종성 == 'ㄾ'):
						self.pronunciation[i].종성 = 'ㄹ'
						self.pronunciation[i+1].초성 = 'ㅌ'
					elif(self.letters[i].종성 ==  'ㅄ'):
						self.pronunciation[i].종성 = 'ㅂ'
						self.pronunciation[i+1].초성 = 'ㅅ'
			elif (i == len(self.letters) - 1):
				if(self.letters[i].종성 == 'ㄳ'):
					self.pronunciation[i].종성 = 'ㄱ'
				elif(self.letters[i].종성 == 'ㄵ'):
					self.pronunciation[i].종성 = 'ㄴ'
				elif(self.letters[i].종성 == 'ㄼ' or self.letters[i].종성 == 'ㄽ' or self.letters[i].종성 == 'ㄾ'):
					self.pronunciation[i].종성 = 'ㄹ'

	def standard11(self):
		'''겹받침 ‘ㄺ, ㄻ, ㄿ’은 어말 또는 자음 앞에서 각각 [ㄱ, ㅁ, ㅂ]으로 발음한다.'''
		for i in range(0, len(self.letters)):
			if (i != len(self.letters) - 1):
				if(self.letters[i+1].초성 != 'ㅇ'):
					if(self.letters[i].종성 == 'ㄺ'):
						self.pronunciation[i].종성 = 'ㄱ'
					elif(self.letters[i].종성 == 'ㄻ'):
						self.pronunciation[i].종성 = 'ㅁ'
					elif(self.letters[i].종성 == 'ㄿ'):
						self.pronunciation[i].종성 = 'ㅂ'
			elif (i == len(self.letters) - 1):
				if(self.letters[i].종성 == 'ㄺ'):
					self.pronunciation[i].종성 = 'ㄱ'
				elif(self.letters[i].종성 == 'ㄻ'):
					self.pronunciation[i].종성 = 'ㅁ'
				elif(self.letters[i].종성 == 'ㄿ'):
					self.pronunciation[i].종성 = 'ㅂ'						

	def standard12(self):
		'''받침 ‘ㅎ’의 발음은 다음과 같다.
		   1. ‘ㅎ(ㄶ, ㅀ)’ 뒤에 ‘ㄱ, ㄷ, ㅈ’이 결합되는 경우에는, 뒤 음절 첫소리와 합쳐서 [ㅋ, ㅌ, ㅊ]으로 발음한다.
				[붙임 1] 받침 ‘ㄱ(ㄺ), ㄷ, ㅂ(ㄼ), ㅈ(ㄵ)’이 뒤 음절 첫소리 ‘ㅎ’과 결합되는 경우에도,
						역시 두 음을 합쳐서 [ㅋ, ㅌ, ㅍ, ㅊ]으로 발음한다.
				[붙임 2] 규정에 따라 ‘ㄷ’으로 발음되는 ‘ㅅ, ㅈ, ㅊ, ㅌ’의 경우에도 이에 준한다.

		   2. ‘ㅎ(ㄶ, ㅀ)’ 뒤에 ‘ㅅ’이 결합되는 경우에는, ‘ㅅ’을 [ㅆ]으로 발음한다.

		   3. ‘ㅎ’ 뒤에 ‘ㄴ’이 결합되는 경우에는, [ㄴ]으로 발음한다.
 				[붙임]‘ㄶ, ㅀ’ 뒤에 ‘ㄴ’이 결합되는 경우에는, ‘ㅎ’을 발음하지 않는다.

		   4. ‘ㅎ(ㄶ, ㅀ)’ 뒤에 모음으로 시작된 어미나 접미사가 결합되는 경우에는, ‘ㅎ’을 발음하지 않는다.'''
		for i in range(0, len(self.letters)):
			if(i != len(self.letters) - 1):
				if((self.letters[i].종성 in ['ㅎ', 'ㄶ', 'ㅀ'] and self.letters[i+1].초성 == 'ㄱ') or 
			      (self.letters[i+1].초성 in ['ㅎ', 'ㄶ', 'ㅀ'] and self.letters[i].종성 in ['ㄱ', 'ㄺ'])):
				   self.pronunciation[i].종성 == ' '
				   self.pronunciation[i+1].초성 == 'ㅋ'
				elif((self.letters[i].종성 in ['ㅎ', 'ㄶ', 'ㅀ'] and self.letters[i+1].초성 == 'ㄷ') or 
			      (self.letters[i+1].초성 in ['ㅎ', 'ㄶ', 'ㅀ'] and self.letters[i].종성 == 'ㄷ')):
				   self.pronunciation[i].종성 == ' '
				   self.pronunciation[i+1].초성 == 'ㅌ'
				elif((self.letters[i].종성 in ['ㅎ', 'ㄶ', 'ㅀ'] and self.letters[i+1].초성 == 'ㅈ') or 
			      (self.letters[i+1].초성 in ['ㅎ', 'ㄶ', 'ㅀ'] and self.letters[i].종성 in ['ㅈ', 'ㄵ'])):
				   self.pronunciation[i].종성 == ' '
				   self.pronunciation[i+1].초성 == 'ㅊ'
				elif(self.letters[i+1].초성 in ['ㅎ', 'ㄶ', 'ㅀ'] and self.letters[i].종성 in ['ㅂ', 'ㄼ']):
					self.pronunciation[i].종성 == ' '
					self.pronunciation[i+1].초성 == 'ㅍ'
				elif(self.letters[i].종성 in ['ㅎ', 'ㄶ', 'ㅀ'] and self.letters[i+1].초성 == 'ㅅ'):
					self.pronunciation[i].종성 = ' '
					self.pronunciation[i+1].초성 = 'ㅆ'
				elif(self.letters[i].종성 == 'ㅎ' and self.letters[i+1].초성 == 'ㄴ'):
					self.pronunciation[i].종성 = 'ㅎ'
					self.pronunciation[i+1].초성 = 'ㄴ'
				elif(self.letters[i].종성 == 'ㄶ' and self.letters[i+1].초성 == 'ㄴ'):
					self.pronunciation[i].종성 = 'ㄴ'
					self.pronunciation[i+1].초성 = 'ㄴ'
				elif(self.letters[i].종성 == 'ㅀ' and self.letters[i+1].초성 == 'ㄴ'):
					self.pronunciation[i].종성 = 'ㄹ'
					self.pronunciation[i+1].초성 = 'ㄴ'

	def standard13_14(self):
		'''홑받침이나 쌍받침이 모음으로 시작된 조사나 어미, 접미사와 결합되는 경우에는, 제 음가대로 뒤 음절 첫소리로 옮겨 발음한다.'''
		for i in range(0, len(self.letters)):
			if(i != len(self.letters) - 1):
				if(self.letters[i+1].초성 == 'ㅇ'):
					if not(self.letters[i].종성 in [" ", "ㄳ", "ㄵ", "ㄶ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ"]):
						self.pronunciation[i+1].초성 = self.letters[i].종성
						self.pronunciation[i].종성 = " "

	def standard15(self):
		'''받침 뒤에 모음 ‘ㅏ, ㅓ, ㅗ, ㅜ, ㅟ’들로 시작되는 __실질 형태소__가 연결되는 경우에는, 대표음으로 바꾸어서 뒤 음절 첫소리로 옮겨 발음한다.'''
		for i in range(0, len(self.letters)):
			if(i != len(self.letters) - 1):
				if(self.letters[i].종성 in ["ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ","ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
				   and self.letters[i+1].초성 == "ㅇ" and self.letters[i+1].중성 in ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅟ']):					
					self.pronunciation[i+1].초성 = self.letters[i].종성
					self.pronunciation[i].종성 = " "
	
	"""
	def standard16(self, input):
		'''한글 자모의 이름은 그 받침소리를 연음하되, ‘ㄷ, ㅈ, ㅊ, ㅋ, ㅌ, ㅍ, ㅎ’의 경우에는 특별히 다음과 같이 발음한다.
			'디귿' => '디긋', '지읒' => '지읏', '치읓' => '치읏', '키읔' => '키윽', '티읕' => '티읏', '피읖' => '피읍', '히읗' => '히읏' ''' 
		for i in range(0, len(input) - 1):
			self.temp = ""
			self.temp = input[i].join(input[i+1])
			if(self.temp in ["디귿", "지읒", "치읓", "티읕", "히읗"]):
				self.pronunciation[i+1].종성 = 'ㅅ'
			elif(self.temp == "키읔"):
				self.pronunciation[i+1].종성 = 'ㄱ'
			elif(self.temp == "피읖"):
				self.pronunciation[i+1].종성 = 'ㅂ'

				"""

	def standard17(self):
		'''받침 ‘ㄷ, ㅌ(ㄾ)’이 조사나 접미사의 모음 ‘ㅣ’와 결합되는 경우에는, [ㅈ, ㅊ]으로 바꾸어서 뒤 음절 첫소리로 옮겨 발음한다.
			[붙임] ‘ㄷ’ 뒤에 접미사 ‘히’가 결합되어 ‘티’를 이루는 것은 [치]로 발음한다. '''
		for i in range(0, len(self.letters) - 1):
			if(self.letters[i].종성 == "ㄷ" and self.letters[i+1].중성 == 'ㅣ'):
				if(self.letters[i+1].초성 == 'ㅇ'):
					self.pronunciation[i].종성 = ' '
					self.pronunciation[i+1].초성 = 'ㅈ'
				elif(self.letters[i+1].초성 == 'ㅎ'):
					self.pronunciation[i].종성 = ' '
					self.pronunciation[i+1].초성 = 'ㅊ'
			elif(self.letters[i].종성 in ['ㅌ', 'ㄾ'] and self.letters[i+1].초성 == 'ㅇ' and self.letters[i+1].중성 == 'ㅣ'):
				self.pronunciation[i].종성 = ' '
				self.pronunciation[i+1].chtjd = 'ㅊ'

	def standard18(self):
		'''받침 ‘ㄱ(ㄲ, ㅋ, ㄳ, ㄺ), ㄷ(ㅅ, ㅆ, ㅈ, ㅊ, ㅌ, ㅎ), ㅂ(ㅍ, ㄼ, ㄿ, ㅄ)’은 ‘ㄴ, ㅁ’ 앞에서 [ㅇ, ㄴ, ㅁ]으로 발음한다.'''
		for i in range(0, len(self.letters) - 1):
			if(self.letters[i+1].초성 in ['ㄴ', 'ㅁ']):
				if(self.pronunciation[i].종성 == 'ㄱ'):
					self.pronunciation[i].종성 = 'ㅇ'
				elif(self.pronunciation[i].종성 == 'ㄷ'):
					self.pronunciation[i].종성 = 'ㄴ'
				elif(self.pronunciation[i].종성 == 'ㅂ'):
					self.pronunciation[i].종성 = 'ㅁ'	

	def standard19(self):
		'''받침 ‘ㅁ, ㅇ’ 뒤에 연결되는 ‘ㄹ’은 [ㄴ]으로 발음한다.
			[붙임]받침 ‘ㄱ, ㅂ’ 뒤에 연결되는 ‘ㄹ’도 [ㄴ]으로 발음한다.'''
		for i in range(0, len(self.letters) - 1):
			if(self.letters[i+1].초성 == 'ㄹ'):
				if(self.letters[i].종성 in ['ㄱ', 'ㅁ', 'ㅂ', 'ㅇ']):
					self.pronunciation[i+1].초성 = 'ㄴ'

	def standard20(self):
		''' ‘ㄴ’은 ‘ㄹ’의 앞이나 뒤에서 [ㄹ]로 발음한다.'''
		for i in range(0, len(self.letters) - 1):
			if(self.letters[i+1].초성 == 'ㄹ'):
				if(self.letters[i].종성 == 'ㄴ'):
					self.pronunciation[i].종성 = 'ㄹ'
			elif(self.letters[i+1].초성 == 'ㄴ'):
				if(self.letters[i].종성 == 'ㄹ'):
					self.pronunciation[i+1].초성 = 'ㄹ'

	def standard23(self):
		''' 받침 ‘ㄱ(ㄲ, ㅋ, ㄳ, ㄺ), ㄷ(ㅅ, ㅆ, ㅈ, ㅊ, ㅌ), ㅂ(ㅍ, ㄼ, ㄿ,ㅄ)’ 뒤에 연결되는 ‘ㄱ, ㄷ, ㅂ, ㅅ, ㅈ’은 된소리로 발음한다.'''
		for i in range(0, len(self.letters) - 1):
			if(self.letters[i].종성 in ['ㄱ', 'ㄲ', 'ㅋ', 'ㄳ', 'ㄺ', 'ㄷ', 'ㅅ', 'ㅈ', 'ㅊ', 'ㅌ', 'ㅂ', 'ㅍ', 'ㄼ', 'ㄿ', 'ㅄ']):
				if(self.letters[i+1].초성 == 'ㄱ'):
					self.pronunciation[i+1].초성 = 'ㄲ'
				elif(self.letters[i+1].초성 == 'ㄷ'):
					self.pronunciation[i+1].초성 = 'ㄸ'
				elif(self.letters[i+1].초성 == 'ㅂ'):
					self.pronunciation[i+1].초성 = 'ㅃ'
				elif(self.letters[i+1].초성 == 'ㅅ'):
					self.pronunciation[i+1].초성 = 'ㅆ'
				elif(self.letters[i+1].초성 == 'ㅈ'):
					self.pronunciation[i+1].초성 = 'ㅉ'

	def standard24_25(self):
		'''어간 받침 ‘ㄴ(ㄵ), ㅁ(ㄻ)’ 뒤에 결합되는 어미의 첫소리 ‘ㄱ, ㄷ, ㅅ, ㅈ’은 된소리로 발음한다.
		   다만, 피동, 사동의 접미사 ‘-기-’는 된소리로 발음하지 않는다. 용언 어간에만 적용.
		   현재단계에서 정확하게 구현할 수 없기 때문에, 이를 한계점으로 인식하고 self.error 변수를 = True로 설정한다.
		   단, 피동 / 사동 접미사인 '이''히''리''기''우''구''추'가 확인되지 않을경우, 법칙을 적용하지 않는다. '''
		for i in range(0, len(self.letters) - 1):
			if(self.letters[i].종성 in ['ㄴ', 'ㄵ', 'ㅁ', 'ㄻ', 'ㄼ', 'ㄾ']):
				if not (self.letters[i+1].초성 in ['ㅇ', 'ㅎ', 'ㄹ', 'ㄱ'] and self.letters[i+1].중성 == 'ㅣ'):
					if(i+1 == len(self.letters) or self.letters[i+2].초성 == ' '):
						if(self.letters[i+1].초성 == 'ㄱ'):
							self.pronunciation[i+1].초성 ='ㄲ'
						elif(self.letters[i+1].초성 == 'ㄷ'):
							self.pronunciation[i+1].초성 ='ㄸ'
						elif(self.letters[i+1].초성 == 'ㅅ'):
							self.pronunciation[i+1].초성 ='ㅆ'
						elif(self.letters[i+1].초성 == 'ㅈ'):
							self.pronunciation[i+1].초성 ='ㅉ'


	def standard30(self):
		'''사이시옷이 붙은 단어는 다음과 같이 발음한다.
			1. ‘ㄱ, ㄷ, ㅂ, ㅅ, ㅈ’으로 시작하는 단어 앞에 사이시옷이 올 때는 이들 자음만을 된소리로 발음하는 것을 원칙으로 하되, 사이시옷을 [ㄷ]으로 발음하는 것도 허용한다.
			2. 사이시옷 뒤에 ‘ㄴ, ㅁ’이 결합되는 경우에는 [ㄴ]으로 발음한다.
			3. 사이시옷 뒤에 ‘이’ 음이 결합되는 경우에는 [ㄴㄴ]으로 발음한다. '''
		for i in range(0, len(self.letters) - 1):
			if(self.letters[i].종성 in ['ㅅ', 'ㅆ']):
				if(self.letters[i+1].초성  == 'ㄱ'):
					self.pronunciation[i+1].초성 = 'ㄲ'
				elif(self.letters[i+1].초성  == 'ㄷ'):
					self.pronunciation[i+1].초성 = 'ㄸ'
				elif(self.letters[i+1].초성  == 'ㅂ'):
					self.pronunciation[i+1].초성 = 'ㅃ'
				elif(self.letters[i+1].초성  == 'ㅅ'):
					self.pronunciation[i+1].초성 = 'ㅆ'
				elif(self.letters[i+1].초성  == 'ㅈ'):
					self.pronunciation[i+1].초성 = 'ㅉ'
				elif(self.letters[i+1].초성 in ['ㄴ', 'ㅁ']):
					self.pronunciation[i].종성 = 'ㄴ'
				elif(self.letters[i+1].초성 == 'ㅇ' and self.letters[i+1].중성 == 'ㅣ'):
					self.pronunciation[i].종성 == 'ㄴ'
					self.pronunciation[i+1].초성 == 'ㄴ'
		

	def standardㅇ(self):
		'''발음규칙이 적용된 후에도 초성에 'ㅇ'이 남아 있다면, 이를 삭제한다'''
		for i in range(0, len(self.letters)):
			if(self.pronunciation[i].초성 == 'ㅇ'):
				self.pronunciation[i].초성 = ''

