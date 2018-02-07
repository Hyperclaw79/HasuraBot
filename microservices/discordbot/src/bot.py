import discord
import inspect
import aiohttp
import os
import asyncio
from textwrap import dedent
from brain import HyperAI
import requests
import math

discord_token = os.environ["DISCORD_TOKEN"]

class Response:
    def __init__(self, content, reply=False, delete_after=0):
        self.content = content
        self.reply = reply
        self.delete_after = delete_after

class HasuraHub:
    def __init__(self):
        self.url = "https://wcbb1vvlrc-dsn.algolia.net/1/indexes/hasura_apps_hub/query"
        headers = {
            'x-algolia-agent':'HasuraBot',
            'x-algolia-application-id':'WCBB1VVLRC',
            'x-algolia-api-key': os.environ["ALOGIA_KEY"]
        }
        self.sess = requests.Session()
        self.sess.headers.update(headers)

    def query(self, param):
        body = {"params":'query={}&hitsPerPage=1000&page=0'.format(param)}
        respo = self.sess.post(url=self.url,json=body).json()
        return [{"name":"{}/{}".format(hit["username"],hit["name"]),"description":hit["description"]} for hit in respo["hits"]]


class HasuraBot(discord.Client):
    def __init__(self):
        self.prefix = '*'
        super().__init__()
        self.aiosession = aiohttp.ClientSession(loop=self.loop)
        self.http.user_agent += ' HasuraBot/1.0'
        self.brain = HyperAI(os.environ["BRAIN_USER"],os.environ["BRAIN_KEY"],"HyperAI")
        self.hubber = HasuraHub()
        
        
    async def on_ready(self):
        print('HasuraBot is now live!')
        game = discord.Game(name="the byte crunching game. #HasuraFTW")
        await self.change_presence(game=game)


    async def cmd_ping(self, message):
        """
        Usage:
            {command_prefix}ping
                        
        Is it alive??
        """
        await message.channel.send("Pong!")

    async def cmd_say(self, message):
        """
        Usage:
            {command_prefix}say [your message]
                        
        Echoes your message after deleting it.
        """
        msg = message.content.replace("{}say".format(self.prefix),'').strip() 
        await message.channel.send(msg)
        try:
            await message.delete()    
        except:
            print('Jeez! I need better permissions in {}.'.format(message.guild))

    async def cmd_shrug(self, message):
        """
        Usage:
            {command_prefix}shrug
                        
        ASCII Shrugimation.
        """
        await message.delete()
        shrugList = ["`¯\__(ツ)/¯`", "`¯\_(ツ)_/¯`", "`¯\(ツ)__/¯`", "`¯\_(ツ)_/¯`"]
        lulz = await message.channel.send(shrugList[1])
        i = 2
        while i < 400:
            await lulz.edit(content=shrugList[i%4])
            i = i + 1    

    async def cmd_wow(self, message):
        """
        Usage:
            {command_prefix}wow [your message]
                        
        Stylize your message using emoji letters.
        """
        message_content = message.content.strip()
        chan = message.channel
        await message.delete()
        mesg = message_content.replace('{}wow'.format(self.prefix), '')
        symbol_dict = {
            '!':":exclamation:",
            '?':":question:",
            '+':":heavy_plus_sign:",
            '-':":heavy_minus_sign:",
            '*':":asterisk:",
            '#':":hash:"
        }
        t = ""
        nums = ['zero','one','two','three','four','five','six','seven','eight','nine']
        for c in mesg:
           if c in symbol_dict.keys():
               c = symbol_dict[c]   
           elif ord(c)<90 and ord(c)>=65:
              c = chr(ord(c)+32)
              c = ":regional_indicator_{}: ".format(c)
           elif c == " ":
              c = "  "
           elif ord(c)>=97 and ord(c)<=122:
              c = ":regional_indicator_{}: ".format(c)
           elif int(c)>=0 and int(c)<=9: 
              c = ":{}:".format(nums[int(c)])
           t = t + c
        await chan.send('\n{}'.format(t))            

    async def cmd_ppap(self, message):
       """
       Usage: 
       {command_prefix}ppap

       PPAP cancer, bot version.
       """
       mes = await message.channel.send("`¯\_(ツ)_/¯`")
       await mes.edit(content=":pen_ballpoint:         \n¯\_(ツ)_/¯")
       await asyncio.sleep(1)	   
       await mes.edit(content=":pen_ballpoint:         :apple:\n¯\_(ツ)_/¯")
       await asyncio.sleep(1) 	   
       await mes.edit(content=":apple::pen_ballpoint:")
       await asyncio.sleep(2.5)
       await mes.edit(content=":pen_ballpoint:         \n¯\_(ツ)_/¯")
       await asyncio.sleep(1) 	   
       await mes.edit(content=":pen_ballpoint:         :pineapple:\n¯\_(ツ)_/¯")
       await asyncio.sleep(1)	   
       await mes.edit(content=":pineapple::pen_ballpoint:")
       await asyncio.sleep(2.5)	   
       await mes.edit(content=":apple::pen_ballpoint:")
       await asyncio.sleep(1)	   
       await mes.edit(content=":pineapple::pen_ballpoint:")
       await asyncio.sleep(2.5)
       contents = [":pen_ballpoint:",":pineapple:",":apple:",":pen_ballpoint:"]
       initial = ""
       for content in contents:
        await mes.edit(content=initial+content)
        initial = mes.content     	     

    async def cmd_moonwalk(self, message):
       """
       Usage:
           {command_prefix}moonwalk
                
       Use to see an emoji perform moonwalk.
       """
       m1 = await message.channel.send(".:walking:")	
       l = [":runner:",":walking:"]
       t = "."
       for i in range(25):
          t = t + "."
          s = t+l[i%2]
          await m1.edit(content=s)

    async def cmd_react(self, message):
        """
        Usage:
            {command_prefix}react <animated> [reaction1 reaction2 ....]
                        
        Add a list of reactions to the previous message. Separate the emojis with spaces.
        For an animated emoji, add the keyword animated and use the emoji name. 
            Eg. aww_yeah instead of :aww_yeah:
        """
        target = await message.channel.history(limit=1, before=message).next()
        if "animated" in message.content:
            emoji_dict = {}
            for emoji in list(message.guild.emojis):
                emoji_dict[emoji.name] = emoji
            reactions = message.content.replace('{}react ','').split(' ')[1:]
            await message.delete()
            for reaction in reactions:
                try:
                    await target.add_reaction(emoji_dict[reaction])
                except Exception as e:
                    print(str(e))    
        else:
            reactions = message.content.replace('{}react ','').split(' ')
            await message.delete()
            for reaction in reactions:
                try:
                    await target.add_reaction(reaction)
                except Exception as e:
                    print(str(e))    
    
    async def cmd_iam(self, message):
        """
        Usage:
            {command_prefix}iam role
                        
        Assign yourself the entry level role.
        """
        def check1(reaction, clicker):
            return clicker == user and reaction.message.id == base.id and reaction.emoji in list(roles_dict.keys())
        intent = message.content.split('{}iam '.format(self.prefix))[1].split(' ')[0].strip()
        user = message.author
        guild = self.get_guild(int(os.environ["GUILD_ID"]))
        user = guild.get_member(user.id)             
        if intent.lower() == "intern":
            intern = [role for role in guild.roles if role.name == "hpdf-intern"][0]
            react = [role for role in guild.roles if role.name == "hpdf-reactjs"][0]
            native = [role for role in guild.roles if role.name == "hpdf-react-native"][0]
            express = [role for role in guild.roles if role.name == "hpdf-nodejs-express"][0]
            flask = [role for role in guild.roles if role.name == "hpdf-python-flask"][0]
            react_icon = [emoji for emoji in guild.emojis if emoji.name == "reactjs"][0]
            native_icon = [emoji for emoji in guild.emojis if emoji.name == "reactnative"][0]        
            express_icon = [emoji for emoji in guild.emojis if emoji.name == "node"][0]
            flask_icon = [emoji for emoji in guild.emojis if emoji.name == "flask"][0]
            roles_dict = {
                            react_icon: react,
                            native_icon: native,
                            express_icon: express,
                            flask_icon: flask
                        }
            await user.add_roles(intern)
            base = await user.send("Hey {}, you've successfully been assigned the `@hpdf-intern` role.".format(user.mention) + \
                    "Please react to this message with your appropriate framework.")
            for reaction in list(roles_dict.keys()):
                await base.add_reaction(reaction)
            reaction, clicker = await self.wait_for('reaction_add', check=check1)
            role = roles_dict[reaction.emoji]
            await user.add_roles(role)
            await base.delete()
            final = await user.send("{}, you've been successfully assigned the `@{}` role. :thumbsup:".format(user.mention, role))
            await user.send("Please keep HPDF conversations in channel under the `HPDF` category.")
            await asyncio.sleep(120)
            await final.delete()
            log = guild.get_channel(int(os.environ["LOG_CHANNEL"]))
            await log.send('User {} has been assigned `@{}` role and they chose the framework `@{}`.'.format(user.name+'#'+user.discriminator, intern, role))
        elif intent.lower() == "ca":
            ca = [role for role in guild.roles if role.name == "HasuraCA"][0]
            await user.add_roles(ca)
            await user.send("Successfully assigned you as `@{}`. :thumbsup:".format(ca))
            await user.send("Please keep the ca related conversation in #hasura-campus-ambassadors." + \
                            "\nFeel free to chat about general things in the public channel.")
            log = guild.get_channel(int(os.environ["LOG_CHANNEL"]))
            await log.send('User {} has been assigned `@{}` role.'.format(user.name+'#'+user.discriminator, role))
        else:
            await user.send('You must either choose `intern` or `CA`.')    

    async def cmd_iamnot(self, message):
        """
        Usage:
            {command_prefix}iamnot [your message]
                        
        Remove a role from yourself.
        """
        param = message.content.split('{}iamnot '.format(self.prefix))[1].split(' ')[0].strip()
        guild = self.get_guild(int(os.environ["GUILD_ID"]))
        role = [role for role in guild.roles if role.name.lower() == param.lower()][0]  
        user = message.author
        user = guild.get_member(user.id)       
        await user.remove_roles(role)
        log = guild.get_channel(int(os.environ["LOG_CHANNEL"]))
        await log.send('User {} has removed the `@{}` role for themselves.'.format(user.name+'#'+user.discriminator, role))
        await user.send("Successfully removed the `@{}` role. :thumbsup:".format(role))

    async def cmd_prune(self, message):
        """
        Usage:
            {command_prefix}prune
                        
        Deletes last X messages. Mods only.
        """
        role = str(message.author.top_role)
        mods = ["admin","team hasura","moderator"]
        if role in mods:
            try:
                count = int(message.content.split('{}prune '.format(self.prefix))[1].split(' ')[0].strip())
                try:
                    await message.channel.purge(limit=count+1)
                    notif = await message.channel.send("Successfully deleted the last {} messages. :thumbsup:".format(count))
                    await asyncio.sleep(30)
                    await notif.delete()
                except PermissionError:
                    await message.channel.send("Looks like I don't have permission to delete messages here. :eyes:")        
                except Exception as e:
                    print(str(e))        
            except IndexError:
                notif = await message.channel.send("You didn't provide the count.")
                await asyncio.sleep(30)
                await notif.delete()
        else:
            await message.author.send("Sorry but only the mods can prune messages. :sweat_smile:")

    async def cmd_help(self, message):
        """
        Usage:
            {command_prefix}help [command]
        
        Prints a help message.
        If a command is specified, it prints a help message for that command.
        Otherwise, it lists the available commands.
        """
        try:
            command = message.content.split("{}help ".format(self.prefix))[1].strip()
            cmdc = getattr(self, 'cmd_' + command, None)
            if cmdc:
                content = dedent(cmdc.__doc__).replace('{command_prefix}', '@   ' + self.prefix)
                content = content.replace('Usage','Usage (exclude the @)').replace('\n\n','\n')
                await message.author.send('```py\n{}```'.format(content))
            else:
                await message.author.send('No such command')
        except:
            msg1 = await message.author.send('**HasuraBot Commands List:**\n')
            commands = []
            cmdc = {}
            #txt2 = ''
            #txt3 = ''
            for att in dir(self):
                if att.startswith('cmd_') and att != 'cmd_help':
                    try:
                        atc = getattr(self, att)
                        cmdc[att] = dedent(atc.__doc__.split('\n')[4])
                    except:
                        print('Skipping hidden command: ' + att)
            comlen = len(cmdc)
            delme = await message.author.send('__Total number of commands__: **{}**\n'.format(comlen))
            txt1 = "```md\n"
            for att in cmdc:
                txt1 += dedent('[{}]( {})\n' .format(att.replace('cmd_', self.prefix),cmdc[att]))
            txt1 += "```"    
            await delme.edit(content=delme.content+txt1)
            await asyncio.sleep(300)
            await msg1.delete()
            await delme.delete()

    async def cmd_hub(self, message):
        """
        Usage:
            {command_prefix}hub <list [quickstart | bot]>
        
        Fetches descriptions of quickstarts or bots (more to come soon) available on Hasura Hub.
        If no arguments are specified, opens up an interactive embed for you to make a choice.
        To get only the list, add the keyword list and type either quickstart or bot.
        Examples:
            To get a list of all bots on the hub:
                {command_prefix}hub list bots
            To get a list of all quickstarts on the hub:
                {command_prefix}hub list quickstart
            To get descriptions along with the project names:
                {command_prefix}hub
                This will open an interactable menu.      
        """
        def check(reaction, user):
            return reaction.message.id == base.id and user == message.author and reaction.emoji in reaction_list

        async def paginator(base,pointers,embeds):
            def reaction_check(reaction,user):
                return user == message.author and reaction.message.id == base.id and reaction.emoji in pointers
            cursor = 0
            while True: 
                reaction, user = await self.wait_for('reaction_add',check=reaction_check)
                op = pointers.index(reaction.emoji)
                if op == 1 and cursor < len(embeds) - 1:
                    cursor += 1
                    await base.edit(embed=embeds[cursor])
                elif op == 0 and cursor > 0:
                    cursor -= 1
                    await base.edit(embed=embeds[cursor])
                else:
                    pass
        
        def embed_generator(flatten,project_list,current,total):
            hub_embed = discord.Embed(title="List of Projects",description="\u200B",color=15728640)
            if flatten:
                for project in project_list:
                    val = '\u200B'
                    hub_embed.add_field(name=project["name"], value=val, inline=False)
            else:
                for project in project_list:
                    if len(project["description"]) <= 1024:
                        hub_embed.add_field(name=project["name"], value=project["description"])
                    else:
                        val = '\n'.join(project["description"].split('\n\n')[:3])
                        hub_embed.add_field(name=project["name"], value=val)
                    hub_embed.add_field(name="\u200B", value="\u200B\n", inline=False)
            hub_embed.set_footer(text="{}/{}".format(current,total),icon_url="http://www.iconsplace.com/download/red-list-256.png")
            return hub_embed

        async def _main(param,flatten):
            if not flatten:
                choices = discord.Embed(title="Choose the corresponding option:",
                    description="1. Quickstarts\n2. Bots",
                    color=15728640)
                choices.set_thumbnail(url="https://hasura.io/rstatic/resources/boilerplates.png")
                base = await message.channel.send(content=message.author.mention,embed=choices)
                reaction_list = ['1\u20e3','2\u20e3']
                param_list = ['hasura/hello','bot']
                for reaction in reaction_list:
                    await base.add_reaction(reaction)
                reaction, user = await self.wait_for('reaction_add',check=check)
                choice = reaction_list.index(reaction.emoji)
                projects = self.hubber.query(param=param_list[choice])
                await base.clear_reactions()
            else:
                base = await message.channel.send("{} Fetching results. Please wait. :hourglass_flowing_sand:".format(message.author.mention))
                if param.lower() in ["quickstart","quickstarts"]:
                    projects = self.hubber.query(param="hasura/hello")
                elif param.lower() in ["bot","bots"]:
                    projects = self.hubber.query(param="bot")
            embeds = [embed_generator(flatten,projects[i:i+4],int(i/4)+1,math.ceil(len(projects)/4)) for i in range(0,len(projects),4) ]
            await base.edit(content=message.author.mention,embed=embeds[0])
            pointers = ['👈','👉']
            for pointer in pointers:
                await base.add_reaction(pointer)
            asyncio.ensure_future(paginator(base,pointers,embeds))
        
        if "list" in message.content:
            param = message.content.replace('{}hub list '.format(self.prefix),'').strip()
            param = param.split(' ')[0]
            flatten = True
        else:
            param = None
            flatten = False
        await _main(param,flatten)        




    async def on_message(self, message):
        if self.prefix not in message.content and message.content != "(╯°□°）╯︵ ┻━┻" and not self.user.mentioned_in(message):
            return
        
        if self.user.mentioned_in(message) and not message.mention_everyone:
            async with message.channel.typing():
                response = await self.brain.query(message.content)
                await message.channel.send("{} {}".format(message.author.mention,response))

        # we do not want the bot to reply to itself or other bots
        if message.author.id == self.user.id or message.author.bot:
            return

        if message.content == "(╯°□°）╯︵ ┻━┻":
            await message.channel.send("┬─┬ ノ( ゜-゜ノ)")    

        #----------------------------------------------------------------------------#
        # Don't worry about this part. We are just defining **kwargs for later use.
        cmd, *args = message.content.split(' ') # The first word is cmd, everything else is args. 
        cmd = cmd[len(self.prefix):].lower().strip() # For '$', cmd = cmd[1:0]. Eg. $help -> cmd = help
        handler = getattr(self,'cmd_{}'.format(cmd),None) # Checks if MyBot has an attribute called cmd_command (cmd_help).
        if not handler: # The command given doesn't exist in our code, so ignore it.
            return
        prms = inspect.signature(handler) # If attr is defined as async def help(a,b='test',c), prms = (a,b='test',c)
        params = prms.parameters.copy() # Copy since parameters are immutable.
        h_kwargs = {}                   # Dict for group testing all the attrs.
        if params.pop('message',None):
            h_kwargs['message'] = message
        if params.pop('mentions',None):
            h_kwargs['mentions'] = list(map(message.server.get_member, message.raw_mentions)) # Gets the user for the raw mention and repeats for every user in the guild.            
        if params.pop('args',None):
            h_kwargs['args'] = args

        # For remaining undefined keywords:
        for key, param in list(params.items()):
            if not args and param.default is not inspect.Parameter.empty: # Junk parameter present for attribute 
                params.pop(key) 
                continue        # We don't want that in our tester.

            if args:
                h_kwargs[key] = args.pop(0) # Binding keys to respective args.
                params.pop(key)

        # Time to call the test.
        res = await handler(**h_kwargs)
        if res and isinstance(res, Response): # Valid Response object
                content = res.content
                if res.reply:
                    content = '{},{}'.format(message.author.mention, content)

                sentmsg = await message.channel.send(content)

bot = HasuraBot()    
bot.run(discord_token)
