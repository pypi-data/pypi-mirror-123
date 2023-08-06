"""Django Session Backend.

Navigator Authentication using Django Session Backend
description: read the Django session from Redis Backend and decrypt.
"""
import base64
import rapidjson
import logging
import asyncio
import jwt
from aiohttp import web, hdrs
from asyncdb import AsyncPool
from .base import BaseAuthBackend
from navigator.exceptions import NavException, UserDoesntExists, InvalidAuth
from datetime import datetime, timedelta
from navigator.conf import (
    SESSION_URL,
    SESSION_TIMEOUT,
    SECRET_KEY,
    PARTNER_KEY,
    JWT_ALGORITHM,
    SESSION_PREFIX,
    default_dsn,
)


class TokenAuth(BaseAuthBackend):
    """API Token Authentication Handler."""

    _pool = None
    _scheme: str = "Bearer"

    def configure(self, app, router):
        async def _make_connection():
            try:
                kwargs = {
                    "min_size": 1,
                    "server_settings": {
                        "application_name": 'AUTH-NAV',
                        "client_min_messages": "notice",
                        "max_parallel_workers": "48",
                        "jit": "off",
                        "statement_timeout": "3600",
                        "effective_cache_size": "2147483647"
                    },
                }
                self._pool = AsyncPool(
                    "pg",
                    dsn=default_dsn,
                    **kwargs
                )
                await self._pool.connect()
            except Exception as err:
                print(err)
                raise Exception(err)

        asyncio.get_event_loop().run_until_complete(_make_connection())
        # executing parent configurations
        super(TokenAuth, self).configure(app, router)

    async def get_payload(self, request):
        token = None
        tenant = None
        id = None
        try:
            if "Authorization" in request.headers:
                try:
                    scheme, id = (
                        request.headers.get("Authorization").strip().split(" ", 1)
                    )
                except ValueError:
                    raise NavException(
                        "Invalid authorization Header",
                        state=400
                    )
                if scheme != self._scheme:
                    raise NavException(
                        "Invalid Authorization Scheme",
                        state=400
                    )
                try:
                    tenant, token = id.split(":")
                except ValueError:
                    raise NavException(
                        "Invalid Token Structure",
                        state=400
                    )
        except Exception as e:
            print(e)
            return None
        return [tenant, token]

    async def reconnect(self):
        if not self.connection or not self.connection.is_connected():
            await self.connection.connection()

    async def authenticate(self, request):
        """ Authenticate, refresh or return the user credentials."""
        try:
            tenant, token = await self.get_payload(request)
            logging.debug(f"Tenant ID: {tenant}")
        except Exception as err:
            raise NavException(err, state=400)
        if not token:
            raise InvalidAuth("Invalid Credentials", state=401)
        else:
            payload = jwt.decode(
                token, PARTNER_KEY, algorithms=[JWT_ALGORITHM], leeway=30
            )
            logging.debug(f"Decoded Token: {payload!s}")
            data = await self.check_token_info(request, tenant, payload)
            if not data:
                raise InvalidAuth(f"Invalid Session: {token!s}", state=401)
            # getting user information
            # making validation
            try:
                u = data["name"]
                username = data["partner"]
                grants = data["grants"]
                programs = data["programs"]
            except KeyError as err:
                print(err)
                raise InvalidAuth(
                    f"Missing attributes for Partner Token: {err!s}", state=401
                )
            # TODO: Validate that partner (tenants table):
            try:
                userdata = dict(data)
                user = {
                    "name": data["name"],
                    "partner": username,
                    "issuer": "Mobileinsight",
                    "programs": programs,
                    "grants": grants,
                    "tenant": tenant,
                    "id": data["name"],
                    "user_id": data["name"],
                }
                token = self.create_jwt(data=user)
                return {
                    "token": f"{tenant}:{token}",
                    **user
                }
            except Exception as err:
                print(err)
                return False

    async def check_credentials(self, request):
        pass

    async def check_token_info(self, request, tenant, payload):
        try:
            name = payload["name"]
            partner = payload["partner"]
        except KeyError as err:
            return False
        sql = f"""
        SELECT name, partner, grants, programs FROM troc.api_keys
        WHERE name='{name}' AND partner='{partner}'
        AND enabled = TRUE AND revoked = FALSE AND '{tenant}'= ANY(programs)
        """
        try:
            result = None
            async with await self._pool.acquire() as conn:
                result, error = await conn.queryrow(sql)
            if error or not result:
                return False
            else:
                return result
        except Exception as err:
            logging.exception(err)
            return False

    async def auth_middleware(self, app, handler):
        async def middleware(request):
            request.user = None
            authz = await self.authorization_backends(app, handler, request)
            if authz:
                return await authz
            tenant, token = await self.get_payload(request)
            if token:
                try:
                    payload = jwt.decode(
                        token, PARTNER_KEY, algorithms=[JWT_ALGORITHM], leeway=30
                    )
                    logging.debug(f"Decoded Token: {payload!s}")
                    result = await self.check_token_info(request, tenant, payload)
                    if not result:
                        raise web.HTTPForbidden(
                            reason="Not Authorized",
                        )
                    else:
                        session = await self._session.get_session(request)
                        session["grants"] = result["grants"]
                        session["partner"] = result["partner"]
                        session["tenant"] = tenant
                except (jwt.DecodeError) as err:
                    raise web.HTTPBadRequest(reason=f"Token Decoding Error: {err!r}")
                except jwt.InvalidTokenError as err:
                    print(err)
                    raise web.HTTPBadRequest(
                        reason=f"Invalid authorization token {err!s}"
                    )
                except (jwt.ExpiredSignatureError) as err:
                    print(err)
                    raise web.HTTPBadRequest(reason=f"Token Expired: {err!s}")
                except Exception as err:
                    print(err, err.__class__.__name__)
                    raise web.HTTPBadRequest(
                        reason=f"Bad Authorization Request: {err!s}"
                    )
            else:
                if self.credentials_required is True:
                    print("Missing Token information")
                    raise web.HTTPUnauthorized(
                        reason="Not Authorized",
                    )
            return await handler(request)

        return middleware
