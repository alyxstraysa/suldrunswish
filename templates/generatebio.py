char_dict = {
    'RACE': 'Drow',
    'STR': 10,
    'DEX': 10,
    'CON': 10,
    'INT': 10,
    'WIS': 10,
    'CHA': 10,

}

bio = "Nine Dogs the {race}, Str: {strength}, Dex: {dexterity}, Con: {constitution}, Int: {intelligence}, Wis: {wisdom}, Charisma: {charisma}"  .format(
    race=char_dict['RACE'])
strength = char_dict['STR'],
dexterity = char_dict['DEX'],
constitution = char_dict['CON'],
intelligence = char_dict['INT'],
wisdom = char_dict['WIS'],
Charisma = char_dict['CHA']

if __name__ == "__main__":
    print(bio)
