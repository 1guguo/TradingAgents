from typing import Optional

from .base_client import BaseLLMClient
from .openai_client import OpenAIClient
from .anthropic_client import AnthropicClient
from .google_client import GoogleClient


def create_llm_client(
    provider: str,
    model: str,
    base_url: Optional[str] = None,
    **kwargs,
) -> BaseLLMClient:
    """
    为指定的服务商创建一个大语言模型（LLM）客户端。

    参数:
        provider: 大模型服务商（openai、anthropic、google、xai、ollama、openrouter、aliyun）
        model: 模型名称/标识符
        base_url: 可选，API 接口的基础 URL
        **kwargs: 其他服务商专属参数
            - http_client: 自定义 httpx.Client，用于 SSL 代理或证书配置
            - http_async_client: 自定义 httpx.AsyncClient，用于异步操作
            - timeout: 请求超时时间，单位为秒
            - max_retries: 最大重试次数
            - api_key: 对应服务商的 API 密钥
            - callbacks: LangChain 回调函数

    返回:
        已配置完成的 BaseLLMClient 实例

    抛出异常:
        ValueError: 当服务商不被支持时抛出
    """
    """Create an LLM client for the specified provider.

    Args:
        provider: LLM provider (openai, anthropic, google, xai, ollama, openrouter, aliyun)
        model: Model name/identifier
        base_url: Optional base URL for API endpoint
        **kwargs: Additional provider-specific arguments
            - http_client: Custom httpx.Client for SSL proxy or certificate customization
            - http_async_client: Custom httpx.AsyncClient for async operations
            - timeout: Request timeout in seconds
            - max_retries: Maximum retry attempts
            - api_key: API key for the provider
            - callbacks: LangChain callbacks

    Returns:
        Configured BaseLLMClient instance

    Raises:
        ValueError: If provider is not supported
    """
    provider_lower = provider.lower()

    if provider_lower in ("openai", "ollama", "openrouter", "aliyun"):
        return OpenAIClient(model, base_url, provider=provider_lower, **kwargs)

    if provider_lower == "xai":
        return OpenAIClient(model, base_url, provider="xai", **kwargs)

    if provider_lower == "anthropic":
        return AnthropicClient(model, base_url, **kwargs)

    if provider_lower == "google":
        return GoogleClient(model, base_url, **kwargs)

    raise ValueError(f"Unsupported LLM provider: {provider}")
