#COMP445 Data Communications and Computer Networks
#Lab Assignment #1

import argparse
import socket
import re
import sys
import os
from urllib.parse import urlparse

#Command line argument parser
parser = argparse.ArgumentParser(description = 'httpc is a curl-like application but supports HTTP protocol only.')
get_post = parser.add_mutually_exclusive_group()
get_post.add_argument('-g', '--get', help = 'Get URL request', type = str)
get_post.add_argument('-p', '--post', help = 'Post URL request', type = str)
parser.add_argument('-v', '--verbose', help = 'Prints the detail of the response such as protocol, status, and headers.', action = 'store_true')
parser.add_argument('--header', help = 'Associates headers to HTTP Request with the format key:value.', type = str)
parser.add_argument('-o','--obonus', help = 'Writes to file.', type = str)
parser.add_argument('--port', help = 'Specifies the port number. Default is 8080', type = int, default = 8080)
file_data = parser.add_mutually_exclusive_group()
file_data.add_argument('-f', '--file', help = 'Associates the content of a file to the body HTTP POST request.', type = str)
file_data.add_argument('-d', '--data', help = 'Associates an inline data to the body HTTP POST request.', type = str)
arguments = parser.parse_args()

class Http:
    server = ""
    url = ""
    header = ""
    file = ""
    data = ""
    obonus = ""
    verbose = False
    port = 8080

def requestParser(cmd_request):
    if cmd_request.get:
        url = urlparse(cmd_request.get)
        cmd_request.file = ""
        Http.data = cmd_request.data
    elif cmd_request.post:
        url = urlparse(cmd_request.post)
        if cmd_request.file and cmd_request.data:
            print("Error: cannot use both -d and -f")
        elif cmd_request.data:
            Http.data = cmd_request.data
        elif cmd_request.file:
            Http.file = cmd_request.file
    if url.scheme == '':
        Http.server = url.path
    else:
        Http.server = url.hostname
    Http.header = cmd_request.header
    Http.verbose = cmd_request.verbose
    if cmd_request.obonus:
        Http.obonus = cmd_request.obonus
    if cmd_request.data:
        Http.data = (re.sub("(\w+):", r'"\1":',  Http.data))
    if cmd_request.port:
        Http.port = cmd_request.port
    return Http

def post_request(command_argument):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        full_argument = requestParser(command_argument)
        print('Connected to ', full_argument.server)
        request = ("POST /post HTTP/1.0\r\nHost:" + full_argument.server + "\r\n")
        request_http_version = "User-Agent:Concordia-HTTP/1.1\r\n"
        request_content_type = full_argument.header + "\r\n"
        request_body = ""
        if full_argument.data:
            request_body = full_argument.data
        elif full_argument.file:
            fileRead = open(full_argument.file, "r")
            request_body = fileRead.read()
        request_body_length = "Content-length:" + str(len(request_body)) + "\r\n\r\n"
        request += request_http_version + request_content_type + request_body_length + request_body
        request = request.encode("utf-8")
        s.connect((full_argument.server, full_argument.port))
        s.sendall(request)
        result = s.recv(1024, socket.MSG_WAITALL)
        result = result.decode("utf-8")
        #bonus for assignment -o
        if full_argument.obonus:
            fileBonus = open(full_argument.obonus, "w")
            fileBonus.write(result)
        #if argument contains verbose
        if full_argument.verbose:
            sys.stdout.write(result)
        else:
            sys.stdout.write(result)
    finally:
        s.close()

def get_request(command_argument):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        full_argument = requestParser(command_argument)
        print('Connected to ', full_argument.server)
        request = "GET /"
        request_url = full_argument.url
        request_http_version = " HTTP/1.1\r\n"
        request_host = "Host: " + full_argument.server + "\r\n\r\n"
        request_body = ""
        if full_argument.data:
            request_body = full_argument.data
        request += request_url + request_http_version + request_host + request_body
        request = request.encode("utf-8")
        s.connect((full_argument.server, full_argument.port))
        print(request)
        s.sendall(request)
        result = s.recv(1024, socket.MSG_WAITALL)
        result = result.decode("utf-8")
        if full_argument.verbose:
            sys.stdout.write('Server ' + full_argument.server + ' responded with: \n' + result)
        else:
            sys.stdout.write('Server ' + full_argument.server + ' responded with: \n' + result)
    finally:
        s.close()

if __name__ == '__main__':
    if arguments.post:
        post_request(arguments)
    elif arguments.get:
        get_request(arguments)
    input()
