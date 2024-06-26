import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Dodanie tego Intentsa

bot = commands.Bot(command_prefix='!', intents=intents)

class MigrationView(discord.ui.View):
    @discord.ui.button(label='Rozpocznij migrację', style=discord.ButtonStyle.primary)
    async def start_migration(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            print(f'Przycisk start_migration został naciśnięty przez {interaction.user.name}.')

            # Sprawdź, czy bot ma uprawnienia do tworzenia kanałów
            if not interaction.guild.me.guild_permissions.manage_channels:
                print('Bot nie ma uprawnień do zarządzania kanałami.')
                await interaction.response.send_message('Nie mam wystarczających uprawnień, aby utworzyć kanał tekstowy.', ephemeral=True)
                return

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True)
            }

            channel_name = f'migration-channel-{interaction.user.name}'
            print(f'Tworzenie kanału: {channel_name}')

            channel = await interaction.guild.create_text_channel(name=channel_name, overwrites=overwrites)

            message = (
                f'Pomyślnie utworzono kanał {channel.mention}! '
                'Proszę odpowiedz na wiadomość w ⁠migration-ticket, aby utworzyć zgłoszenie, jeśli jesteś zainteresowany migracją.\n\n'
                'Otworzymy prywatny kanał\n\n'
                'Następnie poprosimy Cię o podanie kilku informacji:\n'
                '1. 2 zrzuty ekranu profilu - z przodu i z tyłu\n'
                '2. Marsze, które używasz\n'
                '3. Wyposażenie i uzbrojenie dla każdego marszu\n'
                '4. Poziom VIP oraz kolejne dni logowania\n'
                '5. Rola: Pola otwarte / Garnizon / Dowódca rajdu\n'
                '6. Statystyki z ostatniego KvK (Królestwa kontra Królestwa)\n'
                '7. Farmy (moc, centrum, rolnictwo/wypełnianie)\n'
                '8. Wydatki\n'
                '9. Wydatki na technologię kryształów\n\n'
                'Gdy tylko jeden z oficerów będzie online, odpowie tak szybko, jak to możliwe, i kontynuuje rozmowę'
            )

            await channel.send(message)
            await interaction.response.send_message(f'Pomyślnie utworzono kanał {channel.mention}! Zapraszamy do kontynuacji w tym kanale.', ephemeral=True)

        except discord.Forbidden:
            print('Błąd: Brak uprawnień do tworzenia kanału.')
            await interaction.response.send_message('Nie mam wystarczających uprawnień, aby utworzyć kanał tekstowy.', ephemeral=True)

        except Exception as e:
            print(f'Wystąpił wyjątek: {e}')
            await interaction.response.send_message(f'Wystąpił błąd podczas tworzenia kanału: {e}', ephemeral=True)

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')

@bot.command(name='create_migration_ticket')
async def create_migration_ticket(ctx):
    try:
        print(f'Komenda create_migration_ticket została wywołana przez {ctx.author.name}')
        view = MigrationView()
        await ctx.send('Kliknij poniższy przycisk, aby rozpocząć migrację:', view=view)
    except Exception as e:
        print(f'Wystąpił wyjątek w create_migration_ticket: {e}')
        await ctx.send(f'Wystąpił błąd podczas tworzenia biletu migracyjnego: {e}')

TOKEN = os.getenv('TOKEN')

if TOKEN:
    bot.run(TOKEN)
else:
    print('Nie udało się pobrać tokenu. Upewnij się, że zmienna środowiskowa TOKEN jest prawidłowo ustawiona w panelu Secrets w Replit.')
