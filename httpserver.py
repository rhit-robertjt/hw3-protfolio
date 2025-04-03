import io
import socket
import time
import signal
import os

#added for parsing urls
import urllib.parse
#added for tracing prints
import traceback

server_variables = {}
server_variables["abc"] = 123

# Set a constant to determine where we should be loaded files from
# It is a good idea to put your public files here and not your private files
# Why might that be a good idea?
# Fix #1: change to "./public"
WEB_HOME = "./docs"


#   1. Practice Debugging via the Python Debugger
#   2. Refactor Existing Code (pull out code into functions)
#   3. Add a new <li> to list1 on shopping.html via JavaScript
#   4. Make it so button1 clicks will add a new item to list1 based on text1's value
#   5. Make it so mousing over <li> makes them appear differently (JS and CSS versions)
#   6. Make it so that clicking on an <li> adds strikethrough text decoration (and toggle)
#   7. Make it so that clicking on an <li> will move between list1 and list2 (toggle)
#   8. Make it so that all existing items (see data in script.js at top) get added when the page loads

#   As time allows:
#   9. Let's look at an example of dynamic rendering a page instead of using javascript
#   10. Check for duplicates before adding an item to the list
#   11. Use CSS instead of JS to adjust the text-decoration: "line-through" attribute

def main():

    server = create_connection(port = 8080)

    while True:
        connection_to_browser = accept_browser_connection_to(server)

        with(connection_to_browser):

            reader_from_browser = connection_to_browser.makefile(mode='rb')
            writer_to_browser = connection_to_browser.makefile(mode='wb')
            
            with(reader_from_browser):
                try:
                    request_line = reader_from_browser.readline()
                    request_line = request_line.decode("utf-8")
                    request_method = request_line.split(' ')[0]
                    file_name = request_line.split(' ')[1]
                    if len(file_name.split(".")) > 1:
                        file_extension = file_name.split(".")[1]
                    else:
                        file_extension = ""

                    headers = get_headers(reader_from_browser)
                    
                    # In case we want to check it later
                    post_data=""
                    if(request_method == "POST"):
                        post_data = get_post_data(reader_from_browser, headers)
                            
                except socket.timeout:
                    continue
                except KeyboardInterrupt:
                    exit(0)
                except Exception as e:
                    print("Error after reader_from_browser")
                    print( traceback.format_exc() )

            file_name, response_body, dictionary = handle_special_routes(file_name, post_data)

            with(writer_to_browser):
                try:
                    # inject WEB_HOME before opening file to read
                    file_name = f"{WEB_HOME}{file_name}"
                    if response_body == "":
                        response_body = get_response_body(file_name, dictionary)
                    content_type = get_content_type(file_extension)
                    write_to_browser(writer_to_browser, content_type, response_body)
                    
                except Exception as e:
                    # TODO: handle error in a better manner
                    print("Error after writer_to_browser")
                    print( traceback.format_exc() )
                    # TODO: - 1. get an error traceback as a string
                    error_string = traceback.format_exc()
                    # TODO: - 2. use a special error page to show results
                    file_name = f"{WEB_HOME}/error.html"
                    # TODO: - 3. insert error trace into page
                    # dictionary = {}
                    # dictionary['error_message'] = error_string
                    response_body = get_response_body(file_name, {"error_message": error_string})
                    # response_body.decode('utf-8').format(error_message=error_string).encode('utf-8')
                    # TODO: - 4. write to browser
                    content_type = get_content_type("html")
                    write_to_browser(writer_to_browser, content_type, response_body)

            #clear out old data
            connection_to_browser.shutdown(socket.SHUT_RDWR)
            connection_to_browser.close()
            

def create_connection(port):
    addr = ("", port)  # "" = all network adapters; usually what you want.
    server = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True) # prevent rare IPV6 softlock on localhost connections
    server.settimeout(2)
    print(f'Server started on port {port}. Try: http://localhost:{port}/shopping.html')
    return server

