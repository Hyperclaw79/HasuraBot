import aiohttp
import asyncio
import discord
import inspect
import math
import os
import requests
from textwrap import dedent

from utils.brain import Brain
from utils.paginator import Paginator, Embedder
from utils.urbanify import Urban

discord_token = os.environ["DISCORD_TOKEN"]

class HasuraHub:
    def __init__(self):
        self.url = "https://wcbb1vvlrc-dsn.algolia.net/1/indexes/hasura_apps_hub/query"
        headers = {
            'x-algolia-agent':'HasuraBot',
            'x-algolia-application-id':'WCBB1VVLRC',
            'x-algolia-api-key': os.environ["ALGOLIA_KEY"]
        }
        self.sess = requests.Session()
        self.sess.headers.update(headers)

    def query(self, param):
        body = {"params":'query={}&hitsPerPage=1000&page=0'.format(param)}
        respo = self.sess.post(url=self.url,json=body).json()
        return [{"name":"{}/{}".format(hit["username"],hit["name"]),"description":hit["description"]} for hit in respo["hits"]]

class AdminLogin:
    def __init__(self):
        data = {
          "provider": "username",
          "data": {
            "username": "admin",
            "password": os.environ['ADMIN_PASSWORD']
          }
        }
        resp = requests.post('https://auth.{}.hasura-app.io/v1/login'.format(os.environ['CLUSTER_NAME']),json=data)
        self.bearer_token = resp.json()['auth_token']
        
    def get_bearer(self):
        headers = {
            "Authorization":"Bearer {}".format(self.bearer_token)
        }
        resp = requests.get('https://auth.{}.hasura-app.io/v1/user/info'.format(os.environ['CLUSTER_NAME']),headers=headers).json()
        if not resp.get('hasura_id', None):
            self.__init__()
        return self.bearer_token

