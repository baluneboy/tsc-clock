from MySQLdb import *

# FIXME this is where we would want to timeout (with a thread)


# attempt to connect to yoda and get most recent Ku timestamp from gse_packet_rt table
def query_aos(passwd):
    # attempt to get results
    try:
        con = Connection(host='yoda', user='samsops', passwd=passwd, db='samsnew')
        cursor = con.cursor()
        cursor.execute('select ku_timestamp, ku_aos_los_status from gse_packet_rt;')
        results = cursor.fetchall();
        cursor.close()
        con.close()
    except:
        #print 'ERROR IN YODA DB CONNECTION'
        results = None
        
    # check if we have any results (should always just be one)
    if results:
        ku_timestamp, ku_aos_los = results[0]
    else:
        ku_timestamp, ku_aos_los = None, None

    return ku_timestamp, ku_aos_los


# attempt to connect to yoda and get most recent Ku timestamp from gse_packet_rt table
def query_aos_via_out_queue(passwd, out_q):
    # attempt to get results
    try:
        con = Connection(host='yoda', user='samsops', passwd=passwd, db='samsnew')
        cursor = con.cursor()
        cursor.execute('select ku_timestamp, ku_aos_los_status from gse_packet_rt;')
        results = cursor.fetchall();
        cursor.close()
        con.close()
    except:
        #print 'ERROR IN YODA DB CONNECTION'
        results = None
        
    # check if we have any results (should always just be one)
    if results:
        ku_timestamp, ku_aos_los = results[0]
    else:
        ku_timestamp, ku_aos_los = None, None

    out_q.put( (ku_timestamp, ku_aos_los) )


# attempt to connect to yoda and get most recent timestamp from cu_packet_rt table
def query_cu(passwd):
    # FIXME need to do this via an rt table (not yet setup on trek21a) TOO SLOW WITH NON_rt TABLE
    
    # attempt to get results
    try:
        con = Connection(host='yoda', user='samsops', passwd=passwd, db='samsnew')
        cursor = con.cursor()
        cursor.execute('select timestamp from cu_packet order by timestamp desc limit 1;')
        results = cursor.fetchall();
        cursor.close()
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
