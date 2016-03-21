import logging

from txbitcoin.pool import BitcoinPool
from twisted.internet import reactor

logger = logging.getLogger('net')
banlist = set()

def load_banlist(filename):
    banlist = read_from_file(filename)
    sweap_outdate_banlist(banlist)
    
def start_node(args, threads):
    logger.info('Loading addresses...')
    load_peers('peers.dat')
    load_banlist('banlist.dat')
    discover_local_service()

    p = BitcoinPool()
    p.bootstrap()
    reactor.run()
