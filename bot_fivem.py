import discord
from discord import app_commands
from discord.ui import Modal, TextInput, View
import random

# --- CONFIGURAÇÕES ---
TOKEN = 'SEU TOKEN'

# Cargos
ID_CARGO_MEMBRO = 0000000000000000000
ID_CARGO_ADV1 = 0000000000000000000
ID_CARGO_ADV2 = 0000000000000000000
ID_CARGO_ADV3 = 0000000000000000000

# Canais (REGISTRO E ANÚNCIOS)
ID_CANAL_SOLICITACOES = 0000000000000000000
ID_CANAL_LOGS_STAFF = 0000000000000000000
ID_CANAL_ANUNCIOS_PROMO = 0000000000000000000
ID_CANAL_ANUNCIOS_REBAIX = 0000000000000000000

# Canais NOVOS (PD e ADV - Privado e Público)
ID_CANAL_PD_STAFF = 0000000000000000000    # Log detalhado, Só Staff vê
ID_CANAL_PD_PUBLICO = 0000000000000000000  # Anúncio pra geral ver
ID_CANAL_ADV_STAFF = 0000000000000000000   # Log detalhado, Só Staff vê
ID_CANAL_ADV_PUBLICO = 0000000000000000000 # Anúncio pra geral ver

# --- FRASES (Essas frases já estão prontas, caso queira add mais, só colocar seguindo o padrão abaixo) ---
FRASES_PROMOCAO = [
    "Parabéns pela dedicação! Seu esforço foi reconhecido.",
    "Nova patente, novas responsabilidades. Voa garoto!",
    "Merecido demais! Continue fazendo um ótimo trabalho.",
    "A subida é fruto de muito suor. Parabéns pela conquista!",
    "Mais um degrau alcançado. O topo é o limite!"
]

FRASES_REBAIXAMENTO = [
    "Não desanime! Use isso como combustível para voltar mais forte.",
    "Um passo atrás para dar dois à frente. Foco total!",
    "Erros acontecem, o importante é aprender e evoluir. Não desista.",
    "A jornada é feita de altos e baixos. Recupere seu espaço!",
    "Foi apenas um deslize. Acreditamos na sua recuperação."
]

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.add_view(BotaoRegistroView())
        await self.tree.sync()

# --- SISTEMA DE REGISTRO ---

class AdminAprovacaoView(View):
    def __init__(self): super().__init__(timeout=None)
    
    @discord.ui.button(label="Aprovar", style=discord.ButtonStyle.green, custom_id="adm_aprovar", emoji="✅")
    async def aprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.processar_registro(interaction, aprovado=True)
        
    @discord.ui.button(label="Reprovar", style=discord.ButtonStyle.red, custom_id="adm_reprovar", emoji="✖️")
    async def reprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.processar_registro(interaction, aprovado=False)
        
    async def processar_registro(self, interaction: discord.Interaction, aprovado: bool):
        embed = interaction.message.embeds[0]
        user_field = embed.fields[0].value
        user_id = int(user_field.replace('<@', '').replace('>', ''))
        id_game = embed.fields[1].value
        nome_rp = embed.fields[2].value
        
        guild = interaction.guild
        member = guild.get_member(user_id)
        role_verificado = guild.get_role(ID_CARGO_VERIFICADO)
        staff_member = interaction.user
        
        if aprovado:
            if member:
                try:
                    novo_apelido = f"{nome_rp} | {id_game}"
                    if member.id != guild.owner_id: 
                        await member.edit(nick=novo_apelido)
                    
                    if role_verificado: 
                        await member.add_roles(role_verificado)
                    
                    embed.color = discord.Color.green()
                    embed.title = "✅ Registro Aprovado"
                    embed.set_footer(text=f"Aprovado por {staff_member.display_name}")
                    self.clear_items()
                    await interaction.response.edit_message(embed=embed, view=self)
                except discord.Forbidden: 
                    await interaction.response.send_message("❌ Erro de Permissão (Hierarquia de cargos).", ephemeral=True)
            else: 
                await interaction.response.send_message("❌ Usuário saiu do servidor.", ephemeral=True)
        else:
            embed.color = discord.Color.red()
            embed.title = "✖️ Registro Reprovado"
            embed.set_footer(text=f"Reprovado por {staff_member.display_name}")
            self.clear_items()
            await interaction.response.edit_message(embed=embed, view=self)

