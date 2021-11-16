from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Union

import httpx
from pydantic import AnyUrl, IPvAnyAddress
from src.domain.geolocation import Geolocation
from src.helpers.exceptions import HttpClientError


@dataclass
class HttpClient:
    _api_key: str
    base_url: str = "http://api.ipstack.com"

    def __post_init__(self):
        self._client = httpx.AsyncClient(
            params={"access_key": self._api_key}, base_url=self.base_url
        )

    async def get_geolocation_for_address(self, address: str) -> Geolocation:
        stripped_address, is_url = self._strip_address(address)
        res = await self._get(f"/{stripped_address}")
        if "error" in res:
            raise HttpClientError(ipstack_message=res["error"]["info"])

        if is_url:
            res = {**res, "url": address}

        return Geolocation(**res)

    async def _get(self, endpoint: str, params: Optional[Dict[str, str]] = None):
        async with self._client as client:
            resp = await client.get(endpoint, params=params)
            return resp.json()

    def _strip_address(self, address: Union[IPvAnyAddress, AnyUrl]) -> Tuple[str, bool]:
        """
        Due to the construction of IPStack's endpoint, full URLs (with scheme - e.g. http://)
        need to have the scheme removed.
        Returns:
            - IP address or URL with no scheme
            - is_url (bool): info if the address is a URL or an IP
        """
        if isinstance(address, AnyUrl):
            return address.replace(f"{address.scheme}://", "").replace("www.", ""), True

        return address.compressed, False
