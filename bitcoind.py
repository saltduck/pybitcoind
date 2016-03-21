import sys
import argparse

from twisted.python import log
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, Protocol

from txbitcoin.pool import BitcoinPool
from txbitcoin.factory import BitcoinClientFactory
from txbitcoin.protocols import BitcoinProtocol
#from .net import start_node

log.startLogging(sys.stdout)


def parse_parameters():
    parser = argparse.ArgumentParser(description='bitcoin full node')
    parser.add_argument('--daemon', '-d', type=bool, default=False, help='Run as daemon')
    return parser.parse_args()


def init():
    init_logging()
    check_data_dir()
    read_config_file()
    select_chain()
    if args.daemon:
        log.info('Bitcoin server starting...')
        run_as_daemon()
    args.server = True
    try:
        check_parameters(args)
        init_ecc()
        init_sanity_check()
        init_lockfile()
        create_pidfile()
        log.info('Default data directory: {0}'.format(get_default_data_dir()))
        log.info('Using data directory: {0}'.format(args.data_dir))
        log.info('Using config file: {0}'.format(args.config_file))
        log.info('Using atmost {0} connections.'.format(args.max_connections))
        log.info('Using {0} threads for script validation.'.format(args.script_check_thread_number))
        for _ in range(args.script_check_thread_number):
            threads.append(ScriptCheckThread())
        threads.append(Scheduler())
        init_api_servers()
        init_network()
        load_blockchain()
        if args.prune_mode:
            prune_block_files()
        import_block_files()
        start_node(args, threads)
        start_api_servers()
    except Exception:
        interrupt()
        shutdown()
        return -1
    wait_for_shutdown()
    shutdown()
    return 0


if __name__ == '__main__':
    args = parse_parameters()
    pool = BitcoinPool()
    pool.bootstrap()
    #pool.listen()
    reactor.run()
