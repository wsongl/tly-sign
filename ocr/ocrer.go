package ocr

type ocrer interface {
	GetCaptcha(image string) string
}
