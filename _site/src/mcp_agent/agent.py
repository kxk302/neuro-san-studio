# Allows you to interact with the underlying OS using Python
import os
# Core class in Google ADK to create LLM-powered agents
from google.adk.agents import LlmAgent

# Primary ADK integration class for MCP
from google.adk.tools.mcp_tool import McpToolset

# Imports the connection configuration wrapper specific to the ADK
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
# Imports the core configuration class from Anthropic's official mcp Python library
from mcp import StdioServerParameters

TARGET_FOLDER = os.path.abspath("/Users/LarryBird")

root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="filesystem_assistant",
    instruction="Help users manage local files.",
    tools=[
        McpToolset(
            # StdioConnectionParams: wrapper for Google ADK. It takes the low-level StdioServerParameters
            # and tells the ADK how to manage the connection session
            # StdioServerParameters: defines how to launch the server process at the operating system level
            connection_params=StdioConnectionParams(
                # npx stands for "Node Package Executive." It is a tool that comes bundled with Node.js
                # It allows you to download and run Node.js packages directly from the npm registry
                # without needing to manually install them globally on your machine
                # 1st arg: Automatically answers "yes" if npx prompts you to confirm downloading a package
                # 2nd arg: Name of the official Model Context Protocol server package hosted on npm
                # It is a pre-built server created by Anthropic that implements standard file-system
                # operations (like reading, writing, and listing directories) safely over the MCP protocol
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-filesystem", TARGET_FOLDER],
                ),
            ),
            # Optional: Select specific tools exposed to the agent
            # Acts as a security or behavioral constraint. Even though the MCP
            # filesystem server might expose tools to write, delete, or move files,
            # this filter restricts the agent to only list_directory and read_file.
            # The agent can view files and folders, but it cannot edit or delete them
            tool_filter=["list_directory", "read_file"],
        )
    ],
)
