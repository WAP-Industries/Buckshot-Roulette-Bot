import random

from settings import *
from utils import *


class Player:
    def __init__(self, user: nextcord.Member, health: int=5):
        self.User = user
        self.Name = user.name
        self.Health = health

class GameInfo:
    def __init__(self):
        self.Round = 1
        self.Turn = None
        self.Gun = Settings.RoundConfig[self.Round]
        random.shuffle(self.Gun)

class Game:
    def __init__(self, player1: nextcord.Member, player2: nextcord.Member, message: nextcord.Message):
        self.Player1, self.Player2 = Player(player1), Player(player2)
        self.Players = [self.Player1, self.Player2]
        self.Info = GameInfo()
        self.Message = Utils.Message(message)
        
        class B:
            Play = self.ButtonPlay
            Shoot = self.ButtonShoot
        self.Buttons = B

    @staticmethod
    def DebugMessage(text):
        return f"`{text}...`"

    async def UpdateDialogue(self, text):
        self.Message.Embed.set_footer(text=text)
        await self.Message.Reference.edit(content="", embed=self.Message.Embed)

    async def UpdateDisplay(self):
        from bot import BRBot
        AddBlank = lambda d: d.add_field(name="", value="", inline=False) 

        display = BRBot.CreateEmbed("")
        display.add_field(name=f"**{self.Player1.Name} vs {self.Player2.Name}**", value="")
        AddBlank(display)
        display.add_field( 
            name="",
            value = "\n\n".join(['**{}**\n{}'.format(i.Name, "".join("\u258D" for _ in range(i.Health))) for i in self.Players]),
            inline=False
        )
        AddBlank(display)
        self.Message.Embed = display
        await self.Message.Reference.edit(content="", embed=display)

    async def Shoot(self, shooter: Player, target: Player):
        bullet = self.Info.Gun.pop()
        target.Health-=1*bullet
        await self.UpdateDisplay()
        await self.UpdateDialogue(f'{shooter.Name} shot {"themself" if shooter==target else target.Name} with a {["blank", "live"][bullet]} round!')

    async def ButtonPlay(self, interaction: nextcord.Interaction):
        message = Utils.Message(await interaction.response.send_message(content=Game.DebugMessage(Settings.Messages.LoadOptions), ephemeral=True))
        await message.AddButton("Shoot", "🔫", self.Buttons.Shoot)

    async def ButtonShoot(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        message = Utils.Message(await interaction.original_message())
        await interaction.edit_original_message(content=Utils.Blank, view=None)

        current = self.Player1 if self.Player1.User==interaction.user else self.Player2
        enemy = self.Player2 if current==self.Player1 else self.Player2
        
        await message.AddButton("Yourself", "🤓", lambda _: self.Shoot(current, current))
        await message.AddButton(enemy.User.name, "😈", lambda _: self.Shoot(current, enemy))