class FormularioRegistro(Modal, title="Registro FiveM"):
    nome_rp = TextInput(label="Nome do Personagem", placeholder="Ex: Kaua Matoso", max_length=20)
    id_game = TextInput(label="ID do Jogo", placeholder="Ex: 7094", max_length=6, style=discord.TextStyle.short)
    recrutador = TextInput(label="Recrutador", placeholder="Quem te recrutou?", required=False, max_length=30)
    
    async def on_submit(self, interaction: discord.Interaction):
        canal_admin = interaction.guild.get_channel(ID_CANAL_SOLICITACOES)
        if not canal_admin: return
        
        embed = discord.Embed(title="Solicitação de Registro", color=discord.Color.gold())
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.add_field(name="Usuário", value=interaction.user.mention, inline=True)
        embed.add_field(name="ID", value=self.id_game.value, inline=True)
        embed.add_field(name="Nome", value=self.nome_rp.value, inline=True)
        embed.add_field(name="Recrutador", value=self.recrutador.value or "Não informado", inline=False)
        
        await canal_admin.send(embed=embed, view=AdminAprovacaoView())
        await interaction.response.send_message("✅ Solicitação enviada!", ephemeral=True)

class BotaoRegistroView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="INICIAR REGISTRO", style=discord.ButtonStyle.blurple, custom_id="btn_registro_inicio", emoji="📝")
    async def botao_callback(self, interaction: discord.Interaction, button: discord.ui.Button): 
        await interaction.response.send_modal(FormularioRegistro())

client = Client()

@client.event
async def on_ready(): print(f'Bot logado como {client.user}')

@client.tree.command(name="comecar", description="Inicia o sistema de registro")
@app_commands.checks.has_permissions(administrator=True)
async def comecar(interaction: discord.Interaction):
    embed = discord.Embed(title="Verificação Obrigatória", description="Clique abaixo para se registrar.", color=discord.Color.from_rgb(47, 49, 54))
    await interaction.channel.send(embed=embed, view=BotaoRegistroView())
    await interaction.response.send_message("Iniciado!", ephemeral=True)

# --- FUNÇÕES AUXILIARES DE LOG (COM PROTEÇÃO CONTRA ERRO) ---

async def enviar_log_staff(guild, titulo, cor, campos):
    try:
        canal = guild.get_channel(ID_CANAL_LOGS_STAFF)
        if canal:
            embed = discord.Embed(title=titulo, color=cor)
            for nome, valor in campos: embed.add_field(name=nome, value=valor, inline=False)
            embed.set_footer(text=f"Data: {discord.utils.utcnow().strftime('%d/%m/%Y %H:%M')}")
            await canal.send(embed=embed)
    except Exception as e:
        print(f"Erro Log Staff: {e}")

