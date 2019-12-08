import pandas
import numpy
import os
import csv
from collections import namedtuple

def buildCSV () :
    '''
    초기화할 때 한번 실행
    기존의 csv파일을 읽어 이를 배열에 저장한 후 리턴
    '''

    abspath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    csv_data = []
    f = open(abspath + '/resource/CSV source/result.csv', 'r', encoding='utf-8-sig')
    csvReader = csv.reader(f)
    for row in csvReader:
        csv_data.append(row)
    f.close()
    
    return csv_data


def AddToCSV (test_result, csv_data) :
    '''
    csv에 테스트 한번동안 실시된 내용 추가
    기존에 존재하는 statistics.csv파일에 적용
    input으로 받아야 하는 내용은 테스트 10번에 대한 결과

    수정사항은 temp를 만들어 저장해 두었다가
    추가가 완료된 후 원래의 파일을 덮어쓰는 방식으로 저장

    test_result = {{'ㄱ', 'True', '정확도'},
                    'ㄴ', 'False', '40'}
    csv_data : 정답률, 문제 수, 정답 횟수, 오답 횟수, 평균 정확도 (%)
    '''

    LUT = ['ㄱ', 'ㄷ', 'ㅂ', 'ㅅ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
        , 'ㅏ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅐ', 'ㅕ', 'ㅗ', 'ㅘ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅟ', 'ㅠ'
        , 'ㅡ', 'ㅣ', 'ㄴ', 'ㄹ', 'ㅇ', 'ㅁ', 'ㄲ', 'ㄸ', 'ㅃ', 'ㅆ', 'ㅉ']
    temp = csv_data
    for i in range(len(temp)):
        for j in range(len(temp[0])):
            csv_data[i][j] = float(csv_data[i][j])
    for i in range(0, len(test_result)):
        NofQuiz = csv_data[LUT.index(test_result[i].phoneme)][1]
        accuracy = csv_data[LUT.index(test_result[i].phoneme)][4]

        csv_data[LUT.index(test_result[i].phoneme)][1] += 1
        if test_result[i].isCorrect == True:
            csv_data[LUT.index(test_result[i].phoneme)][2] += 1
        else:
            csv_data[LUT.index(test_result[i].phoneme)][3] += 1
            csv_data[LUT.index(test_result[i].phoneme)][0] = float(format(csv_data[LUT.index(test_result[i].phoneme)][2] / csv_data[LUT.index(test_result[i].phoneme)][1] * 100, "2f"))
            csv_data[LUT.index(test_result[i].phoneme)][4] = float(format((accuracy * NofQuiz + test_result[i].accuracy) / csv_data[LUT.index(test_result[i].phoneme)][1], "2f"))

    abspath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    f = open(abspath + '/resource/CSV source/result.csv', 'w', encoding='utf-8-sig')
    wr = csv.writer(f, lineterminator = '\n')

    for i in range(0,len(csv_data)):
        temp_data=csv_data[i]
        wr.writerow(temp_data)

    #wr.writerows(csv_data)
    f.close()

