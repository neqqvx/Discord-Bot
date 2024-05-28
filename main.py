import discord
from discord.ext import commands
import os
import json
import random

TOKEN = ""

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.remove_command('help')
money = {}


#HEEEEEEEELP!!!!!!!!!!!!!!!!!!!!!
@bot.command()
async def help(ctx):
  embed = discord.Embed(title="Команды бота", color=discord.Color.blue())
  embed.add_field(name="!help", value="Показывает список команд", inline=False)
  embed.add_field(name="!rules",
                  value="Показывает правила сервера",
                  inline=False)
  embed.add_field(name="!youtube",
                  value="Показывает youtube разработчика",
                  inline=False)
  embed.add_field(name="!работа",
                  value="Пользователь получает монеты",
                  inline=False)
  embed.add_field(name="!баланс",
                  value="Показывает баланс пользователя",
                  inline=False)
  embed.add_field(
      name="!ставка",
      value="Пользователь ставит ставку(Пример: !ставка 50 красное/черное)",
      inline=False)
  embed.set_footer(text="Бот создан с помощью discord.py(creator wxst)")
  embed.set_thumbnail(url="https://example.com/bot_avatar.png")
  embed.set_image(url="https://example.com/bot_gif.gif")

  await ctx.send(embed=embed)


@bot.command()
async def test1(ctx):
  embed = discord.Embed(title="Привет всем!", )
  await ctx.send(embed=embed)


@bot.command()
async def youtube(ctx):
  embed = discord.Embed(
      color=discord.Colour.blue(),
      title="Ссылка",
      description="Ссылка для перехода на оффициальный YouTube разработчика",
      url='https://www.youtube.com/channel/UCXUtLlXZvqlioNjC2N2BImw',
  )
  await ctx.send(embed=embed)


class Buttons(discord.ui.View):  # класс описывает набор кнопок

  def init(self, *, timeout=180):  # конструктор класса
    super().init(timeout=timeout)

  # этому методу будет сопоставлена кнопка. По клику метод будет вызван.
  @discord.ui.button(label="Button", style=discord.ButtonStyle.gray)
  async def gray_button(self, button: discord.ui.Button,
                        interaction: discord.Interaction):
    # ищи сведения об объекте discord.Interaction, чтобы понять, что ещё можно сделать в обработчике кнопки.
    await interaction.response.edit_message(
        content=f"This is an edited button response!")
    # альтернативно, тут ты можешь вызывать требуемые тебе методы и вообще делать что нужно


@bot.command()
async def button(ctx):  # по команде !button отсылается сообщение с кнопками
  await ctx.send(
      "ТЕСТ!",  # текст сообщения как обычно
      view=Buttons()  # создаём экземпляр класса Buttons и прикрепляем его
  )


@bot.event
async def on_ready():
  print(f'{bot.user.name} has joined Discord!')


#приветствие бота в лс
@bot.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(
      f'Привет {member.name}! Добро пожаловать на наш сервер')
  await member.dm_channel.send(
      f'ВНИМАНИЕ {member.name}! Напиши в чат команду !rules и прочитай правила сервера что бы избежать наказаний'
  )


@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(
      type=discord.ActivityType.watching, name="за сервером(neverlose)"))
  print(f'{bot.user.name} подключился к Discord и настроил профиль!')


#-------------------------casino-------------------------
cool_down_period = 10


@bot.command()
async def работа(ctx):
  if ctx.author.id not in money:
    money[ctx.author.id] = 10

  earned_money = random.randint(500, 5000)
  money[ctx.author.id] += earned_money

  embed = discord.Embed(title="Работа выполнена",
                        description=f"Вы заработали {earned_money} монет🪙!",
                        color=discord.Colour.blue())
  await ctx.send(embed=embed)


@bot.command()
async def ставка(ctx, bet_amount: int, bet: str):
  if ctx.author.id not in money:
    money[ctx.author.id] = 0
  if bet_amount > money[ctx.author.id]:
    embed = discord.Embed(title="Ошибка",
                          description="У вас недостаточно средств для ставки!",
                          color=discord.Colour.red())
    await ctx.send(embed=embed)
    return

  result = random.choice(['красное', 'черное'])
  if result == bet:
    money[ctx.author.id] += bet_amount
    outcome = f"Поздравляю, вы выиграли! Ваш баланс увеличен на {bet_amount} монет🪙"
    color = discord.Colour.blue()
  else:
    money[ctx.author.id] -= bet_amount
    outcome = f"К сожалению, вы проиграли. Ваш баланс уменьшен на {bet_amount} монет⭕️"
    color = discord.Colour.red()

  embed = discord.Embed(title="Результат ставки",
                        description=outcome,
                        color=color)
  await ctx.send(embed=embed)


@bot.command()
async def баланс(ctx):
    if ctx.author.id in money:
      balance = money[ctx.author.id]
    else:
      balance = 0

      embed = discord.Embed(title="Баланс",description=f"Ваш текущий баланс:{balance} монет🪙",
                        color=discord.Colour.blue())
    await ctx.send(embed=embed)


@bot.command(name='open_case')
async def open_case(ctx):
  user = ctx.author
  money = random.randint(10,
                         100)  # Генерация случайного количества монет в кейсе
  await ctx.send(f'{user.mention}, вы открыли кейс и получили {money} монет!')


  #ruleeeeeeeeeeeeeeeeeeeeeeeeeees!!!!!!!!------------------
@bot.command()
async def rules(ctx):
  embed = discord.Embed(
      title="Правила сервера",
      description="Пожалуйста, ознакомьтесь с правилами сервера",
      color=discord.Color.blue())

  rules_text = """
    Правило 1: Будьте вежливы и уважайте других участников.
    Правило 2: Не поощряйте или не участвуйте в незаконных действиях.
    Правило 3: Не размещайте оскорбительный, ненормативный контент.
    Правило 4: Соблюдайте общие правила Discord.
    """

  embed.add_field(name="Правила", value=rules_text, inline=False)
  embed.set_footer(text="Соблюдайте правила и наслаждайтесь общением!")

  await ctx.send(embed=embed)

#КИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИК
@bot.command()
async def kick(ctx, member: discord.Member, reason):
  await ctx.send("Изгоняем участника {0} по причине: {1}".format(
      member, reason))
  await member.kick(reason=f'{ctx.author} Выгнал {member}')


  #МУУУУУУУУУУУУУУУУУУУУУУУУУУТ


@bot.command()
async def case(ctx):
  user = ctx.author
  if user.id not in money:
    money[user.id] = 350
  case_reward = random.randint(10, 10000)
  money[user.id] += case_reward
  embed = discord.Embed(title='Кейс открыт!',
                        description=f'Вы получили {case_reward} монет',
                        color=discord.Color.blue())
  await ctx.send(embed=embed)


async def give_initial_balance():
  while True:
    for user_id in money.keys():
      money[user_id] += 10  # Начисление монет каждые 30 минут
    await asyncio.sleep(1800)


bot.run(token=TOKEN)