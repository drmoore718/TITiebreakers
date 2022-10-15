data = {
    'a': {
        'nameMap': {
            'ig': 'Invictus Gaming',
            'og': 'OG',
            'eg': 'Evil Geniuses',
            'undying': 'Team Undying',
            'vp': 'Virtus.pro',
            't1': 'T1',
            'alliance': 'Alliance',
            'aster': 'Team Aster',
            'tp': 'Thunder Predator',
        },
        'scores': {
            'ig': 13,
            'og': 9,
            'vp': 9,
            'eg': 8,
            'undying': 8,
            't1': 8,
            'aster': 5,
            'alliance': 4,
            'tp': 0,
        },
        'games': [
            ['ig',  'og',           ],
            ['eg',  'undying',      ],
            ['vp',  'aster',        ],
            ['t1',  'tp',           ],
        ]
    },
    'b': {
        'nameMap': {
            'lgd': 'PSG.LGD',
            'vg': 'Vici Gaming',
            'secret': 'Secret',
            'bc': 'beastcoast',
            'elephant': 'Elephant',
            'ts': 'Team Spirit',
            'fnatic': 'Fnatic',
            'qc': 'Quincy Crew',
            'sg': 'SG esports',
        },
        'scores': {
            'lgd': 11,
            'vg': 10,
            'secret': 8,
            'bc': 7,
            'elephant': 6,
            'ts': 6,
            'fnatic': 4,
            'qc': 2,
            'sg': 2,
        },
        'games': [
            ['lgd',     'elephant',     ],
            ['qc',      'sg',           ],
            ['ts',      'bc',           ],
            ['secret',  'fnatic',       ],

            ['secret',  'vg',           ],
            ['lgd',     'bc',           ],
            ['elephant','qc',           ],
            ['ts',      'sg',           ],
        ]
    }
}

