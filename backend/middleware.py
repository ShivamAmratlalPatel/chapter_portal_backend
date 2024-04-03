"""Middleware for the backend application."""
from starlette.responses import Response
from starlette.status import HTTP_413_REQUEST_ENTITY_TOO_LARGE


class ContentSizeLimitMiddleware:
    """
    Content size limiting middleware for ASGI applications

    Args:
      app (ASGI application): ASGI application
      max_content_size (optional): the maximum content size allowed in bytes, None for
                                    no limit
    """

    def __init__(
        self,
        app,
        max_content_size: int | None = None,
    ) -> None:
        """Construct"""
        self.app = app
        self.max_content_size = max_content_size

    def receive_wrapper(self, receive):
        """Receive wrapper"""
        received = 0

        async def inner():
            nonlocal received
            message = await receive()
            if (
                message["type"] != "http.request" or self.max_content_size is None
            ):  # pragma: no cover
                return message
            body_len = len(message.get("body", b""))
            received += body_len
            if received > self.max_content_size:  # pragma: no cover
                return Response(status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE)
            return message

        return inner

    async def __call__(
        self: "ContentSizeLimitMiddleware",
        scope,
        receive,
        send,
    ) -> None:
        """
        Middleware call

        Args:
            scope: ASGI scope
            receive: ASGI receive
            send: ASGI send

        Returns:
            None
        """
        if scope["type"] != "http":  # pragma: no cover
            await self.app(scope, receive, send)
            return

        wrapper = self.receive_wrapper(receive)
        await self.app(scope, wrapper, send)
