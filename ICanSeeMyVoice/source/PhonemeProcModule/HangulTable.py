LUT_u = [[[" " for ycgyh in range(5)] for pmpub in range(5)] for ygd in range(3)]
LUT_u[0][0][0] = 'ㅂ'
LUT_u[0][0][1] = 'ㄷ'
LUT_u[0][0][3] = 'ㄱ'
LUT_u[0][1][1] = 'ㅅ'
LUT_u[0][1][4] = 'ㅎ'
LUT_u[0][2][2] = 'ㅈ'
LUT_u[0][3][1] = 'ㄹ'
LUT_u[0][4][0] = 'ㅁ'
LUT_u[0][4][1] = 'ㄴ'
LUT_u[0][4][3] = 'ㅇ'
LUT_u[1][0][0] = 'ㅍ'
LUT_u[1][0][1] = 'ㅌ'
LUT_u[1][0][3] = 'ㅋ'
LUT_u[1][2][2] = 'ㅊ'
LUT_u[2][0][0] = 'ㅃ'
LUT_u[2][0][1] = 'ㄸ'
LUT_u[2][0][3] = 'ㄲ'
LUT_u[2][1][1] = 'ㅆ'
LUT_u[2][2][2] = 'ㅉ'

LUT_vt = ['ㅏ','ㅑ','ㅖ','ㅓ','ㅔ','ㅕ','ㅗ','ㅘ','ㅚ','ㅛ','ㅜ','ㅝ','ㅟ','ㅠ','ㅡ','ㅣ','ㄴ','ㄹ','ㅁ','ㅇ']
LUT_ut = ['ㄱ','ㄷ','ㅂ','ㅅ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ','ㄲ','ㄸ','ㅃ','ㅆ','ㅉ']

예삿소리 = ['ㄱ','ㄷ','ㅂ','ㅅ','ㅈ','ㅎ','ㅁ','ㄴ','ㅇ','ㄹ']
거센소리 = ['ㅊ','ㅋ','ㅌ','ㅍ']
된소리 = ['ㄲ','ㄸ','ㅃ','ㅆ','ㅉ']

파열음 = ['ㄱ','ㄷ','ㅂ','ㅋ','ㅌ','ㅍ','ㄲ','ㄸ','ㅃ']
마찰음 = ['ㅅ','ㅎ','ㅆ']
파찰음 = ['ㅈ','ㅊ','ㅉ']
유음 = ['ㄹ']
비음 = ['ㅁ,ㄴ,ㅇ']

양순음 = ['ㅂ','ㅍ','ㅃ','ㅁ']
치열음 = ['ㄷ','ㅅ','ㅌ','ㄸ','ㅆ','ㄴ','ㄹ']
경구개음 = ['ㅈ','ㅊ','ㅉ']
연구개음 = ['ㄱ','ㄲ','ㅋ','ㅇ']
후음 = ['ㅎ']

def GetFeat(phoneme):
  if phoneme in 예삿소리:
    ygd = 0
  elif phoneme in 거센소리:
    ygd = 1
  elif phoneme in 된소리:
    ygd = 2
  else:
    ygd = -2

  if phoneme in 파열음:
    pmpub = 0
  elif phoneme in 마찰음:
    pmpub = 1
  elif phoneme in 파열음:
    pmpub = 2
  elif phoneme in 유음:
    pmpub = 3
  elif phoneme in 비음:
    pmpub = 4
  else:
    pmpub = -2
  
  if phoneme in 양순음:
    ycgyh = 0
  elif phoneme in 치열음:
    ycgyh = 1
  elif phoneme in 경구개음:
    ycgyh = 2
  elif phoneme in 연구개음:
    ycgyh = 3
  elif phoneme in 후음:
    ycgyh = 4
  else :
    ycgyh = -2
  
  return ygd, pmpub, ycgyh