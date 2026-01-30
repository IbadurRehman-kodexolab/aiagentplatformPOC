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
                "name": "start_node",
                "description": "Start node",
                "config": {},
            },
            {
                "id": "triage_node",
                "type": "agent_node",
                "name": "triage_node",
                "description": "Triage node that routes to specialist agents",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "You are a triage agent. Analyze the customer's request and route them to the appropriate specialist: technical_agent for technical issues, billing_agent for billing questions, or general_agent for general inquiries. Use the appropriate handoff tool to transfer the customer.",
                    "tools": [],
                    "subagents": ["technical_agent", "billing_agent", "general_agent"],
                },
            },
            {
                "id": "technical_agent",
                "type": "agent_node",
                "name": "technical_agent",
                "description": "Technical support specialist for solving technical issues",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "You are a technical support specialist. Help customers solve technical issues.",
                    "tools": [],
                    "subagents": [],
                },
            },
            {
                "id": "billing_agent",
                "type": "agent_node",
                "name": "billing_agent",
                "description": "Billing support specialist for billing inquiries and refunds",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "You are a billing support specialist. Help customers with billing inquiries and refunds.",
                    "tools": [],
                    "subagents": [],
                },
            },
            {
                "id": "general_agent",
                "type": "agent_node",
                "name": "general_agent",
                "description": "General support agent for general questions",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "You are a general support agent. Answer general questions and provide helpful information.",
                    "tools": [],
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
            {"from": "triage_node", "to": "end_node"},
            {"from": "technical_agent", "to": "end_node"},
            {"from": "billing_agent", "to": "end_node"},
            {"from": "general_agent", "to": "end_node"},
        ],
        "tools": [],
    }
}


simple_agent_template = {
    "workflow": {
        "id": "simple_agent_workflow",
        "name": "Simple Agent Workflow",
        "version": "1.0.0",
        "global_config": {
            "default_model": "gpt-4o",
            "checkpointer": {"enabled": False},
        },
        "dynamic_variables": [],
        "schemas": [],
        "tools": [],
        "nodes": [
            {
                "id": "start_node",
                "type": "start",
                "name": "start_node",
                "description": "Start node",
                "config": {},
            },
            {
                "id": "agent_node",
                "type": "agent_node",
                "name": "agent_node",
                "description": "Agent node",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "You are a simple agent. Answer questions and provide helpful information.",
                    "tools": [],
                    "subagents": [],
                },
            },
            {
                "id": "end_node",
                "type": "end",
                "name": "end_node",
                "description": "End node",
                "config": {},
            },
        ],
        "edges": [
            {"from": "start_node", "to": "agent_node"},
            {"from": "agent_node", "to": "end_node"},
        ],
    }
}


supervisor_agent_template = {
    "workflow": {
        "id": "supervisor_agent_workflow",
        "name": "Supervisor Agent Workflow",
        "version": "1.0.0",
        "global_config": {
            "default_model": "gpt-4o",
            "checkpointer": {"enabled": False},
        },
        "dynamic_variables": [],
        "schemas": [],
        "tools": [],
        "nodes": [
            {
                "id": "start_node",
                "type": "start",
                "name": "start_node",
                "description": "Start node",
                "config": {},
            },
            {
                "id": "supervisor_node",
                "type": "agent_node",
                "name": "supervisor_node",
                "description": "Supervisor node",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "You are a supervisor agent. You are responsible for overseeing the work of the swarm agents.",
                    "tools": [],
                    "subagents": ["billing_agent", "technical_agent", "general_agent"],
                },
            },
            {
                "id": "billing_agent",
                "type": "agent_node",
                "name": "billing_agent",
                "description": "Billing agent",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "You are a billing agent. You are responsible for billing inquiries and refunds.",
                    "tools": [],
                    "subagents": [],
                },
            },
            {
                "id": "technical_agent",
                "type": "agent_node",
                "name": "technical_agent",
                "description": "Technical agent",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "You are a technical agent. You are responsible for technical inquiries and support.",
                    "tools": [],
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
                    "system_prompt": "You are a general agent. You are responsible for general inquiries and support.",
                    "tools": [],
                    "subagents": [],
                },
            },
            {
                "id": "end_node",
                "type": "end",
                "name": "end_node",
                "description": "End node",
                "config": {},
            },
        ],
        "edges": [
            {"from": "start_node", "to": "supervisor_node"},
            {"from": "supervisor_node", "to": "end_node"},
        ],
    }
}


swarm_agent_template = {
    "workflow": {
        "id": "swarm_agent_workflow",
        "name": "Swarm Agent Workflow",
        "version": "1.0.0",
        "global_config": {
            "default_model": "gpt-4o",
            "checkpointer": {"enabled": False},
        },
        "dynamic_variables": [],
        "schemas": [],
        "tools": [],
        "nodes": [
            {
                "id": "start_node",
                "type": "start",
                "name": "start_node",
                "description": "Start node",
                "config": {},
            },
            {
                "id": "billing_agent",
                "type": "agent_node",
                "name": "billing_agent",
                "description": "Billing agent",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "You are a billing agent. You are responsible for billing inquiries and refunds.",
                    "tools": [],
                    "subagents": ["technical_agent", "general_agent"],
                },
            },
            {
                "id": "technical_agent",
                "type": "agent_node",
                "name": "technical_agent",
                "description": "Technical agent",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "You are a technical agent. You are responsible for technical inquiries and support.",
                    "tools": [],
                    "subagents": ["billing_agent", "general_agent"],
                },
            },
            {
                "id": "general_agent",
                "type": "agent_node",
                "name": "general_agent",
                "description": "General agent",
                "config": {
                    "model": "gpt-4o",
                    "system_prompt": "You are a general agent. You are responsible for general inquiries and support.",
                    "tools": [],
                    "subagents": ["billing_agent", "technical_agent"],
                },
            },
            {
                "id": "end_node",
                "type": "end",
                "name": "end_node",
                "description": "End node",
                "config": {},
            },
        ],
        "edges": [
            {"from": "start_node", "to": "billing_agent"},
            {"from": "billing_agent", "to": "end_node"},
            {"from": "technical_agent", "to": "end_node"},
            {"from": "general_agent", "to": "end_node"},
        ],
    }
}
