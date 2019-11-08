def decode_chunked(content):
    content = content.lstrip('\r')
    content = content.lstrip('\n')
    temp = content.find('\r\n')
    strtemp = content[0:temp]
    readbytes = int(strtemp, 16)
    newcont = ''
    start = 2
    offset = temp + 2
    newcont = ''
    while (readbytes > 0):
        newcont += content[offset:readbytes + offset]
        offset += readbytes
        endtemp = content.find('\r\n', offset + 2)
        if (endtemp > -1):
            strtemp = content[offset + 2:endtemp]
            readbytes = int(strtemp, 16)
            if (readbytes == 0):
                break
            else:
                offset = endtemp + 2

    content = newcont
    return content


def chunk_download(url, dest):
    fd = urllib.urlopen(url)
    chunk = decode_chunked(fd.read())
    fd.close()
    f = open(dest, 'w')
    f.write(chunk)
    f.close()