def resolveGroup(name, groupData):
    startScores = groupData['scores']
    games = groupData['games']
    nameMap = groupData['nameMap']
    teamCount = len(startScores)
    results     = {}
    rankings    = {}

    # Expected number of games each team will play, including tiebreaker possibilities
    expectedGames = {x: 0 for x in startScores.keys()}

    for x in games:
        if not x[0] in expectedGames:
            expectedGames[x[0]] = 0
        expectedGames[x[0]] += 2
        if not x[1] in expectedGames:
            expectedGames[x[1]] = 0
        expectedGames[x[1]] += 2

    # If using odds as input, convert to probabilities
    for x in games:
        # If odds/probabilities are not provided, use even-odds
        if len(x) == 2:
            x.extend([0.25, 0.5, 0.25])

        if x[2] >= 1:
            sum = 0
            for i in range(2, len(x)):
                x[i] = 1/x[i]
                sum += x[i]

            for i in range(2, len(x)):
                x[i] = x[i] / sum

    for x in startScores:
        results[x] = [0 for x in range(teamCount)]
        rankings[x] = {
            'upper': 0,
            'upperTie': 0,
            'lower': 0,
            'lowerTie': 0,
            'spreadTie': 0,
            'out': 0,
        }

    tiebreakers = {
        'upper': [[0 for x in range(teamCount)] for y in range(teamCount)],
        'lower': [[0 for x in range(teamCount)] for y in range(teamCount)],
    }

    stack = []

    resolveGame(0, startScores, 1, stack, tiebreakers, results, rankings, games, expectedGames)

    # for key, value in results.items():
    #     output = '{}|{:.2f}%|{:.2f}%|{:.2f}%|{:.2f}%|{:.2f}%|{:.2f}%|{:.2f}%|{:.2f}%|{:.2f}%'.format(teamNameMap[key], value[0]*100, value[1]*100, value[2]*100, value[3]*100, value[4]*100, value[5]*100, value[6]*100, value[7]*100, value[8]*100)
    #     output = output.replace('0.00%','')
    #     print(output)
        #for i in range(len(value)):
        #    if value[i] != 0:
                #print('Place: {} - {:.2f}%'.format(i+1, value[i]/(math.pow(3,len(games))/100)))
                #print('Place: {} - {:.4f}%'.format(i+1, value[i]*100))

    print()
    print('# ' + name)
    print()
    print('## Match outcomes')
    print('Game | 2 : 0 | 0 : 2 | 1 : 1')
    print('----|----|----|----')

    for x in games:
        if len(x) == 5:
            print('{} : {} | {:.2f}% | {:.2f}% | {:.2f}%'.format(
                nameMap[x[0]],
                nameMap[x[1]],
                x[2]*100,
                x[3]*100,
                x[4]*100
            ))
        else:
            print('{} : {} | {:.2f}% | {:.2f}% | ---'.format(
                nameMap[x[0]],
                nameMap[x[1]],
                x[2]*100,
                x[3]*100
            ))

    print()

    print('## Team placements')
    print()
    print('Team | Upper Bracket | Upper Bracket Tiebreaker | Lower Bracket | Elimination Tiebreaker | Eliminated')
    print('----|----|----|----|----|----')
    for key, value in rankings.items():
        print('{} | {:.2f}% | {:.2f}% | {:.2f}% | {:.2f}% | {:.2f}%'.format(nameMap[key],
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

        printedHeader = False
        for i in range(len(value)):
            for j in range(len(value[i])):
                if value[i] != 0 and value[i][j] != 0:
                    #print('{}-way tie for {} - {:.2f}%'.format(i, j+1, value[i][j]/(math.pow(3,len(games))/100)))

                    if not printedHeader:
                        printedHeader = True
                        print()
                        if key == 'upper':
                            print('### Upper Bracket Tiebreakers')
                        else:
                            print('### Elimination Tiebreakers')

                    if j+1 == 1:
                        ordinal = str(j+1) + 'st'
                    elif j+1 == 2:
                        ordinal = str(j+1) + 'nd'
                    elif j+1 == 3:
                        ordinal = str(j+1) + 'rd'
                    else:
                        ordinal = str(j+1) + 'th'

                    print('* {}-way tie for {} - {:.2f}%'.format(i, ordinal, value[i][j]*100))

    # for key, value in expectedGames.items():
    #     print('* {}: {:.2f} games'.format(teamNameMap[key], value))


def resolveGame(gameNum, scores, probability, stack, tiebreakers, results, rankings, games, expectedGames):
    if gameNum >= len(games):
        place = 0
        prevPlace = 0
        prevWins = 0
        numTied = 1
        # progress += probability

        # if int(progress*100) > lastProgress:
        #     #print(int(progress*100))
        #     lastProgress = int(progress*100)

        what = sorted(scores, key=lambda x: scores[x], reverse=True)

        for key in what:

            wins = scores[key]
            actualPlace = place


            if prevWins == wins:
                actualPlace = prevPlace
                numTied += 1

                if place == 8 and numTied + prevPlace > 8 and prevPlace + 1 <= 8:
                    tiebreakers['lower'][numTied][actualPlace] += probability
                    for z in range(prevPlace, prevPlace+numTied):
                        expectedGames[what[z]] += (numTied - 1) * probability
                    if numTied >= 4:
                        print('{} way tie for {}th {}'.format(numTied, actualPlace+1, stack))
            else:
                if numTied + prevPlace > 4 and prevPlace + 1 <= 4:
                    tiebreakers['upper'][numTied][prevPlace] += probability
                    for z in range(prevPlace, prevPlace+numTied):
                        expectedGames[what[z]] += (numTied - 1) * probability
                    if numTied >= 4:
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
            resolveGame(gameNum+1, scores, probability * game[2], stack, tiebreakers, results, rankings, games, expectedGames)
            scores[game[0]] -= 2
            stack.pop()

            stack.append(game[1] + ' > ' + game[0])
            scores[game[1]] += 2
            resolveGame(gameNum+1, scores, probability * game[3], stack, tiebreakers, results, rankings, games, expectedGames)
            scores[game[1]] -= 2
            stack.pop()

            stack.append(game[0] + ' = ' + game[1])
            scores[game[0]] += 1
            scores[game[1]] += 1
            resolveGame(gameNum+1, scores, probability * game[4], stack, tiebreakers, results, rankings, games, expectedGames)
            scores[game[0]] -= 1
            scores[game[1]] -= 1
            stack.pop()
        else:
            stack.append(game[0] + ' > ' + game[1])
            scores[game[0]] += 1
            resolveGame(gameNum+1, scores, probability * game[2], stack, tiebreakers, results, rankings, games, expectedGames)
            scores[game[0]] -= 1
            stack.pop()

            stack.append(game[1] + ' > ' + game[0])
            scores[game[1]] += 1
            resolveGame(gameNum+1, scores, probability * game[3], stack, tiebreakers, results, rankings, games, expectedGames)
            scores[game[1]] -= 1
            stack.pop()

resolveGroup('Group A', data['a'])
resolveGroup('Group B', data['b'])
