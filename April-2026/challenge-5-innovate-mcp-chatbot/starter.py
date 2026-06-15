"""
Challenge 5 (Innovate): Build Your Own MCP-Powered Agent

YOUR TASK:
  Build an innovative agent from scratch that connects to any MCP server.
  The most creative and useful agent gets a special shoutout! 🏆

RULES:
  - Must use Strands Agents SDK
  - Must use at least one MCP server
  - Must use Amazon Nova Pro (or any Bedrock model)
  - Must have an interactive chat loop
  - Must be YOUR OWN idea — be creative!

EXAMPLE MCP SERVERS:
  pip install awslabs.aws-documentation-mcp-server   # AWS Docs
  uvx awslabs.cdk-mcp-server@latest                  # AWS CDK
  uvx awslabs.cost-analysis-mcp-server@latest        # AWS Pricing

BROWSE MORE: https://github.com/modelcontextprotocol/servers

RESOURCES:
  - Strands MCP docs: https://strandsagents.com/latest/user-guide/concepts/tools/mcp-tools/
  - AWS MCP servers: https://github.com/awslabs/mcp

Build something that makes us go "whoa!" 🚀
"""

# Your code here — build the entire agent from scratch!

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

MODEL = "us.amazon.nova-pro-v1:0"

# AWS Documentation MCP Server
mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args=["awslabs.aws-documentation-mcp-server@latest"],
            env={"FASTMCP_LOG_LEVEL": "ERROR"},
        )
    )
)

with mcp_client:
    tools = mcp_client.list_tools_sync()

    agent = Agent(
        model=MODEL,
        tools=tools,
        system_prompt="""
You are an AWS Documentation Expert. 📚

You have access to the official AWS documentation through MCP tools.

When answering:
- Search AWS documentation when needed
- Cite the AWS service you are using
- Explain concepts clearly
- Give examples when helpful
- Be concise but accurate
"""
    )

    print("📚 AWS Docs Chatbot — MCP Powered")
    print("Ask anything about AWS.")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye! 👋")
            break

        if not user_input:
            continue

        try:
            response = agent(user_input)
            print(f"\nAgent: {response}\n")

        except Exception as e:
            print(f"\nError: {e}\n")

print("\n✅ Challenge 5 complete!")
