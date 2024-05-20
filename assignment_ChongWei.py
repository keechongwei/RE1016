import pygame
from PIL import Image
import time
import pandas as pd


# load dataset for keyword dictionary - provided
def load_stall_keywords(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    keywords = {}
    for canteen in canteens:
        keywords[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_keywords_intermediate = copy.set_index('Stall')['Keywords'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_keywords = stall_keywords_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        keywords[stall_canteen][stall] = stall_keywords

    return keywords


# load dataset for price dictionary - provided
def load_stall_prices(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    prices = {}
    for canteen in canteens:
        prices[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_prices_intermediate = copy.set_index('Stall')['Price'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_price = stall_prices_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        prices[stall_canteen][stall] = stall_price

    return prices


# load dataset for location dictionary - provided
def load_canteen_location(data_location="canteens.xlsx"):
    # get list of canteens
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    # get dictionary of {canteen:[x,y],}
    canteen_locations = {}
    for canteen in canteens:
        copy = canteen_data.copy()
        copy.drop_duplicates(subset="Canteen", inplace=True)
        canteen_locations_intermediate = copy.set_index('Canteen')['Location'].to_dict()
    for canteen in canteens:
        canteen_locations[canteen] = [int(canteen_locations_intermediate[canteen].split(',')[0]),
                                      int(canteen_locations_intermediate[canteen].split(',')[1])]

    return canteen_locations


# get user's location with the use of PyGame - provided
def get_user_location_interface():
    # get image dimensions
    image_location = 'NTUcampus.jpg'
    pin_location = 'pin.png'
    screen_title = "NTU Map"
    image = Image.open(image_location)
    image_width_original, image_height_original = image.size
    scaled_width = int(image_width_original * 0.9)  # image's width scaled according to the screen
    scaled_height = int(image_height_original * 0.9)  # image's height scaled according to the screen
    pinIm = pygame.image.load(pin_location)
    pinIm_scaled = pygame.transform.scale(pinIm, (60, 60))
    # initialize pygame
    pygame.init()
    # set screen height and width to that of the image
    screen = pygame.display.set_mode([scaled_width, scaled_height])
    # set title of screen
    pygame.display.set_caption(screen_title)
    # read image file and rescale it to the window size
    screenIm = pygame.image.load(image_location)
    screenIm_scaled = pygame.transform.scale(screenIm, (scaled_width, scaled_height))

    # add the image over the screen object
    screen.blit(screenIm_scaled, (0, 0))
    # will update the contents of the entire display window
    pygame.display.flip()

    # loop for the whole interface remain active
    while True:
        # checking if input detected
        pygame.event.pump()
        event = pygame.event.wait()
        # closing the window
        if event.type == pygame.QUIT:
            pygame.display.quit()
            mouseX_scaled = None
            mouseY_scaled = None
            break
        # resizing the window
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            screen.blit(pygame.transform.scale(screenIm_scaled, event.dict['size']), (0, 0))
            scaled_height = event.dict['h']
            scaled_width = event.dict['w']
            pygame.display.flip()
        # getting coordinate
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get outputs of Mouseclick event handler
            (mouseX, mouseY) = pygame.mouse.get_pos()
            # paste pin on correct position
            screen.blit(pinIm_scaled, (mouseX - 25, mouseY - 45))
            pygame.display.flip()
            # return coordinates to original scale
            mouseX_scaled = int(mouseX * 1281 / scaled_width)
            mouseY_scaled = int(mouseY * 1550 / scaled_height)
            # delay to prevent message box from dropping down
            time.sleep(0.2)
            break

    pygame.quit()
    pygame.init()
    return mouseX_scaled, mouseY_scaled

# Any additional function to assist search criteria can be used
def distance(x1,y1,x2,y2):
    # calculate Euclidean Distance between two points
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def findneareststalls(user_locations,distancedict,k):
    # halve difference between each users x and y coordinates
    # add to smaller of each users x and y coordinates
    # round to nearest integer to get coordinates of midpoint
    midptbtwnuser = (round(min(user_locations[0][0],user_locations[1][0]) + 0.5*abs(user_locations[0][0] - user_locations[1][0])),\
                     round(min(user_locations[0][1],user_locations[1][1]) + 0.5*abs(user_locations[0][1] - user_locations[1][1])))
    print(f"Midpoint Between Users: {midptbtwnuser}")
    workdict = distancedict.copy()
    locations = []
    listofdistances = []
    for stall in workdict:
        #calculate distance of midpoint and users to each stall
        workdict[f'{stall}'] = [distance(midptbtwnuser[0], midptbtwnuser[1], workdict[f'{stall}'][0],
                                            workdict[f'{stall}'][1]),distance(user_locations[0][0], user_locations[0][1], workdict[f'{stall}'][0],
                                            workdict[f'{stall}'][1]),distance(user_locations[1][0], user_locations[1][1], workdict[f'{stall}'][0],
                                            workdict[f'{stall}'][1])]
        listofdistances.append(workdict[f'{stall}'][0])
    #arrange distances in ascending order to find nearest stalls to midpoint of users
    listofdistances.sort()
    #retrieve as many canteens as necessary
    listofdistances = listofdistances[0:k]
    #check if distance in list of distances matches stall distance from midpoint
    for val in listofdistances:
        for stall in workdict:
            if workdict[f'{stall}'][0] == val:
                # if distance matches, append stall name and distance from each user
                locations.append(f"{stall}" +
                                 f"\nDistance From Midpoint: {round(val)}m" +
                                 "\nDistance From User A: " + str(round(workdict[stall][1])) + 'm' +
                                 '\nDistance From User B: ' + str(round(workdict[stall][2])) + 'm')
    return locations

def andkeyword(canteen_stall_keywords,keywords):
    results = []
    #index into each canteen
    for canteen_stall_keyword in canteen_stall_keywords:
        # index into each stall in canteen
        for stall in canteen_stall_keywords[canteen_stall_keyword]:
            count = 0
            # compare each keyword with stall description
            for word in keywords:
                if word not in canteen_stall_keywords[canteen_stall_keyword][stall]:
                    break
                elif word in canteen_stall_keywords[canteen_stall_keyword][stall]:
                    # if all keywords are matched, add canteen and stall name to list
                    if count == len(keywords) - 1:
                        results.append(f"{canteen_stall_keyword} - {stall}")
                    else:
                        count += 1
                        continue
    # remove duplicates by first making a dictionary with keys corresponding to results list
    # make a list of the dictionary keys
    results = list(dict.fromkeys(results))
    return results

def orkeyword(canteen_stall_keywords,keywords):
    results = []
    for word in keywords:
        # index into canteens
        for canteen_stall_keyword in canteen_stall_keywords:
            # index into stalls
            for stall in canteen_stall_keywords[canteen_stall_keyword]:
                # if word in keywords matches keywords of stall
                if word in canteen_stall_keywords[canteen_stall_keyword][stall]:
                    # add canteen name and stall name to results
                    results.append(f"{canteen_stall_keyword} - {stall}")
    # remove duplicates by first making a dictionary with keys corresponding to results list
    # make a list of the dictionary keys
    results = list(dict.fromkeys(results))
    return results

def andprice(canteen_stall_keywords,keywords,max_price):
    results = []
    price_compare = []
    closest_price =''
    price_diff = 0
    for canteen_stall_keyword in canteen_stall_keywords:
        for stall in canteen_stall_keywords[canteen_stall_keyword]:
            count = 0
            # compare each keyword with stall description
            for word in keywords:
                if word not in canteen_stall_keywords[canteen_stall_keyword][stall]:
                    break
                elif word in canteen_stall_keywords[canteen_stall_keyword][stall]:
                    # if all keywords are matched
                    if count == len(keywords) - 1:
                        # if price below max_price, add to results
                        if canteen_stall_prices[canteen_stall_keyword][stall] <= max_price:
                            results.append(f"{canteen_stall_keyword} - {stall} - {canteen_stall_prices[canteen_stall_keyword][stall]}")
                        # save stall with closest price diff
                        else:
                            current_price_diff = abs(canteen_stall_prices[canteen_stall_keyword][stall] - max_price)
                            if price_diff == 0 or current_price_diff < price_diff:
                                price_diff = current_price_diff
                                closest_price = f'{canteen_stall_keyword} - {stall} - {canteen_stall_prices[canteen_stall_keyword][stall]}'
                    else:
                        count += 1
                        continue
    results = list(dict.fromkeys(results))
    for result in results:
        price_compare.append(result.split('-'))
    return results, closest_price, price_compare

def orprice(canteen_stall_keywords,keywords,max_price):
    results = []
    price_compare = []
    closest_price = ''
    price_diff = 0
    for word in keywords:
        for canteen_stall_keyword in canteen_stall_keywords:
            for stall in canteen_stall_keywords[canteen_stall_keyword]:
                if word in canteen_stall_keywords[canteen_stall_keyword][stall]:
                    if canteen_stall_prices[canteen_stall_keyword][stall] <= max_price:
                        results.append(f"{canteen_stall_keyword} - {stall} - {canteen_stall_prices[canteen_stall_keyword][stall]}")
                    # save stall with closest price diff
                    else:
                        current_price_diff = canteen_stall_prices[canteen_stall_keyword][stall] - max_price
                        if price_diff == 0 or current_price_diff < price_diff:
                            price_diff = current_price_diff
                            closest_price = f'{canteen_stall_keyword} - {stall} - {canteen_stall_prices[canteen_stall_keyword][stall]}'
    results = list(dict.fromkeys(results))
    for result in results:
        price_compare.append(result.split('-'))
    return results, closest_price, price_compare

def compare(price_compare):
    compared = False
    while compared == False:
        currentindex = 0
        swaps = 0
        # go through each element in price_compare list which corresponds to [[canteen_name],[stall name],[price]]
        for item in price_compare:
            #typecast price of current element to a float
            currentprice = float(item[2].lstrip())
            # if at last element of price_compare list
            if currentindex == len(price_compare) - 1:
                # if price of current stall is lower than first element of price_compare list
                if currentprice < float(price_compare[0][2].lstrip()):
                    # store current element in temp variable
                    temp = item
                    # store first element of price_compare list in current index
                    price_compare[currentindex] = price_compare[0]
                    # store current element as first element of price_compare list
                    price_compare[0] = temp
                    swaps += 1
                if swaps == 0:
                    compared = True
                    break
            # while not at last element of price_compare list
            elif float(price_compare[currentindex + 1][2].lstrip()) < currentprice:
                # store current element in temp variable
                temp = item
                # store element at next index of list to element at current index of list
                price_compare[currentindex] = price_compare[currentindex + 1]
                # store current element as next index of list
                price_compare[currentindex + 1] = temp
                # advance index
                currentindex += 1
                swaps += 1
            else:
                # advance index if price is equivalent
                currentindex += 1
    return price_compare

def combinepricelist(price_compare):
    stallindex = 0
    # combine each element in price_compare list into strings of ' Canteen - Stall - Price '
    for price in price_compare:
        price_compare[stallindex] = price[0] + '-' + price[1] + '- ' + 'S$' + price[2].lstrip()
        stallindex += 1
        if stallindex == len(price_compare):
            break
    return price_compare


# Keyword-based Search Function - to be implemented
def search_by_keyword(keywords):
    results = []
    keywords = list(dict.fromkeys(keywords))
    if 'And' in keywords:
        # AND
        keywords.remove('And')
        results = andkeyword(canteen_stall_keywords,keywords)
        if len(results) > 0:
            print("Food Stalls found:", len(results))
            for result in results:
                print(result)
        else:
            print("Food Stalls found: No food stalls found with input keyword")
    elif 'Or' in keywords:
        # OR
        keywords.remove('Or')
        results = orkeyword(canteen_stall_keywords,keywords)
        if len(results) > 0:
            print("Food Stalls found:",len(results))
            print("Food Stalls that match 2 keywords:")
            twokeywordresults = andkeyword(canteen_stall_keywords,keywords)
            for value in twokeywordresults:
                print(value)
            print("Food Stalls that match 1 keyword:")
            for twokeywordresult in twokeywordresults:
                results.remove(twokeywordresult)
            for result in results:
                print(result)
        else:
            print("Food Stalls found: No food stalls found with input keyword")
    else:
        # if separated by space, treat as AND
        if len(keywords)>1:
            results = andkeyword(canteen_stall_keywords,keywords)
            if len(results) > 0:
                print("Food Stalls found:", len(results))
                for result in results:
                    print(result)
            else:
                print("Food Stalls found: No food stalls found with input keyword")
        else:
            # only one keyword input
            results = orkeyword(canteen_stall_keywords,keywords)
            if len(results) > 0:
                print("Food Stalls found:", len(results))
                for result in results:
                    print(result)
            else:
                print("Food Stalls found: No food stalls found with input keyword")


# Price-based Search Function - to be implemented
def search_by_price(keywords, max_price):
    keywords = list(dict.fromkeys(keywords))
    if 'And' in keywords:
        # AND
        keywords.remove('And')
        results, closest_price, price_compare = andprice(canteen_stall_keywords,keywords,max_price)
        if len(price_compare) > 0:
            price_compare = compare(price_compare)
            print("Food Stalls found:", len(results))
            price_compare = combinepricelist(price_compare)
            for price in price_compare:
                print(price)
        else:
            print("Food Stalls found: No food stalls found with specified price range.")
            print("Recommended Food Stall with the closest price range.")
            print(closest_price)
    elif 'Or' in keywords:
        # OR
        keywords.remove('Or')
        results, closest_price, price_compare = orprice(canteen_stall_keywords, keywords, max_price)
        if len(price_compare) > 0:
            price_compare = compare(price_compare)
            print("Food Stalls found:", len(results))
            price_compare = combinepricelist(price_compare)
            for price in price_compare:
                print(price)
        else:
            print("Food Stalls found: No food stalls found with specified price range.")
            print("Recommended Food Stall with the closest price range.")
            print(closest_price)
    else:
        # if separated by space, treat as AND
        if len(keywords)>1:
            results, closest_price,price_compare = andprice(canteen_stall_keywords, keywords, max_price)
            if len(price_compare) > 0:
                price_compare = compare(price_compare)
                print("Food Stalls found:", len(results))
                price_compare = combinepricelist(price_compare)
                for price in price_compare:
                    print(price)
            else:
                print("Food Stalls found: No food stalls found with specified price range.")
                print("Recommended Food Stall with the closest price range.")
                print(closest_price)
        else:
            # only one keyword input
            results, closest_price, price_compare = orprice(canteen_stall_keywords, keywords, max_price)
            if len(price_compare) > 0:
                price_compare = compare(price_compare)
                print("Food Stalls found:", len(results))
                price_compare = combinepricelist(price_compare)
                for price in price_compare:
                    print(price)
            else:
                print("Food Stalls found: No food stalls found with specified price range.")
                print("Recommended Food Stall with the closest price range.")
                print(closest_price)


# Location-based Search Function - to be implemented
def search_nearest_canteens(user_locations, k):
     locations = []
     distancedict = canteen_locations.copy()
     locations = findneareststalls(user_locations,distancedict,k)
     print(f"{k} Nearest Canteens Found:")
     for place in locations:
         print(place)



# Main Python Program Template
# dictionary data structures
canteen_stall_keywords = load_stall_keywords("canteens.xlsx")
canteen_stall_prices = load_stall_prices("canteens.xlsx")
canteen_locations = load_canteen_location("canteens.xlsx")


# main program template - provided
def main():
    loop = True

    while loop:
        print("========================")
        print("F&B Recommendation Menu")
        print("1 -- Display Data")
        print("2 -- Keyword-based Search")
        print("3 -- Price-based Search")
        print("4 -- Location-based Search")
        print("5 -- Exit Program")
        print("========================")
        option = int(input("Enter option [1-5]: "))

        if option == 1:
            # print provided dictionary data structures
            print("1 -- Display Data")
            print("Keyword Dictionary: ", canteen_stall_keywords)
            print("Price Dictionary: ", canteen_stall_prices)
            print("Location Dictionary: ", canteen_locations)

        elif option == 2:
            # keyword-based search
            print("2 -- Keyword-based Search")
            keywords = []
            foodwords = input("Enter type of food:")
            while len(foodwords)<1:
                print("No input found. Please try again.")
                foodwords = input("Enter type of food:")
            foodwords = foodwords.split()
            for foodword in foodwords:
                foodword = foodword.lstrip().rstrip().capitalize()
                keywords.append(foodword)
            #call keyword-based search function
            search_by_keyword(keywords)
        elif option == 3:
            # price-based search
            print("3 -- Price-based Search")
            keywords = []
            foodwords = input("Enter type of food:")
            while len(foodwords)<1:
                print("No input found. Please try again.")
                foodwords = input("Enter type of food:")
            foodwords = foodwords.split()
            for foodword in foodwords:
                foodword = foodword.lstrip().rstrip().capitalize()
                keywords.append(foodword)
            price = float(input("Enter maximum meal price (S$):"))
            while price <= 0:
                print("Error: Meal price cannot be a negative number. Please try again.")
                price = float(input("Enter maximum meal price (S$):"))
            max_price = price
            # call price-based search function
            search_by_price(keywords, max_price)
        elif option == 4:
            # location-based search
            print("4 -- Location-based Search")

            # call PyGame function to get two users' locations
            userA_location = get_user_location_interface()
            print("User A's location (x, y): ", userA_location)
            userB_location = get_user_location_interface()
            print("User B's location (x, y): ", userB_location)
            k = int(input("Number of canteens:"))
            if k<1:
                 print("Warning: k cannot be negative value. Default k = 1 is set.")
                 k = 1
            user_locations = (userA_location,userB_location)
             # call location-based search function
            search_nearest_canteens(user_locations, k)
        elif option == 5:
            # exit the program
            print("Exiting F&B Recommendation")
            loop = False


main()
