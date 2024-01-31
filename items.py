from utils import *

class Item:
    def __init__(self, name: str=None, repr: str=None, callback: Utils.Function=None):
        self.Name = name
        self.Repr = repr or "⍰"
        self.Callback = callback

    class Callbacks:
        @staticmethod
        async def Beer(player, game, interaction):
            pass

        @staticmethod
        async def Saw(player, game, interaction):
            pass

        @staticmethod
        async def Cigarette(player, game, interaction):
            player.Health+=1

        @staticmethod
        async def MagnifyingGlass(player, game, interaction):
            from bot import BRBot
            embed = BRBot.CreateEmbed("")
            embed.add_field(
                name="", 
                value=f'🔫\n{"".join("❓" for _ in range(len(game.Info.Gun.Chamber)-1))+"🔵🔴"[game.Info.Gun.Chamber[-1]]}'
            )
            await interaction.response.defer()
            await interaction.followup.send(Utils.Blank, ephemeral=True, embed=embed)

        @staticmethod
        async def Handcuffs(player, game, interaction):
            pass


Items = [
    Item("Beer", "🍺", Item.Callbacks.Beer),
    Item("Hand Saw", "🪚", Item.Callbacks.Saw),
    Item("Cigarette", "🚬", Item.Callbacks.Cigarette),
    Item("Magnifying Glass", "🔍", Item.Callbacks.MagnifyingGlass),
    Item("Handcuffs", "🔗", Item.Callbacks.Handcuffs)
]