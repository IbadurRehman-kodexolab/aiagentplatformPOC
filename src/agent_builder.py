import os
import time

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, MessagesState, StateGraph

from tool_builder import tools

load_dotenv()


def get_tools(node):
    """Get tools for a node"""
    selected_tools = [tool for tool in tools if tool.name in node["config"]["tools"]]
    return selected_tools


def _has_end_edge(node_id, edges):
    """True if this node has an outgoing edge to end_node."""
    return any(e["from"] == node_id and e["to"] == "end_node" for e in edges)


def build_agents_from_template(template):
    """Build agents from template - wrapping sub-agents as tools"""
    workflow_nodes = template["workflow"]["nodes"]
    workflow_edges = template["workflow"]["edges"]
    default_model = template["workflow"]["global_config"]["default_model"]

    agent_nodes = [
        node
        for node in workflow_nodes
        if node["type"] == "agent_node"
    ]

    created_agents = {}
    created_agent_tools = {}

    # Step 1: Create all leaf agents (those without subagents)
    leaf_agents = {}
    for node in agent_nodes:
        if not node["config"].get("subagents", []):
            config = node["config"]
            node_tools = get_tools(node)

            agent = create_agent(
                model=config.get("model", default_model),
                tools=node_tools,
                system_prompt=config.get("system_prompt", ""),
            )

            leaf_agents[node["name"]] = agent
            created_agents[node["id"]] = agent

    # Step 2: Wrap leaf agents as tools
    for node in agent_nodes:
        if not node["config"].get("subagents", []):
            agent_name = node["name"]
            agent_description = node["description"]
            agent = leaf_agents[agent_name]
            return_direct = _has_end_edge(node["id"], workflow_edges)

            # Create a tool that wraps this agent
            def create_agent_tool(agent_instance, name, desc, return_direct):
                @tool(name, description=desc, return_direct=return_direct)
                def agent_tool(request: str) -> str:
                    result = agent_instance.invoke(
                        {"messages": [{"role": "user", "content": request}]}
                    )
                    return result["messages"][-1].content

                agent_tool.name = name
                return agent_tool

            wrapped_tool = create_agent_tool(
                agent, agent_name, agent_description, return_direct
            )
            created_agent_tools[agent_name] = wrapped_tool

    # Step 3: Create parent agents with wrapped sub-agent tools
    for node in agent_nodes:
        config = node["config"]

        if config.get("subagents"):
            node_tools = get_tools(node)

            # Add wrapped sub-agent tools
            for subagent_name in config["subagents"]:
                if subagent_name in created_agent_tools:
                    node_tools.append(created_agent_tools[subagent_name])

            # Create parent agent with all tools (including wrapped sub-agents)
            agent = create_agent(
                model=config.get("model", default_model),
                tools=node_tools,
                system_prompt=config.get("system_prompt", ""),
            )

            created_agents[node["id"]] = agent

    return created_agents


def build_workflow_graph(created_agents, template):
    """Build the workflow graph dynamically from template"""
    workflow_graph = StateGraph(MessagesState)

    # Create mapping of node IDs to agent names
    node_id_to_agent_name = {}
    for node in template["workflow"]["nodes"]:
        if node["type"] == "agent_node":
            node_id_to_agent_name[node["id"]] = node["name"]

    # Determine which agent nodes are referenced in edges
    agent_nodes_in_edges = set()
    for edge in template["workflow"]["edges"]:
        source_node_id = edge["from"]
        target_node_id = edge["to"]

        for node in template["workflow"]["nodes"]:
            if node["id"] == source_node_id and node["type"] == "agent_node":
                agent_nodes_in_edges.add(node["name"])
            if node["id"] == target_node_id and node["type"] == "agent_node":
                agent_nodes_in_edges.add(node["name"])

    # Add agent nodes to workflow graph
    for agent_id, agent in created_agents.items():
        if agent_id in node_id_to_agent_name:
            agent_name = node_id_to_agent_name[agent_id]
            if agent_name in agent_nodes_in_edges:
                workflow_graph.add_node(agent_name, agent)

    # Add edges to workflow graph
    for edge in template["workflow"]["edges"]:
        source_node_id = edge["from"]
        target_node_id = edge["to"]

        # Handle START node
        if source_node_id == "start_node":
            if target_node_id in node_id_to_agent_name and target_node_id in created_agents:
                target_agent_name = node_id_to_agent_name[target_node_id]
                if target_agent_name in agent_nodes_in_edges:
                    workflow_graph.add_edge(START, target_agent_name)

        # Handle END node
        elif target_node_id == "end_node":
            if source_node_id in node_id_to_agent_name and source_node_id in created_agents:
                source_agent_name = node_id_to_agent_name[source_node_id]
                if source_agent_name in agent_nodes_in_edges:
                    workflow_graph.add_edge(source_agent_name, END)

        # Handle agent-to-agent edges
        elif source_node_id in node_id_to_agent_name and target_node_id in node_id_to_agent_name:
            if source_node_id in created_agents and target_node_id in created_agents:
                source_agent_name = node_id_to_agent_name[source_node_id]
                target_agent_name = node_id_to_agent_name[target_node_id]
                if source_agent_name in agent_nodes_in_edges and target_agent_name in agent_nodes_in_edges:
                    workflow_graph.add_edge(source_agent_name, target_agent_name)

    compiled_workflow = workflow_graph.compile(name=template["workflow"]["name"])

    # Create graphs directory if it doesn't exist
    graphs_dir = "graphs"
    if not os.path.exists(graphs_dir):
        os.makedirs(graphs_dir)

    # Draw workflow visualization
    try:
        workflow_name = template['workflow']['name']
        output_path = f"{graphs_dir}/{workflow_name}.png"
        compiled_workflow.get_graph().draw_mermaid_png(output_file_path=output_path)
    except Exception as e:
        print(f"Could not draw workflow graph: {e}")

    return compiled_workflow


def build_agent_workflow(template):
    """Build and compile the agent workflow graph from template"""
    created_agents = build_agents_from_template(template)
    workflow_graph = build_workflow_graph(created_agents, template)
    return workflow_graph


def build_and_run_workflow(template):
    """Build agent workflow and run with test message"""
    workflow_graph = build_agent_workflow(template)
    response = workflow_graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="I need to know my billing details my account number is 1234567890"
                )
            ]
        }
    )

    for msg in response["messages"]:
        msg.pretty_print()
    return response


if __name__ == "__main__":
    from template import (
        multi_agent_template,
        simple_agent_template,
        supervisor_agent_template,
        swarm_agent_template,
    )

    templates = [
        simple_agent_template,
        multi_agent_template,
        supervisor_agent_template,
        swarm_agent_template,
    ]

    for template in templates:
        print("=" * 50)
        start_time = time.time()
        response = build_and_run_workflow(template)
        end_time = time.time()
        print(f"Workflow: {template['workflow']['name']}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print("=" * 50)
