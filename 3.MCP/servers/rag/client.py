import asyncio
import os
from contextlib import AsyncExitStack

import nest_asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


nest_asyncio.apply()
load_dotenv("../.env")


class MCPGeminiClient:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.session = None
        self.exit_stack = AsyncExitStack()
        self.model_name = model_name

        self.gemini_client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY"),
            vertexai=False,
        )
        self.stdio = None
        self.write = None

    async def connect_to_server(self, server_script_path: str):
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
        )

        stido_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stido_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        tools_list = await self.session.list_tools()
        print("Available tools:")
        for tool in tools_list.tools:
            print(f"- {tool.name}: {tool.description}")

        print("Available prompts:")
        prompts_list = await self.session.list_prompts()
        print(prompts_list)
        for prompt in prompts_list.prompts:
            print(f"- {prompt.name}: {prompt.description}")



    async def get_mcp_tools(self):
        tool_results = await self.session.list_tools()
        gemini_tools = [
            types.Tool(
                function_declarations=[
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": {
                            k: v
                            for k, v in tool.inputSchema.items()
                            if k not in ["additionalProperties", "$schema"]
                        },
                    }
                ]
            )
            for tool in tool_results.tools
        ]

        return gemini_tools

    async def process_query(self, query: str):
        tools = await self.get_mcp_tools()
        config = types.GenerateContentConfig(
            tools=tools,
            temperature=0,
        )

        # show prompts to the LLM
        contents = [
            types.Content(
                role="user", 
                parts=[types.Part(text=query)]
            )
        ]

        response = self.gemini_client.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=config,
        )

        # Check for a function call
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            print(f"Function to call: {function_call.name}")
            print(f"Arguments: {function_call.args}")
            result = await self.session.call_tool(
                function_call.name, arguments=dict(function_call.args)
            )

            function_response_part = types.Part.from_function_response(
                name=function_call.name,
                response={"result": result},
            )
            # Append function call and result of the function execution to contents
            contents.append(response.candidates[0].content) # Append the content from the model's response.
            contents.append(types.Content(role="user", parts=[function_response_part])) # Append the function response

            final_response = self.gemini_client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config,
            )


            return final_response.candidates[0].content.parts[0].text




        else:
            print("No function call found in the response.")
            return response.candidates[0].content.parts[0].text

    # async def get_user_friendly_response(self, query_with_tool_output: str):
    #     response = self.gemini_client.models.generate_content(
    #         model=self.model_name, contents=f"{query_with_tool_output}"
    #     )

    #     return response.candidates[0].content.parts[0].text

    async def clean_up(self):
        await self.exit_stack.aclose()


async def main():
    # try:
    client = MCPGeminiClient()
    await client.connect_to_server("server.py")

    # query = "Can I work remote in this company?"
    # print(f"\n Query: {query}")

    # response = await client.process_query(query)
    # print(f"\nResponse: {response}")
    while True:
        user_input = input("\nEnter your query (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            break

        response = await client.process_query(user_input)
        print(f"\nResponse: {response}")

    await client.clean_up()


if __name__ == "__main__":
    asyncio.run(main())
