package main

import (
	//"bytes"
	"net"
	"log"
	"io"
	_"os"

	"encoding/binary"

	"github.com/golang/protobuf/proto"
	pb "github.com/chentknba/demo/proto"
)

const (
	ADDR = ":8000"
)

func main() {
	ln, err := net.Listen("tcp", ADDR)
	if err != nil {
		log.Fatal(err)
		return
	}

	defer ln.Close()

	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Fatal(err)
		}

		log.Printf("accpet new conn.\n")
		go func(c net.Conn) {
			for {
				header := make([]byte, 2)
				if _, err := io.ReadFull(c, header); err != nil {
					log.Printf("%v\n", err)
					break
				}

				log.Printf("header %v\n", header)

				sz := binary.BigEndian.Uint16(header)

				log.Printf("read sz %v\n", sz)

				payload := make([]byte, sz)

				if _, err := io.ReadFull(c, payload); err != nil {
					log.Printf("read payload error, %v\n", err)
					break
				}

				log.Printf("read pay load %v\n", payload)

				snp := &pb.Snapshot{}

				if err := proto.Unmarshal(payload, snp); err != nil {
					log.Printf("unmarshal snapshot error, %v\n", err)
					break
				}

				log.Printf("snapshot %v\n", snp)

			}

			c.Close()
		}(conn)
	}
}
