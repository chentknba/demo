import socket
import select
import struct
import time
import sys
import errno


class netconn(object):
	def __init__(self):
		self.sock = 0
		self.wbuf = bytes()
		self.rbuf = bytes()
		self.stat = 0
		self.conn = (errno.EISCONN, 10057, 10053)
		self.errd = (errno.EINPROGRESS, errno.EALREADY, errno.EWOULDBLOCK)
		self.errc = 0

		
	def connect(self, addr, port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((addr, port))
		self.sock.setblocking(0)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

		self.stat = 2
		self.wbuf = bytes()
		self.rbuf = bytes()
		self.errc = 0
		
		return 0

	def close(self):
		assert(0)
		self.stat = 0
		if not self.sock:
			return 0
		try:
			self.sock.close()
		except:
			pass

		self.sock = 0

		return 0

	def status(self):
		return self.stat

	def error(self):
		return self.errc

	def process(self):
		if self.stat == 0:
			return 0

		if self.stat == 1:
			self.__connect()
		if self.stat == 2:
			self.__send()
		if self.stat == 2:
			self.__recv()
		
	def __connect(self):
		if self.stat == 2:
			return 1
		if self.stat != 1:
			return -1

		try:
			self.sock.recv(0)
		except socket.error as code:
			if code in self.conn:
				return 0

			if code in self.errd:
				self.stat = 2
				self.rbuf = bytes()

				return 1

			self.close()
			return -1

		self.stat = 2

	def __recv(self):
		rdata = bytes()

		while 1:
			data = bytes()

			try:
				data = self.sock.recv(1024)
				
				if not data:
					self.errc = 10000
					self.close()
					return -1

			except socket.error as code:
				if code.args[0] == errno.EWOULDBLOCK:
					#print ("would block.")
					#time.sleep(1)
					return 0
				else:
					self.errc = code
					self.close()

					return -1

			if len(data) == 0:
				break

			rdata = rdata + data

		self.rbuf = self.rbuf + rdata

	def __send(self):
		wsize = 0

		if len(self.wbuf) == 0:
			return 0

		try:
			wsize = self.sock.send(self.wbuf)

		except socket.error as code:
			if not code in self.errd:
				self.errc = code
				self.close()
				return -1

		self.wbuf = self.wbuf[wsize:]

		return wsize

	def rawsend(self, data):
		self.wbuf = self.wbuf + data

		return 0

	def send(self, data):
		sz = struct.pack(">H", len(data))
		
		self.rawsend(sz + data)

	def rawpeek(self, size):
		self.process()
		if len(self.rbuf) == 0:
			return bytes()
		
		if size > len(self.rbuf):
			size = len(self.rbuf)

		rdata = self.rbuf[0:size]

		return rdata

	def rawrecv(self, size):
		rdata = self.rawpeek(size)
		size = len(rdata)
		self.rbuf = self.rbuf[size:]

		return rdata

        def recv(self):
            data = rawpeek(2)
            if len(data) < 2:
                return bytes()

            sz = struct.unpack(">H", data)
            if len(self.rbuf) < sz[0]:
                return bytes()

            self.rawrecv(2)

            return self.rawrecv(sz[0] - 2)

# test
if __name__ == '__main__':
	conn = netconn()
	conn.connect('127.0.0.1', 8000)

	stat = 0

	while 1:
		conn.process()

		time.sleep(0.1)
