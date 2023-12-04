init python:
    def randomize_cards():
        #function to create cards
        global cards
        cards=[]

        for i in range(int(card_amount/2)):
            #fill the cards list with 2 cards (a pair) in each iteration of the loop.
            #The loop iterates card_amount / card_rows times to create the resulting amount of cards.
            # This creates as a nested list that looks like this example:cards=[['card-5','deselected']]
            #1: name of the card, 2: if the card is selected or deselcted ,3: if the card is visible or not
            rand_card_num=renpy.random.randint(9,20)# 6 cards instead.
            cards.append(['card-%s' % rand_card_num, 'deselected', 'visible'])
            cards.append(['card-%s' % rand_card_num, 'deselected', 'visible'])

        # shuffle  the filled list so that each card ends up in a random location instaed to right next to each other
        renpy.random.shuffle(cards)

    def select_card(card_index):
        #function to select a card that was clicked on
        global selected_cards
        global match_found

        #select the card the user clicked on.
        cards[card_index][1]='selected'
        selected_cards.append(card_index)

        if len(selected_cards)==2 and cards[selected_cards[0]][0]==cards[selected_cards[1]][0]:
            #Two matching pairs of cards has been selected.
            match_found = True

    def  deselect_cards():
        #function to deselect cards after 2 have been selected that doesnt match
        global selected_cards

        if len(selected_cards)==2:
            for card in cards:
                if card[1]=='selected':
                    card[1]='deselected'
        selected_cards=[]

    def hide_matches():
        #function to hide matching cards
        global selected_cards
        global match_found
        global hidden_cards

        cards[selected_cards[0]][2]= 'hidden' #first card
        cards[selected_cards[1]][2]= 'hidden'# second card
        hidden_cards+=2
        deselect_cards()
        match_found=False

    #def reset_memory_game():
        #function to reset mini-game
        #global match_found
        #global hidden_cards

        #match_found= False
        #hidden_cards=0
        #randomize_cards()

transform card_fadein:
    alpha 0.0
    easein 0.5 alpha 1.0

screen memory_mini_game:
    image 'Waterloo-Background.png'
    grid int(card_amount/card_rows) card_rows:
        align(0.9,0.5)
        spacing 5# for the position and spacing of the cards
        for i, card in enumerate(cards):
            if card[1]=='deselected' and card[2]=='visible':
                #this card isnt selected and it hasnt been matched to another card yet, so we show the....
                # we set it to be sensitive/clickable only if the player hasnt clicked on 2 cards yet.....
                imagebutton idle 'cat-back.png' sensitive If(len(selected_cards)!=2, True, False) action Function (select_card, card_index= i) at card_fadein
            elif card[1]=='selected' and card[2]=='visible':
                # this card has been selected and is visible, so we flip it to show its image.
                image '%s.png' %card[0] at card_fadein
            else:
                # this card is hidden because it was matched with another card.
                #null to replace 'return none'
                null

    # if theres a matching pair visible on the screen, we want to make them invisible. if there are two.....
    #we do this with timers to make sure the cat has time to observe the cards to see what they are
    if match_found:
        timer 1.0 action Function(hide_matches) repeat True # Hides the cards 1.0 second after it is revealed
    elif len(selected_cards)==2:
        timer 1.0 action Function( deselect_cards) repeat True #Flips the cards back over 1 second after it is revealed
    elif hidden_cards== card_amount:
        #All cards have been matched. We end the game
        timer 0.5   repeat False # action  Function(reset_memory_game) was romoved from middle




    button:
        background "#FFFFFF"
        padding(15, 20)
        align(0.1, 0.1)

        #action Function(reset_memory_game)
        text "Quit" text_align 0.5 color "#00000000" size 25

default card_amount= 24# number of cards
default card_rows =3# change rows when we change card numbers
default cards=[]
default selected_cards=[]
default hidden_cards =0
default match_found= False

label start:
    $randomize_cards()# to call game in another part of visual novel
    call screen memory_mini_game # also to call game in another part of novel in this order
    return
