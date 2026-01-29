from template import multi_agent_template
from langchain.agents import create_agent
from tool_builder import tools
from langchain.messages import AIMessage, ToolMessage
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain.agents import AgentState
from langchain.messages import HumanMessage


load_dotenv()

handoff_tools = []


def build_agent(template):
    return NodeBuilder(template)


def get_tools(node, handoff_tools_usage=False):
    # only return the tools that are in the node config
    print(f"Node: {node}")
    # print(f"Handoff tools: {handoff_tools_usage}")
    selected_tools = [tool for tool in tools if tool.name in node["config"]["tools"]]
    print(f"Selected tools: {selected_tools}")
    if handoff_tools_usage:
        list_of_handoff_tools_names = [
            handoff_tool.name for handoff_tool in handoff_tools
        ]
        for subagent in node["config"]["subagents"]:
            print(f"Subagent: {subagent}")
            if subagent in list_of_handoff_tools_names:
                selected_tools.append(
                    handoff_tools[list_of_handoff_tools_names.index(subagent)]
                )
                print(
                    f"Added handoff tool: {handoff_tools[list_of_handoff_tools_names.index(subagent)].name}"
                )
            else:
                print(f"Subagent {subagent} not found in handoff tools")

    return selected_tools


def create_handoff_tool(agent_name, agent_description, return_direct=False):

    @tool(description=agent_description, return_direct=return_direct)
    def handoff_tool(runtime: ToolRuntime) -> Command:
        last_ai_message = next(
            msg
            for msg in reversed(runtime.state["messages"])
            if isinstance(msg, AIMessage)
        )
        transfer_message = ToolMessage(
            content=f"Transferring to {agent_name}",
            tool_call_id=runtime.tool_call_id,
        )
        return Command(
            goto=agent_name,
            update={
                "active_agent": agent_name,
                "messages": [last_ai_message, transfer_message],
            },
            graph=Command.PARENT,
        )

    handoff_tool.name = agent_name

    print(f"Created handoff tool: {handoff_tool.name}")
    return handoff_tool


def NodeBuilder(template):
    """Build agents from template - first create agents without subagents, then agents with subagents"""
    workflow_nodes = template["workflow"]["nodes"]
    default_model = template["workflow"]["global_config"]["default_model"]

    created_agents = {}

    # Separate nodes into agent nodes and other nodes
    agent_nodes = [
        node for node in workflow_nodes if node["type"] in ["agent_node", "triage_node"]
    ]

    # First pass: Create agents without subagents
    agents_without_subagents = [
        node for node in agent_nodes if not node["config"].get("subagents", [])
    ]

    for node in agents_without_subagents:
        config = node["config"]
        node_tools = get_tools(node=node, handoff_tools_usage=False)

        agent = create_agent(
            model=config.get("model", default_model),
            tools=node_tools,
            system_prompt=config.get("system_prompt", ""),
            name=node["name"],
        )

        created_agents[node["id"]] = agent

        handoff_tool = create_handoff_tool(node["name"], node["description"])

        handoff_tools.append(handoff_tool)

    # Second pass: Create agents with subagents
    agents_with_subagents = [
        node for node in agent_nodes if node["config"].get("subagents", [])
    ]

    for node in agents_with_subagents:
        config = node["config"]
        node_tools = get_tools(node=node, handoff_tools_usage=True)

        agent = create_agent(
            model=config.get("model", default_model),
            tools=node_tools,
            system_prompt=config.get("system_prompt", ""),
            name=node["name"],
        )
        # print(f"Created agent: {agent.name}")
        created_agents[node["id"]] = agent

    return created_agents


# def GraphBuilder(created_agents, template):
#     """Build the graph from the created agents according to template edges"""
#     graph = StateGraph(AgentState)

#     # Create a mapping of node IDs to agent names
#     id_to_name = {}
#     for node in template["workflow"]["nodes"]:
#         if node["type"] in ["agent_node", "triage_node"]:
#             id_to_name[node["id"]] = node["name"]

#     # Add all agent nodes to the graph
#     for agent_id, agent in created_agents.items():
#         graph.add_node(agent.name, agent)

#     # Add edges based on template
#     for edge in template["workflow"]["edges"]:
#         from_node = edge["from"]
#         to_node = edge["to"]

#         # Handle START node
#         if from_node == "start_node":
#             if to_node in id_to_name:
#                 graph.add_edge(START, id_to_name[to_node])
#         # Handle END node
#         elif to_node == "end_node":
#             if from_node in id_to_name:
#                 graph.add_edge(id_to_name[from_node], END)
#         # Handle agent-to-agent edges
#         elif from_node in id_to_name and to_node in id_to_name:
#             graph.add_edge(id_to_name[from_node], id_to_name[to_node])

#     graph = graph.compile()

#     # Draw graph without xray to show agent names clearly
#     graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

#     return graph


def SimpleGraphBuilder(created_agents, template):
    """Build a simple graph from the created agents"""
    graph = StateGraph(AgentState)

    # Create a mapping of node IDs to agent names
    id_to_name = {}
    for node in template["workflow"]["nodes"]:
        if node["type"] in ["agent_node", "triage_node"]:
            id_to_name[node["id"]] = node["name"]

    # Add all agent nodes to the graph
    # for agent_id, agent in created_agents.items():
    #     graph.add_node(agent.name, agent)

    print(f"Id to name: {id_to_name}")

    # Add edges based on template
    for edge in template["workflow"]["edges"]:
        from_node = edge["from"]
        to_node = edge["to"]

        # Handle START node
        if from_node == "start_node":
            if to_node in id_to_name:
                graph.add_node(id_to_name[to_node], created_agents[to_node])
                graph.add_edge(START, id_to_name[to_node])
                graph.add_edge(id_to_name[to_node], END)
    graph = graph.compile()
    graph.get_graph(xray=True).draw_mermaid_png(output_file_path="graph.png")

    return graph


if __name__ == "__main__":
    created_agents = build_agent(multi_agent_template)
    # for agent_id, agent in created_agents.items():
    #     print(f"Agent {agent.name}: {agent}")
    # print(f"Created {len(created_agents)} agents")

    graph = SimpleGraphBuilder(created_agents, multi_agent_template)

    response = graph.invoke(
        {"messages": [HumanMessage(content="I need help with my account")]}
    )
    print(response)