async def enviar_anuncio_publico(guild, membro, tipo, cargo_antigo, cargo_novo, motivo):
    if tipo == "promo":
        canal = guild.get_channel(ID_CANAL_ANUNCIOS_PROMO)
        cor = discord.Color.green()
        titulo = "🎉 Nova Promoção!"
        frase = random.choice(FRASES_PROMOCAO)
        emoji_novo = "🌟"
    else:
        canal = guild.get_channel(ID_CANAL_ANUNCIOS_REBAIX)
        cor = discord.Color.red()
        titulo = "⚠️ Atualização de Cargo"
        frase = random.choice(FRASES_REBAIXAMENTO)
        emoji_novo = "🔻"

    if not canal: return

    try:
        nome_real, id_jogo = membro.display_name.split('|')
    except:
        nome_real = membro.display_name
        id_jogo = "Não definido"

    embed = discord.Embed(title=titulo, description=frase, color=cor)
    embed.set_thumbnail(url=membro.display_avatar.url)
    
    embed.add_field(name="Membro", value=f"**{nome_real.strip()}**", inline=True)
    embed.add_field(name="Passaporte (ID)", value=f"`{id_jogo.strip()}`", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    
    if cargo_antigo:
        embed.add_field(name="🔽 Cargo Anterior", value=cargo_antigo.mention, inline=True)
        
    embed.add_field(name=f"{emoji_novo} Novo Cargo", value=cargo_novo.mention, inline=True)

    if membro.avatar:
        embed.set_footer(text=f"ID Discord: {membro.id}", icon_url=membro.avatar.url)
    else:
        embed.set_footer(text=f"ID Discord: {membro.id}")

    try:
        await canal.send(embed=embed)
    except:
        print(f"ERRO: Não consegui enviar no canal de promoções {canal.id} (Verifique permissões!)")

# --- SISTEMA PD e ADV ---

async def log_pd_completo(guild, membro, staff, motivo):
    # 1. Log Privado
    try:
        canal_priv = guild.get_channel(ID_CANAL_PD_STAFF)
        if canal_priv:
            embed = discord.Embed(title="💀 REGISTRO DE PD (PRIVADO)", color=discord.Color.dark_grey())
            embed.set_thumbnail(url=membro.display_avatar.url)
            embed.add_field(name="Membro", value=f"{membro.mention} (`{membro.id}`)", inline=False)
            embed.add_field(name="Aplicado por", value=staff.mention, inline=False)
            embed.add_field(name="Motivo", value=motivo, inline=False)
            embed.set_footer(text=f"Data: {discord.utils.utcnow().strftime('%d/%m/%Y %H:%M')}")
            await canal_priv.send(embed=embed)
        else:
            print(f"ERRO: Canal PD Staff não encontrado. ID: {ID_CANAL_PD_STAFF}")
    except Exception as e:
        print(f"ERRO no Log PD Staff: {e}")

    # 2. Anúncio Público
    try:
        canal_pub = guild.get_channel(ID_CANAL_PD_PUBLICO)
        if canal_pub:
            embed_pub = discord.Embed(title="💀 MEMBRO DESLIGADO", description=f"O membro {membro.mention} recebeu **PD** e não faz mais parte da organização.", color=discord.Color.dark_grey())
            embed_pub.add_field(name="Motivo", value=motivo, inline=False)
            embed_pub.set_image(url="https://media.tenor.com/P5Gf8c4WqY4AAAAC/wasted-gta.gif") 
            await canal_pub.send(embed=embed_pub)
        else:
            print(f"ERRO: Canal PD Público não encontrado. ID: {ID_CANAL_PD_PUBLICO}")
    except discord.Forbidden:
        print("ERRO CRÍTICO: O Bot não tem permissão de 'Enviar Mensagens' no canal de PD PÚBLICO!")
    except Exception as e:
        print(f"ERRO no Log PD Público: {e}")


# --- COMANDOS DE GESTÃO ---

@client.tree.command(name="promover", description="Adiciona um novo cargo ao membro (Acumulativo).")
@app_commands.checks.has_permissions(manage_roles=True)
async def promover(interaction: discord.Interaction, membro: discord.Member, cargo: discord.Role, motivo: str = "Reconhecimento"):
    if membro.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
        await interaction.response.send_message("❌ Hierarquia insuficiente.", ephemeral=True)
        return

    try:
        await membro.add_roles(cargo)
        await interaction.response.send_message(f"✅ Promovido! (Cargo {cargo.name} adicionado)", ephemeral=True)
        
        await enviar_log_staff(interaction.guild, "📈 Log de Promoção", discord.Color.blue(), [
            ("Staff", interaction.user.mention),
            ("Membro", membro.mention),
            ("Cargo Adicionado", cargo.mention),
            ("Motivo", motivo)
        ])
        await enviar_anuncio_publico(interaction.guild, membro, "promo", None, cargo, motivo)
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ Erro: Permissão negada.", ephemeral=True)

@client.tree.command(name="rebaixar", description="Rebaixa um membro (Troca de cargo).")
@app_commands.checks.has_permissions(manage_roles=True)
async def rebaixar(interaction: discord.Interaction, membro: discord.Member, cargo_atual: discord.Role, novo_cargo: discord.Role, motivo: str = "Reajuste"):
    if membro.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
        await interaction.response.send_message("❌ Hierarquia insuficiente.", ephemeral=True)
        return

    try:
        await membro.remove_roles(cargo_atual)
        await membro.add_roles(novo_cargo)
        await interaction.response.send_message(f"✅ Rebaixado!", ephemeral=True)
        
        await enviar_log_staff(interaction.guild, "📉 Log de Rebaixamento", discord.Color.orange(), [
            ("Staff", interaction.user.mention),
            ("Membro", membro.mention),
            ("Perdeu o Cargo", cargo_atual.mention),
            ("Recebeu o Cargo", novo_cargo.mention),
            ("Motivo", motivo)
        ])
        await enviar_anuncio_publico(interaction.guild, membro, "rebaixar", cargo_atual, novo_cargo, motivo)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Erro: Permissão negada.", ephemeral=True)

@client.tree.command(name="pd", description="💀 Aplica PD (Remove do servidor e registra nos 2 canais).")
@app_commands.checks.has_permissions(kick_members=True)
async def pd(interaction: discord.Interaction, membro: discord.Member, motivo: str):
    if membro.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
        await interaction.response.send_message("❌ Você não pode dar PD em alguém com cargo maior ou igual ao seu!", ephemeral=True)
        return

    try:
        try:
            await membro.send(f"🚨 **VOCÊ RECEBEU UM PD**\n**Motivo:** {motivo}\n**Servidor:** {interaction.guild.name}")
        except: pass

        await membro.kick(reason=motivo)
        await interaction.response.send_message(f"💀 **PD Aplicado com sucesso em {membro.display_name}!**", ephemeral=True)

        await log_pd_completo(interaction.guild, membro, interaction.user, motivo)

    except discord.Forbidden:
        await interaction.response.send_message("❌ Erro: Permissão negada para expulsar.", ephemeral=True)


@client.tree.command(name="adv", description="⚠️ Aplica Advertência (Automático 1->2->3 + PD).")
@app_commands.checks.has_permissions(manage_roles=True)
async def adv(interaction: discord.Interaction, membro: discord.Member, motivo: str):
    if membro.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
        await interaction.response.send_message("❌ Hierarquia insuficiente.", ephemeral=True)
        return

    guild = interaction.guild
    role_adv1 = guild.get_role(ID_CARGO_ADV1)
    role_adv2 = guild.get_role(ID_CARGO_ADV2)
    role_adv3 = guild.get_role(ID_CARGO_ADV3)

    if not role_adv1 or not role_adv2 or not role_adv3:
        await interaction.response.send_message("❌ Erro na configuração dos cargos de ADV!", ephemeral=True)
        return

    novo_nivel = "ADV 1"
    acao_extra = ""
    foi_kickado = False

    try:
        if role_adv2 in membro.roles:
            await membro.remove_roles(role_adv2)
            await membro.add_roles(role_adv3)
            novo_nivel = "ADV 3 (PD AUTOMÁTICO)"
            acao_extra = "Membro removido automaticamente."
            
            try: await membro.send(f"🚨 **VOCÊ FOI REMOVIDO (ADV 3)**\n**Motivo:** {motivo}")
            except: pass
            
            await membro.kick(reason=f"ADV 3 acumulada - {motivo}")
            foi_kickado = True

        elif role_adv1 in membro.roles:
            await membro.remove_roles(role_adv1)
            await membro.add_roles(role_adv2)
            novo_nivel = "ADV 2"
        else:
            await membro.add_roles(role_adv1)
            novo_nivel = "ADV 1"

        await interaction.response.send_message(f"⚠️ **Advertência aplicada!** Nível: {novo_nivel}", ephemeral=True)

        await log_adv_completo(guild, membro, interaction.user, novo_nivel, motivo, acao_extra)

        if foi_kickado:
            motivo_pd = f"Acúmulo de Advertências (ADV 3) - Último motivo: {motivo}"
            await log_pd_completo(guild, membro, interaction.user, motivo_pd)

    except discord.Forbidden:
        await interaction.response.send_message("❌ Erro de permissão.", ephemeral=True)

client.run(TOKEN)
