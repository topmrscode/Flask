package main
import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
)
func MakeRequest() {
	formData := url.Values{
		"username": {"Coralie"},
		"email":    {"coralie@gmail.com"},
		"password": {"coralie123"},
	}
	resp, err := http.PostForm("http://localhost:5000/register/", formData)
	if err != nil {
		log.Fatalln(err)
	}
	bodyBytes, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	bodyString := string(bodyBytes)
	fmt.Println(bodyString)
}
func main() {
	MakeRequest()
}