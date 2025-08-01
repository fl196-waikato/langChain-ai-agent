from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
import os
from dotenv import load_dotenv

load_dotenv()

# 定义 memory 用于持久记忆存储
memory = MemorySaver()

# 初始化LLM模型
model = init_chat_model("gemini-1.5-flash", model_provider="google-genai", temperature=0.7)


# 定义工具
search = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"), max_results=2)
tools = [search]

# 创建反应式代理，添加系统提示
agent = create_react_agent(
    model, 
    tools, 
    checkpointer=memory,
    state_modifier="""You are a helpful assistant with access to a web search tool called 'tavily_search'. 

IMPORTANT: When users ask about:
- Current weather information
- Recent news or events  
- Real-time data
- Any information that might change frequently

You MUST use the tavily_search tool to find up-to-date information. Do NOT say you cannot access real-time data - you CAN access it through the search tool.

Always search first before responding to questions about current information."""
)

# 交互式对话循环
print("开始LangChain代理对话...")
print("您可以询问任何问题，比如：")
print("- 'What's the weather like in Auckland?'")
print("- '帮我搜索一下奥克兰的天气'")
print("- 输入 'quit' 或 'exit' 退出")
print("-" * 50)

# 初始化对话
config = {"configurable": {"thread_id": "weather-chat"}}

while True:
    try:
        # 获取用户输入
        user_input = input("\n您: ").strip()
        
        if user_input.lower() in ['quit', 'exit', '退出', 'q']:
            print("再见！")
            break
            
        if not user_input:
            continue
            
        # 构建消息
        input_message = {"role": "user", "content": user_input}
        
        print("\n代理正在思考...")
        
        # 获取代理响应
        response_count = 0
        for step in agent.stream({"messages": [input_message]}, config, stream_mode="values"):
            response_count += 1
            if response_count <= 3:  # 显示前3个响应
                step["messages"][-1].pretty_print()
            else:
                print("响应完成！")
                break
                
    except KeyboardInterrupt:
        print("\n\n程序被用户中断，再见！")
        break
    except Exception as e:
        print(f"错误: {e}")
        print("请重试...")





