#!/bin/bash

# AI Agent Docker 部署脚本

echo "🚀 开始部署 LangChain AI Agent..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查docker-compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose 未安装，请先安装 docker-compose"
    exit 1
fi

# 检查.env文件是否存在
if [ ! -f .env ]; then
    echo "⚠️  .env 文件不存在，请创建.env文件并配置API密钥"
    echo "示例内容："
    echo "GOOGLE_API_KEY=your_google_api_key"
    echo "GEMINI_API_KEY=your_gemini_api_key"
    echo "TAVILY_API_KEY=your_tavily_api_key"
    exit 1
fi

# 构建并启动容器
echo "📦 构建 Docker 镜像..."
docker-compose build

echo "🚀 启动 AI Agent 容器..."
docker-compose up -d

echo "✅ AI Agent 已成功启动！"
echo ""
echo "📋 使用以下命令管理容器："
echo "  查看日志: docker-compose logs -f"
echo "  进入容器: docker-compose exec ai-agent bash"
echo "  停止服务: docker-compose down"
echo "  重启服务: docker-compose restart"
echo ""
echo "🔗 连接到AI Agent:"
echo "  docker-compose exec ai-agent python main.py"
