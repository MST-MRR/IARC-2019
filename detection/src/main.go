package main

import (
	"encoding/base64"
	"github.com/streadway/amqp"
	"gocv.io/x/gocv"
	//"image"
	//"image/color"
	"log"
)

func main() {
	conn, err := amqp.Dial("amqp://guest:guest@localhost:5672/")
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"image-queue", // name
		true,          // durable
		false,         // delete when unused
		false,         // exclusive
		false,         // no-wait
		nil,           // arguments
	)
	failOnError(err, "Failed to declare a queue")

	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	failOnError(err, "Failed to register a consumer")

	forever := make(chan bool)

	classifier := gocv.NewCascadeClassifier()
	defer classifier.Close()

	if !classifier.Load("classifier.xml") {
		log.Printf("Error reading cascade file: ../classifier.xml\n")
		return
	}

	imgs := make(chan gocv.Mat)

	for i := 0; i < 5; i++ {
		go func(i int, classifier gocv.CascadeClassifier, imgs chan gocv.Mat) {
			for d := range msgs {
				//blue := color.RGBA{0, 0, 255, 0}
				log.Printf("%d: Received a message", i)
				decodedData := make([]byte, base64.StdEncoding.EncodedLen(len(d.Body)))
				_, err := base64.StdEncoding.Decode(decodedData, d.Body)
				failOnError(err, "Failed to decode base64")

				var flags gocv.IMReadFlag
				img, erg := gocv.IMDecode(decodedData, flags)
				failOnError(erg, "No image boiii")
				rects := classifier.DetectMultiScale(img)
				log.Printf("found %d faces\n", len(rects))
				/*for _, r := range rects {
					gocv.Rectangle(&img, r, blue, 3)

					size := gocv.GetTextSize("Human", gocv.FontHersheyPlain, 1.2, 2)
					pt := image.Pt(r.Min.X+(r.Min.X/2)-(size.X/2), r.Min.Y-2)
					gocv.PutText(&img, "Human", pt, gocv.FontHersheyPlain, 1.2, blue, 2)
				}*/
				//imgs <- img
			}
		}(i, classifier, imgs)
	}

	//window := gocv.NewWindow("Face Detect")
	//defer window.Close()

	//for img := range imgs {
	//	window.IMShow(img)
	//}

	log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
	<-forever
}

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}
