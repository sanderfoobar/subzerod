from typing import List
import itertools

from subzerod.utils import validate_domain
from subzerod.sites import DuckDuckEnum, CrtEnum, BaiduEnum, AskEnum, ThreatCrowd, PassiveDNS, DomainLookup


class SubZerod:
    @staticmethod
    async def find_subdomains(domain: str) -> List[str]:
        if not validate_domain(domain):
            raise Exception("Error: Please enter a valid domain\n")

        import asyncio

        tasks = []
        for engine in [
            DuckDuckEnum,
            CrtEnum,
            BaiduEnum,
            AskEnum,
            ThreatCrowd,
            PassiveDNS,
        ]:
            tasks.append(engine(domain).enumerate())

        results: List[str] = await asyncio.gather(*tasks)
        if not results:
            return []

        results = list(sorted(set(itertools.chain(*results))))
        return results

    @staticmethod
    async def find_domains(ipv4: str):
        """Discover domains on a shared IP"""
        import asyncio

        tasks = []
        for engine in [DomainLookup]:
            tasks.append(engine(ipv4).enumerate())

        results: List[str] = await asyncio.gather(*tasks)
        if not results:
            return []

        results = list(sorted(set(itertools.chain(*results))))
        return results
