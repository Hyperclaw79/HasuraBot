import discord
import inspect
import aiohttp
import os
import asyncio

discord_token = os.environ["DISCORD_TOKEN"]

class Response:
    def __init__(self, content, reply=False, delete_after=0):
        self.content = content
        self.reply = reply
        self.delete_after = delete_after

class HasuraBot(discord.Client):
    def __init__(self):
        self.prefix = '*'
        super().__init__()
        self.aiosession = aiohttp.ClientSession(loop=self.loop)
        self.http.user_agent += ' HasuraBot/1.0'

    async def on_ready(self):
        print('HasuraBot is now live!')
        game = discord.Game(name="the byte crunching game. #HasuraFTW")
        await self.change_presence(game=game)


    async def cmd_ping(self, message):
        await message.channel.send("Pong!")

    async def cmd_say(self, message):
        msg = message.content.replace("{}say".format(self.prefix),'').strip() 
        await message.channel.send(msg)
        try:
            await message.delete()    
        except:
            print('Jeez! I need better permissions in {}.'.format(message.guild))

    async def cmd_shrug(self, message):
        await message.delete()
        shrugList = ["`¯\__(ツ)/¯`", "`¯\_(ツ)_/¯`", "`¯\(ツ)__/¯`", "`¯\_(ツ)_/¯`"]
        lulz = await message.channel.send(shrugList[1])
        i = 2
        while True:
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

        t = ""
        nums = ['zero','one','two','three','four','five','six','seven','eight','nine']
        for c in mesg:
           if ord(c)<90 and ord(c)>=65:
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

       PPAP cancer bot version.
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
       await mes.edit(content=":pen_ballpoint:")		
       await mes.edit(content=":pen_ballpoint::pineapple:")		
       await mes.edit(content=":pen_ballpoint::pineapple::apple:")	   
       await mes.edit(content=":pen_ballpoint::pineapple::apple::pen_ballpoint:")    

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

    async def cmd_iam(self, message):
        def check1(reaction, clicker):
            return clicker == user and reaction.message.id == base.id and reaction.emoji in list(roles_dict.keys())
        intent = message.content.split('{}iam '.format(self.prefix))[1].split(' ')[0].strip()
        user = message.author
        guild = self.get_guild(407792526867693568)
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
            log = guild.get_channel(408641974640443413)
            await log.send('User {} has been assigned `@{}` role and they chose the framework `@{}`.'.format(user.name+'#'+user.discriminator, intern, role))
        elif intent.lower() == "ca":
            ca = [role for role in guild.roles if role.name == "HasuraCA"][0]
            await user.add_roles(ca)
            await user.send("Successfully assigned you as `@{}`. :thumbsup:".format(ca))
            await user.send("Please keep the ca related conversation in #hasura-campus-ambassadors." + \
                            "\nFeel free to chat about general things in the public channel.")
            log = guild.get_channel(408641974640443413)
            await log.send('User {} has been assigned `@{}` role.'.format(user.name+'#'+user.discriminator, role))
        else:
            await user.send('You must either choose `intern` or `CA`.')    

    async def cmd_iamnot(self, message):
        param = message.content.split('{}iamnot '.format(self.prefix))[1].split(' ')[0].strip()
        role = [role for role in guild.roles if role.name.lower() == param.lower()][0]  
        user = message.author       
        await user.remove_roles(role)
        await user.send("Successfully removed the `@{}` role. :thumbsup:".format(role))
        guild = self.get_guild(407792526867693568)
        log = guild.get_channel(408641974640443413)
        await log.send('User {} has removed the `@{}` role for themselves.'.format(user.name+'#'+user.discriminator, role))

    async def cmd_prune(self, message):
        role = str(message.author.top_role)
        mods = ["admin","team hasura","moderator"]
        if role in mods:
            try:
                count = int(message.content.split('{}prune '.format(self.prefix))[1].split(' ')[0].strip()) + 1
                try:
                    await message.channel.purge(limit=count)
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

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
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
        if params.pop('channel',None):
            h_kwargs['channel'] = message.channel
        if params.pop('guild',None):
            h_kwargs['guild'] = message.guild
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
