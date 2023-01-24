import asyncio
import json
import random
import os
import tmdbsimple as tmdb

terminal_width = int(str(os.get_terminal_size()).split(',')[0].split('=')[1])

async def main():
    tmdb.API_KEY = "caaca20260daef3d857f502f4e6c1147"
    search = tmdb.Search()
    usr_input = input("Enter the TV Show you would like to watch: ")
    search.tv(query = usr_input)
    if search.results:
        show = search.results[0]
        show = tmdb.TV(show['id'])
        print('\nSelected Show: ' + show.info()['name'] + '\n')
        episode_list = []
        for season_number in range(1,len(show.info()['seasons'])):
            for i in tmdb.TV_Seasons(show.info()['id'],season_number).info()['episodes']: 
                if i['vote_average'] == 0 or i['vote_average'] == None:
                    i['vote_average'] == 5 
                episode_list.append(i)
        file = open("savedlist.json",'w')
        json.dump(episode_list,file)
        file.close()
        final_list = weighted_shuffle(episode_list)
        the_best_list = the_best(episode_list)
        final_list.extend(the_best_list)
        output_list = []
        output(final_list,output_list)

def output(final_list,output_list):
        print_list("Your picks", final_list, 0, 6, output_list)
        print_list("\nTop episodes", final_list, 6,9, output_list)
        episode_interaction(output_list,final_list)

def randomized(items,i):
    try:
        if items[i]['vote_average'] == 0:
            items[i]['vote_average'] = 5
        return random.random() ** (1.0 / (items[i]['vote_average']))
    except:
        print(items[i])

def weighted_shuffle(items):
    #Sourced from stackexchange
    order = sorted(range(len(items)), key=lambda i: randomized(items,i))
    return [items[i] for i in order]

def the_best(items):
    order = sorted(range(len(items)), key = lambda i: items[i]['vote_average'], reverse=True)
    return [items[i] for i in order]

def print_list(title, items, start_index, end_index, output_list):
    print(f"{title}: ")
    for i in items[start_index:end_index]:
        output = "[%i] S%02iE%02i" % (len(output_list),i['season_number'],i['episode_number']) + f" {i['name']} - Rating(""%0.1f) Desc: " % i['vote_average']
        output = output + f"{i['overview']}"
        output_list.append(i)
        if len(output) > terminal_width:
            output = output[:terminal_width-4]+"..."
        print(output)

def episode_interaction(output_list,final_list):
    try:
        usr_in = int(input(f"\n[{len(output_list)}] Search for an episode\n"))
        if usr_in < len(output_list):
            episode = output_list[usr_in]
            print("S%02iE%02i - %s" % (episode['season_number'],episode['episode_number'],episode['name']),
                "\n\nDesc: %s" % episode['overview']
            )
            goback = input('[0] Go back')
            if goback == '0':
                output(final_list,output_list)
        elif usr_in == len(output_list):
            #TODO implement search for episode
            pass
        else:
            Exception
    except:
        print("Input a number!")

asyncio.run(main())