def accept_browser_connection_to(server):
    while True:
        try:
            (conn, address) = server.accept()
            conn.settimeout(2)
            return conn
        except socket.timeout:
            print(".", end="", flush=True)
        except KeyboardInterrupt:
            exit(0)

def handle_special_routes(file_name: str, post_data=None):
    special_response_body = ""
    special_dict = {}
    
    if(file_name == "/shutdown"):
        print("Shutting down")
        exit()
    elif(file_name == "/API/demo"):
        special_response_body = bytearray("Hello World Demo", encoding='utf-8')
    elif(file_name == "/template.html"):
        special_dict = {}
        special_dict["foo"] = "barrrrrrr"
        
    return file_name, special_response_body, special_dict

def write_to_browser(writer_to_browser: io.BufferedWriter, content_type: str, response_body: str) -> None:
    response_headers = bytearray("\r\n".join([
        'HTTP/1.1 200 OK',
        f'Content-Type: {content_type}',
        f'Content-length: {len(response_body)}',
        'Connection: close',
        '\r\n'
    ]), encoding = "utf-8")

    print()
    print('Response headers:')
    print(response_headers)
    print()
    print('Response body:')
    print(response_body)
    print()

    writer_to_browser.write(response_headers)
    writer_to_browser.write(response_body)
    writer_to_browser.flush()

def get_response_body(file_name: str, dictionary={}) -> bytearray:
    with(open(file_name, "rb") as fd):
        response_body = bytearray(fd.read())
        if (dictionary != {}):
            # html_contents = response_body.decode('utf-8')
            # html_contents = html_contents.format(**dictionary)
            # response_body = html_contents.encode("utf-8")
            response_body = response_body.decode('utf-8').format_map(dictionary).encode('utf-8')
    return response_body

def get_content_type(file_extension: str) -> str:
    if(file_extension == "html"):
        content_type = 'text/html; charset=utf-8'
    elif(file_extension == "png"):
        content_type = 'image/png'
    elif(file_extension == "ico"):
        #https://www.w3schools.com/html/html_favicon.asp
        content_type = 'image/x-icon'
    elif(file_extension == "jpeg"):
        content_type = 'image/jpeg'
    elif(file_extension == "jpg"):
        content_type = 'image/jpg'
    elif(file_extension == "js"):
        content_type = 'text/javascript; charset=utf-8'
    elif(file_extension == "css"):
        content_type = 'text/css; charset=utf-8'
    else:
        #let's try to allow reading anything as html
        content_type = 'text/html; charset=utf-8'
    return content_type

def get_post_data(reader_from_browser: io.BufferedReader, headers: dict) -> dict:
    request_body = reader_from_browser.read(int(headers["Content-Length"]))
    post_lines = request_body.decode("utf-8")

    post_data = {}
    if(headers["Content-Type"] == "text/plain"):
        fields = post_lines.split("\r\n")
        for field in fields:
            if(field == ""):
                continue
            split_field = field.split("=")
            post_data[split_field[0]] = split_field[1]
    elif (headers["Content-Type"] == "application/x-www-form-urlencoded"):
        fields = post_lines.split("&")
        for field in fields:
            if(field == ""):
                continue
            split_field = field.split("=")
            post_data[urllib.parse.unquote_plus(split_field[0])] = urllib.parse.unquote_plus(split_field[1]) 
    else:
        print( f"Content-Type: {headers['Content-Type']} not recognized. Post data not processed.")
    return post_data

def get_headers(reader_from_browser: io.BufferedReader) -> dict:
    headers = {}
    header_line = reader_from_browser.readline().decode("utf-8")
    while(True):
        if(header_line == '\r\n'):
            break
        pair = header_line.split(": ")
        headers[pair[0]] = pair[1].strip()  # Remove trailing whitespace
        header_line = reader_from_browser.readline().decode("utf-8")
    return headers

main()
# print(os.getcwd()) # show where we are
# print(os.listdir()) # show what we can see