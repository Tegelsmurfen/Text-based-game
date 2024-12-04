import random as rand
import ASCII_art as ascii

print(ascii.text("Through the Trollgate"))

class Player:
    def __init__(self, difficulty):
        self.HP = {"1": 100, "2": 75, "3": 50}.get(difficulty, 0)
        self.inventory = []
        self.level = 1 #startnivå
        self.xp = 0 # start XP
        self.xp_to_next_level = 100 # XP som krävs för att nå nästa nivå
    
    def gain_xp(self, amount):
        self.xp += amount
        print(f"Du fick {amount} XP! Total XP: {self.xp}/{self.xp_to_next_level}")

    def check_level_up(self):
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5) #ökar krav till nästa level
            self.HP += 10 
            print(f"Du gick upp i level {self.level}! Ditt HP är nu {self.HP}.")

    def add_item(self, item):
        if len(self.inventory) < 5:
            self.inventory.append(item)
            print(f"Du hittade en {item}!")
        else:
            print("Din ryggsäck är full")
    
    def take_damage(self, damage):
        self.HP -= damage
        print(f"Du tog {damage} skada! Nuvarande HP: {self.HP}")

class Monster:
    monster_types = [
        ("Lilltrollet", 40), 
        ("Jätten", 50), 
        ("Lilleskutt", 60)
    ]

    def __init__(self):
        random_monster = rand.choice(self.monster_types)  # Slumpa ett monster från listan
        self.name = random_monster[0]  # Monstrets namn
        self.strength = random_monster[1]  # Monstrets styrka, som också används som dess HP

class Game:
    def __init__(self):
        self.player = None

    def start(self):
        if input("ÄR DU REDO?\n[1] Spela!\n[2] Avbryt\n> ") == "1":
            difficulty = input("Vilken svårighetsgrad vill du spela på? \n[1] Lätt  100hp\n[2] Medel 75hp\n[3] Svårt 50hp\n> ")
            self.player = Player(difficulty)
            if not self.player.HP:
                print("Ogiltigt val! Spelet avslutas.")
                return
            self.main_menu()
        else:
            print("Spelet avslutas. Hej då!")
    
    def main_menu(self):
        while self.player.HP > 0:
            choice = input("Vad vill du göra? \n[1] Inventory\n[2] Dörrar\n[3] Se dina egenskaper\n> ")
            if choice == "1":
                print(f"Ditt inventory: {self.player.inventory}")
            elif choice == "2":
                self.enter_doors()
            elif choice == "3": 
                print(f"HP: {self.player.HP}")
                print(f"Level: {self.player.level}")
            else:
                print("Ogiltigt val!")
            
            if self.player.HP <= 0:
                break
            
            while True:
                user_input = input("Fortsätta spela? (ja/nej): ").lower()
                if user_input == "ja":
                    break
                elif user_input == "nej":
                    print("spelet avslutas. Tack för du spelade!")
                    return
                else:
                    print("Ogiltigt svar, försök igen.")

        # Om HP är mindre än 0 avslutas spel med meddelande             
        print("Spelet är över!" if self.player.HP <= 0 else "Tack för att du spelade!")
    
    def enter_doors(self):
        if input("Välj dörr [1, 2, 3]: ") in ["1", "2", "3"]:
            rand.choice([self.monster_event, self.chest_event, self.trap_event])()
        else:
            print("Ogiltigt val!")
    
    def monster_event(self):
        monster = Monster()  # Skapa ett slumpat monster
        print(f"Du möter {monster.name}! Styrka: {monster.strength} HP: {monster.strength}")

        while self.player.HP > 0 and monster.strength > 0:
            print(f"\n Ditt HP: {self.player.HP} | {monster.name} HP: {monster.strength}")
            print("[1] Attackera [2] Blockera [3] Använd föremål")
            choice = input("Vad vill du göra? > ")

            if choice == "1":
                # Attackera
                player_damage = rand.randint(10, 25)
                monster.strength -= player_damage
                print(f"Du attackerar {monster.name} och gör {player_damage} skada!")
            elif choice == "2":
                # Blockera
                block_value = rand.randint(5, 15)
                if "Sköld" in self.player.inventory:
                    self.player.inventory.remove("Sköld")
                    block_value * 1.5 # osäker om det funkar
                    return
                print(f"Du förbereder dig för att blockera och reducerar inkommande skada med {block_value}!")
            elif choice == "3":
                # Använd föremål
                if "Hälsodryck" in self.player.inventory:
                    self.player.inventory.remove("Hälsodryck")
                    heal_amount = rand.randint(15, 30)
                    self.player.HP += heal_amount
                    print(f"Du drack en hälsodryck och återhämtade {heal_amount} HP! Din HP är nu {self.player.HP}.")
                else:
                    print("Du har inga hälsodrycker kvar!")
            else:
                print("Ogiltigt val. Du förlorar en tur!")
            
            # Kontrollera om monstret besegrats
            if monster.strength <= 0:
                xp_reward = rand.randint(20,50)
                print(f"\n Du besegrade {monster.name} och fick {xp_reward} XP!")
                self.player.gain_xp(xp_reward)
                break

            # Monstrets tur
            print(f"\n {monster.name}'s tur!")
            monster_choice = rand.choice(["attack", "special", "taunt"])

            if monster_choice == "attack":
                monster_damage = rand.randint(10, 20)
                print(f"{monster.name} attackerar och gör {monster_damage} skada!")
                self.player.take_damage(monster_damage)
            elif monster_choice == "special":
                monster_damage = rand.randint(15, 30)
                print(f"{monster.name} använder en kraftfull specialattack och gör {monster_damage} skada!")
                self.player.take_damage(monster_damage)
            elif monster_choice == "taunt":
                print(f"{monster.name} hånar dig och gör ingen skada denna tur!")

            # Kontrollera om spelaren besegrats
            if self.player.HP <= 0:
                print(f"\n {monster.name} besegrade dig! Du förlorade spelet.")
                break

    def chest_event(self):
        loot = rand.randint(1, 50)
        if loot <= 15:
            self.player.add_item("Sköld")
        elif loot <= 30:
            self.player.add_item("Hälsodryck")
        else:
            print("Du hittade inget i kistan")

    def trap_event(self):
        print("Du gick in i en fälla!")
        trap_damage = rand.randint(10,20)
        self.player.take_damage(trap_damage)

if __name__ == "__main__":
    game = Game()
    game.start()