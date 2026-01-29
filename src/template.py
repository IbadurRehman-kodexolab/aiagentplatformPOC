# This is the template for multi-agent workflow.
multi_agent_template = {
    "workflow": {
        "id": "multi_agent_workflow",
        "name": "Multi Agent Workflow",
        "version": "1.0.0",
        "global_config": {
            "default_model": "gpt-4o",
            "checkpointer": {"enabled": False},
        },
        "dynamic_variables": ["customer_name"],
        "schemas": [],
        "nodes": [
            {
                "id": "start_node",
                "type": "start",
                "name": "start_node_name",
                "description": "Start node",
                "config": {},
            },
            {
                "id": "triage_node",
                "type": "triage_node",
                "name": "triage_node_name",
                "description": "Triage node",
                "config": {
                    "model": "gpt-4o",
                    # "system_prompt": "You are a triage agent and you are taking to  {customer_name}. Categorize customer queries as technical, billing, or general. Assess urgency and provide a brief summary.",
                    "system_prompt": "You are a triage agent. call the tools.",
                    "tools": ["tool1", "tool2"],
                    "subagents": ["technical_agent", "billing_agent", "general_agent"],
                },
            },
            {
                "id": "technical_agent",
                "type": "agent_node",
                "name": "technical_agent",
                "description": "Technical agent",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "You are a technical support specialist. Help customers solve technical issues.",
                    "tools": ["tool1", "tool2"],
                    "subagents": [],
                },
            },
            {
                "id": "billing_agent",
                "type": "agent_node",
                "name": "billing_agent",
                "description": "Billing agent",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "You are a billing support specialist. Help customers with billing inquiries and refunds.",
                    "tools": ["tool1", "tool2"],
                    "subagents": [],
                },
            },
            {
                "id": "general_agent",
                "type": "agent_node",
                "name": "general_agent",
                "description": "General agent",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "You are a general support agent. Answer general questions and provide helpful information.",
                    "tools": ["tool1", "tool2"],
                    "subagents": [],
                },
            },
            {
                "id": "end_node",
                "type": "end",
                "name": "end_node_name",
                "description": "End node",
                "config": {},
            },
        ],
        "edges": [
            {"from": "start_node", "to": "triage_node"},
            {"from": "triage_node", "to": "technical_agent"},
            {"from": "triage_node", "to": "billing_agent"},
            {"from": "triage_node", "to": "general_agent"},
            {"from": "technical_agent", "to": "end_node"},
            {"from": "billing_agent", "to": "end_node"},
            {"from": "general_agent", "to": "end_node"},
        ],
        "tools": [
            {
                "id": "rag_id",
                "name": "RAG",
                "description": "RAG is a tool that allows you to search the knowledge base for information.",
                "parameters": {
                    "type": "object",
                    "properties": {"max_results": {"type": "integer", "default": 5}},
                    "required": ["max_results"],
                },
            }
        ],
    }
}
