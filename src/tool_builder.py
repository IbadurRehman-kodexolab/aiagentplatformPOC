from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the weather of a city"""
    return f"The weather of {city} is sunny"


@tool
def get_news(topic: str) -> str:
    """Get the news of a topic"""
    return f"The news of {topic} is about the weather"


@tool
def get_stock_price(stock: str) -> str:
    """Get the stock price of a stock"""
    return f"The stock price of {stock} is 100"


tools = [get_weather, get_news, get_stock_price]
