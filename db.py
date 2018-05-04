from sqlalchemy import create_engine


def query_aos(passwd, table='gse_packet_rt', schema='samsnew', host='yoda', user='samsops'):
    """return ku_timestamp, ku_aos_los from samsnew.gse_packet_rt table on yoda"""
    constr = 'mysql://%s:%s@%s/%s' % (user, passwd, host, schema)
    query = 'select ku_timestamp, ku_aos_los_status from %s;' % table
    engine = create_engine(constr, echo=False)
    try:
        con = engine.connect()
        cursor = con.execute(query)
        results = cursor.first()
        cursor.close()
        con.close()
    except:
        #print 'ERROR IN YODA DB CONNECTION'
        results = None

    # check if we have any results (should always just be one)
    if results:
        ku_timestamp, ku_aos_los = results
    else:
        ku_timestamp, ku_aos_los = None, None

    return ku_timestamp, ku_aos_los


# attempt to connect to yoda and get most recent timestamp from cu_packet_rt table
def query_cu_not_used_yet(passwd):
    # FIXME need to do this via an rt table (not yet setup on trek21a) TOO SLOW WITH NON_rt TABLE
    
    # attempt to get results
    try:
        con = Connection(host='yoda', user='samsops', passwd=passwd, db='samsnew')
        result = con.result()
        result.execute('select timestamp from cu_packet order by timestamp desc limit 1;')
        results = result.fetchall();
        result.close()
        con.close()
    except:
        #print 'ERROR IN YODA DB CONNECTION'
        results = None
        
    # check if we have any results (should always just be one)
    if results:
        timestamp = results[0]
    else:
        timestamp = None

    return timestamp