class HasuraBot(discord.Client):
    def __init__(self):
        self.prefix = '*'
        super().__init__()
        self.owner = None
        self.loop = asyncio.get_event_loop()
        self.aiosession = aiohttp.ClientSession(loop=self.loop)
        self.http.user_agent += ' HasuraBot/1.5'
        self.brain = Brain(os.environ["BRAIN_USER"],os.environ["BRAIN_KEY"],"HasuraAI",self.loop)
        self.hubber = HasuraHub()
        self.data_connector = requests.Session()
        self.admin = AdminLogin()
        self.admin_token = ''

    async def on_ready(self):
        info = await self.application_info()
        self.owner = info.owner
        print('HasuraBot.\nVersion 1.0\nCreated by {}.'.format(self.owner))
        self.admin_token = self.admin.get_bearer()
        created_brain = await self.brain.create()
        print(created_brain)

    def is_owner(self, user):
        return self.owner.id == user.id    

    def is_mod(self, user):
        mod_roles = ["moderator","admin","team hasura"]
        return any((role for role in mod_roles if role in (role.name for role in user.roles)))

    def is_admin(self, user):
        mod_roles = ["admin","team hasura"]
        return any((role for role in mod_roles if role in (role.name for role in user.roles)))

    async def cmd_exec(self, message):
        if self.is_owner(message.author):
            parsed = message.content.replace('{}exec '.format(self.prefix),'')
            parsed = parsed.replace('```py','').replace('```','')
            namespace = {}
            exec(parsed, namespace)
            await message.channel.send(namespace["content"])

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
        try:
            await message.delete()
        except:
            pass
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
        try:
            await message.delete()
        except:
            pass
        mesg = message_content.replace('{}wow'.format(self.prefix), '')
        symbol_dict = {
            '!':":exclamation:",
            '?':":question:",
            '+':":heavy_plus_sign:",
            '-':":heavy_minus_sign:",
            '*':":asterisk:",
            '#':":hash:",
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
           elif ord(c)>=48 and ord(c)<=57: 
              c = ":{}:".format(nums[int(c)])
           else:
               c = "**{}**".format(c)   
           t = t + c
        await chan.send('\n{}'.format(t))            

    async def cmd_ppap(self, message):
        """
        Usage:
            {command_prefix}ppap
                        
        PPAP Cancer, bot version.
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
            reactions = message.content.replace('{}react '.format(self.prefix),'').split(' ')[1:]
            try:
                await message.delete()
            except:
                pass
            for reaction in reactions:
                try:
                    await target.add_reaction(emoji_dict[reaction])
                except Exception as e:
                    print(str(e))    
        else:
            reactions = message.content.replace('{}react '.format(self.prefix),'').split(' ')
            try:
                await message.delete()
            except:
                pass
            for reaction in reactions:
                try:
                    await target.add_reaction(reaction)
                except Exception as e:
                    print(str(e))

    async def cmd_ud(self, message):
        """
        Usage:
            {command_prefix}ud <word>
                        
        Get the meanings of a word/phrase from urban dictionary.
        If no word is given, gets a single meaning of a random word.
        """
        word = message.content.replace("{}ud".format(self.prefix),'').strip()
        urban = Urban()
        responses = urban.fetch(word)
        if len(responses) == 0:
            await message.channel.send("Sorry {}, couldn't find any results for {}.".format(message.author.mention, word))
            return
        embedder = Embedder(message.author.avatar_url)
        embeds = [
                embedder.generate(
                    responses[i]["word"], 
                    {
                        "Meaning":responses[i]["meaning"], 
                        "Example":responses[i]["example"]
                    },
                    i+1,
                    len(responses)
                ) for i in range(len(responses))
            ]
        if len(embeds) == 1:   
            await message.channel.send(content=message.author.mention,embed=embeds[0])
        else:
            base = await message.channel.send("{} Fetching results. Please wait. :hourglass_flowing_sand:".format(message.author.mention))
            pager = Paginator(message, base, embeds, self)
            await pager.run()    

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
        log = guild.get_channel(int(os.environ["LOG_CHANNEL"]))
        framework_change = False             
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
            existing = [role for role in list(roles_dict.values()) if role in user.roles]
            await user.add_roles(intern)
            if intern not in user.roles:
                base = await user.send("Hey {}, you've successfully been assigned the `@hpdf-intern` role.".format(user.mention) + \
                    "Please react to this message with your appropriate framework.")
                framework_change = True    
            elif len(existing) > 0:
                base = await user.send("You already have a framework assigned to you." + \
                    "Please use `*iamnot {}` before trying this command.".format(existing[0]))
                return    
            else:
                base = await user.send("Please react to this message with your appropriate framework.")
            for reaction in list(roles_dict.keys()):
                await base.add_reaction(reaction)
            reaction, clicker = await self.wait_for('reaction_add', check=check1)
            role = roles_dict[reaction.emoji]
            await user.add_roles(role)
            await base.delete()
            content = "{}, you've been successfully assigned the `@{}` role. :thumbsup:".format(user.mention, role.name) + \
            "\nPlease keep HPDF conversations in channel under the `HPDF` category."
            final = await user.send(content)
            await asyncio.sleep(120)
            await final.delete()
            content = "User {} has switched to the {} framework.".format(user.name+'#'+user.discriminator,role.name.replace("hpdf-",''))
            if framework_change:
                content = content.replace("switched to","been assigned `@hpdf-intern` role and they chose")
            await log.send(content)
        elif intent.lower() == "ca":
            ca = [role for role in guild.roles if role.name == "Hasura CA"][0]
            if ca in user.roles:
                await user.send("You already have the `@Hasura CA` role.")
                return    
            await user.add_roles(ca)
            content = "Successfully assigned you as `@{}`. :thumbsup:".format(ca) + \
                "\nPlease keep the ca related conversation in #hasura-campus-ambassadors." + \
                "\nFeel free to chat about general things in the public channel."
            await user.send(content)
            await log.send('User {} has been assigned `@{}` role.'.format(user.name+'#'+user.discriminator, role))
        else:
            await user.send('You must either choose `intern` or `CA`.')    

    async def cmd_iamnot(self, message):
        """
        Usage:
            {command_prefix}iamnot [your message]
                        
        Remove a role from yourself.
        """
        param = message.content.split('{}iamnot '.format(self.prefix))[1].strip()
        guild = self.get_guild(int(os.environ["GUILD_ID"]))
        try:
            role = [role for role in guild.roles if role.name.lower() == param.lower()][0]  
            user = message.author
            user = guild.get_member(user.id)       
            await user.remove_roles(role)
            log = guild.get_channel(int(os.environ["LOG_CHANNEL"]))
            await log.send('User {} has removed the `@{}` role for themselves.'.format(user.name+'#'+user.discriminator, role))
            await user.send("Successfully removed the `@{}` role. :thumbsup:".format(role))
        except:
            await message.author.send("Couldn't find the specified role. Please retry.".format(param))

    async def cmd_prune(self, message):
        """
        Usage:
            {command_prefix}prune
                        
        Deletes last X messages. Mods only.
        """
        def admin_check(msg):
            return not self.is_admin(msg.author)

        if self.is_mod(message.author):
            try:
                count = int(message.content.split('{}prune '.format(self.prefix))[1].split(' ')[0].strip())
                try:
                    await message.channel.purge(limit=count+1, check=admin_check)
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
        def embedder(command):
            cmdc = getattr(self, 'cmd_' + command, None)
            content = dedent(cmdc.__doc__).replace('{command_prefix}', self.prefix)
            seperator = content.split('Usage:\n')[1].split('\n\n')
            syntax = seperator[0]
            details = '\n'.join(seperator[1:])
            embed = discord.Embed(title=command.title(), description='\u200B', color=15728640)
            embed.add_field(name='Syntax', value=syntax, inline=False)
            if 'Examples' in details:
                desc, examples = details.split('Examples:')
                embed.add_field(name='Description', value=desc.strip(), inline=False)
                embed.add_field(name='Examples', value=examples.strip(), inline=False)
            else:
                embed.add_field(name='Description', value=details.strip(), inline=False)
            embed.set_thumbnail(url=self.user.avatar_url)
            return embed
        def valid(att):
            validity_checks = [
                att.startswith('cmd_'),
                att != 'cmd_help',
                getattr(self, att, None).__doc__!=None
            ]
            return all(validity_checks)

        try:
            command = message.content.split("{}help ".format(self.prefix))[1].strip()
            cmdc = getattr(self, 'cmd_' + command, None)
            if cmdc:
                embed = embedder(command)
                await message.author.send(embed=embed)
            else:
                await message.author.send('No such command')
        except:
            embeds = []
            valids = [att for att in dir(self) if valid(att)]
            for valid in valids:
                embed = embedder(valid.replace('cmd_', ''))
                current = valids.index(valid) + 1
                embed.set_footer(text="{}/{}".format(current, len(valids)),icon_url=message.author.avatar_url)
                embeds.append(embed)
            base = await message.author.send(content='**HasuraBot Commands List:**\n', embed=embeds[0])
            pager = Paginator(message, base, embeds, self)
            await pager.run(content='**HasuraBot Commands List:**\n')
            

    async def cmd_hub(self, message):
        """
        Usage:
            {command_prefix}hub <list [quickstart | bot]>
        
        Fetches descriptions of quickstarts, bots, webstacks, etc. available on Hasura Hub.
        If no arguments are specified, opens up an interactive embed for you to make a choice.
        To get only the list, add the keyword 'list'.
        To do a simple search, add the keyword 'search'.
        Examples:
        To get a list of all bots on the hub:
            {command_prefix}hub list bots
        To get a list of all quickstarts on the hub:
            {command_prefix}hub list quickstart
        To get descriptions along with the project names:
            {command_prefix}hub
            This will open an interactable menu.
        To get description of a specific project, say, ShowBot:
            {command_prefix}hub search ShowBot              
        """
        
        async def _main(param, flatten, search):
            def check(reaction, user):
                return user == message.author and reaction.message.id == base.id and reaction.emoji in reaction_list
        
            mappings = {
                'Quickstarts :smiling_imp:': 'hasura/hello',
                'Bots :robot:': 'bot',
                'AR/VR :eyeglasses:': 'ar/vr',
                'Datascience/ML/AI :microscope:': 'data science',
                'Mobile :iphone:': 'mobile',
                'Webstacks :books:':'web'
            }
            try:
                if not any([flatten, search]):
                    choices = discord.Embed(title="Choose the corresponding option:",
                        description=''.join(["{}. {}\n".format(i+1,q) for i,q in enumerate(mappings.keys())]),
                        color=15728640)
                    choices.set_thumbnail(url="https://hasura.io/rstatic/resources/boilerplates.png")
                    base = await message.channel.send(content=message.author.mention,embed=choices)
                    reaction_list = ['{}\u20e3'.format(i+1) for i in range(6)]
                    param_list = ['hasura/hello','bot','ar/vr','data science','mobile','web']
                    for reaction in reaction_list:
                        await base.add_reaction(reaction)
                    reaction, user = await self.wait_for('reaction_add',check=check)
                    choice = int(reaction.emoji.split('\u20e3')[0]) - 1
                    projects = self.hubber.query(param=param_list[choice])
                    await base.clear_reactions()
                elif search:
                    base = await message.channel.send("{} Fetching results. Please wait. :hourglass_flowing_sand:".format(message.author.mention))
                    projects = self.hubber.query(param=param.lower())
                else:
                    exists = [key for key in mappings.keys() if param.lower() in key.lower()]
                    base = await message.channel.send("{} Fetching results. Please wait. :hourglass_flowing_sand:".format(message.author.mention))
                    if len(exists) > 0:
                        projects = self.hubber.query(param=mappings[exists[0]])
                    else:
                        projects = self.hubber.query(param=param.lower())
                if flatten:
                    for project in projects:
                        project["description"] = '\u200B'
                project_batch = [projects[i:i+4] for i in range(0,len(projects),4) ]
                book = []
                for job in project_batch:
                    page = {}
                    for project in job:
                        page[project["name"]] = project["description"]
                    book.append(page)
                embedder = Embedder(message.author.avatar_url)    
                embeds = [embedder.generate(
                                "List of Projects", 
                                book[i], 
                                i+1,
                                len(book)) for i in range(len(book))]
                pager = Paginator(message, base, embeds, self)
                await pager.run()
            except:
                await message.channel.send("Sorry {}, couldn't find any results for {}.".format(message.author.mention,param))
                await base.delete()

        if "list" in message.content:
            param = message.content.replace('{}hub list '.format(self.prefix),'').strip()
            param = param.split(' ')[0]
            flatten = True
            search = False
        elif "search" in message.content:
            param = message.content.replace('{}hub search '.format(self.prefix),'').strip()
            flatten = False
            search = True
        else:
            param = None
            flatten = False
            search = False
        await _main(param, flatten, search)        

    async def cmd_purge_dupes(self, message):
        def _get_members(member):
            roles = [role for role in member.roles if "hpdf" in role.name and role.name != 'hpdf-intern']
            if len(roles) > 1:
                return True, roles
            else:
                return False, None    

        if self.is_mod(message.author):
            intern = [role for role in message.guild.roles if "intern" in role.name][0]
            users = [(member, _get_members(member)[1]) for member in intern.members if _get_members(member)[0]]
            for user in users:
                rolesText = '```'+'\n'.join([role.name for role in user[1]])+'```'
                await user[0].send("Since you have these duplicate roles: {}\n".format(rolesText) + \
                    "You are being unassigned of these roles. Please use `*iam intern` again.")
                await user[0].remove_roles(*user[1])


    async def cmd_feedback(self, message):
        """
        Usage:
            {command_prefix}feedback [Message]
                        
        Send a feedback message to the creator.
        If you spam, you will be automatically blacklisted from using the bot commands.
        Be reasonable. Thank you.
        """
        template = "User **{}** from the **{}** says:\n```\n{}\n```"
        content = message.content.replace("{}feedback ".format(self.prefix),'').strip()
        if content != "" and not self.is_owner(message.author):  #Remove the second condition during tests. 
            if message.guild:
                await self.owner.send(template.format(message.author.name, message.guild.name, content))
            else:
                template = template.replace('from the **{}** ','')
                await self.owner.send(template.format(message.author.name, content))
            await message.author.send("Thank you for your feedback. :thumbsup::skin-tone-1:")

    async def cmd_code(self, message, mentions):
        """
        Usage:
            {command_prefix}code [@username] <prefix>
                        
        If you ever spot someone posting a code without using codeblock, please use this command as shown.
        Provide the prefix of the language too, if you know which language that is.
        Examples:
        User test_dummy typed some code but you don't recognize the language:
            {command_prefix}code @test_dummy
        User test_dummy typed some code and you know it is in python:
            {command_prefix}code @test_dummy py
        """
        def user_check(msg):
            return msg.author.id == mentions[0].id and len(msg.mentions)==0
        try:
            prefix = message.clean_content.split('{}code @{}'.format(self.prefix, mentions[0].display_name))[1]
            prefix = prefix.strip()
        except:
            prefix = ""
        target = await message.channel.history(before=message).find(user_check)
        try:
            await message.delete()
            await target.delete()
        except:
            pass
        await message.channel.send('**{}**:\n```{}\n{}\n```'.format(mentions[0].display_name, prefix, target.content))

    async def cmd_add_tag(self, message):
        """
        Usage:
            {command_prefix}add_tag tag_name
                        
        Moderators and above can add tags using this interface.
        """
        def check(msg):
            checks = [
                message.author.id == msg.author.id,
                '=' in msg.content
            ]
            return  all(checks) 
        if self.is_mod(message.author):
            command = message.content.replace('{}custom'.format(self.prefix),'').strip()
            template = "{} enter the response for \n```\n{}\n```\nStart your response with `reply=`."
            await message.channel.send(template.format(message.author.mention, command))
            reply_holder = await self.wait_for('message', check=check)
            reply = reply_holder.clean_content.split("=")[1].strip()
            url = "https://data.{}.hasura-app.io/v1/query".format(os.environ['CLUSTER_NAME'])
            requestPayload = {
                "type": "insert",
                "args": {
                    "table": "custom_commands",
                    "objects": [
                        {
                            "command": command.lower(),
                            "reply": reply
                        }
                    ]
                }
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.admin_token)
            }
            resp = self.data_connector.post(url, json=requestPayload, headers=headers)        
            if resp.status_code in [200, 304]:
                await reply_holder.add_reaction("👍🏻")
            else:
                await message.channel.send("Sorry {}, something went wrong. :confused:".format(message.author.mention))

    async def cmd_tag(self, message):
        """
        Usage:
            {command_prefix}tag tag_name
                        
        Display the reply for a given tag name.
        """
        command = message.content.replace('{}tag'.format(self.prefix),'').strip()
        url = "https://data.{}.hasura-app.io/v1/query".format(os.environ['CLUSTER_NAME'])
        requestPayload = {
            "type": "select",
            "args": {
                "table": "custom_commands",
                "columns": [
                    "reply"
                ],
                "where": {
                    "command": {
                        "$like": "%{}%".format(command.lower())
                    }
                }
            }
        }
        headers = {
            "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.admin_token)
        }
        resp = self.data_connector.post(url, json=requestPayload, headers=headers)        
        if resp.status_code in [200, 304]:
            res = resp.json()
            if res:
                await message.channel.send("{}\n{}".format(message.author.mention, res[0]["reply"]))
            else:
                await message.channel.send("Sorry {}, couldn't find any such tag".format(message.author.mention))
        else:
            print(resp.content)
            await message.channel.send("Sorry {}, something went wrong. :confused:".format(message.author.mention))

    async def cmd_bomb(self, message):
        """
        Usage:
            {command_prefix}bomb
                        
        Use this when you're really bored and got nothing better to do. XD
        """
        def check(rct, user):
            return rct.message.id == base.id and rct.emoji == '🔥' and user.id != self.user.id
        
        base = await message.channel.send(':bomb:')
        await base.add_reaction('🔥')
        try:
            reaction, user = await self.wait_for('reaction_add', check=check, timeout=25.0)
            await base.clear_reactions()
            embed = discord.Embed(title=f"OMG {user.display_name}!", description="What a sadist!", color=15728640)
            embed.set_image(url='https://vignette.wikia.nocookie.net/clashroyale/images/3/39/EXPLOSION%21.gif')
            await base.edit(content=None, embed=embed)
        except Exception as e:
            print(str(e))
            await base.clear_reactions()
            await base.edit(content='Phew Saved!')
        await asyncio.sleep(10.0)
        await base.delete()


    async def on_message(self, message):
        if self.prefix not in message.content and message.content != "(╯°□°）╯︵ ┻━┻" and not self.user.mentioned_in(message):
            return
        
        if self.user.mentioned_in(message) and not message.mention_everyone:
            async with message.channel.typing():
                response, status = await self.brain.query(message.content)
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
        handler = getattr(self,'cmd_{}'.format(cmd),None) # Checks if HasuraBot has an attribute called cmd_command (cmd_help).
        if not handler: # The command given doesn't exist in our code, so ignore it.
            return
        prms = inspect.signature(handler) # If attr is defined as async def help(a,b='test',c), prms = (a,b='test',c)
        params = prms.parameters.copy() # Copy since parameters are immutable.
        h_kwargs = {}                   # Dict for group testing all the attrs.
        if params.pop('message',None):
            h_kwargs['message'] = message
        if params.pop('mentions',None):
            h_kwargs['mentions'] = list(map(message.guild.get_member, message.raw_mentions)) # Gets the user for the raw mention and repeats for every user in the guild.            
        

        # For remaining undefined keywords:
        for key, param in list(params.items()):
            if param.default is not inspect.Parameter.empty: # Junk parameter present for attribute 
                params.pop(key) 
                continue        # We don't want that in our tester.

            if args:
                h_kwargs[key] = args.pop(0) # Binding keys to respective args.
                params.pop(key)

        # Time to call the test.
        res = await handler(**h_kwargs)

bot = HasuraBot()    
bot.run(discord_token)
