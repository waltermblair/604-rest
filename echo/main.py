# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is a sample Hello World API implemented using Google Cloud
Endpoints."""

# [START imports]
import db_connect
import MySQLdb
import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote
# [END imports]


# [START messages]
class EchoRequest(messages.Message):
    content = messages.StringField(1)


class EchoResponse(messages.Message):
    """A proto Message that contains a simple string field."""
    content = messages.StringField(1)


ECHO_RESOURCE = endpoints.ResourceContainer(
    EchoRequest,
    n=messages.IntegerField(2, default=1))
# [END messages]


# [START echo_api]
@endpoints.api(name='echo', version='v1')
class EchoApi(remote.Service):
    @endpoints.method(
        # This method takes an empty request body.
        message_types.VoidMessage,
        # This method returns an Echo message.
        EchoResponse,
        http_method='GET',
        name='getPosts')
    def getPosts(self, request):
        query = "SELECT * FROM 604_db.posts"
        rows = ''
	try:
		conn = db_connect.connect_to_cloudsql()
		cursor = conn.cursor()	
		cursor.execute(query)

                data = cursor.fetchall()
                for row in data:
                    rows += (str(row[0]) + ': ' + str(row[1]))
	except Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()
##        output_content = ' '.request.content
        return EchoResponse(content=rows)

    @endpoints.method(
        # This method takes a ResourceContainer defined above.
        ECHO_RESOURCE,
        # This method returns an Echo message.
        EchoResponse,
        path='echo',
        http_method='POST',
        name='echo')
    def echo(self, request):
	query = "INSERT INTO 604_db.posts(id, content) " \
                "VALUES(%s, %s)"
        content = ' '.join([request.content] * request.n)
        # id can easily be converted to datetime
        args = (2, content)
	try:
		conn = db_connect.connect_to_cloudsql()
		cursor = conn.cursor()	
		cursor.execute(query, args)
		if cursor.lastrowid:
			print('last insert id', cursor.lastrowid)
		else:
			print('last insert id not found')
		conn.commit()
	except Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()
        output_content = ' '.join([request.content] * request.n)
        return EchoResponse(content=output_content)

    @endpoints.method(
        # This method takes a ResourceContainer defined above.
        ECHO_RESOURCE,
        # This method returns an Echo message.
        EchoResponse,
        http_method='DELETE',
        name='deletePost')
    def deletePost(self, request):
        query = "DELETE FROM 604_db.posts WHERE id=%s"
        arg = ' '.join(request.content)
	try:
		conn = db_connect.connect_to_cloudsql()
		cursor = conn.cursor()	
		cursor.execute(query, arg)
                conn.commit()
	except Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()
##        output_content = ' '.join([request.content] * request.n)
        return EchoResponse(content="deleted")

    @endpoints.method(
        # This method takes a ResourceContainer defined above.
        ECHO_RESOURCE,
        # This method returns an Echo message.
        EchoResponse,
        http_method='PUT',
        name='replacePost')
    def replacePost(self, request):
	query = "REPLACE INTO 604_db.posts(id, content) " \
                "VALUES(%s, %s)"
        content = ' '.join([request.content] * request.n)
        # id can easily be converted to datetime
        args = (2, content)
	try:
		conn = db_connect.connect_to_cloudsql()
		cursor = conn.cursor()	
		cursor.execute(query, args)
		if cursor.lastrowid:
			print('last insert id', cursor.lastrowid)
		else:
			print('last insert id not found')
		conn.commit()
	except Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()
        output_content = ' '.join([request.content] * request.n)
        return EchoResponse(content=output_content)

    
# [END echo_api]


# [START api_server]
api = endpoints.api_server([EchoApi])
# [END api_server]
