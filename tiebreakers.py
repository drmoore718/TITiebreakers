from datetime import datetime

data = {
    'a': {
        'nameMap': {
            'eg': 'Evil Geniuses',
            'rng': 'Royal Never Give Up',
            'og': 'OG',
            'tl': 'Team Liquid',
            'gg': 'Gaimin Gladiators',
            'h': 'Hokori',
            'lgd': 'PSG.LGD',
            's': 'Soniqs',
            'boom': 'BOOM Esports',
            'bb': 'BetBoom Team',
        },
        'scores': {
            'eg': 14,
            'lgd': 11,
            'tl': 11,
            'rng': 9,
            'h': 9,
            'og': 8,
            'gg': 6,
            's': 5,
            'bb': 4,
            'boom': 3,
        },
        'games': [
            # ['eg','bb'],
            # ['og','h'],
            # ['s','boom'],
            # ['tl','gg'],
            # ['lgd','rng'],

            # ['tl','og'],
            # ['lgd','boom'],
            # ['s','bb'],
            # ['eg','gg'],
            # ['rng','h'],

            # ['eg','rng'],
            # ['tl','boom'],
            # ['lgd','gg'],
            # ['og','bb'],
            # ['s','h'],

            ['og','rng', 2.61, 3.81, 2.16],
            ['lgd','bb', 1.35, 9.26, 3.73],
            ['tl','h', 1.95, 6.19, 2.3],
            ['eg','boom', 1.9, 5.84, 2.44],
            ['s','gg', 3.77, 2.83, 2.04],
        ]
    },
    'b': {
        'nameMap': {
            'aster': 'Team Aster',
            'secret': 'Team Secret',
            'ts': 'Team Spirit',
            'ta': 'Thunder Awaken',
            'tsm': 'TSM',
            'te': 'Tundra Esports',
            'bc': 'beastcoast',
            'ent': 'Entity',
            'fnatic': 'Fnatic',
            'talon': 'Talon Esports',
        },
        'scores': {
            'te':       10,
            'aster':    9,
            'secret':   9,
            'ta':       8,
            'ts':       7,
            'fnatic':   7,
            'bc':       6,
            'ent':      6,
            'talon':    4,
            'tsm':      4,
        },
        'games': [
            ['talon','ent', 5.48, 2.26, 2.07],
            ['secret','aster', 2.8, 3.51, 2.14],
            ['ta','tsm', 3.01, 3.26, 2.13],
            ['ts','bc', 1.83, 6.19, 2.5],
            ['fnatic','te', 5.19, 2.05, 2.33],

            ['aster','ts', 3.35, 2.93, 2.14],
            ['fnatic','tsm', 3.39, 3.13, 2.02],
            ['te','ent', 2.04, 3.49, 2.03],
            ['secret','talon', 1.92, 6.31, 2.32],
            ['ta','bc', 2.61, 4.53, 1.98],
        ]
    }
}

progress = 0
lastProgress = 0

def resolveGroup(name, groupData):
    global progress
    global lastProgress

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
            x.extend([0.25, 0.25, 0.50])

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
        'spread': [[0 for x in range(teamCount)] for y in range(teamCount)],
    }

    stack = []

    progress = 0
    lastProgress = 0
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
    print('## Match outcome probabilities')
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

    hasSpreadTies = False
    for key, value in rankings.items():
        if value['spreadTie'] != 0:
            hasSpreadTies = True

    print('## Team placements')
    print()

    if hasSpreadTies:
        print('Team | Upper Bracket | Upper Bracket Tiebreaker | Lower Bracket | Elimination Tiebreaker | Spread Tiebreaker | Eliminated')
        print('----|----|----|----|----|----|----')
        for key, value in rankings.items():
            print('{} | {:.2f}% | {:.2f}% | {:.2f}% | {:.2f}% | {:.2f}%'.format(nameMap[key],
                    value['upper']*100,
                    value['upperTie']*100,
                    value['lower']*100,
                    value['lowerTie']*100,
                    value['spreadTie']*100,
                    value['out']*100,
                )
            )
    else:
        print('Team | Upper Bracket | Upper Bracket Tiebreaker | Lower Bracket | Elimination Tiebreaker | Eliminated')
        print('----|----|----|----|----|----')
        for key, value in rankings.items():
            print('{} | {:.2f}% | {:.2f}% | {:.2f}% | {:.2f}% | {:.2f}%'.format(nameMap[key],
                    value['upper']*100,
                    value['upperTie']*100,
                    value['lower']*100,
                    value['lowerTie']*100,
                    value['out']*100,
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
                        elif key == 'lower':
                            print('### Elimination Tiebreakers')
                        else:
                            print('### Spread Tiebreakers')

                    if j+1 == 1:
                        ordinal = str(j+1) + 'st'
                    elif j+1 == 2:
                        ordinal = str(j+1) + 'nd'
                    elif j+1 == 3:
                        ordinal = str(j+1) + 'rd'
                    else:
                        ordinal = str(j+1) + 'th'

                    print('* {}-way tie for {} - {:.2f}%'.format(i, ordinal, value[i][j]*100))

    print()
    print('## Expected number of games to play')

    for key, value in expectedGames.items():
        print('* {}: {:.2f} games'.format(nameMap[key], value))

    print()
    print()

def resolveGame(gameNum, scores, probability, stack, tiebreakers, results, rankings, games, expectedGames):
    global progress
    global lastProgress

    if gameNum >= len(games):
        teamCount = len(rankings)
        progress += probability

        if int(progress*100) > lastProgress:
            # print(f'{datetime.now()} {int(progress*100)}')
            lastProgress = int(progress*100)

        what = sorted(scores, key=lambda x: scores[x], reverse=True)

        place = 0
        while place < teamCount:
            startPlace = place

            key = what[place]
            wins = scores[key]

            while place+1 < teamCount and scores[what[place+1]] == wins:
                place += 1

            numTied = place - startPlace + 1

            if place <= 3:
                ranking = 'upper'
            elif startPlace >= 8:
                ranking = 'out'
            elif startPlace <= 3 and place >= 8:
                ranking = 'spreadTie'
                tiebreakers['spread'][numTied][startPlace] += probability
            elif startPlace <= 3 and place >= 4:
                ranking = 'upperTie'
                tiebreakers['upper'][numTied][startPlace] += probability
            elif startPlace >= 4 and place >= 8:
                ranking = 'lowerTie'
                tiebreakers['lower'][numTied][startPlace] += probability
            else:
                ranking = 'lower'

            # if numTied >= 7:
            #     print('{} way tie for {}th {}'.format(numTied, startPlace+1, stack))

            if 'Tie' in ranking:
                for z in range(startPlace, startPlace+numTied):
                    # 2-way tie is bo3, add 2.5 games
                    # 3+ way tie is round robin, add n-1 games
                    if numTied == 2:
                        expectedGames[what[z]] += 2.5 * probability
                    else:
                        expectedGames[what[z]] += (numTied - 1) * probability

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
