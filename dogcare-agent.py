from ai_engine.chitchat import ChitChatDialogue
from ai_engine.messages import DialogueMessage
from uagents import Agent, Context, Model
from premai import Prem
from uagents.setup import fund_agent_if_low


mailbox_key = '4fd4524b-6623-41c2-ae84-f118884add43'


# Initialize the agent with the name, seed, mailbox, and log level
agent = Agent(
    name="dog-car-rag-agent",
    seed="dog-car-rag-agent-seed",
    mailbox=f"{mailbox_key}@https://agentverse.ai",
    log_level="DEBUG",
)

fund_agent_if_low(agent.wallet.address())


async def dog_query(query):
  client = Prem(api_key="<YOUR_PREM_API_KEY>"
  )    #Paste the PREM API key
  messages = [
        { "role": "user", "content": query },
    ]
  repositories = dict(
      ids=[1234],    #Replace with the Repository ID created in PREM
      similarity_threshold=0.25,
      limit=5
  )
  # Create completion
  response = client.chat.completions.create(
      project_id=1234,      #Replace with the Project ID created in PREM
      messages=messages,
      repositories=repositories,
      stream=False,
      model="gpt-4o",      #You can define a different LLM here based on performance
    )
  print(response.choices[0].message.content)
    final_response = response.choices[0].message.content
    return final_response


# define dialogue messages; each transition needs a separate message
class InitiateChitChatDialogue(Model):
    """I initiate ChitChat dialogue request"""
    pass

class AcceptChitChatDialogue(Model):
    """I accept ChitChat dialogue request"""
    pass

class ChitChatDialogueMessage(DialogueMessage):
    """ChitChat dialogue message"""
    pass

class ConcludeChitChatDialogue(Model):
    """I conclude ChitChat dialogue request"""
    pass

class RejectChitChatDialogue(Model):
    """I reject ChitChat dialogue request"""
    pass


# instantiate the dialogues
chitchat_dialogue = ChitChatDialogue(
    version="0.1",
    storage=agent.storage,
)


#Dialogue message handlers
@chitchat_dialogue.on_initiate_session(InitiateChitChatDialogue)
async def start_chitchat(
    ctx: Context,
    sender: str,
    _msg: InitiateChitChatDialogue,
):
    ctx.logger.info(f"Received init message from {sender} Session: {ctx.session}")
    # do something when the dialogue is initiated
    await ctx.send(sender, AcceptChitChatDialogue())


@chitchat_dialogue.on_start_dialogue(AcceptChitChatDialogue)
async def accepted_chitchat(
    ctx: Context,
    sender: str,
    _msg: AcceptChitChatDialogue,
):
    ctx.logger.info(
        f"session with {sender} was accepted. This shouldn't be called as this agent is not the initiator."
    )


@chitchat_dialogue.on_reject_session(RejectChitChatDialogue)
async def reject_chitchat(
    ctx: Context,
    sender: str,
    _msg: RejectChitChatDialogue,
):
    # do something when the dialogue is rejected and nothing has been sent yet
    ctx.logger.info(f"Received conclude message from: {sender}")


@chitchat_dialogue.on_continue_dialogue(ChitChatDialogueMessage)
async def continue_chitchat(
    ctx: Context,
    sender: str,
    msg: ChitChatDialogueMessage,
):
    # do something when the dialogue continues
    ctx.logger.info(f"Received message: {msg.user_message} from: {sender}")
    try:

        response = await dog_query(msg.user_message)
        await ctx.send(
            sender,
            ChitChatDialogueMessage(
                type="agent_message",
                agent_message=response,
            ),
        )
    except EOFError:
        await ctx.send(sender, ConcludeChitChatDialogue())


@chitchat_dialogue.on_end_session(ConcludeChitChatDialogue)
async def conclude_chitchat(
    ctx: Context,
    sender: str,
    _msg: ConcludeChitChatDialogue,
):
    # do something when the dialogue is concluded after messages have been exchanged
    ctx.logger.info(f"Received conclude message from: {sender}; accessing history:")
    ctx.logger.info(ctx.dialogue)


agent.include(chitchat_dialogue, publish_manifest=True)


if __name__ == "__main__":
    print(f"Agent address: {agent.address}")
    agent.run()