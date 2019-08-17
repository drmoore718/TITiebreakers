import copy
import math
import numpy as np
import GroupA
import GroupB

module = GroupB

startScores = module.startScores
games       = module.games
results     = {}
rankings    = {}

teamNameMap = {
    'vp': 'VP',
    'eg': 'EG',
    'nip': 'NIP',
    'infamous': 'Infamous',
    'rng': 'RNG',
    'fnatic': 'Fnatic',
    'vg': 'VG',
    'og': 'OG',
    'navi': 'Na\'vi',
    'lgd': 'LGD',
    'secret': 'Secret',
    'newbee': 'Newbee',
    'tnc': 'TNC',
    'mineski': 'Mineski',
    'alliance': 'Alliance',
    'liquid': 'Liquid',
    'keen': 'Keen',
    'chaos': 'Chaos',
}

# Convert odds to probabilities
for x in games:
    if x[2] > 1:
        sum = 0
        for i in range(2, len(x)):
            x[i] = 1/x[i]
            sum += x[i]
        
        for i in range(2, len(x)):
            x[i] = x[i] / sum

for x in startScores:
    results[x] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    rankings[x] = {
        'upper': 0,
        'upperTie': 0,
        'lower': 0,
        'lowerTie': 0,
        'spreadTie': 0,
        'out': 0,
    }

tiebreakers = {
    'upper': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
    'lower': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
}

stack = []
progress = 0
lastProgress = 0

def resolveGame(gameNum, scores, probability):
    global progress
    global lastProgress

    if gameNum >= len(games):
        place = 0
        prevPlace = 0
        prevWins = 0
        numTied = 1
        progress += probability

        if int(progress*100) > lastProgress:
            #print(int(progress*100))
            lastProgress = int(progress*100)

        what = sorted(scores, key=lambda x: scores[x], reverse=True)

        for key in what:

            wins = scores[key]
            actualPlace = place


            if prevWins == wins:
                actualPlace = prevPlace
                numTied += 1

                if place == 8 and numTied + prevPlace > 8 and prevPlace + 1 <= 8:
                    tiebreakers['lower'][numTied][actualPlace] += probability
                    if numTied >= 6:
                        print('{} way tie for {}th {}'.format(numTied, actualPlace+1, stack))
            else:
                if numTied + prevPlace > 4 and prevPlace + 1 <= 4:
                    tiebreakers['upper'][numTied][prevPlace] += probability
                    if numTied >= 6:
                        print('{} way tie for {}th {}'.format(numTied, prevPlace+1, stack))


                prevPlace = place
                numTied = 1

            results[key][actualPlace] += probability
            place += 1
            prevWins = wins
        
        place = 0
        while place < 9:
            startPlace = place

            key = what[place]
            wins = scores[key]

            while place+1 < 9 and scores[what[place+1]] == wins:
                place += 1
            

            if place <= 3:
                ranking = 'upper'
            elif startPlace >= 8:
                ranking = 'out'
            elif startPlace <= 3 and place == 8:
                ranking = 'spreadTie'
            elif startPlace <= 3 and place >= 4:
                ranking = 'upperTie'
            elif startPlace >= 4 and place == 8:
                ranking = 'lowerTie'
            else:
                ranking = 'lower'

            for i in range(startPlace, place+1):
                rankings[what[i]][ranking] += probability

            place += 1

    else:
        game = games[gameNum]
        if len(game) == 5:
            stack.append(game[0] + ' > ' + game[1])
            scores[game[0]] += 2
            resolveGame(gameNum+1, scores, probability * game[2])
            scores[game[0]] -= 2
            stack.pop()

            stack.append(game[1] + ' > ' + game[0])
            scores[game[1]] += 2
            resolveGame(gameNum+1, scores, probability * game[3])
            scores[game[1]] -= 2
            stack.pop()

            stack.append(game[0] + ' = ' + game[1])
            scores[game[0]] += 1
            scores[game[1]] += 1
            resolveGame(gameNum+1, scores, probability * game[4])
            scores[game[0]] -= 1
            scores[game[1]] -= 1
            stack.pop()
        else:            
            stack.append(game[0] + ' > ' + game[1])
            scores[game[0]] += 1
            resolveGame(gameNum+1, scores, probability * game[2])
            scores[game[0]] -= 1
            stack.pop()

            stack.append(game[1] + ' > ' + game[0])
            scores[game[1]] += 1
            resolveGame(gameNum+1, scores, probability * game[3])
            scores[game[1]] -= 1
            stack.pop()


resolveGame(0, startScores, 1)


for key, value in results.items():
    output = '{}|{:.2f}%|{:.2f}%|{:.2f}%|{:.2f}%|{:.2f}%|{:.2f}%|{:.2f}%|{:.2f}%|{:.2f}%'.format(teamNameMap[key], value[0]*100, value[1]*100, value[2]*100, value[3]*100, value[4]*100, value[5]*100, value[6]*100, value[7]*100, value[8]*100)
    output = output.replace('0.00%','')
    print(output)
    #for i in range(len(value)):
    #    if value[i] != 0:
            #print('Place: {} - {:.2f}%'.format(i+1, value[i]/(math.pow(3,len(games))/100)))
            #print('Place: {} - {:.4f}%'.format(i+1, value[i]*100))

print()

print('## Match outcomes')
print('Game | 2:0 | 0:2 | 1:1')
print('----|----|----|----')

for x in games:
    print('{}:{} | {:.2f}% | {:.2f}% | {:.2f}%'.format(
        teamNameMap[x[0]],
        teamNameMap[x[1]],
        x[2]*100,
        x[3]*100,
        x[4]*100
    ))

print()

print('## Team placements')
print()
print('Team | Upper Bracket | Upper Bracket Tiebreaker | Lower Bracket | Elimination Tiebreaker | Eliminated')
print('----|----|----|----|----|----')
for key, value in rankings.items():
    print('{} | {:.2f}% | {:.2f}% | {:.2f}% | {:.2f}% | {:.2f}%'.format(teamNameMap[key], 
            value['upper']*100,
            value['upperTie']*100,
            value['lower']*100,
            value['lowerTie']*100,
            value['out']*100,
            #value['spreadTie']*100,
        )
    )

print()

print('## Tiebreaker Probabilities')
for key, value in tiebreakers.items():
    print()
    if key == 'upper':
        print('### Upper Bracket Tiebreakers')
    else:
        print('### Elimination Tiebreakers')
    for i in range(len(value)):
        for j in range(len(value[i])):
            if value[i] != 0 and value[i][j] != 0:
                #print('{}-way tie for {} - {:.2f}%'.format(i, j+1, value[i][j]/(math.pow(3,len(games))/100)))
                
                if j+1 == 1:
                    ordinal = str(j+1) + 'st'
                elif j+1 == 2:
                    ordinal = str(j+1) + 'nd'
                elif j+1 == 3:
                    ordinal = str(j+1) + 'rd'
                else:
                    ordinal = str(j+1) + 'th'

                print('* {}-way tie for {} - {:.2f}%'.format(i, ordinal, value[i][j]*100))
