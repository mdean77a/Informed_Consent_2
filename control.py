import chainlit as cl

@cl.on_chat_start
async def start():
    # Sending an action button within a chatbot message
    actions = [
        cl.Action(
            name="summary_button",
            icon="mouse-pointer-click",
            payload={"value": "summary"},
            label="Write summary"
        ),
        cl.Action(
            name="risk_button",
            icon="mouse-pointer-click",
            payload={"value": "risks"},
            label="Write risk section"
        ),
        cl.Action(
            name="benefits_button",
            icon="mouse-pointer-click",
            payload={"value": "benefits"},
            label="Write benefits section"
        ),
        cl.Action(
            name="file_button",
            icon="mouse-pointer-click",
            payload={"value": "markdown"},
            label="Create final file"
        )
    ]

    await cl.Message(content="Select consent form sections:", actions=actions).send()

@cl.action_callback("summary_button")
async def on_action(action: cl.Action):
       await cl.Message(content=f"Executed {action.payload["value"]}").send()
       await action.remove()

@cl.action_callback("risk_button")
async def on_action(action: cl.Action):
       await cl.Message(content=f"Executed {action.payload["value"]}").send()
       await action.remove()

@cl.action_callback("benefits_button")
async def on_action(action: cl.Action):
       await cl.Message(content=f"Executed {action.payload["value"]}").send()
       await action.remove()

@cl.action_callback("file_button")
async def on_action(action: cl.Action):
       await cl.Message(content=f"Executed {action.payload["value"]}").send()
       await action.remove()