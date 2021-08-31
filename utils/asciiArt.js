const imageToAscii = require("image-to-ascii");

// Passing options
let min = 18;
let max = 30;
let imgs = [];

for (let i = max; i >= min; i--) {
  imageToAscii("/Users/colinmford/Downloads/IMG_0499.jpg", {
      colored: false,
      preserve_aspect_ratio: true,
      size: {
        width: i
      },
      pixels: " .:*-+#+−×÷=&%@░▒▓"
  }, (err, converted) => {
      console.log(converted)
  });
}
