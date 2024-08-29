package main

import (
	"fmt"
	"os"
	"path"

	"github.com/libp2p/go-libp2p/core/crypto"
)

const filepath = "/opt/p2p"

func main() {

	privKey, pubKey, err := crypto.GenerateKeyPair(crypto.RSA, 2048)
	if err != nil {
		panic(err)
	}
	// create dir
	_ = os.Mkdir(filepath, 0775)
	// output public key to file
	dataPub, err := crypto.MarshalPublicKey(pubKey)
	if err != nil {
		panic(err)
	}
	writePubErr := os.WriteFile(path.Join(filepath, "pubKey"), dataPub, 0644)
	if writePubErr != nil {
		panic(writePubErr)
	}
	fmt.Printf("Output public key at: %s\n", path.Join(filepath, "pubKey"))
	// output private key to file
	dataPriv, err := crypto.MarshalPrivateKey(privKey)
	if err != nil {
		panic(err)
	}
	writePrivErr := os.WriteFile(path.Join(filepath, "privKey"), dataPriv, 0600)
	if writePrivErr != nil {
		panic(writePrivErr)
	}
	fmt.Printf("Output private key at: %s\n", path.Join(filepath, "privKey"))
}

