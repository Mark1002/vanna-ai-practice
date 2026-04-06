
from vanna import Agent, AgentConfig
from vanna.servers.fastapi import VannaFastAPIServer
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext
from vanna.integrations.anthropic import AnthropicLlmService
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.integrations.sqlite import SqliteRunner
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.capabilities.sql_runner import RunSqlToolArgs
from vanna.tools.visualize_data import VisualizeDataArgs


class SimpleUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        # In production, validate cookies/JWTs here
        user_email = request_context.get_cookie('vanna_email') or "admin@example.com"
        
        print(f"Resolving user for email: {user_email}")

        if user_email == "admin@example.com":
            return User(id="admin1", email=user_email, group_memberships=['admin'])
        
        return User(id="user1", email=user_email, group_memberships=['user'])


def main():
    tools = ToolRegistry()
    tools.register_local_tool(RunSqlTool(sql_runner=SqliteRunner(database_path="./Chinook.sqlite")), access_groups=['admin', 'user'])
    tools.register_local_tool(VisualizeDataTool(), access_groups=['admin', 'user'])
    agent_memory = DemoAgentMemory(max_items=1000)
    tools.register_local_tool(SaveQuestionToolArgsTool(), access_groups=['admin'])
    tools.register_local_tool(SearchSavedCorrectToolUsesTool(), access_groups=['admin', 'user'])

    llm = AnthropicLlmService(model="claude-opus-4-6")

    # Create agent with your options
    agent = Agent(
        llm_service=llm,
        tool_registry=tools,
        user_resolver=SimpleUserResolver(),
        config=AgentConfig(),
        agent_memory=agent_memory
    )

    # 4. Create and run server
    server = VannaFastAPIServer(agent)
    server.run()

if __name__ == "__main__":
    main()
